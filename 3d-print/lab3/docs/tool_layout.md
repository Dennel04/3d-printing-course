# Tööriista paigutuse tööleht

Täida füüsiliste komponentide mõõtmise järel ja enne lõpliku CAD-i alustamist.
Mõõtmata väärtus on `TODO — waiting for physical measurement`; füüsiliselt
kontrollimata sobivus või otsus on `TODO — waiting for physical test`.

## Komponentide tabel

| Komponent | Mõõdetud mõõdud (mm) | Mõõdetud mass (g) | Kinnitusviis | Olek | Märkused |
|---|---|---:|---|---|---|
| 3/2 solenoidklapp koos kasutatavate liitmikega | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test | Kinnitusavad, liitmikud ja pistik peavad jääma ligipääsetavaks. |
| Süstal kavandatud tööolekus | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test | Viita süstla ja otsiku ID-le. |
| Otsik | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test | Viita otsiku ID-le. |
| UV LED ja jahutusradiaator | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test | Jahutusradiaatori ümber peab jääma õhuruum. |
| LED-i draiver, kui see paikneb tööriistal | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test | Lõplik asukoht on valimata. |
| Iminapp ja olemasolev imuriist | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test | Lab 2 CAD-eeldust ei märgita mõõdetud väärtuseks. |
| Kaamera | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test | Kontrolli USB-C ja objektiivi keep-out-tsooni. |
| Voolikud ja juhtmed | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test | Sisalda tõmbetõket ja liikumisvaru. |

## Kaalueelarve

MG400 ametlik tööriista kogukoormuse piir Lab 3 ülesandes on **500 g**, kaasa
arvatud kogu tööriist, täis süstal ja klaas iminapa küljes korraga. Allolevad massid tuleb
füüsiliselt kaaluda; neid ei asendata CAD-i arvutuse või internetiandmetega.

Summeeri ainult robotil olevad, omavahel kattumata osad. Kui aluskoostu
mass sisaldab mõnda allolevat komponenti, märgi see kaasatuks ja ära lisa
eraldi massi uuesti. Tühi kontrollkoost ja lõplik kontrollkaalumine on
kontrollread, mitte summale lisatavad komponendid.

| Rida | Mass (g) | Liik / märkus |
|---|---:|---|
| MG400 ametlik tööriista kogukoormus | 500 g | Ametlik piir. |
| Uus tööriistahoidik / aluskoost | TODO — waiting for physical measurement | Kirjelda koosseisu; ära liida sama osa topelt. |
| Klapp koos kasutatavate liitmikega | TODO — waiting for physical measurement | MG400 koormuses ainult tööriistal paiknedes; laual olev klapp ja tema kinnitus ei kuulu robotikoormusesse. Liitmikud arvesta ainult siin või teise osakoostu sees. |
| Süstal kavandatud tööolekus | TODO — waiting for physical measurement | Mõõdetud mass. |
| Otsik | TODO — waiting for physical measurement | Mõõdetud mass. |
| UV LED ja jahutusradiaator | TODO — waiting for physical measurement | Mõõdetud mass. |
| LED-i draiver, kui robotil | TODO — waiting for physical measurement | Laual paiknev osa robotikoormusesse ei kuulu. |
| Süstla päis ja O-rõngas | TODO — waiting for physical measurement | Kui süstla kaalumine neid juba sisaldab, ära liida uuesti. |
| Klaas iminapa küljes | TODO — waiting for physical measurement | Eraldi kaalumine. |
| Iminapp ja kinnitus | TODO — waiting for physical measurement | Ainult kui aluskoostu massis ei sisaldu. |
| Must UV-kate, kui robotil | TODO — waiting for physical measurement | Laual olev kate robotikoormusesse ei kuulu. |
| Kaamera | TODO — waiting for physical measurement | Mõõdetud mass. |
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
