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

## Iminapa tööriist pildil

* Dobot MG400 lõppflantsi ametlik CAD (`sim/robot/meshes/mg400_end_flange.stl`, allikas `MG400_End_Flange_3D.stp`,
  Dobot / Pololu; MG400 User Guide V1.7 joonis 5.3: Ø40 × 4 ketas + Ø22 × 10 nukk J4 võllil Ø8 × 12).
* Hoidiku plaat Ø40 × 4, 4 sisekuuskantkruvi altpoolt, alumiiniumkere Ø16, külgmine 4 mm kiirliitmik, O-rõngas,
  adapter (fotod; avalikku CAD-i pole).
* Napp: kummil tempel **C20** = SMC ZP20C tüüpi lame ribidega napp Ø20 (SMC kataloog ZPT 13-11-6: välis-Ø23,
  kõrgus C 14; nihik: Ø22,25 × 13,8). Puhvrivedru ei ole: kokku surutakse ainult kummiserv.
* Napa kokkusurumist näitab leht (`audit_scene.py`). TODO nihikuga: hoidiku vaba pikkus.
