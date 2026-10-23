# Riistvara mõõtmise kontrollnimekiri

Täida see fail päris detailide, tööriista, roboti ja laua juures. Kõik mõõdud märgitakse millimeetrites, mass grammides, nurgad kraadides ning elektrilised väärtused koos ühikuga. Mõõtmata väljade olek: `TODO — waiting for physical test`.

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

23.10.26 märkused (G-1, nelja sisenurga meetod; toorandmed [`calibration_g-1_corners.csv`](calibration_g-1_corners.csv)):

- Ruut B-2 osutus liiga lähedaseks: raadiusel ~192 mm J1-st jõuab käsi ainult Z ≈ −98-ni (J3 105° piir, `mg400-base` `kinematics.py`), kasti põhja ei ulatu. Seetõttu kalibreeriti kaugemas ruudus **G-1** (ülesande järgi "near the limit" tsoon).
- Kalibreerimiskast `gridfinity-calibration-v1` (STL-ist): välismõõt 41,2 × 41,2 × 20 mm, sisemus **37,2 × 37,2 mm**, teravad sisenurgad, põhi 4 mm, sisemuse sügavus 16 mm.
- Iminapa käik kasti sees: X ≈ 14,8 mm, Y ≈ 15,3 mm → napa efektiivne läbimõõt **≈ 22 mm** (37,2 − käik). Pehme napp kaldub seina vastu juba enne, kui robot tegelikult "puudutab"; puudutuse kriteerium = napp sirge ja seina vastas, kalle näitab ülesurumist.
- G-1 keskpunkt mudelist (`MG 400 rakis.md` §4) roboti raamis eeldusel X_robot = −x, Y_robot = −y: **391,5 / 21,0**. Eeldatav nihe mõõdetud − arvutatud ≈ **+5,3 / +5,4 mm**. Eelinfo: neljas nurk kinnitamata ja Xmin+Ymax nurk teisel Z-l; telgede suund kontrollimata (vaja kontrollruutu lähemal robotile, nt C+2).

Kui hiljem leitakse vale mõõt, ära kustuta seda. Lisa kuupäevaga parandus vana väärtuse alla ning selgita mõõtekonteksti.
