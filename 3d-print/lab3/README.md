# 3D printimine ja CAD: Labor 3 — Tööriist: napp, süstal ja UV-lamp

**Maht:** 28 tundi | **Hindamine:** 20 punkti | **Meeskond:** 3 tudengit | **Välja antud:** 27.10.26 | **Tellimine:** 06.11.2026 | **Esimene kaitsmine:** 19.11.2026, veebis

See on meeskonna tööpäevik ja otsuste register. Täielik ametlik ülesanne on failis [`assignment-EST.md`](assignment-EST.md), mis on bait-baidilt identne [Kaspar Kallase ajakohase failiga](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/3D%20printing/3D%20Printing%20%5BLab%203%5D%20EST.md). Kontrollitud 25.10.2026; Git blob SHA: `b15821c7c47bc22f1549b3aed6b7280a8cb4b651` (sama kui 24.10.2026 kontrollversioon). Ametlik ülesanne on varasemate plaanide suhtes ülimuslik. Mõõtmised, arvutused, CAD-referentsid ja füüsilised katsed hoitakse eraldi; varasemad päevikukirjed säilivad.

## Eesmärk ja tööjärjekord

Uus MG400 tööriistahoidik kinnitub roboti nina külge ja kannab iminappa, Metcal 910-B 10 cc süstalt, 405 nm UV-lampi ning kaamerat. Uue hoidikuga õpetatakse punktid uuesti. Tööjärjekord on **doseerimine → klaasi tõstmine → kõvendamine → väljund**: üks pump kas puhub või imeb, mõlemat korraga ei tee.

Pneumaatika: **pump → Y-liitmik → iminapp / 3/2 klapp → süstal**. Napp on otse pumba harus; klapi kolmas ava on atmosfääri väljalase. Voolu all ühendab klapp süstla pumbaga, vooluta atmosfääriga. Rõhuandur ühendatakse teise Y-liitmikuga Andmehõive valitud kohta; võimalik nõelventiil napi harus tuleb skeemile märkida. Ühtegi pumba maksimaalset rõhku ei eeldata: see mõõdetakse.

MG400 ametlik **500 g** piir sisaldab kogu flantsi küljes olevat koostu suurima koormaga: **täis süstal ja klaas iminapa küljes korraga**. Kõik tegelikud massid ja varu on veel mõõta/arvutada. Selles laboris on süstal katsete ajal tühi; täis süstla massikontrolli korraldus tuleb õppejõuga kooskõlastada, mitte asendada vaikimisi tühimassiga.

**KAARDISTA ISE — eesmärk nii, nagu ta tegelikult välja tuli.**

TODO — kirjeldada pärast tegelikke meeskonna otsuseid.

## Kontrollnimekiri

Järgmised 14 kohustuslikku punkti on ametlikust ülesandest sõna-sõnalt. Ühtegi füüsilist kriteeriumi ei loeta dokumentatsiooni uuendamisega tehtuks.

- [ ] Kõik osad mõõdetud nihikuga ja Fusionis kehadena olemas: klapp koos kinnitusega, süstal, süstla otsikud, UV LED jahutusradiaatoril, napp, kaameramoodul.
- [ ] Õhu teekond skeemina ja kaalueelarve tabelina failis `docs/tool_layout.md`.
- [ ] Klapi kinnitus süsteemi küljes: prinditud ja kokku pandud failist `Solenoidklapi kinnitus.f3z`, voolik hambaorgiga lukus ja silikooniga tihendatud, voolikud ei murdu.
- [ ] Tööriist roboti küljes: napp, süstal, UV-lamp ja kaamera. Kaal alla 500 g suurima koormaga: täis süstal ja klaas napa küljes korraga.
- [ ] Süstal vahetub ühe käega, ilma tööriistadeta. 20 vahetust järjest, klamber terve.
- [ ] UV-lambi koonus tabab liimi kohta ja läheb süstla otsikust mööda. Kontrollitud Fusionis ja valge paberiga laual.
- [ ] Valgustamine käib musta katte all: valgus ei paista välja, kontrollitud valge paberiga.
- [ ] Iga otsiku nihe flantsi suhtes mõõdetud ja kirjas failis `docs/tool_offsets.md`.
- [ ] Süstla päis lõpuni tehtud: O-rõngas komplektist, soon arvutatud, päis peab vastu pumba suurima rõhu.
- [ ] Lekkekatse: süstla haru hoiab rõhku 5 minutit, iga liitekoht seebiveega üle käidud. Tulemus failis `docs/leak_test.csv`.
- [ ] Prügitopsi hoidik ja otsiku parkimiskoht ruudustikus.
- [ ] Kuiv läbijooks: mine doseerimise kohta, tõsta klaas, mine kõvendamise kohta, 20 korda. Miski ei haagi. Tulemus failis `docs/cycle_test.csv`.
- [ ] Tellimus 06.11 failis `docs/bom.md`.
- [ ] Repo ja arenduspäevik täidetud, tag `3d-print-lab3`.

