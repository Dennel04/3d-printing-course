# Kaksiku 3D-vaade

Brauseris mängitav klaasitsükkel: MG400 (Doboti URDF), rakis, hoidikud `layout.json` järgi, XIAO kinnitus,
iminapp ja klaasid. Asendid arvutab sama kaksik, mis `dry_run.py` (sama `cycle.py`, `cells.py`, liigesemudel);
iga liikumise värv ajajoonel on `dry_run.py` otsus (roheline ok, kollane < 3 mm, punane kokkupõrge).

```
cd 3d-print/sim
.venv/Scripts/python export_viewer.py            # layout.json nii, nagu robot seda praegu käitaks
.venv/Scripts/python export_viewer.py --full     # planeeritud täistsükkel
python -m http.server -d viewer 8020             # ava http://127.0.0.1:8020
```

Lehel: paus/mängi (tühik), kiirus, ajajoone lohistamine, sammu klõps paremas loendis, kaamerad
(üldvaade, ülalt, küljelt, jälgi nappi), napa tee ja rakise sisse/välja.

## Fusionist uus objekt

1. Fusionis: detail `MG 400 rakis` koostu õigesse kohta, eksport STL-iks **koostu koordinaatides**
   (nagu veebikaamera posti osad).
2. Lisa rida faili `viewer/extras.json` (tee labori kausta või `sim/` suhtes):
   ```json
   [{"name": "minu detail", "stl": "veebikaamera-post/stl/minu-detail.stl", "frame": "rig", "color": "#f26b1d"}]
   ```
   `frame`: `rig` = Fusioni rakise koordinaadid (vaikimisi), `world` = roboti koordinaadid (mm).
3. `export_viewer.py` uuesti ja lehe värskendus.

Hoidikud tulevad ise `slot-picker/layout.json`-ist (tüüp → STL `twin.py` `HOLDER_STL`-is); uus hoidikutüüp = uus rida seal.
`viewer/data/` genereeritakse, gitis seda ei ole.
