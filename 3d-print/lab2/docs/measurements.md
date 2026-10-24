# Riistvara mõõtmise kontrollnimekiri

Täida see fail päris detailide, tööriista, roboti ja laua juures. Kõik mõõdud märgitakse millimeetrites, mass grammides, nurgad kraadides ning elektrilised väärtused koos ühikuga. Mõõtmata väljade olek: `TODO — waiting for physical test`.

## 23.10.2026 — Maksimi mõõtetabeli ülekanne

Allikas: Maksim Naprejevi `Measurements.xlsx`, leht `Measurements`, kasutaja edastatud 23.10.2026. Töövihiku metaandmete viimane salvestus on 04.10.2026; see ei tõenda mõõtmise kuupäeva. Mõõtevahendit, mõõtemääramatust ega iga mõõtmise kuupäeva tabelis ei nimetata; väärtusi ei nimetata seetõttu nihikuga mõõdetuks. Meeskond kinnitas vestluses klaasi paranduse ja allolevad põhiväärtused. Allikafaili SHA-256: `946e7466c0eb05d63c17f2222aefe6852a7c1d1670e59d97a939765f6bedd495`.

Algset Excelit ei lisatud avaldamiseks: metaandmetes on isikliku profiiliga seotud ülikooli sisemine võrgutee. Fail säilib kasutaja antud kohalikus asukohas muutmata; allpool on avaldamiseks sobiv eestikeelne ülekanne koos lahtriviidetega.

Olekud: `measured` = allikas nimetab mõõdetuks; `nominal` = nimimõõt, mitte füüsiline mõõtmine; `confirmed` = tabelis või meeskonna poolt kinnitatud; `planned` = kavatsus, nõue või ligikaudne lähteasend, mitte katsetulemus; `TODO` = puuduv mõõtmine või kontroll. Füüsiliselt kontrollimata tulemuse tekst on `TODO — waiting for physical test`. Allpool toodud register täiendab varasemat kontrollnimekirja; varasemad TODO-read säilivad ajaloo jaoks ega tühista uut registrit.

| Detail / omadus | Väärtus | Olek | Allikas ja piirang |
|---|---|---|---|
| AtomS3 X × Y × Z | 24 × 24 × 12,9 mm | nominal; meeskond kinnitas nimimõõdu | D2:E4; tegelikud gabariidid: TODO — waiting for physical test |
| AtomS3 USB-C keskjoon valitud servast | 11,4 mm | measured | D5:E5; serva nimetus ja mõõtesuund puuduvad, vajavad fotot / skeemi; mitte automaatselt roboti nihe |
| AtomS3 ekraan ja nupp ligipääsetavad | jah | confirmed, tabeli kirjeldus | D6:E6; uue hoidiku kontroll: TODO — waiting for physical test |
| AtomS3 orientatsioon hoidikus | ekraan üles | planned | D7:E7; fikseeritud orientatsioon korduvaks võtmiseks |
| Klaas nr 1 X × Y × Z | 30 × 30 × 2 mm | confirmed | D8:E10; mõõtevahend ja mõõtemääramatus puuduvad |
| Klaas nr 2 X × Y × Z | 30 × 30 × 2 mm | confirmed | D11:E13; mitte eraldi nihikumõõtmise tõend |
| Klaas nr 3 X × Y × Z | 30 × 30 × 2 mm | confirmed | D14:E16; mitte eraldi nihikumõõtmise tõend |
| Klaas nr 4 X × Y × Z | 30 × 30 × 2 mm | confirmed | D17:E19; mitte eraldi nihikumõõtmise tõend |
| Nelja klaasi min–max ja hajuvus | TODO — waiting for physical test | TODO | D20:E20; kinnitatud täisarvudest ei järeldata nullhajuvust |
| Akumoodul X × Y × Z | 24,04 × 24,01 × 21,97 mm | measured | D21:E23; vahend ja määramatus märkimata |
| Akumooduli pistiku asukoht | mõõtmine vahele jäetud | planned, lähteallika SKIP | D24:E24: „not needed”; pole mõõdetud ega null; kui pistik mõjutab pesa, siis TODO — waiting for physical test |
| Akumooduli orientatsioon | kontaktid üles | planned | D25:E25; fikseeritud orientatsioon korduvaks võtmiseks |
| XIAO ESP32S3 Sense põhiplaat X × Y × Z | 17,74 × 21,33 × 1,21 mm | measured | D26:E28; D26 ujukomaarv esitatud kahe komakohaga; ei kirjelda kaameralaiendust ega kogu koostu |
| Tööriistakaamera ligikaudne nurk | 90°; vertikaalselt alla | planned | D47:E47; nulltasapind täpsustamata, pole mõõdetud vaatenurk ega lõplik paigaldusnurk |
| Kaamera USB-C ligipääs | peab jääma vabaks | planned | D52:E52: „yes” on konstruktsiooninõue, mitte läbitud sobivuskatse |

