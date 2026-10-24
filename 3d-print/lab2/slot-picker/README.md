# Slot picker

Veebiaken, kus ruudustiku lahtrile klõpsates viib MG400 iminapa selle lahtri kohale. Režiimis **Edit layout** saab hoidikuid lisada, nimetada, neile tüüpi anda, nihutada ja kustutada. Kasutab `mg400-base` serverit (`http://127.0.0.1:8000`), mis peab olema ühendatud ja lubatud (enabled).

```bash
python slot_picker.py          # ava http://127.0.0.1:8010
python slot_picker.py --check  # prindi G-1, E+3, D-2, B+5, F-4 arvutatud X/Y
```

Ainult Pythoni standardteek, lisapakette pole vaja.

## Kuidas liigub

Iga klõps teeb kolm liigutust ja ootab pärast igaüht, kuni käsi kohale jõuab:

1. üles `travel_z`-ni samas X/Y-s;
2. üle `travel_z` kõrgusel lahtri keskpunkti kohale;
3. alla hõljumiskõrgusele (Hover Z).

Pessa ei laskuta: ruudustiku pinna Z puudutus on veel tegemata. R on alati `tool_r` (33), sest napp ei ole J4 teljel ja X/Y sõltub R-ist.

## Kaitsed

- Liikumine ainult siis, kui "Motion enabled" on märgitud; STOP katkestab ja peatab käe (`/api/stop`).
- Kiirus mg400-base-s peab olema ≤ `max_speed_ratio` (30 %); esimene jooks 20 %.
- Lahtrid väljaspool `radius_min`–`radius_max` ja `no_go` hoidikud (veebikaamera post) on hallid.
- Kui mg400-base piirab sihtpunkti (clamp) või robotil on viga/alarm, liikumine peatub.
- Hover Z lubatud vahemik on `min_hover_z` … `travel_z` (24.10.26: `travel_z` −90, hover −110 … −90, vaikimisi −110; hoidikute ülaservast ~50 / ~30 mm kõrgemal). Enne liikumist kontrollitakse `/api/check`-iga, kas hover-punkt ja sirge tee `travel_z` kõrgusel on käeulatuses (aluse lähedalt läbiv tee jõuab J3−J2 piirini); ridade A rakud ei jõua nii madalale (J3−J2 piir).

## Paigutuse redaktor (Edit layout)

- **Lohistamine**: vajuta hoidiku lahtrile ja lohista — kogu hoidik liigub kursori/sõrmega kaasa (teise hoidiku peale või ruudustikust välja ei lähe, jääb viimasesse lubatud kohta). Tühjal lahtril vajutades ja lohistades valitakse ristkülik.
- Klõps lahtril valib/eemaldab selle (sinine raam). Nimi + tüüp + **Add holder from selection** lisab hoidiku.
- Hoidiku real: nime ja tüübi muutmine, nooled nihutavad kogu hoidikut ühe lahtri võrra (← → numbrite, ↑ ↓ tähtede suunas), **Use selection** asendab hoidiku lahtrid valitutega, **Delete** kustutab.
- Lahter saab kuuluda ainult ühele hoidikule; ruudustikust välja nihutada ei saa.
- Midagi ei salvestata enne **Save layout**; server kontrollib (nimi olemas ja kordumatu, tüüp tuntud, lahtrid olemas, kattuvusi pole) ja kirjutab `layout.json`-i. Salvestamata muudatustega Drive-režiimis ei liiguta.
- Tüübid on `layout.json` → `types` (glass, atom, battery, workstation, output, reject, calibration, camera_post, other): nimi ja värv; `no_go: true` (veebikaamera post) teeb lahtrid sõiduks keelatuks. Uue tüübi jaoks lisa sinna rida.

## Test: klaasi tsükkel ja refit-test

Vahekaart **Test** teeb ülesande osa 3 (`assignment-EST.md`): klaas sisendist töökohale, töökohalt väljundisse, neli tükki järjest; tulemused faili `../docs/refit_test.csv`. Loogika failis [`cycle.py`](cycle.py).

**24.10.26 otsus: praegu testime ainult ülekannet** — üks klaas ühest klaasialusest teise, töökohata. See on vaikimisi (`cycle.workstation_step: false`): rollides ainult Input ja Output, õpetada sisendi `pick_z` ja väljundi `place_z` (+ XY), **Run one glass** viib klaasi n sisendi n-ndast lahtrist väljundi n-ndasse. Mitme klaasi käivitus („Loaded input pockets“) on selles režiimis peidetud ja serveris keelatud. CSV-s jäävad töökoha veerud tühjaks (mitte `no`). Täistsükkel töökohaga: märgi **Workstation step** ja **Save roles**. Testitud simuleeritud robotiga; päris robotiga: TODO — waiting for physical test.

