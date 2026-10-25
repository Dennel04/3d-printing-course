# Töökoha digitaalne kaksik (MG400 + ruudustik + hoidikud)

Ühine kõigile laboritele (`3d-print/sim`): robot, rakis, liigesemudel ja kokkupõrked on samad. Laboripõhised sisendid (kalibreerimine `calibration/cells.py`, `slot-picker/layout.json` ja `cycle.py`, detailide STL-id) ja tulemused (`docs/`) on labori kaustas; valik `--lab` (vaikimisi `../lab2`) või keskkonnamuutuja `SIM_LAB`.

Eesmärk: enne päris robotit näha, kuhu käsi ulatub, kui madalale iminapp võib minna, kas tsükkel kuskile vastu läheb ja kui suurt kalibreerimisviga tsükkel talub. Kaksik kasutab **samu andmeid ja sama koodi** mis robot: labori `slot-picker/layout.json`, `slot-picker/cycle.py`, `calibration/cells.py` ja `mg400-base` liigesepiirid.

## Käivitamine

```
cd 3d-print/sim
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python reach_map.py          # <lab>/docs/sim_reach.csv, <lab>/docs/photos/sim-reach-map.png
.venv/Scripts/python check_calibration.py  # kus nelja nurga meetod kalibreerimiskastiga töötab
.venv/Scripts/python dry_run.py            # layout.json nii nagu on (režiim, rollid, õpetatud Z), <lab>/docs/sim_dry_run.txt
.venv/Scripts/python dry_run.py --full     # planeeritud täistsükkel sisend -> töökoht -> väljund, <lab>/docs/sim_dry_run_full.txt
.venv/Scripts/python tolerance.py          # kalibreerimisvea taluvus, <lab>/docs/sim_tolerance.txt
.venv/Scripts/python reach_map.py --lab ../lab3   # teine labor (vajab oma calibration/, slot-picker/)
```

## Millest kaksik koosneb

| Osa | Allikas | Kontroll päris robotiga |
|---|---|---|
| Liigesed ja piirid | `mg400_kin.py` = meie `mg400-base` fork (`kinematics.py`, 982ebf8), lülid sobitatud 6 päris poosile (rms 0,01 mm), piirid J1 ±160, J2 −25…85, J3 −25…105, J3−J2 ±60, varu 2° | G-1 J2 piir Z −135,8 vs päris −138; B-2 raadius 192 J3 piir −99 vs −98; raadius 227 −150 vs ~−147 (3 mm) |
| Käe 3D-kuju | Dobot `MG400_ROS` URDF + võrgud (MIT, commit 2bcf6a9), kaust `robot/` | URDF vs sobitatud mudel: z ±1,1 mm, raadius kuni 3,9 mm → tööriist (napp, XIAO kinnitus) seotud **sobitatud** flantsiga |
| Rakis | `scene/rakis_*.stl` (Fusion, `MG 400 rakis`) + laud ruudustiku alumisel serval (z −16,72) | — |
| Ruudustik → robot | labori `calibration/cells.py` (24.10 kolme ruudu sobitus, +0,87°) | kaksiku lahtrikeskmed vs `cells.py` ≤ 0,06 mm |
| Hoidikud | labori `layout.json` tüüp → STL (`twin.py` `HOLDER_STL`, praegu Lab 2 detailid); vanade jalgadega hoidik tõuseb taladele (jala 3 mm pikendus, +2,85 mm) | — |
| Iminapp | Ø 20 mm (**oletus**), J4 teljest 31,1 mm roboti poole R 33 juures (sobituse nihe, eeldus: robot istub rakises nagu CAD-is), pikkus J4 mootori alt **66,2 mm** | pikkus D-2 puudutusest (Z −150 klaasihoidiku v1 põhjal); kontroll: 23.10 G-1 nurgad jäävad 1,6 mm kalibreerimiskasti v1 põhja kohale |
| XIAO kinnitus | `camera-mounts/stl/xiao-square-mount-v2.stl` J4 mootori all | — |
| Kokkupõrked | `python-fcl` täpsed kolmnurkvõrgud (mitte kumerad kestad), `trimesh` | negatiivtestid allpool |

## Mida dry_run kontrollib

Vaikimisi kontrollitakse seda, mida robot praegu teeks: `layout.json` režiim (`workstation_step`), rollid (võivad olla sama hoidik) ja õpetatud dx/dy/Z; õpetamata Z tuletatakse geomeetriast ning õpetatud ja tuletatud väärtus kirjutatakse kõrvuti. `--full` kontrollib planeeritud täistsüklit (rollid ettepanekupaigutusest, kõik Z tuletatud); `tolerance.py` kasutab täistsüklit.

