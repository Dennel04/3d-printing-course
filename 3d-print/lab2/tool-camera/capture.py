"""Grab one JPEG from the XIAO tool camera over USB.

Usage: python capture.py COM5 docs/photos/tool-camera-workstation.jpg

open_port() and read_frame() are also used by the slot picker's live view, which keeps the port
open and asks for a frame every 1/fps s.
"""
import sys
import time

import serial


def open_port(port: str) -> serial.Serial:
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
    return s


def read_frame(s: serial.Serial) -> bytes:
    """Ask for one frame ('c') and return the JPEG; RuntimeError on any camera problem."""
    s.write(b"c")
    while True:
        line = s.readline().decode(errors="replace").strip()
        if not line:
            raise RuntimeError("no answer from camera")
        if line.startswith("ERR"):
            raise RuntimeError(line)
        if line.startswith("JPG "):
            size = int(line.split()[1])
            break
    data = s.read(size)
    if len(data) != size:
        raise RuntimeError(f"short read: {len(data)} of {size} bytes")
    return data


def capture(port: str, path: str) -> int:
    s = open_port(port)
    try:
        data = read_frame(s)
    finally:
        s.close()
    with open(path, "wb") as f:
        f.write(data)
    return len(data)


if __name__ == "__main__":
    port = sys.argv[1] if len(sys.argv) > 1 else "COM5"
    out = sys.argv[2] if len(sys.argv) > 2 else "tool-camera.jpg"
    try:
        print(f"{out}: {capture(port, out)} bytes")
    except RuntimeError as exc:
        raise SystemExit(str(exc))
