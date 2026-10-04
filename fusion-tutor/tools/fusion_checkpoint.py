"""PreToolUse-хук: автоматический чекпоинт Fusion перед каждым изменением.

Как чекпоинты в Claude Code, только на истории версий Fusion: если в активном
документе есть несохранённые правки, хук сам сохраняет версию с подписью
"claude checkpoint" ДО того, как учитель что-то поменяет. Откат — /rewind.
Read-only скрипты проходят без чекпоинта. Всё пишется в
people/<я>/log/fusion-actions.jsonl. Студенту ничего не запрашивается.
"""
import datetime
import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import whoami  # noqa: E402

MCP_URL = "http://127.0.0.1:27182/mcp"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def log_path():
    me, _ = whoami.resolve()
    if me:
        return os.path.join(ROOT, "people", me, "log", "fusion-actions.jsonl")
    return os.path.join(ROOT, ".unassigned-actions.jsonl")  # в git не идёт

CHECKPOINT_SCRIPT = '''import adsk.core
def run(_context: str):
    app = adsk.core.Application.get()
    doc = app.activeDocument
    if not doc:
        print("NO_DOC")
        return
    if not doc.isSaved:
        print("NEVER_SAVED " + doc.name)
        return
    if doc.isModified:
        if not doc.save(DESCRIPTION):
            raise RuntimeError("save() returned False")
        print("SAVED " + doc.name)
    else:
        print("CLEAN " + doc.name)
'''


def mcp_call(name, arguments, timeout=90):
    headers = {"Content-Type": "application/json",
               "Accept": "application/json, text/event-stream"}

    def post(payload, extra=None):
        req = urllib.request.Request(MCP_URL, json.dumps(payload).encode(),
                                     {**headers, **(extra or {})})
        return urllib.request.urlopen(req, timeout=timeout)

    with post({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {
            "protocolVersion": "2025-06-18", "capabilities": {},
            "clientInfo": {"name": "fusion-tutor-checkpoint", "version": "1"}}}) as r:
        sid = r.headers.get("MCP-Session-Id")
    extra = {"MCP-Session-Id": sid, "MCP-Protocol-Version": "2025-06-18"}
    post({"jsonrpc": "2.0", "method": "notifications/initialized"}, extra).close()
    with post({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
               "params": {"name": name, "arguments": arguments}}, extra) as r:
        res = json.loads(r.read().decode("utf-8"))["result"]
    return json.loads(res["content"][0]["text"])


def needs_checkpoint(tool, args):
    obj = args.get("object") or {}
    if tool.endswith("fusion_mcp_update"):
        return True  # undo/redo
    if not tool.endswith("fusion_mcp_execute"):
        return False
    ft = args.get("featureType")
    if ft == "script":
        return obj.get("readOnly") is not True
    if ft == "document":
        return obj.get("operation") in ("open", "close")  # не потерять правки
    return False


def main():
    call = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    tool = call.get("tool_name", "")
    args = call.get("tool_input") or {}
    entry = {"time": datetime.datetime.now().isoformat(timespec="seconds"),
             "tool": tool.split("__")[-1], "featureType": args.get("featureType")}
    obj = args.get("object") or {}
    if obj.get("script"):
        entry["script"] = obj["script"][:4000]
        entry["readOnly"] = obj.get("readOnly") is True

    decision, reason = "allow", ""
    code = obj.get("script") or ""
    if "messageBox" in code or "inputBox" in code:
        decision = "deny"
        reason = ("Не используй ui.messageBox/inputBox: модальное окно вешает Fusion и MCP, "
                  "пока студент не нажмёт OK. Печатай через print(), исключения не лови.")
    elif needs_checkpoint(tool, args):
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        script = CHECKPOINT_SCRIPT.replace(
            "DESCRIPTION", repr(f"claude checkpoint {stamp} (before {entry['tool']}/{entry['featureType']})"))
        try:
            res = mcp_call("fusion_mcp_execute",
                           {"featureType": "script", "object": {"script": script}})
            out = (res.get("message") or res.get("error") or "").strip()
            entry["checkpoint"] = out
            if not res.get("success"):
                decision = "deny"
                reason = ("Чекпоинт не удался, изменение не выполнено: " + out +
                          " Возможно, у студента открыт диалог команды — попроси закрыть его.")
            elif out.startswith("NEVER_SAVED"):
                decision = "deny"
                reason = ("Документ ещё ни разу не сохранён — откатиться будет некуда. "
                          "Попроси студента сохранить его (Ctrl+S) в проект и повтори.")
        except Exception as e:  # Fusion/MCP недоступен — не меняем вслепую
            decision = "deny"
            reason = f"Чекпоинт не удался ({e}); изменение не выполнено."
            entry["checkpoint"] = f"ERROR {e}"

    entry["decision"] = decision
    log = log_path()
    os.makedirs(os.path.dirname(log), exist_ok=True)
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    out = {"hookEventName": "PreToolUse", "permissionDecision": decision}
    if reason:
        out["permissionDecisionReason"] = reason
    print(json.dumps({"hookSpecificOutput": out}))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # fail closed: без чекпоинта ничего не меняем
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny",
            "permissionDecisionReason": f"fusion_checkpoint hook error: {e!r}"}}))