1. **Rollid** — vali, milline hoidik on sisend, töökoht (ja mis lahter temas) ning väljund. Klaas n võetakse sisendi n-ndast lahtrist ja pannakse väljundi n-ndasse lahtrisse (lahtri järjekord nagu redaktori loendis; ruudustikul sildid `in 1`…`out 4`, `ws`).
2. **Punktide õpetamine** — **Go above** viib käe pesa kohale (`cycle.travel_z`, vaikimisi −100), Jog-nuppudega (0,2 / 1 / 5 mm) lastakse alla ja **Set** salvestab praeguse asendi: sisend `pick_z`, töökoht `place_z` + `pick_z`, väljund `place_z`, igale ka XY nihe lahtri keskpunktist. Väärtused on hoidiku juures (`holders[].teach`), mitte lahtri juures: kui hoidik pannakse teise ruutu, kasutatakse sama nihet + 42 mm sammu — see on refit-testi 42 mm küsimus. Õpetada R 33 juures.
3. **Käivitus** — üks klaas või kõik **laaditud** pesad: linnukesed „Loaded input pockets 1–4“ ütlevad, millistes sisendi pesades klaas on (robot ise klaasi ei näe; rõhuandur ja kaamera on järgmiste laborite asi). Märkimata pesadesse robot ei sõida. Kontrollitud 24.10.26 simuleeritud mg400 API-ga: märgitud 1 ja 3 → robot laskus ainult D-3, E-3, D+1, D+3, E+3 kohal. Iga klaas: üles → sisendi kohale → `approach_mm` (5 mm) kõrgemale → `pick_z` → imemine, `suck_dwell_s` → üles → töökohale → `place_z` → puhumine `blow_s` → välja → … → väljund. Pärast iga asetamist teeb tööriistakaamera kaadri kausta `frames/` (kaamera viga tsüklit ei peata). Kiirus seatakse mg400-base-s (≤ `max_speed_ratio`).
4. **Tulemus** — linnukesed täituvad sammudest, mis robot lõpetas; robot klaasi ei näe, seega kontrolli ja võta linnuke ära, kui ei õnnestunud, kirjuta märkus. **Save round** kirjutab read `refit_test.csv`-sse: tühi malli rida (ring, klaas) täidetakse, juba täidetud rida jääb alles ja uus tulemus lisatakse selle alla (midagi ei kustutata).

**Move one glass** (Test, 24.10.26): vali lahter, kust klaas võtta (`pick Z`, vaikimisi −150) ja kuhu panna (`place Z`, vaikimisi −145). Käsi: üles `travel_z`-ni, From kohale, alla `pick Z`-ni, imemine, kandmine `travel_z` kõrgusel, To kohal alla `place Z`-ni, puhumine, pump välja, üles. Hoidiku õpetatud XY-nihe (`teach` dx/dy) rakendub. Enne liikumist kontrollitakse käeulatust, teed ja mg400-base Z põrandat.

Ringide vahel võta kõik hoidikud ruudustikust välja ja pane tagasi, ära õpeta punkte uuesti. STOP jätab pumba nagu oli (kantav klaas ei kuku); Pump **Off** vabastab.

Ilma rõhuandurita (Atom COM4) haaratakse õpetatud kõrgusel; vaakumi kontrolli veel pole. Testitud 24.10.26 ainult simuleeritud mg400 API-ga (98 käsku, 4 klaasi, CSV kirjutamine); päris robotiga: TODO — waiting for physical test.

## Kaamera (View)

**View** teeb XIAO tööriistakaameraga (`camera_port`, COM5) kaadri kausta `frames/` (gitignore); leht näitab alati kõige uuemat kaadrit sellest kaustast — ka neid, mille sinna salvestab Claude.

**Live camera** näitab otsepilti (MJPEG `/stream.mjpg`, kuni 4 kaadrit/s, 1600 × 1200). COM5 on avatud ainult siis, kui keegi kaadreid tahab (otsepilt, View, tsükli kaader), ja vabaneb ~10 s pärast; alles siis saab `tool-camera/capture.py` porti kasutada. Olekureal `camera on, N fps` või viga. Testitud 24.10.26 simuleeritud kaameraga (4,0 kaadrit/s); päris XIAO kiirus USB kaudu: TODO — waiting for physical test.

## Rõhk (Atom, COM4)

