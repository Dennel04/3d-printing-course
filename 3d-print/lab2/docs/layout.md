# Töövoog ja paigutus

Täida pärast päris laua, roboti ja detailide ülevaatust, enne hoidikute lõplikku modelleerimist. Ära märgi ruutu ega nihkeid eelduste põhjal.

## Koordinaadid ja töövoog

- Ruudustik: 7 x 10 ruutu, samm 42 mm.
- Täht näitab kaugust robotist; number näitab külge keskjoonest. Kontrolli füüsilisel laual tähtede kasvusuund, numbrite järjestus ja roboti keskjoon.
- Roboti kalibreerimise lähtepunkt ja koordinaatide suund:
- Gridfinity kalibreerimishoidiku ruut:
- Iga hoidiku lähtekoha nihe ruudu keskpunktist, X/Y/Z (mm):

Töövoog:

1. AtomS3, klaas ja akumoodul sisendhoidikutest.
2. Robot paigaldab ainult klaasi Atomi mannekeenile töökoha hoidikus.
   - 23.10.26: mannekeeni asemel on töökohal päris AtomS3.
3. Valmis detail liigub heade väljundisse; ebaõnnestunud detail liigub praagi väljundisse.

Töökoha sammude arv ja roboti täpsusala tuleb kinnitada tegeliku protsessi põhjal:

| Samm | Tegevus | Hoidiku ruut | Pesa / sihtpunkt | Nihe ruudu keskpunktist X/Y/Z (mm) |
|---|---|---|---|---|
| Sisend 1 | AtomS3, vähemalt 4 tk | | | |
| Sisend 2 | Polükarbonaatklaas, vähemalt 4 tk | | | |
| Sisend 3 | Akumoodul, vähemalt 4 tk | | | |
| Töökoht | Klaasi tõstmine Atomi mannekeenile | | | |
| Väljund | Valmis detail (`valjundhoidik-v1`, 2 × 2 lahtine kast) | | | |
| Väljund | Praak (23.10.26 parandus: oranž `ready-parts-input-holder-v1`; varem `gridfinity-calibration-v1`) | | | |

## Ruudustiku plaan

Skeem on tühi plaan. Kirjuta igasse lahtrisse hoidiku ruut (nt `B-2`) pärast füüsilise koordinaadistiku kinnitamist. Tähista ka robot ja keskjoon.

| Robotist kauguse rida / külg keskjoonest | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| A | | | | | | | | | | |
| B | | | | | | | | | | |
| C | | | | | | | | | | |
| D | | | | | | | | | | |
| E | | | | | | | | | | |
| F | | | | | | | | | | |
| G | | | | | | | | | | |

## Mõõtmised

Lisa detaili mõõtmed nihikuga, pesa mõõtmed, kasutatud lõtk ja iga roboti sihtpunkt. Kui mõõtmist parandatakse, lisa uus kuupäevaga tulemus vana alla.

| Detail / pesa | Detaili mõõt X/Y/Z (mm) | Pesa X/Y/Z (mm) | Kasutatud lõtk ja allikas (mm) | Ruudu tähis | Nihe X/Y/Z (mm) |
|---|---|---|---|---|---|
| AtomS3 | | | | | |
| Klaas | | | | | |
| Akumoodul | | | | | |
| Töökoha mannekeen | | | | | |
| Heade väljund | | | | | |
| Praagi väljund | | | | | |

## Kaamerad

- XIAO ESP32S3 Sense töökoha vaade, kinnitus ja korduspaigalduse kontroll:
- Kaamera toiteallikas, pinge/vool ja katse tulemus:
- Tööriista mass enne/pärast kaamera lisamist (g):
- USB UHD veebikaamera kõrgus ja asukoht:
- Kogu ruudustik ja robot kaadris:
- Pildi liikumine roboti liikumise ajal (px või mõõdetud mm):

## 23.10.2026 — Maksimi mõõteandmete täiendus ja klaasi parandus

Allikas: Maksimi `Measurements.xlsx`, leht `Measurements`; täielik lahtrite ja olekute register: [`measurements.md`](measurements.md). Varasemad tühjad väljad säilivad algse plaani ajaloo jaoks. Allolevad mõõdud ei määra veel ruute ega roboti sihtpunkte.

| Detail | Lähteväärtus X/Y/Z | Olek | Orientatsioon ja mõju paigutusele |
|---|---|---|---|
| Klaas | 30 × 30 × 2 mm | confirmed; D8:E19 ja meeskond | Varasem 24 × 24 × 2 mm ei kirjelda meie klaasi. Määrata haaramispind ja keskme referents; 30 mm klaasi serv ulatub sama keskme korral 3 mm kaugemale kui varasema vale 24 mm lähteväärtuse puhul. |
| AtomS3 | 24 × 24 × 12,9 mm | nominal; D2:E4 | Ekraan üles (`planned`, D7:E7); USB-C keskjoon 11,4 mm valitud servast (`measured`, D5:E5). Lähteserv ja mõõtesuund vajavad skeemi. |
| Akumoodul | 24,04 × 24,01 × 21,97 mm | measured; D21:E23 | Kontaktid üles (`planned`, D25:E25); sisend ja töökoht vastavalt varasemale otsusele `ready-parts-input-holder`. Pistiku asukoht jäeti Excelis vahele, seda ei loeta nulliks. |
| XIAO põhiplaat | 17,74 × 21,33 × 1,21 mm | measured; D26:E28 | Ei hõlma kaameralaienduse ega kogu koostu gabariite. Kontrollida renne, antenniala ja USB-C ligipääsu. |

- Klaasi sisendi, töökoha, väljundi ja praagi ruudud, pesade mõõdetud lõtk ning keskme X/Y/Z nihked: `TODO — waiting for physical test`.
- Kesksele 24 mm Atomile asetatud 30 mm klaasi üleulatus on arvutuslikult 3 mm külje kohta. Kontrollida naaberpesasid, seinu ning iminapa ja kaamera laskumisteed; robotiga transpordil arvestada ka klaasi pööratud ümbrist.
- `valjundhoidik` on üks lahtine kast, mitte neli fikseerivat pesa. Kavandada neli 30 mm klaasi 2 × 2 paigutuses, määrata sihtpunktid ja vahed; mahtumine ja kordustäpsus: `TODO — waiting for physical test`.
- Tööriistakaamera ligikaudne orientatsioon Excelis on 90° alla (`planned`, D47:E47). Mõõta kõrgus klaasi kohal ja kaugus töökohast (mm); kontrollida, et kogu 30 × 30 mm klaas ja Atom on kaadris. Kaamera USB-C ligipääs on konstruktsiooninõue (`planned`, D52:E52), mitte katsetulemus.
- Olemasolev USB-kaadri tõend on README 23.10.26 sessioonis. Kaabli pikkus, kinnituspunktid, liikumistee ja J4 kontroll, kaamera mass ning kogu tööriista mass enne/pärast (g) jäävad: `TODO — waiting for physical test`.
- Konkreetne mudelite ja trajektoori kontrollnimekiri: [`cad-measurement-review.md`](cad-measurement-review.md). Geomeetriat ega õpetatud robotipunkte selles sessioonis ei muudetud.
