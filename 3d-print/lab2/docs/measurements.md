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
| Iminapa füüsiline läbimõõt | mm | D41:E41 | TODO — waiting for physical test |
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

## 13.11.2026 — AtomS3 ja klaas nihikuga

Mõõtis Denys nihikuga laboris 13.11.2026.

| Detail | X × Y × Z (mm) | Võrdlus |
|---|---|---|
| AtomS3 | 24 × 24 × 12,9 | sama mis M5Stacki mudel (`3d-print/models/m5stack-atoms3`) |
| Polükarbonaatklaas | 30 × 30 × 1,2 | 4 klaasi |

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
| Valitud toide | USB-C kaabel arvutist (USB 5 V) | Kaabel annab ka pildi; läheb roboti taha, J4 pööre ei sega. |
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

### Kalibreerimiskast

`gridfinity-calibration` (1 × 1, 41,5 × 41,5 × 21 mm, standardne Gridfinity jalg generaatorist, sisetasku 37 × 37 mm, rist põhjas): istub ruudustikus täielikult ega loksu.

### Kalibreerimine 13.11.2026

Ruudustik on lükatud roboti platvormi (pesa) vastu. R 33, napp flantsi all keskel (nihe J4 teljest ≈ 0). Kalibreerimiskast kahes kauges ruudus; Denys seadis napa silmaga pesa keskele, napp lasti kasti põhjani. Toorandmed: [`calibration.csv`](calibration.csv).

| Ruut | Roboti X (mm) | Roboti Y (mm) | Z põhjal (mm) | Märkus |
|---|---|---|---|---|
| F-2 | 353,80 | 69,80 | −155,0 | kauge ruut |
| C+4 | 232,80 | −144,20 | −155,0 | teine ots, pöörde jaoks |

- Jäik sobitus (pööre + nihe, mudel pööratud 180° ümber Z) failis [`calibration/cells.py`](../calibration/cells.py): pööre **+1,48°**. Kaugus F-2 ↔ C+4 mõõdetud 245,84 mm, CAD-is 244,90 mm → jääkviga **0,47 mm** punkti kohta.
- Ruudustiku asukoht kaksikus „vastu ja keskel“ suhtes: +0,7 mm (= vastu), −2,8 mm külgsuunas piki torusid (`twin.grid_slide()`).
- Kontroll: slot picker sõitis uue kalibreerimisega D+3-sse (heade väljund); Denys: napp keskel, „все идеально“.
- B-2 (ülesande soovitatud ruut) ei sobi: raadiusel ~192 mm J1-st jõuab napp ainult Z ≈ −98-ni (J3 105° piir), kasti põhja ei ulatu.
- Mõõtmata: kasti välja/tagasi kordustäpsus.

### Klaasi sisendhoidiku õpetus (24.10.26 õhtu)

- 18:16: Denys seadis napa klaasi sisendhoidiku pesa D-4 keskele (Z −150,0): **293.56 / 154.20**. Varasem õpetus (Raimo 17:06) näitas 294.41 / 153.09 → vahe -0.85 / +1.11 mm. Salvestatud hoidiku õpetusena (`teach` dx -1.50, dy +2.50 lahtri D-4 keskpunktist), mitte `cells.py`-sse: hoidik on vanade jalgadega (lõtk ~1 mm), seega pesa keskpunkt sisaldab hoidiku asendit ruudustikus. `pick_z` muutmata (−150,5).
- 18:19: sama D-5 pesas: **292,10 / 196,19** (lahtri keskpunkt 294,60 / 193,69 → −2,50 / +2,50). D-4 → D-5 mõõdetud −1,46 / +41,99 = 42,02 mm (samm õige), suund −1,99° → hoidik on ruudustikus veidi pööratud (vanad jalad). Slot picker hoiab ühte nihet hoidiku kohta → kahe pesa keskmine **dx −2,00, dy +2,50** (kummaski pesas ≤ 0,5 mm X-viga). E-4 / E-5 mõõtmata.

24.10.26 õhtu — töökoha õpetamine (paigutus B, oranž hoidik C±1):

- C+1 pesas akumoodul + AtomS3 (ekraan üles) + klaas peal (Denys). Napp R 33, kiirus 5 %, XIAO kaamera v2 kinnitusel kontrolliks.
- XY: lahtri C+1 keskpunkt `cells.py` järgi 254,88 / −16,75 — Denys: napp klaasi keskel → oranži hoidiku nihe **0 / 0**.
- Z: Denys laskis napa klaasi puudutuseni, madalamale ei saa: **Z −119,0** → `place_z` ja `pick_z` = −119,0 (slot picker Test → Set, `cycle.workstation_cell` = C+1).
- Kaksik ennustas −114,1 → päris virn on 4,9 mm madalamal. Põhjus selgitamata (aku pesa sügavus, oranži hoidiku vanad jalad, AtomS3 nimimõõt 12,9): TODO.
- Väljund (`valjundhoidik-v1`, D/E +4/+5): klaas D+4 lahtris põhjal, Denys laskis napa klaasi puudutuseni lahtri keskel 298,25 / −142,29: **Z −153,0** → väljundi nihe 0 / 0, `place_z` −153,0 (kaksik −151,3).
- Kõik kolm päris punkti on kaksikust madalamal: sisend −1,5, väljund −1,7, töökoht −4,9 mm. Sisendi ja väljundi ühine ~1,6 mm viitab kaksiku napa pikkusele (66,2 mm); töökohal lisaks ~3,3 mm (virn). Kaksiku kõrgused tuleb nende punktide järgi parandada: TODO.
## 24.10.2026 — iminapa mõõtmised, massihinnang ja sisendhoidikute sobivus