- iga liikumine sirgjoonena iga 2 mm järel (**eeldus**: `mg400-base` liigub sirgelt): liigesepiirid, käe, XIAO kinnituse, napa ja kantava klaasi (30 × 30 × 2) kokkupõrge rakise, hoidikute, posti, pesades olevate klaaside ning aku + Atomi virnaga;
- oma sihtmärki (klaas, Atom, väljundi põhi) võib napp/klaas puudutada ainult lähenemisel ja **mitte sügavamalt kui 1,5 mm** (õpetatud võtmine surub 1 mm);
- võtmisel: napa nihe klaasi keskelt ≤ 5 mm (Ø 20 napp 30 mm klaasil);
- vabastamisel: millele klaas jääb (töökohal ainult Atomi ekraanile).

Negatiivtestid (24.10.26), kõik leitud: travel Z −140 → 15 kokkupõrget; töökoht 10 mm liiga madal → „surub 10 mm Atomisse“; võtmine 3 mm liiga madal → „surub 4,1 mm klaasi“; väljund +40 mm küljele → klaas vastu oranži hoidikut; +70 mm → seina sisse; −70 mm → „VALE KOHT: klaas jääb ruudustikule“; töökoht +15 mm → „VALE KOHT: hoidiku servale“; 6 mm viga võtmisel → „napp pole täielikult klaasil“.

## Lab 2 tulemused 24.10.26 (ettepanekupaigutus `lab2/slot-picker/layout.json`)

- Kaart: `../lab2/docs/photos/sim-reach-map.png`, tabel `../lab2/docs/sim_reach.csv`. A±1, A±2, G±4, G±5 kättesaamatud; B±1/B±2 ja G-rida piirab liiges (napp ei jõua alla 19–40 mm ruudustiku kohal).
- **B-2 ei sobi kalibreerimiseks** (ülesanne soovitab B-2): napp jõuab B-2-s alla ainult +19,1 mm ruudustiku kohale, kalibreerimiskasti ülaserv on +16,0 mm — napp ei mahu kasti. `check_calibration.py`: nelja nurga meetod töötab C-2, C-1, D-2, E±3, F-2, F-3; ei tööta B-2, B-3, G-1. Ettepanek: kalibreerimine **C-2**-s, kontroll E+3-s.
- Klaasitsükkel (4 klaasi) on kokkupõrgeteta; väikseim vahe 6,1 mm; travel Z −100 jätab Atomi kohale 14 mm.
- Kalibreerimisvea taluvus (`../lab2/docs/sim_tolerance.txt`): võtmine talub 5 mm, **väljund ainult 3 mm** (klaas pannakse lahtri keskele, 21 mm kasti keskelt → klaasi serv seinast 3 mm). Ettepanek: väljundi kohad kasti keskele lähemale (±16 mm → varu 8 mm).

## Piirid (mida kaksik ei näe)

Printimise vead (elevandijalg, tugede jäägid, kahanemine) — selleks on füüsiline jala test ja nihik. Pehme napa kaldumine seina vastu. Füüsika (klaasi libisemine) — järgmine samm (MuJoCo). TODO mõõta: napa läbimõõt, napa nihe J4 teljest, napa pikkus J4 mootori alt.

## 24.10.26 õhtu: kontroll (layout pärast 17:06 muudatusi)

- Täistsükkel (`--full`): 4 klaasi kokkupõrgeteta, taluvus endine (võtmine 5 mm, väljund 3 mm).
- Ülekandetest (praegune `layout.json`: kõik rollid = Glass input, D-4/D-5/E-4/E-5): kokkupõrkeid pole; output `place_z` pole õpetatud (slot picker ei lase seda käivitada, kaksik tuletab −147,0).
- Päris robot 24.10 õhtul C-2-s: kalibreerimiskasti põhja puudutus Z −155,0 vs kaksik −154,8 → napa pikkus kinnitatud; napa efektiivne läbimõõt ≈ 23 mm (kaksik eeldab 20).
- Õpetatud `pick_z −150,5`: kaksiku järgi algab klaasi puudutus Z −147,9 ja tühja pesa põhi −149,9 → klaasiga surub −150,5 napa 2,6 mm (lubatud 1,5). 24.10 17:06 Z-proovi kaadrites on pesad tühjad ja napp surutakse kokku juba alates −151 → tõenäoliselt õpetati tühja põhja peale. **Kontrollida**: kas õpetamisel oli klaas pesas.
