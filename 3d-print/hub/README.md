# MG400 Station Hub

One page for the MG400 cell: the robot (simulated or real), the slot picker, the live 3D twin, a
DobotStudio-style jog pad and the twin checks.

```
cd 3d-print/hub
../sim/.venv/Scripts/python -m pip install -r requirements.txt   # once (sim packages + pyserial)
../sim/.venv/Scripts/python hub.py                               # http://127.0.0.1:8020
```

The hub always starts in **Simulation**. Do not run the old `slot_picker.py` on the same COM ports at
the same time (tool camera COM5, pressure COM4).

## Robot: Simulation or Real

| | Simulation | Real robot |
|---|---|---|
| What answers | `sim_robot.py` in the hub process, same calls and replies as mg400-base | mg400-base server from `layout.json` → `mg400_api` (`http://127.0.0.1:8000/api`) |
| Limits | joint limits and reach from `sim/mg400_kin.py`, Z floor −160 | the same model inside mg400-base, plus the robot's own |
| Speed | 300 mm/s × ratio | the robot's |
| Before use | nothing | mg400-base running, connected and enabled (DobotStudio in TCP/IP mode) |

Switching needs a second click on **Real robot** and is refused while a sequence runs. After every
switch **Motion enabled** is cleared.

## Tabs

- **Jog** — two pads like DobotStudio. Cartesian: X± / Y± and Z± / R±. Joint: J1± / J2± and J3± / J4±; a joint
  step is turned into a Cartesian target through the robot's joint model (R = J1 + J4) and checked against
  the joint limits before it is sent. Steps 0.2 / 1 / 5 / 10 or **Hold** (1 mm or 1° every 0.2 s while
  pressed). Keys: arrows X/Y, PgUp/PgDn Z, Q/E R, Esc = STOP. Pump suck / blow / off.
- **Picker** — the slot picker (Drive / Edit layout / Test, teach points, glass cycle, refit CSV) on whichever
  robot is selected. Hub version `static/picker.html` (same API as `lab2/slot-picker/index.html`, which still
  works on its own): status chips for robot, vacuum sensor and camera, and an **Events** log (moves, teach points,
  runs, saved rounds, errors; Copy for the devlog) instead of the status block; STOP, speed and camera live in the hub.
- **Tests** — the twin checks on the current `layout.json`: dry run (as the robot runs it and the planned
  full cycle), refit rounds 2-5, calibration error tolerance, scene audit, rebuild of the 3D scene, and
  the hub self-test. Each gets pass / warn / fail, a one-line summary and its full output.
- **Camera** — the XIAO tool camera stream.

The 3D stage follows the selected robot live (**Live arm**) or plays the planned cycle with the
dry-run verdict on the timeline (**Cycle replay**). Scene: `sim/viewer/data`, made by **Rebuild 3D scene**.

- **Glasses follow the pump** in Live arm: when the pump starts sucking with the cup on a glass (within 12 mm),
  the glass rides with the cup; on blow / off it stays where it was released. Picture only, the robot cannot
  see a glass. **Reset glasses** puts them back into the input holder.
- **Layout → 3D** rebuilds the scene from the picker's saved `layout.json` (~20 s); **Save layout** in the
  picker does the same automatically, and Edit layout has **Show in 3D**.

## Tests

```
cd 3d-print/hub/tests
../../sim/.venv/Scripts/python -m unittest -v test_hub
```

Simulation only: the simulated robot (moves, jog, reach, Z floor, pump), the joint jog maths, the hub API
(page, picker page, state, jog limits, the slot picker on the simulation, mode switch, foreign Origin refused).
