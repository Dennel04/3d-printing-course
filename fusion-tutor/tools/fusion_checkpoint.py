"""PreToolUse hook: Fusion health check and automatic checkpoint before changes.

Version 2 (2026-10-04, ported from Denys's personal tutor). What it does:

1. Quick ping (8 s) before every Fusion call. If Fusion is silent it is almost
   always a modal dialog ("save / don't save", a message, sign-in), so the
   hook denies right away with a clear reason instead of waiting 90 s.
2. Active command. Read-only calls are never blocked by it. Before a change:
   - orbit/pan/zoom or an empty Delete: the hook closes it itself
     (ui.terminateActiveCommand) and tells the student;
   - a real command (Extrude, Sketch...) is left alone, since that is the
     student's work; the hook denies and names the command.
3. A new/opened document while other documents have unsaved changes: deny with
   the list (on 04.10 a "save?" dialog for _tutor-sandbox froze everything).
4. Checkpoint as before: unsaved changes -> a version "claude checkpoint ...".
5. people/<me>/log/fusion-actions.jsonl also gets the active command, open
   documents, what the hook did and how long it took.

Scripts the hook sends to Fusion are read-only, except the checkpoint save
itself. They never catch exceptions (Fusion MCP rule).
"""
import datetime
import json
import os
import re
import sys
import time
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import whoami  # noqa: E402

MCP_URL = os.environ.get("FUSION_MCP_URL") or "http://127.0.0.1:27182/mcp"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PING_TIMEOUT = 8
SAVE_TIMEOUT = 90

# Navigation commands: safe to close, there is no student work in them.
NAV_RE = re.compile(r"(Orbit|Pan|Zoom|LookAt)Command$", re.I)
IDLE = ("", "SelectCommand")
CREATES_DOC = re.compile(r"documents\.(add|open)\(|importToNewDocument|uploadFile\(")

STATE_SCRIPT = '''import adsk.core, json
def run(_context: str):
    app = adsk.core.Application.get()
    ui = app.userInterface
    cmd = ui.activeCommand or ""
    cdef = ui.commandDefinitions.itemById(cmd) if cmd else None
    act = app.activeDocument
    docs = [{"name": d.name, "active": act is not None and d == act,
             "modified": d.isModified, "saved": d.isSaved} for d in app.documents]
    sel = ui.activeSelections  # None while no document is open
    print(json.dumps({"cmd": cmd, "cmdName": cdef.name if cdef else "",
                      "sel": sel.count if sel else 0, "docs": docs}))
'''

TERMINATE_SCRIPT = '''import adsk.core, json
def run(_context: str):
    ui = adsk.core.Application.get().userInterface
    before = ui.activeCommand
    ok = ui.terminateActiveCommand()
    print(json.dumps({"before": before, "ok": ok, "after": ui.activeCommand}))
'''

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


def log_path():
    if os.environ.get("FUSION_HOOK_LOG"):
        return os.environ["FUSION_HOOK_LOG"]
    me, _ = whoami.resolve()
    if me:
        return os.path.join(ROOT, "people", me, "log", "fusion-actions.jsonl")
    return os.path.join(ROOT, ".unassigned-actions.jsonl")  # not in git


class Fusion:
    """One MCP session for the whole hook run."""

    HEADERS = {"Content-Type": "application/json",
               "Accept": "application/json, text/event-stream"}

    def __init__(self):
        self.extra = None
        self.next_id = 1

    def _post(self, payload, timeout, extra=None):
        req = urllib.request.Request(MCP_URL, json.dumps(payload).encode(),
                                     {**self.HEADERS, **(extra or {})})
        return urllib.request.urlopen(req, timeout=timeout)

    def _connect(self, timeout):
        with self._post({"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {
                "protocolVersion": "2025-06-18", "capabilities": {},
                "clientInfo": {"name": "fusion-tutor-checkpoint", "version": "2"}}},
                timeout) as r:
            sid = r.headers.get("MCP-Session-Id")
        self.extra = {"MCP-Session-Id": sid, "MCP-Protocol-Version": "2025-06-18"}
        self._post({"jsonrpc": "2.0", "method": "notifications/initialized"},
                   timeout, self.extra).close()

    def script(self, code, read_only, timeout):
        if self.extra is None:
            self._connect(timeout)
        self.next_id += 1
        obj = {"script": code}
        if read_only:
            obj["readOnly"] = True
        with self._post({"jsonrpc": "2.0", "id": self.next_id, "method": "tools/call",
                         "params": {"name": "fusion_mcp_execute",
                                    "arguments": {"featureType": "script", "object": obj}}},
                        timeout, self.extra) as r:
            res = json.loads(r.read().decode("utf-8"))["result"]
        return json.loads(res["content"][0]["text"])

    def state(self):
        res = self.script(STATE_SCRIPT, True, PING_TIMEOUT)
        if not res.get("success"):
            raise RuntimeError(res.get("error") or res.get("message"))
        return json.loads(res["message"].strip().splitlines()[-1])


def is_mutating(tool, args):
    obj = args.get("object") or {}
    if tool.endswith("fusion_mcp_update"):
        return True
    if not tool.endswith("fusion_mcp_execute"):
        return False
    if args.get("featureType") == "script":
        return obj.get("readOnly") is not True
    return args.get("featureType") == "document"


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
        return obj.get("operation") in ("open", "close")  # don't lose changes
    return False


