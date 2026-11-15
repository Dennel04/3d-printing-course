# Töökoha digitaalne kaksik (MG400 + ruudustik + hoidikud)

Ühine kõigile laboritele (`3d-print/sim`): robot, rakis, liigesemudel ja kokkupõrked on samad. Laboripõhised sisendid (kalibreerimine `calibration/cells.py`, `slot-picker/layout.json` ja `cycle.py`, detailide STL-id) ja tulemused (`docs/`) on labori kaustas; valik `--lab` (vaikimisi `../lab2`) või keskkonnamuutuja `SIM_LAB`.

Kaksik hindab ulatust, kokkupõrkeid ja tundlikkust kalibreerimisveale. Ta kasutab Slot Pickeriga sama `layout.json`-i, `cycle.py` tegevusplaani, `calibration/cells.py` kalibreerimist ning sama liigesemudeli lähteandmeid. Kokkupõrkekontroll on geomeetriline arvutus. Lab 2-l on toimiv sisendkomplekt. Lab 3 tööriista jaoks tuleb sisendid ja mudel eraldi ette valmistada.

## Käivitamine

Loo simulatsioonikaustas Python 3.11 virtuaalkeskkond. Windows PowerShellis kasuta
`py -3.11 -m venv .venv` ja macOS-is/Linuxis `python3.11 -m venv .venv`.
Näited kasutavad Windowsi Pythoni teed. macOS-is/Linuxis asenda `.venv/Scripts/python` teega `./.venv/bin/python`.

```
cd 3d-print/sim
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python reach_map.py          # <lab>/docs/sim_reach.csv, <lab>/docs/photos/sim-reach-map.png
.venv/Scripts/python check_calibration.py  # kus nelja nurga meetod kalibreerimiskastiga töötab
.venv/Scripts/python dry_run.py            # layout.json nii nagu on (režiim, rollid, õpetatud Z), <lab>/docs/sim_dry_run.txt
.venv/Scripts/python dry_run.py --full     # planeeritud täistsükkel sisend -> töökoht -> väljund, <lab>/docs/sim_dry_run_full.txt
.venv/Scripts/python tolerance.py          # kalibreerimisvea taluvus, <lab>/docs/sim_tolerance.txt
.venv/Scripts/python refit_sim.py         # korduskatse ringid 2-5: hoidikud juhuslikult jala lõtku piires (--play 1), <lab>/docs/sim_refit.txt
.venv/Scripts/python export_viewer.py     # 3D-vaade brauseris (viewer/), vt viewer/README.md
.venv/Scripts/python audit_scene.py       # hoidikute istumine, klaaside vahe ja mudeli kontaktikõrgus
```

`--lab` viitab kaustale, kus on kalibreerimine, paigutus, tsükli kood ja mudelid. Kui soovid
salvestatud aruandeid säilitada, käivita faile kirjutavad käsud eraldi töökoopias.

## Millest kaksik koosneb

