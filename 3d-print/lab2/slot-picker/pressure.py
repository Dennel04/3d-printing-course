"""pressure.py — vacuum reading from the Atom (pressure_port in layout.json, COM4).

Uses the Atom firmware already on the shared AtomS3R: the Data Acquisition Lab 2 measurement
firmware DA2_MEASURE_V1 (data-acquisition/lab2/src/README.md). It streams one JSON line per
10 ms after {"cmd":"measure_start","config":"raw","run":<16 hex>}; "adc" is the raw 12-bit
G5 code, not calibrated to kPa. Lines with "adc" from the Lab 1 firmware work too (it streams
without a start command).

The monitor never stops the robot. When samples stop for stale_s it reports an error, keeps
retrying the port, and the cycle carries on without the vacuum check.
"""
import json
import secrets
import threading
import time
from collections import deque

import serial


def open_port(port):
    # DTR/RTS low before open, as the DA logger does: toggling them resets the ESP32-S3.
    s = serial.Serial()
    s.port, s.baudrate, s.timeout = port, 115200, 0.5
    s.dtr = s.rts = False
    s.open()
    return s


class PressureMonitor:
    def __init__(self, port, stale_s=1.0, opener=open_port):
        self.port, self.stale_s, self.opener = port, stale_s, opener
        self.lock = threading.Lock()
        self.samples = deque(maxlen=300)  # (pc time, adc), ~3 s at 100 Hz
        self.baseline = None  # adc with the pump off / cup open, set by mark_baseline()
        self.error = None if port else "pressure_port not set in layout.json"
        if port:
            threading.Thread(target=self._loop, daemon=True).start()

    def latest(self):
        """(adc, age_s) of the newest sample, or (None, None)."""
        with self.lock:
            if not self.samples:
                return None, None
            t, adc = self.samples[-1]
        return adc, time.time() - t

    def ok(self):
        _, age = self.latest()
        return age is not None and age < self.stale_s

    def mean(self, seconds=0.3):
        """Mean adc over the last `seconds`, or None when the data is stale."""
        if not self.ok():
            return None
        now = time.time()
        with self.lock:
            vals = [a for t, a in self.samples if t > now - seconds]
        return sum(vals) / len(vals) if vals else None

    def mark_baseline(self):
        self.baseline = self.mean()
        return self.baseline

    def vacuum(self):
        """Baseline minus the current mean, in ADC codes: grows as the cup seals
        (MPX5700AP is absolute, Vout falls with vacuum). None without data or baseline."""
        m = self.mean()
        if m is None or self.baseline is None:
            return None
        return self.baseline - m

    def state(self):
        adc, age = self.latest()
        with self.lock:
            n = sum(1 for t, _ in self.samples if t > time.time() - 1.0)
        ok = age is not None and age < self.stale_s
        if ok:
            error = None
        elif age is not None:
            error = f"no pressure data for {age:.0f} s ({self.error or 'Atom silent'})"
        else:
            error = self.error or "no pressure data yet"
        vac = self.vacuum()
        return {"ok": ok, "adc": adc, "rate_hz": n, "error": error,
                "baseline": None if self.baseline is None else round(self.baseline, 1),
                "vacuum": None if vac is None else round(vac, 1)}

    def _loop(self):
        while True:
            s = None
            try:
                s = self.opener(self.port)
                s.reset_input_buffer()
                # stop first: a start while a run is going is rejected and ends the run
                s.write(b'{"cmd":"measure_stop"}\n')
                time.sleep(0.1)
                s.write(b'{"cmd":"measure_start","config":"raw","run":"%s"}\n' % secrets.token_hex(8).encode())
                last = time.time()
                while time.time() - last < self.stale_s * 2:
                    line = s.readline()
                    if not line.startswith(b"{"):
                        continue  # "# ..." status lines and timeouts
                    try:
                        msg = json.loads(line)
                    except ValueError:
                        continue
                    if isinstance(msg.get("adc"), int):
                        last = time.time()
                        with self.lock:
                            self.samples.append((last, msg["adc"]))
                        self.error = None
                self.error = "Atom stopped sending; restarting the run"
            except Exception as exc:
                self.error = f"{self.port}: {exc}"[:200]
            finally:
                if s is not None:
                    try:
                        s.close()
                    except Exception:
                        pass
            time.sleep(1.0)