## Tööplaan ja dokumenteeritavad tõendid

1. **Mõõda ja paiguta:** mõõda kõik päris osad, klaas ja süstal tühjana ning kavandatud täisolekus; koosta [mõõteleht](docs/measurements.md), [õhuskeem ja kaalueelarve](docs/tool_layout.md). LED-i saab enne saabumist esitada andmelehe mõõtudega eraldi märgistatud CAD-kehana; pärast saabumist mõõda üle.
2. **Klapi kinnitus:** kasuta õpetaja valmis Fusioni koostu `Solenoidklapi kinnitus.f3z`: klapp, kaks prinditud tükki, seibid, kolm M4 polti mutritega. Hambaork lukustab vooliku ja silikoon tihendab. Meeskond valmistab valitud asukoha jaoks hoidiku/adapteri. Kui adapter vajab sisseprinditud mutrit, tee esmalt väike taskukatse ning salvesta paus 3MF-is.
3. **Uus tööriist:** iga osa eraldi Fusioni komponent; ühenda osad omavahel ja roboti ninaga tööriistaga **Joint**, kontrolli **Motion Study** abil sisendit, töökohta, väljundit ja kõiki hoidikuid ning tee **Interference**-kontroll. CAD-kontroll ei tõenda füüsilist sobivust.
4. **Süstal ja päis:** kasuta Metcal 910-B 10 cc päris süstalt. `Süstla päis poolik.f3z` on lõpetamata ja tihendita; vali komplektist O-rõngas, arvuta soone kokkusurumine, venitus ja täitumine ning katseta väikest proovikeha. Õpetaja koostu rõngas ja lõtk pole kinnitatud disainivalik. Päis peab taluma pumba mõõdetud suurimat rõhku.
5. **Süstlavahetus:** 20 järjestikust ühe käega tööriistadeta vahetust; lisa iga tõrge/deformatsioon. Mõõda viiel vahetusel aeg ja otsiku asend enne/pärast ning põhjenda klambri paindumist Lab 1 tulemusega.
6. **UV:** lamp peab olema otsikust vähemalt 30 mm kaugusel (ülesande nõue, mitte mõõtetulemus); kontrolli koonuse möödumist otsikust Fusionis ja valge paberiga. Kõvendamine ja paberikatse käivad **musta PLA-katte all**; radiaator jääb katte välja õhu kätte. Kirjuta katte seina paksus, perimeetrid ja täidis; kontrolli valgusleket pimedas ruumis helendava paberi või kleebisega katte ümber. Mõõda radiaatori temperatuur kavandatud kõvendusaja järel.
7. **Neli nihet:** mõõda samast flantsi referentsist iminapa keskpunkt, süstla otsiku tipp, UV-laigu keskpunkt ja **kaamera pildi keskpunkt**; korda pärast tööriista eemaldamist/tagasipanekut. Kirjuta [nihete lehele](docs/tool_offsets.md).
8. **Rõhk ja leke:** otsik suletud, napi haru suletud, klapp voolu all; survekatse pumba täisvõimsusel kuni rõhk stabiliseerub. Eraldi viieminutisel lekkekatsel pump peatub, **klapp jääb kogu katseks voolu alla**. Kontrolli iga liidet seebiveega ja korda lekkekatset pärast 100 klapilülitust. Säilita ebaõnnestumised ja parandused [CSV-s](docs/leak_test.csv).
9. **Abikohad ja kuivkatse:** planeeri prügitops ja pime otsikupark Lab 2 paigutuse kõrvale; asukohad on valimata. Tee 20 tsüklit järjekorras doseerimine → tõstmine → kõvendamine → väljund, tühi süstal ja LED väljas. Esimene jooks on 20 % kiirusel, otsikud 20 mm kõrgemal õhus. Tulemused lähevad [CSV-sse](docs/cycle_test.csv).
10. **Tellimus ja kaitsmine:** LED-i ja draiveri valib meeskond, õppejõud ostab Mouserist; kinnitatud valiku juurde tuleb Mouseri tootekood ja põhjendus [BOM-is](docs/bom.md). Tellimus 06.11.2026, esimene kaitsmine 19.11.2026 veebis. Tag lisatakse alles eraldi esitamisotsusega.

