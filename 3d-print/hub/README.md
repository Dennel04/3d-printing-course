# MG400 Station Hub

One page for the MG400 cell: the robot (simulated or real), the slot picker, the live 3D twin, a
DobotStudio-style jog pad and the twin checks.

```
cd 3d-print/hub
../sim/.venv/Scripts/python -m pip install -r requirements.txt   # once (sim packages + pyserial)
../sim/.venv/Scripts/python hub.py                               # http://127.0.0.1:8020
../sim/.venv/Scripts/python hub.py --robot-ip 192.168.1.6 --z-floor -160              # Real defaults
```

The hub always starts in **Simulation**. Do not run the old `slot_picker.py` on the same COM ports at
the same time (tool camera COM5, pressure COM4).

## Robot: Simulation or Real

| | Simulation | Real robot |
|---|---|---|
| What answers | `sim_robot.py` in the hub process | `real_robot.py` in the hub process: the arm over TCP/IP (`mg400/driver.py`, `--robot-ip`, default 192.168.1.6) |
| Limits | joint limits and reach from `sim/mg400_kin.py`, Z floor −160 | the same model (`mg400/kinematics.py`), Z floor `--z-floor` (default −160), plus the robot's own |
| Speed | 300 mm/s × ratio, 0.5 s ramp | 200 mm/s × ratio, 0.5 s ramp |
| Before use | nothing | robot powered, nothing else driving it (no mg400-base server, DobotStudio not in JOG); API mode is switched on by Connect |

Switching needs a second click on **Real robot** (the button turns red: "Confirm: real arm") and is refused
while a sequence runs.

**One motion lock for the whole hub.** Every request that can move the arm (jog, picker drive, go above, move
glass, cycle, probe) is refused by the server until the **Motion** switch at the top of the Jog tab is on.
It stays on until it is switched off, the robot is switched or the hub restarts. A jog pressed while it is
off makes the switch blink. STOP / Esc always works.

**Layout.** Drag the bar between the 3D view and the panel to resize it (double-click resets, arrow keys
nudge, the arrow collapses the panel; the size is remembered in this browser). The view cube in the 3D corner
turns the view to a face (TOP, X±, Y± in robot axes); Fit and Tool are the two fixed views. Enable robot and
Clear error appear only when they are needed; messages pop up under the top bar.

The hub remembers the last selected robot (`hub/.mode`, not in git) and opens it again after a restart;
on Real it opens the link to the arm by itself. Motion always starts off, Enable stays a click.
**Enable robot** also shows when the arm says ENABLED but the hub has stopped following (after a fault):
the arm ignores moves until it is pressed.

If the robot drops off (power, cable, e-stop, DobotStudio took it) the top bar shows **Connect**: it
reconnects to the robot without moving; then **Enable robot** (the arm holds where it is) and **Motion** on in the Jog tab.

## Tabs

- **Jog** — two pads like DobotStudio. Cartesian: X± / Y± and Z± / R±. Joint: J1± / J2± and J3± / J4±; a joint
  step is turned into a Cartesian target through the robot's joint model (R = J1 + J4) and checked against
  the joint limits before it is sent. Steps 0.2 / 1 / 5 / 10 or **Hold**: moves at the set speed while
  the key is held and brakes smoothly on release (the page renews it every 0.1 s; without a renewal for 0.35 s
  the arm brakes by itself). R alone turns with the controller's MoveJog(J4±), since the MG400 ignores a ServoP
  that changes only R. Keys: arrows X/Y, PgUp/PgDn Z, Q/E R, Esc = STOP. Pump suck / blow / off.
- **Picker** — the slot picker (Drive / Edit layout / Test, teach points, glass cycle, refit CSV) on whichever
  robot is selected. Hub version `static/picker.html` (same API as `lab2/slot-picker/index.html`, which still
  works on its own): status chips for robot, vacuum sensor and camera, and an **Events** log (moves, teach points,
  runs, saved rounds, errors; Copy for the devlog) instead of the status block; STOP, speed and camera live in the hub.
- **Tests** — the twin checks on the current `layout.json`: dry run (as the robot runs it and the planned
  full cycle), refit rounds 2-5, calibration error tolerance, scene audit, rebuild of the 3D scene, and
  the hub self-test. Each gets pass / warn / fail, a one-line summary and its full output.
- **Camera** — the XIAO tool camera stream.

The 3D stage follows the selected robot live (**Live arm**) or plays the planned cycle with the
dry-run verdict on the timeline (**Cycle replay**). Scene: `sim/viewer/data`; it is rebuilt by itself after
**Save layout** in the picker and when the hub starts with a layout newer than the scene. **Put glasses back**
shows only while a 3D glass is away from the input holder.
**Webcam** shows the table webcam on the post (Verbatim 49580 UHD, picked by name, any other camera from the
list) in the same area, 3840×2160 when the camera gives it. The browser opens the camera itself, so the
Windows Camera app or a video call must not hold it. **Save frame** stores a full-size JPEG in
`lab2/webcam-frames/` (git-ignored).

- **Glasses follow the pump** in Live arm: when the pump starts sucking with the cup on a glass (within 12 mm),
  the glass rides with the cup; on blow / off it stays where it was released. Picture only, the robot cannot
  see a glass.
- **Picker → Edit layout:** each holder is one block with its full name. Drag it, or click it and use the arrow
  keys / the arrow pad (Delete removes, Esc lets go). Drag over empty cells to add a holder. The workstation
  cell of the cycle moves with its holder when the layout is saved (the picker alone left it behind).

## Tests

```
cd 3d-print/hub/tests
../../sim/.venv/Scripts/python -m unittest -v test_hub
```

Simulation only: the simulated robot (moves, jog, reach, Z floor, pump), the joint jog maths, the hub API
(page, picker page, state, jog limits, the slot picker on the simulation, mode switch, foreign Origin refused).
