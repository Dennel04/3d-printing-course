# Prindisuunad ja analüüs Jupyteris

## Kolm mudelit, kolm orientatsiooni

Tee PrusaSliceris ühe eksemplariga projekt iga rea kohta. Kasuta sama printeri, otsiku, PLA, kihikõrguse, perimeetrite ja täidise profiili. Säilita algne O-A 3MF lähtepunktina. Tugi ja brim lisa vajaduse järgi sama reegli alusel ning märgi seade reale. Kontrolli tegelikke ekstrusiooniradu, esimest kihti ja tugede eemaldamise võimalust. Märgi ebaõnnestunud viilutus või sobimatu paigutus koos põhjusega. Originaali piloot kasutab olemasolevat detaili või algsest 3MF-ist tehtud asendust. Võrdlusseerias säilita O geomeetria ja vali kõigi kolme versiooni orientatsioon mõõdiku järgi. [Originaali profiil](../docs/analysis_original.md#klaasihoidiku-lähtegeomeetria-ja-print)

Klaasihoidiku asendite ettepanek on A = jalad all (mudeli +Z üles), B = külg all (+X üles), C = pesa servad all (−Z üles). Kontrolli kõigil mudelitel sama teljestikku. Salvesta vajadusel pöördenurk ja telg. Märgi kihtide suhe tegeliku koormuse ja kriitilise koha tõmbepingega. Vali iga versiooni jaoks kiireim lubatud orientatsioon, mis jääb prinditavuse, liideste ja [tugevusprognoosi](../docs/simulation.md) piiridesse. Füüsiline tugevus selgub katsega.

| Versioon | Orientatsioon | 3MF / profiili viide | Slaiseri ajahinnang (min) | Slaiseri filamendihinnang (g) | Slaiseri tugi / brim (g) | Kihid ja koormussuund | Valik või kõrvalejätmise põhjus |
| --- | --- | --- | ---: | ---: | ---: | --- | --- |
| O | A · +Z | [Lab 2 algne 3MF](../../lab2/glass-input-holder/3mf/glass-input-holder.3mf) | 41,97 | 28,19 | 0 / 0 | | Originaali asend. Slaiser hoiatas pikkade sildade eest. |
| O | B · +X | | | | | | |
| O | C · −Z | | | | | | |
| H | A · +Z | | | | | | |
| H | B · +X | | | | | | |
| H | C · −Z | | | | | | |
| G | A · +Z | | | | | | |
| G | B · +X | | | | | | |
| G | C · −Z | | | | | | |

Lukusta üks seeria orientatsioon versiooni kohta ning kanna see enne printimist ennustusse ja proovide CSV-sse. Üheksa viilutust annavad asendivaliku. Üheksa füüsilist eksemplari on kolm kordust iga versiooni valitud asendis.

## Notebooki tööplaan

1. Transkribeeri orientatsioonitabel notebooki või eraldi CSV-sse ja kontrolli, et `variant + orientation_id` on kordumatu ja kõik üheksa kombinatsiooni on olemas. Võrdle PrusaSliceri aega ja tugimassi. Soovi korral arvuta originaali ristlõikepindala Z suunas ja seosta tulemused viilutaja rajavaatega.
2. Loe [test.csv](../data/test.csv) pandas'ega. Kontrolli üheksat unikaalset `sample_id` väärtust, kolme proovi variandi kohta, valitud asendi ühtsust versiooni sees ja füüsilise katse unikaalset järjekorda. Tühjad mõõtmised jäävad puuduvaks. `planned` tähendab ootel. `failure`, `limit_reached` ja `invalid` tähendavad [protseduuris](../docs/test-procedure.md) kirjeldatud lõppseise.
3. Tunnused ja ühikud tulevad veerunimedest. Kasuta `*_ok` väljadel `yes`/`no` ja `tested_at` väljal ISO 8601 aega koos nihkega. `revision` on CAD-i revisjon ja `test_setup_id` viitab fikseeritud protokollile. Lisa nihiku üksiknäidud ning koormuse ajalugu viidatud tõendfailidesse. Seo katsed STL-i ja tegeliku prindiprojektiga.
4. Arvuta versiooni kaupa kehtivate katsete arv, prindiaegade ja masside keskmine ning min…max. Näita üksikuid mõõtmisi, tegeliku ja slaiseri aja erinevust, toe massi ning rikkejõude. Arvuta jõu keskmine ja vahemik mõõdetud rikkejõududest, tuues nende arvu välja. Näita `limit_reached` väärtusi alampiiridena ja põhjenda iga `invalid` katse. Kui rike tuvastati jõuastme järel, näita ka viimase läbitud astme väärtust. Puudulike andmetega ära tee samaväärse tugevuse järeldust.
5. Kõrvuta ennustuse ja katse jõud ning rikkekohad. Kui sama rikkejõud mõlemal poolel on teada, arvuta hinnangu viga N ja protsentides. Rakenda eelnevalt kinnitatud tugevuse ja istuvuse vastuvõtureeglit ning koosta [lõppvõrdlus](../docs/design_comparison.md#tulemused).

Kodus saab notebooki laadimise, kontrollid ja graafikukoodi ette valmistada olemasoleva tühja malliga. Lisa mõõteandmed pärast füüsilisi katseid.