`pressure.py` loeb vaakumit jagatud AtomS3R-ilt (`pressure_port`, COM4). Uut Atomi püsivara pole: kasutatakse Andmehõive Labor 2 mõõtmis-püsivara `DA2_MEASURE_V1` (`data-acquisition/lab2/src/README.md`), mis pärast `measure_start` käsku saadab G5 ADC toorväärtuse JSON-reana iga 10 ms järel. Väärtus pole kPa-ks kalibreeritud; vaakum = ADC enne imemist (pump väljas) miinus ADC pärast `suck_dwell_s` (MPX5700AP on absoluutandur, vaakumiga ADC langeb). Ära käivita samal ajal Andmehõive logijat — COM4 saab olla ainult ühel programmil.

- Tsüklis enne igat imemist `baseline`, pärast `suck_dwell_s` `grip`: tulemus `vacuum N ADC ok` / `LOW` lehel Test-vahekaardi all ("grip: …"). See ainult märgib, tsüklit ei peata.
- Kui ridu ei tule üle 1 s (juhe lahti, Atom vaikib, port puudub), näitab olekurida punast viga "running without the vacuum check"; tsükkel jätkab ilma vaakumi kontrollita ja Atomit proovitakse iga sekundi järel uuesti.
- `cycle.grip_min_vacuum_adc` = 100 on oletus (Labor 1 −60 kPa ≈ 427 koodi, `141 Pa/kood`); päris haarde väärtus: TODO — waiting for physical test.

Testitud 24.10.26 simuleeritud Atomiga (~95 Hz, vaakum, katkestus ja taastumine) ja ühe klaasi tsükliga ilma Atomita (tsükkel lõppes, kõik 4 sammu); päris Atomiga: TODO — waiting for physical test.

## Probe (puudutuse andmed)

Test-vahekaardil Jog-nuppude all. Kogub andmeid, millega hiljem häälestada puudutuse tuvastus (kaamera + vaakum) ja isekalibreerimine; ise veel midagi ei tuvasta.

1. Jogi käsi mõne mm kõrgusele pinnast (Z ↓) või seina kõrvale kalibreerimiskastis (X±/Y±, roboti teljed).
2. Vali samm (0,2 / 0,5 / 1 mm), vahemaa (≤ `probe.max_distance_mm`, 10 mm), soovi korral **suction** ja silt, vajuta **Probe**.
3. Iga sammu järel ootab `probe.settle_s` ja kirjutab rea faili `probes/<aeg>-<silt>-<telg>/probe.csv` (siht ja tegelik asend, Atomi ADC 0,3 s keskmine, vaakum, pump, kaadri nimi) ning kaadri `step-NN.jpg`. Algasend on samm 0.
4. Lõpus: suction korral pump välja (all, mitte üles tõustes), siis tagasi algasendisse. STOP katkestab, juba kirjutatud read jäävad; käsi jääb sinna, pump nagu oli.

Kaamera või Atomi puudumine ei peata sondeerimist (tühi veerg / `no frame: …`). Ühe jooksu kaadrid ~150 KB tükk; `probes/` ei ole gitignore'is, et head jooksud saaks commitida. Testitud 24.10.26 simuleeritud roboti, kaamera ja Atomiga (sammud, vaakumi hüpe CSV-s, STOP, vigased sisendid); päris robotiga: TODO — waiting for physical test.

Kasulikud esimesed jooksud: Z ↓ ruudustiku pinnale (ilma ja koos imemisega), Z ↓ klaasile sisendhoidikus imemisega, ning G-1 kalibreerimiskastis kõik neli seina 0,5 mm sammuga.

## Seaded — `layout.json`

- `calibration` — ainult `tool_r` (33). Lahtrite X/Y tuleb failist [`../calibration/cells.py`](../calibration/cells.py) (24.10.26 kolme ruudu sobitus, pööre +0,87°); uue kalibreerimise järel muuda seal `MEASURED`.
- `motion` — Drive-režiimi kõrgused, kiiruse piir, ulatus.
- `cycle` — tsükli rollid, töökoha lahter, `travel_z`, `approach_mm`, `suck_dwell_s`, `blow_s`.
- `types` — hoidikute tüübid (nimi, värv, `no_go`).
- `holders` — hoidikud: `name`, `type`, `cells`, `status`. Muuda redaktoriga. Praegused read on **ettepanek**, mitte kinnitatud paigutus (`docs/layout.md`); 24.10.26 oli klaas tegelikult B+5 hoidikus.

Testitud ainult simuleeritud mg400-base API-ga. Päris robotiga: TODO — waiting for physical test.
