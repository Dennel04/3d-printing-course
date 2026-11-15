# Võrreldav Fusioni simulatsioon

**TODO.** Kõigi kolme Static Stress uuringu tulemused ja printimiseelsed ennustused ootavad mõõdetud koormust, pilootkatset ja lõplikke mudeleid.

## Ühine seadistus

1. Too [piloodist](test-procedure.md#2-koormus-ja-originaali-piloot) mõõdetud töökoormus ja katses kasutatav jõusuund, pind, rakis ning tabamuspunkt. Kui töökoormuse ja võrdluskatse suund või kontakt erineb, tee kummalegi oma koormusjuht ja korda mõlemat kõigil kolmel mudelil.
2. Loo Fusionis kolm **Static Stress** uuringut. Kasuta sama materjalikaarti, koormuse väärtust ja suunda, kinnituste ja kontaktide tüüpi, samaväärseid pindu ning sama võrgusilma suurust millimeetrites. Märgi, millised ruudustiku pinnad takistavad liikumist ja kus kontakt võib lahti tulla. Kui võrgutundlikkuse kontroll nõuab tihedamat võrku, rakenda sama muudatus kõigis kolmes uuringus. [Autodesk · generatiivse tulemuse staatiline kontroll](https://help.autodesk.com/cloudhelp/ENU/Fusion-Simulate/files/GUID-D0947E92-01B7-47BC-ADD8-CB3745200228.htm)
3. Salvesta deformatsioon, pinge, ohutustegur ning eeldatav rikke koht. Kasuta kõrvutavatel piltidel võrdset vaadet ja skaalat. Lisa iga pildi juurde uuringu arhiivi viide. Lõpliku, puhastatud G-keha puhul kontrolli koormuse ja kinnituste ülekandumist.
4. Lineaarses piirkonnas võib hinnata piiri valemiga `F_piir = F_ref × (σ_piir / σ_ref)`, kus pinged käivad sama rikkemehhanismi kohta ja `F_ref` on vastava katse referentsjõud. Dokumenteeri, kas skaleerid materjali tugevuse või mõõdetava deformatsioonipiirini. Kui kontakt avaneb, plast deformeerub mittelineaarselt või tulemust juhib kinnituse pingesingulaarsus, lisa tundlikkuse hinnang ja ennustuse piirang. Suure läbipainde puhul ära esita lineaarset ekstrapolatsiooni täpse murdejõuna.

## FDM ja Lab 1

[Lab 1 paindekatse](../../lab1/README.md#osad) annab PLA kolme paksuse painde ja murdumise vaatlused. Meeskonna failides puudub võrreldav piki kihti ja kihtide vahel mõõdetud jõusuhe. Küsi algandmed ja mõõtetingimused. Kui andmed puuduvad, lepi õppejõuga kokku, kas mõõta sobivatest sama profiiliga suunaproovidest suhe või käsitleda seda ennustuses vahemikuna koos dokumenteeritud allikaga. Läbipaine millimeetrites ja purunemisnurk annavad eri suurused kui purunemisjõud.

Märgi iga asendi kihi normaal ning ohtliku tsooni peamise tõmbepinge suund. Kõige nõrgem võib olla ühendus, mida tõmme avab risti kihtide tasapinnaga. Kontrolli seda ka siis, kui välisjõud on surve ja põhjustab detailis paindetõmmet. Kasuta mõõdetud suhet `F_kihtide_vahel / F_piki_kihti` piirjõu korrigeerimiseks ainult võrreldavates tingimustes ja selgita kihtide suunast sõltuvat rakendust. Ilma sobiva arvulise aluseta esita isotroopne hinnang koos põhjendatud määramatusega ja kvalitatiivne kihirisk. FDM perimeetrid, täidis ja ühendused mõjutavad ka lõpptulemust.

## Ennustus enne printi

Täida pärast [kolme orientatsiooni viilutamist iga mudeli jaoks](../notebooks/README.md), enne esimese võrdluseksemplari printi. Märgi uuringute ühine koormus, kinnitused, võrgusilm, materjalikaardi allikas ja versioon. Salvesta kuupäev koos ennustusega, et seda saaks hiljem katseandmetega võrrelda.

| Versioon | Kuupäev ja uuring | Prindisuund | Ennustatud rikkekoht ja -viis | Piirjõu hinnang (N) ja määramatus | Kihimõju alus |
| --- | --- | --- | --- | --- | --- |
| O | | | | | |
| H | | | | | |
| G | | | | | |

Pärast katset lisa [võrdlusse](design_comparison.md#tulemused) tegelik jõud või katsega tõendatud alampiir ja nähtud rikkekoht. Uuri prognoosivea puhul esmalt kihisuunda, rakise elastsust, koormuseasendit ning pingetipu asukohta.