### Exceli lahtised mõõtmised ja kaamera

| Mõõtmine / kontroll | Ühik / sisu | Allika lahtrid | Olek / järgmine tegevus |
|---|---|---|---|
| Kaameraplaadi X/Y/Z | mm | D29:E31 | TODO — waiting for physical test |
| Objektiivi keskme X/Y nihe | mm; määrata esmalt lähteservad | D32:E33 | TODO — waiting for physical test; Z puudub tabelist ja tuleb samuti määrata |
| XIAO USB-C keskjoone asukoht | mm | D34:E34 | TODO — waiting for physical test |
| Antenni vaba ala | mm ja kirjeldus; mitte katta | D35:E35 | TODO — waiting for physical test |
| Iminapa hoidiku vaba kinnituspinna laius/kõrgus/sügavus | mm | D36:E38 | TODO — waiting for physical test |
| Kinnituspunkti kaugus iminapast | mm; määrata nullpunkt | D39:E39 | TODO — waiting for physical test |
| Vabaks jäävad alad | voolik, flants, kruvid, liikumistee | D40:E40 | TODO — waiting for physical test |
| Iminapa füüsiline läbimõõt | mm | D41:E41 | TODO — waiting for physical test; G-1 katsest tuletatud ligikaudne efektiivne läbimõõt ei asenda mõõtmist |
| Iminapa tööriista kogulaius ja -kõrgus | mm | D42:E43 | TODO — waiting for physical test |
| Mass enne kaamerat / kaamerakoost / mass pärast kinnitamist | g | D44:E46 | TODO — waiting for physical test |
| Objektiivi kaugus töökohast / kõrgus klaasi kohal | mm tööasendis | D48:E49 | TODO — waiting for physical test |
| Kogu 30 × 30 mm klaas kaadris | katsepilt | D50:E50 | TODO — waiting for physical test |
| Atom ja töökoht kaadris | katsepilt | D51:E51 | TODO — waiting for physical test |
| Valitud USB-C kaabli pikkus | mm | D53:E53 | TODO — waiting for physical test |
| Kaabli kinnituspunktid robotil | kirjeldus | B54:E54; pealkiri poolik, väärtus tühi | TODO — waiting for physical test |

Olemasolev tõend eraldi Excelist: README 23.10.26 kaamerasessioon ja commit `9e68690` kirjeldavad arvuti USB-C toidet, USB kaudu JPEG-kaadrit 1600 × 1200 px ning OV3660 sensorit (PID 0x3660). See ei kinnita kogu klaasi nähtavust ega kokkupõrkevabadust. Toite pinge/vool, kaabli marsruut, tõmbetõke ja tööriista mass: `TODO — waiting for physical test`.

### Parandus klaasi mõõdule

23.10.2026: varasem `24 × 24 × 2 mm` on meie füüsilise klaasi kohta vale. Õige kinnitatud lähteväärtus on **30 × 30 × 2 mm** (D8:E19 ja meeskonna kinnitus). `24 × 24 mm` kuulub AtomS3 nimimõõdule ning aku ligikaudsele gabariidile; aku tegelik allikaväärtus on 24,04 × 24,01 mm. Ametliku ülesande originaal ja varasemad kirjed säilivad; need ei ole meie klaasi mõõteallikas. CAD-i ja trajektoori kontroll: [`cad-measurement-review.md`](cad-measurement-review.md).

## AtomS3

| Väli | Mõõdetud väärtus | Meetod / märkus |
|---|---|---|
| X (mm) | TODO — waiting for physical test | |
| Y (mm) | TODO — waiting for physical test | |
| Z (mm) | TODO — waiting for physical test | |
| Orientatsioon hoidikus | TODO — waiting for physical test | Ekraan üles; kinnitada detailil. |
| USB-C pesa asukoht | TODO — waiting for physical test | |
| Nupu ligipääsetavus | TODO — waiting for physical test | |

