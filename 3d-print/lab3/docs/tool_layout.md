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
arvatud kogu tööriist ja kavandatud tööolekus süstal. Allolevad massid tuleb
füüsiliselt kaaluda; neid ei asendata CAD-i arvutuse või internetiandmetega.

| Rida | Mass (g) | Liik / märkus |
|---|---:|---|
| MG400 ametlik tööriista kogukoormus | 500 g | Ametlik piir. |
| Praegune tööriist | TODO — waiting for physical measurement | Mõõdetud mass. |
| Klapp koos kasutatavate liitmikega | TODO — waiting for physical measurement | Mõõdetud mass. |
| Süstal kavandatud tööolekus | TODO — waiting for physical measurement | Mõõdetud mass. |
| Otsik | TODO — waiting for physical measurement | Mõõdetud mass. |
| UV LED ja jahutusradiaator | TODO — waiting for physical measurement | Mõõdetud mass. |
| Kaamera | TODO — waiting for physical measurement | Mõõdetud mass. |
| Prinditud kinnitused | TODO — waiting for physical measurement | Lõplike füüsiliste osade mass. |
| Voolikud ja juhtmed | TODO — waiting for physical measurement | Tööriistaga liikuv osa. |
| Lõplik kogumass | TODO — waiting for physical measurement | Kõigi robotil olevate osade summa. |
| Allesjääv varu | TODO — waiting for physical measurement | `500 g − lõplik kogumass`. |

## Pneumaatika teekond

Tööversioon, mitte lõplik paigutus:

```text
Pump → 3/2 klapp → iminapa haru / süstla haru
```

Vooluta olekus peab olema avatud iminapa haru. Kinnita tegelikud pordid klapi
märgistuse ja füüsilise katsega.

| Lõik | Mõõdetud pikkus (mm) | Liitmiku tüüp | Marsruut / konflikt |
|---|---:|---|---|
| Pump → 3/2 klapp | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test |
| 3/2 klapp → iminapp | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test |
| 3/2 klapp → süstal | TODO — waiting for physical measurement | TODO — waiting for physical measurement | TODO — waiting for physical test |

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
