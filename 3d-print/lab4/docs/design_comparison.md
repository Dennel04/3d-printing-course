# Kolme disaini võrdlus

Tööplaan lähtub [soovitatud v3 klaasihoidikust](analysis_original.md). Kinnita detail, mõõdik, koormus ja originaalil proovitud katse enne ümberjoonistamist.

| Tähis | Versioon | Töö Fusionis |
| --- | --- | --- |
| O | Originaal v3 | Ava olemasolev Lab 2 arhiiv ja kontrolli, et see vastab STL-ile, algsele 3MF-ile ning füüsilisele detailile. Salvesta Lab 4 töökoopia ja hoia originaali geomeetriat eraldi komponendina. [Algfailid](analysis_original.md#detaili-valik) |
| H | Käsitsi | Tee koopia **samas Fusioni disainifailis**. Seo liidesed lukustatud alusvisandiga. Uuri, kas materjali saab võtta põhja vähe koormatud aladelt ja asendada jõutee ribidega. Sea seina paksus vastavusse valitud profiili ekstrusiooniradade laiusega. Kasuta vajaduse korral tugede asemel faasi. Kui rakis või valitud detail kasutab polte, järgi Lab 3 reeglit, et polt kannab tõmmet ja plast survet. [Lab 3 ülesanne](../../lab3/assignment-EST.md) |
| G | Generatiivne | Kasuta samu liideseid ja mõõdetud koormusi. Vali üks uuringu tulemus, puhasta keha, kontrolli liideseid ning viiluta lõplik geomeetria uuesti. [Uuringu seadistus](generative_setup.md) |

Võrdle Fusionis kõigi nelja pesa keskust, põranda ja serva kõrgust, seinu, nurki ning kõigi Gridfinity jalgade kontaktpindu ja sammu. Hoia ka klaasi ja napa liikumistee vaba. Salvesta mõõdukontroll ja ekraanipildid koos muudetava Fusioni faili viitega. Füüsiliste liideste lubatud kõrvalekalded lepi kokku [piloodis](test-procedure.md#2-koormus-ja-originaali-piloot).

Pärast valiku kinnitamist hoia uued failid detaili nimega alamkaustas. Kasuta `src/` Fusioni arhiividele (`.f3d` või lingitud koostul `.f3z`), `stl/` eksporditud kehadele ja `3mf/` viilutusprojektidele. Seo iga prinditud eksemplar tema STL-i ja 3MF-iga. Sama geomeetria ning profiiliga kordused võivad viidata samale failipaarile. Kui faili sisu muutub, salvesta uue versioonina. Lisa fotod ja simulatsioonipildid tõendi tekkimisel ning lingi muudetavad uuringud.

## Tulemused

Täida pärast üheksat katset. Kuvamiseks kasuta keskmist ja vahemikku min…max ning lisa kehtivate mõõtmiste arv. Aja puhul too kõrvuti viilutaja prognoos ja printeri tegelik prindiaeg. Jõukatse puhul kõrvuta enne printi fikseeritud ennustus mõõdetud tulemusega.

| Versioon | Valitud orientatsioon | Aeg slaiseris / tegelik aeg (min) | Kaalutud mass (g) | Tugi (g) | Ennustatud rikkejõud ja koht | Mõõdetud rikkejõud (N), n ja koht | Sobivus ja otsus |
| --- | --- | --- | --- | --- | --- | --- | --- |
| O | TODO. A-asendi viilutus on olemas. | | | | | | |
| H | Ootab viilutust | | | | | | |
| G | Ootab viilutust | | | | | | |

Võidab väikseima keskmise **tegeliku prindiajaga** versioon, mis täidab enne ümberjoonistamist kokku lepitud tugevuse ja sobivuse tingimused. Kui ajavahe jääb mõõtehajuvuse piiridesse või jõupiir takistab tugevuse võrdlust, märgi, mida tulemused lubavad järeldada. Anna ühes lõigus vastus, kas käsitsi variant oli generatiivsest parem ja miks. Lisa selgitus, kus simulatsiooni ennustus ja katsetulemus lahknesid. [Katsetulemused](../data/test.csv) · [Analüüsi plaan](../notebooks/README.md) · [Võitja paigaldus](integration.md)