Füüsilised mõõtmised: `TODO — waiting for physical measurement`. Kõik uue Lab 3 tööriista sobivused, rõhu-, UV-, vahetus- ja robotikatsed: `TODO — waiting for physical test`.

## Varasemate laborite lähteandmed ja piirangud

- Lab 1: `0,4 mm` lõtk liikus vabalt, `0,2 mm` kiilus, `0,3 mm` pole füüsiliselt testitud. Paindekatse tulemused on [Lab 1 README-s](../lab1/README.md); neid ei kanta automaatselt teise geomeetriaga klambrile.
- [Lab 2 mõõteregister](../lab2/docs/measurements.md): klaas `30 × 30 × 2 mm` on meeskonna kinnitatud, mõõtevahend ja hajuvus pole teada; klaasi mass on veel kaaluda. Eraldi kummist napa `22,25 mm` läbimõõt ja `13,80 mm` kõrgus on nihikuga mõõdetud, kuid samasus robotil oleva napaga pole kinnitatud. Tööriista varasem hinnanguline mass pole kaalumistulemus ega massieelarve alus.
- [Lab 2 README](../lab2/README.md) ja [paigutus](../lab2/docs/layout.md) dokumenteerivad 24.10.2026 ühe ringi nelja klaasiga ning olemasoleva kaamera ja hoidikute tõendid. Need ei ole Lab 3 doseerimis-, UV- ega 20 tsükli tulemused.
- [Kasutatav kalibreerimine](../lab2/calibration/cells.py) on vana nihutatud napa jaoks `R = 33°`; nelja ruudu sobituse jääkvead ulatuvad ligikaudu 1–2 mm-ni. [Nelja sisenurga meetod](../lab2/docs/test-procedure.md) ja mõõteregistri hilisemad parandused on lähtekontekst, mitte uue tööriista punktid. Uue hoidiku, J4 suuna ja nelja nihke järel tuleb punktid füüsiliselt üle õpetada/kontrollida.
- [Ühine digitaalne kaksik](../sim/README.md) kasutab Lab 2 geomeetriat ja [slot-picker](../lab2/slot-picker/README.md) Lab 2 klaasitsüklit. Nende praegused tulemused ei kinnita Lab 3 uut tööriista ega pneumaatikat; selles sessioonis neid ei muudeta ega käivitata.
- Andmehõivega kooskõlastada rõhuanduri asukoht, rõhuandmete kalibreerimine, süstlaharu lubatud pikkus ja võimalik nõelventiil; Nutikate Lahendustega nelja nihke kasutamine.

## Õpetaja CAD-referentsid