## Polükarbonaatklaas

Mõõda vajaduse korral mitu klaasi ja säilita kõik üksiktulemused, et hiljem saaks arvutada tegeliku hajuvuse.

| Klaasi ID | X (mm) | Y (mm) | Z (mm) | Mõõtevahend / märkus |
|---|---|---|---|---|
| 1 | TODO — waiting for physical test | TODO — waiting for physical test | TODO — waiting for physical test | |
| 2 | TODO — waiting for physical test | TODO — waiting for physical test | TODO — waiting for physical test | |
| 3 | TODO — waiting for physical test | TODO — waiting for physical test | TODO — waiting for physical test | |
| 4 | TODO — waiting for physical test | TODO — waiting for physical test | TODO — waiting for physical test | |

- Mõõdetud miinimum–maksimum ja tegelik hajuvus (mm): TODO — waiting for physical test

## Akumoodul

| Väli | Mõõdetud väärtus | Meetod / märkus |
|---|---|---|
| X (mm) | TODO — waiting for physical test | |
| Y (mm) | TODO — waiting for physical test | |
| Z (mm) | TODO — waiting for physical test | |
| Pistiku asukoht | TODO — waiting for physical test | |
| Orientatsioon hoidikus | TODO — waiting for physical test | |

## XIAO ESP32S3 Sense

| Väli | Mõõdetud väärtus | Meetod / märkus |
|---|---|---|
| Plaadi X/Y/Z (mm) | TODO — waiting for physical test | |
| Kaameralaienduse X/Y/Z (mm) | TODO — waiting for physical test | |
| Objektiivi asukoht X/Y/Z (mm) | TODO — waiting for physical test | Märgi kasutatud nullpunkt. |
| USB-C pesa asukoht | TODO — waiting for physical test | |
| Antenni ala ja keep-out-tsoonid | TODO — waiting for physical test | Ära kata ega ümbritse metalliga. |

## Olemasolev iminapa tööriistahoidik

| Väli | Mõõdetud väärtus | Meetod / märkus |
|---|---|---|
| Kinnituseks vabad pinnad | TODO — waiting for physical test | |
| Kinnitusala mõõdud X/Y/Z (mm) | TODO — waiting for physical test | |
| Kaugus iminapani (mm) | TODO — waiting for physical test | Märgi mõõtesuund ja nullpunkt. |
| Alad, mida ei tohi katta | TODO — waiting for physical test | Flants, voolik, iminapa liikumistee jm. |

## Tööriistakaamera

| Väli | Mõõdetud / valitud väärtus | Katse / märkus |
|---|---|---|
| Valitud vaatenurk (°) | TODO — waiting for physical test | |
| Kõrgus töökoha suhtes (mm) | TODO — waiting for physical test | |
| Nähtav ala (mm või px) | TODO — waiting for physical test | |
| Tööriista mass enne (g) | TODO — waiting for physical test | |
| Tööriista mass pärast (g) | TODO — waiting for physical test | |
| Valitud toide | TODO — waiting for physical test | Pinge ja vool koos ühikutega. |
| Kaabli marsruut | TODO — waiting for physical test | Kontrollida kogu käe liikumisel ja J4 pööramisel. |
| Tõmbetõke | TODO — waiting for physical test | |

## USB üldvaate veebikaamera

| Väli | Mõõdetud / valitud väärtus | Katse / märkus |
|---|---|---|
| Kaamera X/Y/Z (mm) | TODO — waiting for physical test | |
| Kinnituse tüüp ja liides | TODO — waiting for physical test | |
| MG400 käe suurim kõrgus (mm) | TODO — waiting for physical test | Mõõta tegelikul liikumisteel. |
| Vajalik kaamera kõrgus (mm) | TODO — waiting for physical test | Kogu ruudustik ja robot peavad kaadrisse mahtuma. |
| Asukoht ruudustiku suhtes | TODO — waiting for physical test | Ruut või mõõdetud nihe X/Y/Z (mm). |
| USB-kaabli pikkus (mm) | TODO — waiting for physical test | |
| Vibratsioon (px või mm laual) | TODO — waiting for physical test | Märgi roboti kiirus ja mõõtemeetod. |
| Kordustäpsus pärast eemaldamist/tagasipanekut (px või mm) | TODO — waiting for physical test | |

## Gridfinity kalibreerimine

### Esimene kalibreerimisprint

