"""jog.py AXIS:DELTA ... — one small jog at a time through the mg400-base server
(http://127.0.0.1:8000), waiting until the arm arrives. Example: python jog.py y:-0.5 x:0.5
Set speed first: POST /api/speed {"ratio": 2}, /api/smoothness {"secs": 1.5}, /api/sync."""
import json, sys, time, urllib.request
A = "http://127.0.0.1:8000/api"
def call(path, body=None):
    req = urllib.request.Request(A + path, data=None if body is None else json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=5))
for step in sys.argv[1:]:
    axis, delta = step.split(":")
    r = call("/jog", {"axis": axis, "delta": float(delta)})
    if not r.get("ok"):
        sys.exit(f"jog refused: {r}")
    t = r["target"]
    t0 = time.time()
    while True:
        s = call("/status")
        if s["error"] or s["alarm_ids"] or not s["enabled"]:
            sys.exit(f"STOP: robot fault {s['mode_name']} {s['alarm_ids']} {s.get('fault_label')}")
        p = s["pose"]
        if max(abs(p[i] - t[k]) for i, k in enumerate("xyz")) < 0.05:
            break
        if time.time() - t0 > 15:
            sys.exit(f"STOP: not arriving, pose {p} target {t}")
        time.sleep(0.2)
    print(f"{step:>8}  pose X {p[0]:.2f}  Y {p[1]:.2f}  Z {p[2]:.2f}")