Failid asuvad [ametlikus kaustas](https://github.com/KKallas/Narva-subjects/tree/main/EST/2026-27/3D%20printing). Allpool on 25.10.2026 kontrollitud blob SHA-d; binaarfaile meeskonna reposse ei kopeeritud. Mudelid ja andmelehe mõõdud on CAD-referentsid, mitte füüsilised mõõtmised.

| Fail | Git blob SHA |
|---|---|
| [Solenoidklapi kinnitus.f3z](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/3D%20printing/Solenoidklapi%20kinnitus.f3z) | 47725dade20f2d89db92c7ad3aa95b0140030110 |
| [Süstla päis poolik.f3z](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/3D%20printing/S%C3%BCstla%20p%C3%A4is%20poolik.f3z) | 6e97b1e0e1479f38be063089150a0e316151f9fb |
| [Süstla päis ja süstal 10cc.f3d](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/3D%20printing/S%C3%BCstla%20p%C3%A4is%20ja%20s%C3%BCstal%2010cc.f3d) | ff33802ee4826f57b7ad9ac992932d0b076f6f6e |
| [Metcal 910 süstal 10cc.f3d](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/3D%20printing/Metcal%20910%20s%C3%BCstal%2010cc.f3d) | 1b2f915bcb28ea7942ca613f2bd27b48f61b7d3b |
| [Metcal 910-N süstal 10cc.f3d](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/3D%20printing/Metcal%20910-N%20s%C3%BCstal%2010cc.f3d) | 41777aa8cf7f65f7ac4d31c961179478e34b4558 |
| [Metcal 910-WW kolb 10cc.f3d](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/3D%20printing/Metcal%20910-WW%20kolb%2010cc.f3d) | 5c091e776f37aa382d2e44a456cfd23f8b80e55c |
| [Metcal 910-3RHB.f3d](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/3D%20printing/Metcal%20910-3RHB.f3d) | ec965efc7e5c3bafc33fdb226304c93ec218cfe2 |

`Süstla päis poolik.f3z` on õpetaja uuendatud fail; vana kohalik koopia ei tõenda ajakohasust. Enne CAD-tööd võrdle allikafaili blob SHA-d tabeliga. Parameetriline süstlamudel sisaldab ka hinnangulisi mõõte; Metcali süstla-, kolvi- ja päisemudelid on võrdluseks, mitte tihendi sobivuse tõend.

## Tööfailid

- [`assignment-EST.md`](assignment-EST.md) — täpne ametlik koopia.
- [`docs/measurements.md`](docs/measurements.md) — mõõtmised, O-rõnga arvutuse ja UV-katte väljad.
- [`docs/test-procedure.md`](docs/test-procedure.md) — mõõtmise, CAD-kontrolli ja füüsiliste katsete juhend.
- [`docs/tool_layout.md`](docs/tool_layout.md) — õhuskeem, kaalueelarve, klapi ja abikohtade asukoha otsus.
- [`docs/tool_offsets.md`](docs/tool_offsets.md) — neli nihet flantsi suhtes.
- [`docs/leak_test.csv`](docs/leak_test.csv) — surve- ja lekkekatsete kirjed.
- [`docs/cycle_test.csv`](docs/cycle_test.csv) — 20 tühja kuivtsükli rida.
- [`docs/bom.md`](docs/bom.md) — inventuur ja põhjendatud tellimisvajadus.

## CAD-failide tulevane hoidmine

Iga füüsiline iteratsioon säilitatakse eraldi versioonina koos lähtefaili, STL-i ja 3MF-iga. Praegu uut CAD-i ega eksporti ei loodud. Olemasolevad kaustad: `nut-pocket-test/` (vajadusel adapteri mutritasku), `valve-mount/` (õpetaja kinnituse süsteemiadapter), `tool/` (uus tööriistahoidik ja süstla päis), `purge-cup-holder/`, `nozzle-park/`.

## Ohutus

Järgi [ametliku ülesande ohutusosa](assignment-EST.md#ohutus) ja [katsejuhendit](docs/test-procedure.md). Hoidikud ja süstal vahetatakse keelatud robotiga; hädastopp jääb käeulatusse. LED-i kasutamisel on kõigil 405 nm kaitseprillid, valgustamine katte all; LED-i ei vaadata ega kätt/nahka katte alla panda. Survestatud süstal on hoidikus; enne eemaldamist vii klapp vooluta olekusse ning kinnita süstlaharu rõhu vabanemine. Mutri prindipausil kasuta pintsette.

## Arenduspäevik

Lisa iga töökorra lõppu uus sissekanne; ära kirjuta varasemaid sissekandeid ümber.

**PP.KK.AA — kes olid kohal**
- Tegime:
- Juhtus (numbrid):
- Otsustasime, ja miks:
- Lahti järgmiseks korraks:

**11.10.26 — osalejad teadmata**
- Tegime: koostasime esimese füüsilise töökorra jaoks mõõtmislehe ja samm-sammulise katsejuhendi; täiendasime lekkekatse, 20 tsükli kuivkatse, tööriista paigutuse, nihete ja inventuuri/tellimuse tühje vorme.
- Probleemid ja ebaõnnestunud katsed: füüsilistele komponentidele, printerile ega robotile puudus selle ettevalmistuse ajal ligipääs; füüsilisi katseid ei tehtud.
- Parandused: eraldasime ametliku `500 g` koormuspiiri mõõdetavatest massidest ning märkisime kõik mõõtmist või füüsilist kinnitamist nõudvad väljad olekuga `TODO — waiting for physical measurement` või `TODO — waiting for physical test`.
- Mõõdud ja parameetrid: uusi füüsilisi mõõte ega testitulemusi ei lisatud. Lab 1 kinnitatud lähteinfo jääb muutmata: `0,4 mm` lõtk liikus vabalt, `0,2 mm` kiilus ja `0,3 mm` ei ole füüsiliselt kontrollitud.
- Oodatav tulemus: esimesel Lab 3 töökorral saab meeskond alustada inventuurist ja nihikuga mõõtmisest ning liikuda väikeste kontrollprintide ja kuivkatseteni ühtse juhendi järgi.
- Tegelik tulemus: dokumentatsiooni ettevalmistus valmis; `TODO — waiting for physical test`.
- Otsustasime, ja miks: Lab 3 CAD-i ei alustata enne tegelike komponentide mõõtmist; klapi asukohta tööriistal või laual ei valita ilma massi-, vooliku- ja liikumisandmeteta.
- Failid: `docs/measurements.md`, `docs/test-procedure.md`, `docs/leak_test.csv`, `docs/cycle_test.csv`, `docs/tool_layout.md`, `docs/tool_offsets.md`, `docs/bom.md`, `README.md`, juurkausta `AGENTS.md`.
- Lahti järgmiseks korraks: teha inventuur, mõõta päris detailid nihiku ja kaaluga ning dokumenteerida tulemused enne Fusion 360 CAD-i alustamist.

**25.10.2026 — dokumentatsiooni sünkroonimine; füüsilist sessiooni ei toimunud**
- Tegime: sünkroonisime puhta töökoopia fast-forward abil seisule `235ee8e56f3e903308ceda1c8d0c58c9a6d86496`, kontrollisime ametlikku Lab 3 ülesannet ja uuendasime README ning seitse abidokumenti.
- Allikas ja parameetrid: ametliku faili Git blob SHA `b15821c7c47bc22f1549b3aed6b7280a8cb4b651`; 14 kontrollpunkti kopeeriti sõna-sõnalt. Tähtajad: tellimus 06.11.2026, esimene kaitsmine 19.11.2026.
- Probleem ja parandus: varasem tööversioon kasutas vananenud õhuskeemi, tööjärjekorda ja kolme nihet. Kehtiv alus on Y-haruga napp, süstla atmosfääri tühjendav klapp, doseerimine enne klaasi võtmist ning neli nihet koos kaamera pildi keskpunktiga.
- Tegelik tulemus: ainult dokumentatsioon uuendatud; CAD-i, füüsilisi mõõtmisi ega katseid ei tehtud ja uusi tulemusi ei lisatud. Kõik Lab 3 füüsilised katsed: `TODO — waiting for physical test`.
- Otsused ja põhjused: Lab 2 mõõtmised, ühe ringi tulemus ning kalibreerimise piirangud säilitati viidetena; need ei kinnita uut tööriista. Õpetaja seitse CAD-allikat on viidatud koos blob SHA-ga, binaarfaile ei kopeeritud.
- Failid: `assignment-EST.md`, `README.md`, `docs/tool_layout.md`, `docs/measurements.md`, `docs/tool_offsets.md`, `docs/test-procedure.md`, `docs/leak_test.csv`, `docs/cycle_test.csv`, `docs/bom.md`, juurkausta `AGENTS.md`.
- Oodatav tulemus ja järgmine tegevus: inventuur, päris Metcal 910-B mõõtmine, komponentide kaalumine ning rõhuanduri asukoha kooskõlastus; seejärel õpetaja mudelite ülevaatus ja LED-i/draiveri põhjendatud valik.
