# Tööriista paigutuse tööleht

Täida füüsiliste komponentide mõõtmise järel ja enne lõpliku CAD-i alustamist.
Mõõtmata väärtus on `TODO — waiting for physical measurement`; füüsiliselt
kontrollimata sobivus või otsus on `TODO — waiting for physical test`.

## Komponentide tabel

| Komponent | Mõõdetud mõõdud (mm) | Mõõdetud mass (g) | Kinnitusviis | Olek | Märkused |
|---|---|---:|---|---|---|
| 3/2 solenoidklapi koost | TODO — waiting for physical measurement | 68,84 | Prinditud kinnitus. Lõplik paigalduskoht on lahtine. | Kaalutud 15.11.2026. | Koos kinnituse, kinnitusvahendite ja lühikeste voolikutega. Kinnitusavad, liitmikud ja pistik peavad jääma ligipääsetavaks. |
| Süstal kavandatud tööolekus | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test | Viita süstla ja otsiku ID-le. |
| Otsik | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test | Viita otsiku ID-le. |
| UV LED ja jahutusradiaator | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test | Jahutusradiaatori ümber peab jääma õhuruum. |
| LED-i draiver, kui see paikneb tööriistal | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test | Lõplik asukoht on valimata. |
| Iminapp, metallhoidik ja liitmik | TODO — waiting for physical measurement | 42,03 | TODO — waiting for physical measurement | Kaalutud 15.11.2026. | Uue tööriista paigutus on lahtine. |
| XIAO tööriistakaamera | TODO — waiting for physical measurement | 4,05 | Lab 2-s MG400 J4 juures prinditud hoidikus. | Moodul kaalutud 15.11.2026. | Hoidiku ja kaabli mass on lahtine. Kontrolli USB-C ja objektiivi vaba ruumi. |
| Verbatimi üldvaatekaamera | TODO — waiting for physical measurement | ≈135,68 | Eraldi kõrgel postil. | 15.11 ligikaudne mass koos kaabliga. | Üldvaatekaamera jääb väljapoole MG400 kaalueelarvet. |
| Voolikud ja juhtmed | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test | Sisalda tõmbetõket ja liikumisvaru. |