| Väli | Tulemus | Märkus |
|---|---|---|
| Kandidaatversioon | TODO — waiting for physical test | Näiteks `gridfinity-calibration-v2.scad`; kirja panna päriselt prinditud versioon. |
| Sobitusparandus külje kohta (mm) | TODO — waiting for physical test | CAD-i `fit_adjustment`; täislaiuse muutus on sellest kaks korda suurem. |
| Istub täielikult põhja | TODO — waiting for physical test | |
| Loks | TODO — waiting for physical test | |
| Eemaldamiseks vajalik jõud / pingutus | TODO — waiting for physical test | Kui mõõdad jõudu, kirjuta ühik N. |
| Vajalikud muudatused | TODO — waiting for physical test | Uue prindi korral salvesta eraldi versioon. |

| Väli | Mõõdetud / arvutatud väärtus | Meetod / märkus |
|---|---|---|
| Kasutatud ruut | TODO — waiting for physical test | Soovituslik algusruut B-2. |
| Füüsiline sobivus | TODO — waiting for physical test | |
| Loks | TODO — waiting for physical test | Mõõt või kirjeldatud kontroll. |
| Roboti mõõdetud X/Y/Z (mm) | TODO — waiting for physical test | |
| Valemiga arvutatud X/Y/Z (mm) | TODO — waiting for physical test | Kasuta `MG 400 rakis.md` valemit ja kinnitatud telgede teisendust. |
| Nihe X/Y/Z (mm) | TODO — waiting for physical test | Mõõdetud miinus arvutatud. |
| Kauge kontrollruut | TODO — waiting for physical test | Näiteks E+3. |
| Kauge ruudu viga X/Y/Z (mm) | TODO — waiting for physical test | |

### Nelja sisenurga meetod (vt `test-procedure.md`, A1)

| Ruut | Nurk 1 X/Y | Nurk 2 X/Y | Nurk 3 X/Y | Nurk 4 X/Y | Keskpunkt X/Y | Pööre (°) | Märkus |
|---|---|---|---|---|---|---|---|
| B-2 | TODO — waiting for physical test | TODO | TODO | TODO | TODO | TODO | |
| B-2 (pärast välja/tagasi) | TODO — waiting for physical test | TODO | TODO | TODO | TODO | TODO | kordustäpsus |
| E+3 | TODO — waiting for physical test | TODO | TODO | TODO | TODO | TODO | kauge ruudu viga |
| G-1 (23.10.26, poolik) | Xmax+Ymin: 404.47 / 18.80 | Xmax+Ymax: 403.98 / 34.34 | Xmin+Ymax: 389.47 / 33.80 (Z −150.85) | Xmin+Ymin: 389.50 / 18.77 — kinnitamata | eeldatav ≈ 396.85 / 26.43 | ≈ −1,8 (ebakindel) | vt allpool |
| G-1 (24.10.26, diagonaal) | Xmin+Ymax: 403.81 / 44.90 (Z −87.27) | Xmax+Ymin: 437.19 / 10.20 | — | — | **420.50 / 27.55** | vt E+3 | R 32.76; pärast J4 lahtikerimist |
| E+3 (24.10.26, diagonaal) | Xmax+Ymin: 357.50 / −118.46 (Z −87.00) | Xmin+Ymax: 323.50 / −83.83 (Z −85.00) | — | — | **340.50 / −101.15** | **+1,82** (G-1 ja E+3 vahel) | R 33.00 |

23.10.26 märkused (G-1, nelja sisenurga meetod; toorandmed [`calibration_g-1_corners.csv`](calibration_g-1_corners.csv)):

- Ruut B-2 osutus liiga lähedaseks: raadiusel ~192 mm J1-st jõuab käsi ainult Z ≈ −98-ni (J3 105° piir, `mg400-base` `kinematics.py`), kasti põhja ei ulatu. Seetõttu kalibreeriti kaugemas ruudus **G-1** (ülesande järgi "near the limit" tsoon).
- Kalibreerimiskast `gridfinity-calibration-v1` (STL-ist): välismõõt 41,2 × 41,2 × 20 mm, sisemus **37,2 × 37,2 mm**, teravad sisenurgad, põhi 4 mm, sisemuse sügavus 16 mm.
- Iminapa käik kasti sees: X ≈ 14,8 mm, Y ≈ 15,3 mm → napa efektiivne läbimõõt **≈ 22 mm** (37,2 − käik). Pehme napp kaldub seina vastu juba enne, kui robot tegelikult "puudutab"; puudutuse kriteerium = napp sirge ja seina vastas, kalle näitab ülesurumist.
- G-1 keskpunkt mudelist (`MG 400 rakis.md` §4) roboti raamis eeldusel X_robot = −x, Y_robot = −y: **391,5 / 21,0**. Eeldatav nihe mõõdetud − arvutatud ≈ **+5,3 / +5,4 mm**. Eelinfo: neljas nurk kinnitamata ja Xmin+Ymax nurk teisel Z-l; telgede suund kontrollimata (vaja kontrollruutu lähemal robotile, nt C+2).