def creates_document(args):
    obj = args.get("object") or {}
    if args.get("featureType") == "document" and obj.get("operation") == "open":
        return True
    return bool(CREATES_DOC.search(obj.get("script") or ""))


def decide(tool, args, entry):
    """Returns (decision, reason, user_message)."""
    obj = args.get("object") or {}
    code = obj.get("script") or ""
    if "messageBox" in code or "inputBox" in code:
        return ("deny", "Don't use ui.messageBox/inputBox: a modal dialog freezes Fusion and MCP "
                        "until the student clicks OK. Use print(), don't catch exceptions.", "")

    fusion = Fusion()
    t0 = time.time()
    try:
        st = fusion.state()
    except Exception as e:
        entry["ping"] = f"ERROR {e}"
        return ("deny",
                f"Fusion did not answer within {PING_TIMEOUT} s ({e}). Almost always a modal "
                "dialog in Fusion: \"save / don't save\", a message, sign-in. Or Fusion is "
                "closed / MCP Server is off (Preferences > General > API). Ask the student to "
                "look at the Fusion window and close the dialog; nothing was changed.",
                "Fusion is not answering: check for an open dialog in Fusion.")
    entry["ping_ms"] = int((time.time() - t0) * 1000)
    entry["activeCommand"] = st["cmd"]
    entry["docs"] = st["docs"]

    if not is_mutating(tool, args):
        return ("allow", "", "")  # an active command doesn't block reading

    user_msg = ""
    if st["cmd"] not in IDLE:
        nav = bool(NAV_RE.search(st["cmd"])) or (st["cmd"] == "FusionDeleteCommand" and st["sel"] == 0)
        if not nav:
            name = st["cmdName"] or st["cmd"]
            return ("deny",
                    f"The student has the \"{name}\" command ({st['cmd']}) open in Fusion. Not "
                    "touching it: their work may be in it. Ask them to finish it (OK) or cancel "
                    "it (Esc), then retry.", "")
        res = fusion.script(TERMINATE_SCRIPT, True, PING_TIMEOUT)
        entry["terminated"] = res.get("message", res.get("error", "")).strip()
        st = fusion.state()
        if st["cmd"] not in IDLE:
            return ("deny",
                    f"Could not close \"{st['cmdName'] or st['cmd']}\". Ask the student to press "
                    "Esc in Fusion (if the model keeps orbiting with the mouse, drag the ViewCube "
                    "by a corner towards the screen centre).", "")
        user_msg = "Closed orbit/navigation in Fusion to apply the change."

    if creates_document(args):
        dirty = [d["name"] for d in st["docs"] if d["modified"] and not d["active"]]
        if dirty:
            return ("deny",
                    "Fusion has unsaved documents in the background: " + ", ".join(dirty) +
                    ". A new/opened document will pop up a \"save?\" dialog and Fusion will "
                    "freeze. Ask the student to save or close them, then retry.", "")

    if needs_checkpoint(tool, args):
        stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        script = CHECKPOINT_SCRIPT.replace(
            "DESCRIPTION", repr(f"claude checkpoint {stamp} (before {entry['tool']}/{entry['featureType']})"))
        try:
            res = fusion.script(script, False, SAVE_TIMEOUT)
        except Exception as e:
            entry["checkpoint"] = f"ERROR {e}"
            return ("deny", f"Checkpoint failed ({e}); nothing was changed. A version may be "
                            "uploading to the cloud: wait and retry.", "")
        out = (res.get("message") or res.get("error") or "").strip()
        entry["checkpoint"] = out
        if not res.get("success"):
            return ("deny", "Checkpoint failed, nothing was changed: " + out, "")
        if out.startswith("NEVER_SAVED"):
            return ("deny", "The document has never been saved, so there is nothing to roll "
                            "back to. Ask the student to save it to a project (Ctrl+S), or do "
                            "saveAs yourself if they asked, then retry.", "")
    return ("allow", "", user_msg)


def main():
    call = json.loads(sys.stdin.buffer.read().decode("utf-8"))
    tool = call.get("tool_name", "")
    args = call.get("tool_input") or {}
    t0 = time.time()
    entry = {"time": datetime.datetime.now().isoformat(timespec="seconds"),
             "tool": tool.split("__")[-1], "featureType": args.get("featureType") or args.get("queryType")}
    obj = args.get("object") or {}
    if obj.get("script"):
        entry["script"] = obj["script"][:4000]
        entry["readOnly"] = obj.get("readOnly") is True

    decision, reason, user_msg = decide(tool, args, entry)

    entry["decision"] = decision
    if reason:
        entry["reason"] = reason
    entry["hook_ms"] = int((time.time() - t0) * 1000)
    log = log_path()
    os.makedirs(os.path.dirname(log), exist_ok=True)
    with open(log, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    out = {"hookEventName": "PreToolUse", "permissionDecision": decision}
    if reason:
        out["permissionDecisionReason"] = reason
    result = {"hookSpecificOutput": out}
    if user_msg:
        result["systemMessage"] = user_msg
    print(json.dumps(result))  # ASCII-escaped: the Windows console is not cp65001


if __name__ == "__main__":
    try:
        main()
    except Exception as e:  # fail closed: no check, no change
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse", "permissionDecision": "deny",
            "permissionDecisionReason": f"fusion_checkpoint hook error: {e!r}"}}))