| Osa | Allikas | Kontroll päris robotiga |
|---|---|---|
| Liigesed ja piirid | `mg400_kin.py` = meie `mg400-base` fork (`kinematics.py`, 982ebf8), lülid sobitatud 6 päris poosile (rms 0,01 mm), piirid J1 ±160, J2 −25…85, J3 −25…105, J3−J2 ±60, varu 2° | G-1 J2 piir Z −135,8 vs päris −138; B-2 raadius 192 J3 piir −99 vs −98; raadius 227 −150 vs ~−147 (3 mm) |
| Käe 3D-kuju | Dobot `MG400_ROS` URDF + võrgud (MIT, commit 2bcf6a9), kaust `robot/` | URDF vs sobitatud mudel: z ±1,1 mm, raadius kuni 3,9 mm → tööriist (napp, XIAO kinnitus) seotud **sobitatud** flantsiga |
| Rakis | `scene/rakis_*.stl` (Fusion, `MG 400 rakis`) + laud ruudustiku alumisel serval (z −16,72). Laud Treston, 700 mm sügav (CAD-i laud; Treston TP on 500/700/800): tagaserv roboti taga tagumiste L-ide all (rakise x +163,5), esiserv x −536,5 eesmiste L-ide all; 670 mm torud ulatuvad ette ~50 mm üle serva, veebikaamera post toru otsas. Laua laius 700 (mõõtmata). Pesa ja roboti alus on roboti juures (URDF: J1 on aluse kasti keskelt 5 mm taga); ruudustik on pesa vastu ja selle asukoht tuleb `cells.py`-st. `twin.grid_slide()`: ruudustik „vastu ja keskel“ suhtes +0,7 mm (= vastu), −2,8 mm külgsuunas piki torusid | kaksiku lahtrikeskmed = `cells.py` (viga 0,0 mm) |
| Ruudustik → robot | labori `calibration/cells.py` (13.11.26 kahe ruudu sobitus F-2 + C+4, +1,48°) | kaksiku lahtrikeskmed vs `cells.py` ≤ 0,06 mm |
| Hoidikud | labori `layout.json` tüüp → STL (`twin.py` `HOLDER_STL`, praegu Lab 2 detailid); vanade jalgadega hoidik tõuseb taladele (jala 3 mm pikendus, +2,85 mm) | — |
| Iminapp | `CUP_D` on Ø 22,25 mm, 24.10 mõõdetud eraldi kummilt. Mudeli XY-nihe J4 teljest R = 33° juures on (0, 0). J4 mootori alt tipuni **66,2 mm** tuletati 24.10 vana hoidiku puudutusest. | Kalibreerimiskasti põhja puudutuse võrdlus Z −155,0 (päris) vs −154,8 (mudel). Paigaldatud napa samasus mõõdetud kummiga, vaba kogupikkus ja lubatav kokkusurumine vajavad füüsilist kontrolli. [Lab 2 mõõteregister](../lab2/docs/measurements.md#eraldi-kummist-iminapp--measured) |
| XIAO kinnitus + kaamera | `camera-mounts/stl/xiao-square-mount-v2.stl` J4 mootori all; selles Seeedi ametlik XIAO ESP32S3 Sense mudel (`../models/xiao-esp32s3-sense/`) täpselt nagu `xiao-square-mount-v2.f3d`-s, Fusionist eksporditud kinnituse koordinaatides: `scene/xiao-esp32s3-sense-in-mount-v2.stl` | — |
| Aku + AtomS3 töökohal | M5Stacki CAD (`../models/`): Atomic Battery Base (põhi + kate) 18,0 mm, AtomS3 12,9 mm; virn pesa põhjal. M5Stacki failis on ainult plastkorpus (ekraani pole, raami ava 16,1 × 16,1 näitab sisemust) → kaksik lisab tumeda ekraaniploki ava täiteks, pealispind raami faasi põhjas 0,8 mm raami pealt (eeldus, mõõtmata) | mõõdetud akumoodul on 21,97 mm (`measurements.md`) — CAD-virnaga on töökoha 24.10 puudutus 1,2 mm esimesest puudutusest madalamal nagu sisend/väljund (0,7–1,2), mõõdetud kõrgusega oleks vahe 5,1 mm. TODO nihikuga: aku kõrgus ilma Atomita |
| Kokkupõrked | `python-fcl` täpsed kolmnurkvõrgud (mitte kumerad kestad), `trimesh` | negatiivtestid allpool |

## Mida dry_run kontrollib

Vaikimisi kasutab `dry_run.py` [Lab 2 paigutust](../lab2/slot-picker/layout.json), kus
`workstation_step: true` ja töökoht on E+2. `cycle.py` lisab 13.11 `cells.py` järgi arvutatud
lahtrikeskmetele hoidikute õpetatud XY-nihked (sisend +1,0/+0,5 mm, töökoht ja väljund 0/0).
R on 33° ning õpetatud Z on sisendis −152 mm, töökohas panekul −119 mm ja võtmisel −121 mm,
väljundis −153 mm. Puuduva õpetatud Z tuletab kaksik mudelist ja kuvab selle aruandes.
[Kalibreerimine](../lab2/docs/measurements.md#kalibreerimine-13112026) · [Õpetatud punktid](../lab2/docs/layout.md#roboti-sihtpunktid-ruut--nihe-r-33)

`--full` kasutab vaikimisi kolme rolli, jätab õpetatud XY- ja Z-väärtused kõrvale ning võtab
töökohaks hoidiku esimese lahtri (praeguses failis E+1). `tolerance.py` ja `refit_sim.py` kasutavad
seda varianti. Vaaturi eksport kasutab samu kahte režiimi.

- Sirgjoonelist liikumist kontrollitakse ligikaudu 2 mm sammuga. Mudel kontrollib liigesepiire ning käe, kaamera, napa ja klaasi kokkupõrkeid. **30 × 30 × 1,2 mm** pärineb 13.11 nihikumõõdust. `dry_run.GLASS` määrab klaasi kokkupõrkekeha, paigutuse ja tuletatud Z. `export_viewer.py` kasutab sama mõõtu. Varasem 2 mm oli 23.10 Exceli lähteväärtus. [Klaasi mõõtmine](../lab2/docs/measurements.md#13112026--atoms3-ja-klaas-nihikuga)
- Lubatud sihtkontakti korral võrdleb mudel laskumise lõpp-Z-d esimese arvutusliku puudutusega. Muu geomeetria vaba ruumi puhul märgib `WARN_CLEARANCE = 3.0` alla 3 mm tulemuse `close`-iks.
- Võtmisel on kesknihke piir `PICK_OFFSET_MAX = (30 − 22,25) / 2` ehk 3,875 mm. Vabastamisel kontrollib mudel all olevat pinda (töökohal Atomi ekraan).

### Kontaktikõrgus ja füüsiline kokkusurumine

`dry_run.py` praegune `PRESS_ALLOWED = 6.0` mm on laskumise lubatud **Z-erinevus mudeli esimesest
puudutusest**. Algne 1,5 mm oli 24.10 kaksiku kriteerium. 25.10 asendati see 6,0 mm-ga pärast
võrdlust esimese füüsilise ringi õpetatud punktidega. Koodi kommentaaris olevad 4,2 / 5,2 / 0,7 mm
on mudeli ja õpetatud Z erinevused. Neisse võib jääda tööriista pikkuse, hoidikute ja koostu kõrguse
viga. Hilisem ülevaatus tuvastas, et tööriistal puudub vedrupuhver. [Piiri muutus](https://github.com/Dennel04/3d-printing-course/commit/1816b0449939a38d81a9694e5f766d2fade2ba34) · [Puhvrita tööriista täpsustus](https://github.com/Dennel04/3d-printing-course/commit/057761a7ca657385d74ea30dee27fcf442dc5ebd)

Napa ohutu füüsiline kokkusurumine on mõõtmata. Vaaturi näidatud deformatsioon on arvutusliku vahe
visualiseering. Salvestatud vaikimisi jooksus arvutab mudel töökoha vabastusel 3,5 mm kukkumise.
Enne töökoormuse või liikumispiiri muutmist mõõda paigaldatud tööriista vaba pikkust, tegelikku
kontakti ja napa deformatsiooni. Kontrolli töökohal aku ning Atomi koostukõrgust. [Salvestatud arvutus](../lab2/docs/sim_dry_run.txt)

Negatiivtestid (24.10.26), kõik leitud: travel Z −140 → 15 kokkupõrget; töökoht 10 mm liiga madal → „surub 10 mm Atomisse“; võtmine 3 mm liiga madal → „surub 4,1 mm klaasi“; väljund +40 mm küljele → klaas vastu oranži hoidikut; +70 mm → seina sisse; −70 mm → „VALE KOHT: klaas jääb ruudustikule“; töökoht +15 mm → „VALE KOHT: hoidiku servale“; 6 mm viga võtmisel → „napp pole täielikult klaasil“.

## Lab 2 ajaloolised simulatsioonitulemused 24.10.26 (ettepanekupaigutus)

- Kaart: `../lab2/docs/photos/sim-reach-map.png`, tabel `../lab2/docs/sim_reach.csv`. A±1, A±2, G±4, G±5 kättesaamatud; B±1/B±2 ja G-rida piirab liiges (napp ei jõua alla 19–40 mm ruudustiku kohal).
- **B-2 ei sobi kalibreerimiseks** (ülesanne soovitab B-2): napp jõuab B-2-s alla ainult +19,1 mm ruudustiku kohale, kalibreerimiskasti ülaserv on +16,0 mm — napp ei mahu kasti (J3 piir). Kalibreeritakse kaugetes ruutudes F-2 ja C+4.
- Klaasitsükkel (4 klaasi) on kokkupõrgeteta; väikseim vahe 6,1 mm; travel Z −100 jätab Atomi kohale 14 mm.
- Kalibreerimisvea taluvus (`../lab2/docs/sim_tolerance.txt`): võtmine talub 5 mm, **väljund ainult 3 mm** (klaas pannakse lahtri keskele, 21 mm kasti keskelt → klaasi serv seinast 3 mm). Ettepanek: väljundi kohad kasti keskele lähemale (±16 mm → varu 8 mm).

## Piirid (mida kaksik ei näe)

Kaksik ei mõõda printimisvigu, napa elastset käitumist ega klaasi libisemist. Hubi `Live arm` vaate
klaasi haarde- ja kandmiskõrguses kasutab `LivePose` eraldi 1,0 mm keskme nihet. Seetõttu võib selle
kuva erineda 1,2 mm klaasi eksporditud taasesitusest. Lab 3 mõõtis 15.11 napa koostu massiks
42,03 g. Uue tööriista gabariidid, kaugus flantsist ja neli nihet vajavad mõõtmist ning uut geomeetriat.
[Lab 3 mõõtmised](../lab3/docs/measurements.md#mõõtmised-15112026) · [Nihked](../lab3/docs/tool_offsets.md)

## 24.10.26 õhtu: kontroll (layout pärast 17:06 muudatusi)

Allolevad kirjed kirjeldavad 24.10 paigutust ja selleaegset 1,5 mm mudelikriteeriumi.

- Täistsükkel (`--full`): 4 klaasi kokkupõrgeteta, taluvus endine (võtmine 5 mm, väljund 3 mm).
- Ülekandetest (praegune `layout.json`: kõik rollid = Glass input, D-4/D-5/E-4/E-5): kokkupõrkeid pole; output `place_z` pole õpetatud (slot picker ei lase seda käivitada, kaksik tuletab −147,0).
- Õpetatud `pick_z −150,5`: kaksiku järgi algab klaasi puudutus Z −147,9 ja tühja pesa põhi −149,9 → klaasiga surub −150,5 napa 2,6 mm (lubatud 1,5). 24.10 17:06 Z-proovi kaadrites on pesad tühjad ja napp surutakse kokku juba alates −151 → tõenäoliselt õpetati tühja põhja peale. **Kontrollida**: kas õpetamisel oli klaas pesas.