24.10.26 kalibreerimine (asendab 23.10 eelinfot; toorandmed samas CSV-s):

- Enne algust oli J4 loendur 814,9° (üle +180° piiri, viga `Joint4 exceeds positive limit`); kaabel ei olnud keerdus. J4 keerati DobotStudio Pro Jog-režiimis tagasi → 26,4°. Tööriista füüsiline suund muutus, seega 23.10 nurgad (R 36) ei ole tänastega võrreldavad. **Kõik punktid võetakse R ≈ 33 juures**, sest napp ei ole päris J4 teljel ja X/Y sõltub R-ist.
- Keskpunkt = kahe vastasnurga keskmine (diagonaal).
- Ainult nihkega (G-1 järgi +29,00 / +6,55) andis E+3 vea +4,0 / −2,7 mm → ruudustik on roboti telgede suhtes **pööratud +1,82°**. Mõõdetud kaugus G-1 → E+3 151,54 mm, mudelis 151,43 mm (mastaap 1,0007) → telgede suund (mudel pööratud 180° ümber Z) ja 42 mm samm on õiged.
- Teisendus: mudeli punkt (X = −x, Y = −y) pööratakse +1,82° ümber G-1 ja E+3 mudelkeskpunktide keskmise (349,5 / −42,0) ja nihutatakse mõõdetud keskmisse (380,50 / −36,80).
- Kontroll Z −53 juures: robot viidi arvutatud keskpunktidesse **E+2 339,19 / −59,12** ja **E+4 341,86 / −143,08** — mõlemad kasutaja hinnangul keskel. Kalibreerimine kinnitatud.
- Veel tegemata: Z puudutus ruudustiku pinnal; kasti välja/tagasi kordustäpsus.

24.10.26 hiljem — parandus (eelmised read jäävad alles):

- D-2 kontroll klaasi sisendhoidiku pesas Z −150 juures (iminapp pesa põhjas, kasutaja seadis keskele): mõõdetud **297,20 / 67,48**, G-1+E+3 teisendus ennustas 293,20 / 65,48 → viga **+4,0 / +2,0 mm**.
- Kaugused ei klapi jäiga ruudustikuga: G-1–D-2 mõõdetud 129,60, mudelis 132,82 (−3,21 mm). Tõenäoline põhjus: G-1 ja E+3 nurgad võeti Z −85…−87 juures, ~50 mm kasti/ruudustiku kohal, silma järgi (parallaks); D-2 võeti puutes.
- Uus teisendus: kolme ruudu (G-1, E+3, D-2) jäik vähimruutude sobitus, pööre **+0,87°**, R 33. Jääkvead G-1 −1,80/+0,53, E+3 +0,27/−0,91, D-2 +1,53/+0,38 mm. Skript [`calibration/cells.py`](../calibration/cells.py) (ruut → roboti X/Y).
- Kontroll ruutudes, mida sobitus ei kasutanud: **B+5 215,52 / −186,15** ja **F-4 378,39 / 152,37** — kasutaja hinnangul keskel (Z −130 / −100, silma järgi). Kalibreerimine praegu kasutatav.
- Täpsustamiseks: korrata nurkade mõõtmist puutes (kasti põhjas, Z ≈ −155) 3–4 ruudus, eesmärk jääkviga < 0,5 mm.

24.10.26 õhtu — kontroll kalibreerimiskastiga v3 ruudus C-2 (toorandmed [`calibration_c-2_v3.csv`](calibration_c-2_v3.csv)):

