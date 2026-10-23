"""Grab one JPEG from the XIAO tool camera over USB.

Usage: python capture.py COM5 docs/photos/tool-camera-workstation.jpg
"""
import sys
import time

import serial


def capture(port: str, path: str) -> int:
    # DTR/RTS low: toggling them resets the ESP32-S3.
    s = serial.Serial()
    s.port = port
    s.baudrate = 115200
    s.timeout = 5
    s.dtr = False
    s.rts = False
    s.open()
    time.sleep(0.3)
    s.reset_input_buffer()
    s.write(b"c")
    while True:
        line = s.readline().decode(errors="replace").strip()
        if not line:
            raise SystemExit("no answer from camera")
        if line.startswith("ERR"):
            raise SystemExit(line)
        if line.startswith("JPG "):
            size = int(line.split()[1])
            break
    data = s.read(size)
    s.close()
    if len(data) != size:
        raise SystemExit(f"short read: {len(data)} of {size} bytes")
    with open(path, "wb") as f:
        f.write(data)
    return size


if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else "COM5"
    out = sys.argv[2] if len(sys.argv) > 2 else "tool-camera.jpg"
    print(f"{out}: {capture(port, out)} bytes")
