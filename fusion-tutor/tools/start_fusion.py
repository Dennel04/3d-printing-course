"""Start Fusion if it is not running and wait for its MCP server: python tools/start_fusion.py [timeout_s]

Fusion is installed for all users (shortcut "Autodesk Fusion.lnk" in the common
Start menu), not under LocalAppData. Running Fusion but no answer = a modal
dialog or MCP switched off: this script says so and does not start a second copy.
"""
import glob
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fusion_checkpoint as hook  # noqa: E402

SHORTCUTS = [
    os.path.join(os.environ.get("ProgramData", r"C:\ProgramData"), r"Microsoft\Windows\Start Menu\Programs\**\Autodesk Fusion*.lnk"),
    os.path.join(os.environ.get("APPDATA", ""), r"Microsoft\Windows\Start Menu\Programs\**\Autodesk Fusion*.lnk"),
]


def running():
    out = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Fusion360.exe", "/NH"],
                         capture_output=True, text=True).stdout
    return "Fusion360.exe" in out


def answers():
    try:
        hook.Fusion().state()
        return True
    except Exception:
        return False


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    timeout = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    if answers():
        print("Fusion: already answering")
        return 0
    if running():
        print("Fusion runs but MCP does not answer: close the dialog in Fusion, or enable "
              "Preferences > General > API > Fusion MCP Server")
        return 1
    links = [p for pat in SHORTCUTS for p in glob.glob(pat, recursive=True)]
    if not links:
        print("Fusion shortcut not found in the Start menu: start Fusion by hand")
        return 1
    os.startfile(links[0])
    print(f"started {links[0]}, waiting for MCP (up to {timeout} s)...")
    t0 = time.time()
    while time.time() - t0 < timeout:
        time.sleep(5)
        if answers():
            print(f"Fusion: answering after {int(time.time() - t0)} s")
            return 0
    print("Fusion started but MCP did not answer in time: a dialog on start (recovered documents, "
          "sign-in) or MCP off in Preferences > General > API")
    return 1


if __name__ == "__main__":
    sys.exit(main())