- Kast `gridfinity-calibration-v3` (standardne Gridfinity jalg, pesa 37 × 37 mm, rist põhjas) ruudus **C-2**; C-2 ei olnud `cells.py` sobituses, seega see on sõltumatu kontroll. R 33, kiirus 2 %, sammud 0,5 mm; puudutust hindas Denys silmaga (napp sirge ja seina vastas, kast ei kaldu).
- Z puudutus kasti põhjal/ristil lahtri keskel: **Z −155,0** (kaksik ennustas põhja −154,8, risti pealt −154,2) → napa pikkus kaksikus õige ±0,8 mm piires.
- Neli nurka Z −152 juures (3 mm põhja kohal): +X+Y 260,68 / 75,46; +X−Y 260,68 / 61,46; −X−Y 246,68 / 61,46; −X+Y 247,18 / 75,46. Teise nurga esimene katse Y 60,46 juures surus seina ja kallutas kasti veidi — tagasi 1 mm, kast istus tagasi; arvesse läks 61,46.
- Kontroll: vastasküljed 14,00 / 14,01 ja 14,00 / 13,50, diagonaalid 19,80 / 19,45 mm (erinevus ≤ 0,5 mm = silmaga puudutuse täpsus).
- Keskpunkt (nelja nurga keskmine): **253,81 / 68,46**; `cells.py` ennustas 253,68 / 66,46 → viga **+0,12 / +2,00 mm**. Kontroll: napp viidi mõõdetud keskpunkti Z −150 juurde — Denys: keskel risti kohal.
- Napa käik 37 mm pesas 14 mm → napa efektiivne läbimõõt sellel kõrgusel **≈ 23 mm** (23.10 v1 kastiga ≈ 22; kaksik eeldab 20).
- Tähelepanek: sama +2 mm Y-suunas õpetati 24.10 klaasi sisendhoidikus D-4 (`teach.dy 2.0`, slot picker). Võimalik põhjus: `cells.py` sobituse D-2 punkt võeti vanade jalgadega klaasihoidikus (jala lõtk ~0,95 mm külje kohta), uus v3 kast istub lõtkuta. Otsus `cells.py` uue sobituse kohta: TODO — meeskond.
- Kasti välja/tagasi kordustäpsust ei mõõdetud (Denys: keskpunkt sobib, uuesti ei kalibreeri).
- Samal õhtul (Denys: „поменяй“): C-2 lisati `cells.py` sobitusse (4 ruutu, pööre **+0,61°**). Jääkvead G-1 −1,88/+0,45, E+3 +0,76/−1,35, D-2 +1,26/−0,27, C-2 −0,14/+1,16 mm — jäik sobitus ei mahu 1 mm sisse, nõrgimad on G-1 ja E+3 (silma järgi Z −87, parallaks) ning D-2 (vanade jalgadega hoidik). Täpsustamiseks: 2–3 ruutu (nt E+3, F-3) kastiga v3 puutes ja uus sobitus ainult nende põhjal.
- Klaasi sisendhoidiku õpetus teisendati nii, et D-4 päris punkt jääb samaks (294,40 / 153,09): dx 0 → −0,64, dy 2,0 → 1,35.
- 18:14: Denys seadis slot pickeriga napa C-2-s kasti põhjal (Z −155,0) risti keskele: **253,94 / 68,30** (nelja nurga tulemus 253,81 / 68,46, vahe 0,13 / 0,16 mm). `cells.py`-s kasutatakse nüüd seda punkti; sobitus +0,62°, C-2 arvutuslik 253,97 / 67,24 → jääkviga C-2-s endiselt −0,03 / +1,06 mm, sest jäik sobitus kaalub nelja punkti võrdselt ja G-1, E+3, D-2 vead on 1–2 mm. Klaasi sisendhoidiku õpetus uuesti teisendatud (dx −0,65, dy 1,39), D-4 päris punkt sama.
- 18:16: Denys seadis napa klaasi sisendhoidiku pesa D-4 keskele (Z −150,0): **293.56 / 154.20**. Varasem õpetus (Raimo 17:06) näitas 294.41 / 153.09 → vahe -0.85 / +1.11 mm. Salvestatud hoidiku õpetusena (`teach` dx -1.50, dy +2.50 lahtri D-4 keskpunktist), mitte `cells.py`-sse: hoidik on vanade jalgadega (lõtk ~1 mm), seega pesa keskpunkt sisaldab hoidiku asendit ruudustikus. `pick_z` muutmata (−150,5).

Kui hiljem leitakse vale mõõt, ära kustuta seda. Lisa kuupäevaga parandus vana väärtuse alla ning selgita mõõtekonteksti.