Laboris leitud must süstlapäis kaalub **24,05 g**. See on CAD-i
võrdlusdetaili kandidaat. Süstla pöördkinnitus ja vooliku mehaaniline
püsimine on kuivalt kontrollitud. Näidise mass on kirjas eraldi.
Lõppkoostu kaalueelarvesse kantakse valitud päise tegelik mass.
[Kuivsobitus](test-procedure.md#kordusproov-ja-leitud-süstlapäis-15112026).

## Kaalueelarve

[15.11 kaalutud koosseisud](measurements.md#mõõtmised-15112026) · [Lab 2 kaamerate paigaldus](../../lab2/README.md#kaamerad-cad-etapi-tulemus-ja-smart-solutionsi-jätkutöö).

MG400 ametlik tööriista kogukoormuse piir Lab 3 ülesandes on **500 g**, kaasa
arvatud kogu tööriist, täis süstal ja klaas iminapa küljes korraga.
Kogumass ja varu arvutatakse pärast lõpliku koosseisu selgumist ning
puuduvate masside kaalumist.

Summeeri ainult robotil olevad, omavahel kattumata osad. Kui aluskoostu
mass sisaldab mõnda allolevat komponenti, märgi see kaasatuks ja ära lisa
eraldi massi uuesti. Tühi kontrollkoost ja lõplik kontrollkaalumine on
kontrollread, mitte summale lisatavad komponendid.

| Rida | Mass (g) | Liik / märkus |
|---|---:|---|
| MG400 ametlik tööriista kogukoormus | 500 g | Ametlik piir. |
| Uus tööriistahoidik / aluskoost | TODO — waiting for physical measurement | Kirjelda koosseisu; ära liida sama osa topelt. |
| 3/2 klapi mõõdetud koost | 68,84 | MG400 koormuses ainult tööriistal paiknedes. Selle koostu kinnitust, kinnitusvahendeid ja lühikesi voolikuid arvesta üks kord. |
| Süstal kavandatud tööolekus | TODO — waiting for physical measurement | Mõõdetud mass. |
| Otsik | TODO — waiting for physical measurement | Mõõdetud mass. |
| UV LED ja jahutusradiaator | TODO — waiting for physical measurement | Mõõdetud mass. |
| LED-i draiver, kui robotil | TODO — waiting for physical measurement | Laual paiknev osa robotikoormusesse ei kuulu. |
| Süstla päis ja O-rõngas | TODO — waiting for physical measurement | Kui süstla kaalumine neid juba sisaldab, ära liida uuesti. |
| Klaas iminapa küljes | 1,70 | 15.11 eraldi kaalutud klaas. |
| Iminapp koos metallhoidiku ja liitmikuga | 42,03 | Arvesta üks kord, kui see koost kuulub lõppkoostu. |
| Must UV-kate, kui robotil | TODO — waiting for physical measurement | Laual olev kate robotikoormusesse ei kuulu. |
| XIAO tööriistakaamera | 4,05 | Moodul. Tööriistaga kaasaliikuva hoidiku ja kaabli tegelik mass on veel kaaluda. |
| Prinditud kinnitused | TODO — waiting for physical measurement | Lõplike füüsiliste osade mass. |
| Voolikud ja juhtmed | TODO — waiting for physical measurement | Tööriistaga liikuv osa. |
| Poldid, mutrid, seibid, liitmikud ja muud robotil olevad osad | TODO — waiting for physical measurement | Ära liida osakoostudes juba kaalutut uuesti. |
| Tühi kontrollkoost | TODO — waiting for physical measurement | Mõõda valmis koost tühja süstlaga. |
| Lõplik kogumass | TODO — waiting for physical measurement | Kõik robotil olevad osad + täis süstal + klaas; kontrollkaalumine. |
| Allesjääv varu | TODO — waiting for physical measurement | `500 g − lõplik kogumass`. |

## Pneumaatika teekond

Tööversioon, mitte lõplik paigutus:

```text
Pump → Y1 ┬→ iminapp (otse; vajadusel nõelventiil)
          └→ 3/2 klapp → süstal
                └→ atmosfäär (klapi kolmas ava)

Y2 ühendatakse ainult ühte järgmistest magistraalidest:
A: pumba magistraal enne klappi → Y2 ┬→ edasi klapini
                                    └→ rõhuandur
B: klapp → Y2 ┬→ süstal
              └→ rõhuandur
```

Napp ei käi läbi klapi. Voolu all ühendub süstal pumbaga; vooluta
atmosfääriga. Pump kas puhub või imeb: doseerimine → klaasi tõstmine →
kõvendamine → väljund. Kinnita tegelikud pordid märgistuse ja füüsilise
katsega. Nõelventiil napi harus on tingimuslik Andmehõive valik.

Y2 tegelik asukoht (A või B) ja põhjendus: TODO — Andmehõive otsus.
Valitud asukoha füüsiline kontroll: TODO — waiting for physical test.
Süstlaharu lubatud pikkus ning tilga alguse/lõpu viivitus Andmehõivest:
TODO — waiting for physical test.

| Lõik | Mõõdetud pikkus (mm) | Liitmiku tüüp | Marsruut / konflikt |
|---|---:|---|---|
| Pump → Y1 | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test |
| Y1 → iminapp | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test |
| Y1 → 3/2 klapp | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test |
| 3/2 klapp → süstal | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test |
| Y2 → rõhuandur | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test |
| Nõelventiili lõik, kui valitud | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test |
| Klapi atmosfääriava / väljalaske vaba ruum | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test |

## Klapi asukoha otsus

### Klapp tööriistal

| Plussid | Miinused | Vajalikud mõõtmised/katsed |
|---|---|---|
| Lühem süstlaharu võib vähendada pneumaatilist viivitust. | Lisab robotile massi ning liikuva juhtme ja komponendi. | Klapi mass koos liitmikega; lühima ohutu vooliku pikkus; juhtme marsruut; kuumenemine; kogu tööriista mass; kokkupõrkeala. |

### Klapp laual

| Plussid | Miinused | Vajalikud mõõtmised/katsed |
|---|---|---|
| Robotil on väiksem mass ja vähem elektrilisi osi. | Pikem süstlaharu võib suurendada viivitust; voolik peab liikuma kogu tööalal. | Vooliku vajalik pikkus; minimaalne painderaadius; liikumiskonfliktid; pneumaatiline viivitus; laua Gridfinity asukoht ja ligipääs. |

**Lõplik valik:** TODO — waiting for physical test

**Valiku põhjendus mõõtmistega:** TODO — waiting for physical test

Kasuta õpetaja valmis klapikinnitust ja tee valitud asukoha jaoks
süsteemiadapter; valmis kinnituse ümberjoonistamine ei ole lähteülesanne.
Robotile tuleb uus tööriistahoidik. Joint, Motion Study ja Interference
kontrollid ning füüsiline massi- ja liikumiskatse on veel tegemata.

## Lab 3 abikohtade paigutus

Lab 2 [paigutus](../../lab2/docs/layout.md) jääb lähteallikana muutmata.
Planeeri uued kohad siin; ära käsitle Lab 2 slot-pickerit Lab 3 tsüklina.

| Koht | Ruut / nihe X/Y/Z (mm) | Ligipääs ja põhjendus | Füüsiline kontroll |
|---|---|---|---|
| Prügitopsi hoidik | TODO — waiting for physical measurement | TODO — waiting for physical test | TODO — waiting for physical test |
| Pime otsikupark | TODO — waiting for physical measurement | TODO — waiting for physical test | TODO — waiting for physical test |
| UV-katte töökoht | TODO — waiting for physical measurement | TODO — waiting for physical test | TODO — waiting for physical test |
