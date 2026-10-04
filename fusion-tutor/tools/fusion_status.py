"""Fusion state in one command: python tools/fusion_status.py [N]

Shows whether Fusion MCP answers, the active command, open documents (what is
unsaved) and the last N entries of people/<me>/log/fusion-actions.jsonl.
Changes nothing in the model.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fusion_checkpoint as hook  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding="utf-8")  # the Windows console defaults to cp1252
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    try:
        st = hook.Fusion().state()
    except Exception as e:
        print(f"Fusion: NOT ANSWERING ({e}): a modal dialog in Fusion, Fusion closed or MCP off")
    else:
        cmd = st["cmd"] or "-"
        idle = "idle" if st["cmd"] in hook.IDLE else "COMMAND ACTIVE"
        print(f"Fusion: answering | command: {st['cmdName'] or cmd} ({cmd}) - {idle}")
        for d in st["docs"]:
            flags = []
            if d["active"]:
                flags.append("active")
            if d["modified"]:
                flags.append("UNSAVED CHANGES")
            if not d["saved"]:
                flags.append("never saved")
            print(f"  document: {d['name']}  {', '.join(flags)}")
    log = hook.log_path()
    print(f"\nLast {n} actions ({os.path.relpath(log, hook.ROOT)}):")
    if not os.path.exists(log):
        print("  (none yet)")
        return
    with open(log, encoding="utf-8") as f:
        lines = f.readlines()[-n:]
    for line in lines:
        e = json.loads(line)
        what = e.get("featureType") or ""
        if e.get("readOnly"):
            what += " (read)"
        extra = e.get("checkpoint") or e.get("terminated") or e.get("reason") or ""
        print(f"  {e['time']}  {e['tool']}/{what:<16} {e['decision']:<5} {extra[:90]}")


if __name__ == "__main__":
    main()