Allikas: kasutaja 24.10.2026 edastatud füüsilised mõõtmised ja käsitsi tehtud sobivuskontroll. Allolev täiendus ei muuda varasemaid Exceli andmeid ega kalibreerimiskirjeid.

### Eraldi kummist iminapp — measured

| Tähis / omadus | Väärtus | Olek | Mõõtemeetod ja ulatus |
|---|---|---|---|
| D41 — iminapa välisläbimõõt | 22,25 mm | measured | Kasutaja mõõtis nihikuga 24.10.2026 eraldi kummist iminappa. Täiendab Exceli D41 puuduvat väärtust; algset Excelit ei muudetud. |
| H1 — iminapa kõrgus | 13,80 mm | measured | Sama eraldi kummist iminapp, nihik, 24.10.2026. H1 on lisamõõdu tähis, mitte Exceli lahtriviide ega Lab 2 eraldi kohustuslik nõue. |
| Napa tüüp | tempel „C20“ = SMC ZP20C tüüpi lame ribidega napp Ø20 | photo 25.10.2026 | SMC kataloog ZPT 13-11-6: välis-Ø23, kõrgus C 14 mm — klapib nihikumõõtudega. Puhvrivedru hoidikus ei ole. |

Mõõdetud eksemplari samasus robotile paigaldatud iminapaga pole dokumentaalselt kinnitatud. Seetõttu ei esitata neid arve otse paigaldatud tööriista mõõtudena. H1 ei ole kogu vaakumtööriista kõrgus. Varasemad kalibreerimisest tuletatud efektiivsed läbimõõdud ≈ 22 mm ja ≈ 23 mm jäävad oma katsekontekstis alles; need ei asenda nihikumõõtu ega tõenda eksemplaride samasust.

### Vaakumtööriista mass enne kaamerat — estimated, not measured

Kasutaja esialgne hinnang on **umbes 80 g (?)**, orientiirina **60–110 g**. Olek: **estimated, not measured**. Alus on visuaalne insenerihinnang eeldusel, et korpus on valdavalt alumiiniumist; materjali ega massi pole selle hinnanguga kontrollitud. Vahemik ei ole mõõtemääramatus ega kinnitatud massipiir. Laboris pole kaalu. Teise DOBOT haaratsi massi meie tööriistale üle ei kanta ja hinnang ei kinnita kandevõime nõude täitmist.

- Tegelik mass enne kaamera lisamist (g): `TODO — waiting for physical test`.
- Tegelik mass koos kaamera ja kinnitusega (g): `TODO — waiting for physical test`.
- Enne lõplikku kaitsmist tuleb tööriist päriselt kaaluda enne ja pärast kaamera paigaldamist; kohustuslikku massikontrolli ei märgita tehtuks.

### Sisendhoidikud — Physical fit confirmed

| Hoidikutüüp | Kontrollitud detail | Füüsiline sobivus | Prinditud pesa X/Y/Z ja arvuline lõtk (mm) |
|---|---|---|---|
| `ready-parts-input-holder` — aku sisend | Akumoodul | confirmed — kasutaja käsitsi tehtud kontroll, 24.10.2026 | TODO — waiting for physical test |
| `atoms3-input-holder` — Atomi sisend | AtomS3 | confirmed — kasutaja käsitsi tehtud kontroll, 24.10.2026 | TODO — waiting for physical test |
| `glass-input-holder` — klaasi sisend | Polükarbonaatklaas | confirmed — kasutaja käsitsi tehtud kontroll, 24.10.2026 | TODO — waiting for physical test |

Kõigi kolme hoidikutüübi kohta kinnitas kasutaja: detail läheb vastavasse pesasse ja jõuab põhjani, liigub olemasoleva lõtku piires vabalt, tuleb sõrmedega välja ning kontrollil ei kiilunud. Kontrollitud pesade arvu ja klaasihoidiku prindiversiooni ei täpsustatud; kõigi 12 pesa eraldi nihikuga kontrollimist ei kinnitata. See on detaili sobivus pesas, mitte Gridfinity jala istumise, eemaldamise/tagasipaneku kordustäpsuse ega kogu robotitsükli kinnitus.

Komponentide kokkulepitud lähteväärtused jäävad ülaloleva Maksimi registri järgi: AtomS3 `nominal`, aku `measured`, klaas `confirmed`; uusi komponendi nihikunäite ega varasemate mõõtmiste kuupäevi ei lisata. Olemasolevate `.f3d` ja `.stl` failide kontroll ning digitaalsed pesamõõdud on [`CAD-ülevaate 24.10 täiendusena`](cad-measurement-review.md). **CAD dimensions**, **Physical fit confirmed** ja **Physical pocket dimensions** on eraldi tõendid: CAD-arvud ei täida siinse tabeli puuduvaid füüsilisi mõõte.

Kui hiljem leitakse vale mõõt, ära kustuta seda. Lisa kuupäevaga parandus vana väärtuse alla ning selgita mõõtekonteksti.
