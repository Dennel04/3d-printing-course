## 3D printimine ja CAD: Labor 3 — Tööriist: napp, süstal ja UV-lamp

**Töömaht:** 28 tundi | **Hindamine:** 20 punkti | **Meeskond:** 3 tudengit | **Välja antud:** 27.10.26 | **Tellimise kuupäev:** 06.11.26 | **Esimene kaitsmine:** 17.11.26, veebis

### Kuidas see dokument töötab

* Repo ja töökord on Laborist 1 olemas ja samad.
* Too sellest dokumendist oma projekti repo juurde see, mida vaja: selle labori kaust, `README.md`, kuhu lähevad su enda numbrid, otsused ja KAARDISTA ISE vastused, ja failid, mida kontrollnimekiri nimetab. Tervet dokumenti üle kopeerida ei ole vaja.

### Eesmärk

Laud on valmis ja hoidikud on ruudustikus. Käe otsas on napp ja kaamera, ja sellega saab tõsta. Aga silt ei saa kokku ainult tõstmisega: klaas **liimitakse** Atomi ekraani peale.

Liim on läbipaistev vaik, mis kõveneb 405 nm valguse käes. Seega peab robot oskama kolme asja:

* **tõsta** — iminapp, nagu seni;
* **doseerida** — süstal, millest õhurõhk surub tilga välja;
* **kõvendada** — UV LED, mis valgustab liimi läbi klaasi.

Käsi on üks ja tööriista keegi vahepeal ei vaheta. Kõik kolm on ühes tööriistas, koos kaameraga, mis seal Laborist 2 juba on.

Pumpa on samuti üks. Tema õhk läheb kas napale või süstlale, ja selle üle otsustab **solenoidklapp**: kolme avaga klapp, mis voolu all lülitab pumba süstlale ja vooluta laseb vedrul ta tagasi napale. Klapp tuleb kuhugi kinnitada, ja voolikud peavad kuhugi minema.

See on esimene detail sellel kursusel, millel on korraga kolm vaenlast. **Rõhk** leiab üles iga prao kihtide vahel. **Kaal** on piiratud: käsi tõstab 500 g koos tööriistaga. Ja **geomeetria**: kolm otsikut ühes tööriistas segavad üksteist, kui sa ei ole läbi mõelnud, kes millal all on.

Selles laboris on viis asja:

1. **Mõõda ja paiguta.** Kõik osad nihikuga, õhu teekond skeemina, kaal kokku arvutatuna — enne kui Fusioni avad.
2. **Klapi kinnitus.** Kus klapp elab ja mis teda kinni hoiab.
3. **Tööriist.** Napp, süstal, UV-lamp ja kaamera ühes tükis, nii et ükski ei sega teist.
4. **Õhk peab pidama.** Süstla õhuühendus ja lekkekatse.
5. **Katse.** Kogu liigutus kuivalt läbi, ja kohad ruudustikus, mida doseerimine juurde tahab.

Esimesel päeval uusi osi ei ole. Ehita sellest, mis riiulil on, ja kirjuta puuduv tellimuseks, mis läheb välja 06.11.

*See on elav dokument. Uuenda eesmärke, kui need töö käigus muutuvad — uued teadmised teevad vanad eesmärgid vahel mõttetuks. Mõte on hoida meeskond kogu aeg sihil, et ei eksitaks detailide metsa ja põhiprobleem ei jääks lahendamata.*

**KAARDISTA ISE — eesmärk nii, nagu ta tegelikult välja tuli.**

### Kontrollnimekiri

**Peab olema tehtud**

- [ ] Kõik osad mõõdetud nihikuga ja Fusionis kehadena olemas: klapp koos liitmikega, süstal, süstla otsikud, UV LED jahutusradiaatoril, napp, kaameramoodul.
- [ ] Õhu teekond skeemina ja kaalueelarve tabelina failis `docs/tool_layout.md`.
- [ ] Klapi kinnitus valmis: klapp on kinni oma kinnitusaukudest, mutrid on prindi sisse pandud, voolikud ei murdu.
- [ ] Tööriist roboti küljes: napp, süstal, UV-lamp ja kaamera. Kaal alla 500 g koos täis süstlaga.
- [ ] Süstal vahetub ühe käega, ilma tööriistadeta. 20 vahetust järjest, klamber terve.
- [ ] UV-lambi koonus tabab liimi kohta ja läheb süstla otsikust mööda. Kontrollitud Fusionis ja valge paberiga laual.
- [ ] Iga otsiku nihe flantsi suhtes mõõdetud ja kirjas failis `docs/tool_offsets.md`.
- [ ] Lekkekatse: süstla haru hoiab rõhku 5 minutit, iga liitekoht seebiveega üle käidud. Tulemus failis `docs/leak_test.csv`.
- [ ] Prügitopsi hoidik ja otsiku parkimiskoht ruudustikus.
- [ ] Kuiv läbijooks: tõsta klaas, mine doseerimise kohta, mine kõvendamise kohta, 20 korda. Miski ei haagi. Tulemus failis `docs/cycle_test.csv`.
- [ ] Tellimus 06.11 failis `docs/bom.md`.
- [ ] Repo ja arenduspäevik täidetud, tag `3d-print-lab3`.

**KAARDISTA ISE — kuupäevad ja sinu enda sammud.**

### Sisendid

* Õppejõult: 3/2 solenoidklapp koos 4 mm kiirliitmikega, süstlad ja otsikud, 405 nm LED tähekujulisel jahutusradiaatoril koos draiveriga, 405 nm kaitseprillid.
* Vanade asjade kastist: eelmise aasta süstlahoidikud ja süstlakorgid. Korgid lekkisid. Enne kui oma teed, vaata, miks.
* 3D printimise L1-st: lõtk, paindumise ja murdumise numbrid.
* 3D printimise L2-st: hoidikud ruudustikus, kaamera kinnitus ja toide, olemasolev iminapa tööriistahoidik, tööriista kaal.
* Andmehõive L3-st: kus andur voolikus istub ja kui pikk voolik klapi ja süstla vahel olla tohib.
* Nutikate Lahenduste L1-st: jaam, millega punkte õpetada ja üle mängida.

### Vahendid

1. Fusion 360, hariduslitsents
2. PrusaSlicer, labori printerid, PLA
3. Nihik, 300 mm joonlaud, köögikaal (1 g)
4. MG400 koos baaspaketi, pumbakasti ja iminapaga
5. 3/2 solenoidklapp, 4 mm voolik, kiirliitmikud
6. Süstlad ja otsikud; tühjad, selles laboris vaiku süstlas ei ole
7. 405 nm LED jahutusradiaatoril koos draiveriga, 405 nm kaitseprillid
8. Poldid, mutrid, seibid; pihustipudel seebiveega
9. Git, üks repo meeskonna kohta, `AGENTS.md` juurkaustas

*Kui plaan muutub, uuenda ka vahendeid, või tee draw.io skeem, mis näitab, kuidas asjad omavahel töötavad.*

**KAARDISTA ISE — mida sa päriselt kasutasid.**

### Taustainfo

* **Süstal roboti otsas, näide**
  [https://www.youtube.com/watch?v=MKC5gWasoKE](https://www.youtube.com/watch?v=MKC5gWasoKE)
* **Metall prindi sees: mutrid ja poldid**
  [https://www.youtube.com/watch?v=XpDG8VxZsw4](https://www.youtube.com/watch?v=XpDG8VxZsw4)
* **Poldid risti kihtidega**
  [https://www.youtube.com/watch?v=cC5KlelZlx4](https://www.youtube.com/watch?v=cC5KlelZlx4)
  Ja õpime teiste vigadest
  [https://www.youtube.com/watch?v=A1d8aFPtQ8c](https://www.youtube.com/watch?v=A1d8aFPtQ8c)
* **3D prinditavad vedrud ja klambrid**
  [https://www.youtube.com/watch?v=wpriGP45Unw](https://www.youtube.com/watch?v=wpriGP45Unw)
* **Komponent vs keha**
  [https://www.youtube.com/watch?v=L6MMw-dfS8s](https://www.youtube.com/watch?v=L6MMw-dfS8s)
* **Kas detailid lähevad üksteisest läbi (Interference)**
  [https://www.youtube.com/watch?v=wy6chd2hP24](https://www.youtube.com/watch?v=wy6chd2hP24)
* **Printimise peatamine kindlal kihil PrusaSliceris**
  (link puudu — YouTube: "PrusaSlicer pause print embed nut")
* **O-rõnga soon**
  (link puudu — YouTube: "o-ring groove design 3D printed seal")
* **MG400 flants**
  [https://a360.co/4nruicX](https://a360.co/4nruicX)

*Lisa siia oma allikaid ja kasulikku infot, mis aitaks sul projektist aru saada ka aastaid hiljem, kui selle uuesti lahti teed.*

**KAARDISTA ISE — sinu allikad.**

### Osad

#### 1. Mõõda ja paiguta

Enne kui Fusioni avad, on kolm asja paberil.

**Osad.** Mõõda nihikuga kõik, mis tööriista sisse või külge läheb: klapp koos liitmikega ja tema kinnitusaukude samm, süstal (läbimõõt, krae, pikkus koos otsikuga), iga otsik, LED koos jahutusradiaatoriga, napp, kaameramoodul. Kaalu igaüks. Fusionis on iga osa lihtne keha õigete mõõtudega — mitte ilus, vaid õige suurusega. Siis näed enne printimist, mis millest läbi läheb.

**Õhk.** Joonista teekond: pump → klapp → kaks haru, üks napale ja teine süstlale. Märgi peale, kumb haru on lahti, kui klapil voolu ei ole. See peab olema napp: kui midagi läheb valesti ja vool kaob, ei tohi süstlast midagi välja tulla. Märgi peale ka iga vooliku pikkus. Voolik klapi ja süstla vahel on ruum, mis tuleb enne täis pumbata, kui tilk liikuma hakkab — mida pikem, seda aeglasem ja laisem tilk. Andmehõive mõõdab seda; küsi neilt, kui pikk ta olla tohib.

**Kaal.** Liida kokku. Käsi tõstab 500 g koos tööriistaga, ja täis süstal on raskem kui tühi. Mis jääb üle, on see, mida su prinditud osad kaaluda tohivad. Kui number on negatiivne, ei käi klapp käe otsa.

Siit tuleb selle labori esimene päris otsus: **kas klapp elab käe otsas või laua peal?** Käe otsas on voolik süstlani lühike ja tilk terav, aga klapp on kaal ja tema juhe peab käega kaasa käima. Laua peal on käsi kerge, aga voolik on pikk. Mõlemad on kaitstavad. Vali numbritega.

Kirjuta üles failis `docs/tool_layout.md`: iga osa mõõdud ja kaal; õhu skeem voolikute pikkustega; kaalueelarve tabelina; kus klapp elab ja miks.

#### 2. Klapi kinnitus

Klapil on oma kinnitusaugud. Kasuta neid. Klapp, mis on plastklambri vahele pigistatud, on klapp, mis kahe nädala pärast loksub: klapp läheb töötades soojaks ja PLA annab sooja käes järele.

Reegel, mis kehtib sellest laborist alates iga poldi kohta: **polt kannab tõmmet, plast kannab ainult survet.** Polt käib läbi detaili nii, et ta surub kihte kokku, mitte ei kisu neid lahti. Labori 1 murdumise number ütleb sulle, miks: kihtide vahelt on prinditud detail mitu korda nõrgem kui piki kihti.

Mutter ei käi plasti keermesse ega liimiga tagaküljele. **Mutter prinditakse sisse.** Sa jätad mudelisse tasku, peatad printeri õigel kihil, paned mutri taskusse ja lased printeril edasi minna, üle mutri. Kolm asja peavad paigas olema: tasku on mutrist natuke suurem (kui palju, ütleb Labori 1 lõtk), tasku on mutrist natuke sügavam, nii et otsik üle sõites vastu ei lähe, ja peatus on esimesel kihil pärast tasku ülaserva. Proovi kõigepealt väikese klotsi peal, mis prindib kümme minutit. Mitte klapi kinnituse peal, mis prindib kaks tundi.

Kinnitus ise sõltub osa 1 otsusest. Kui klapp on laua peal, on ta Gridfinity hoidik nagu kõik muu, ja juhe läheb ruudu alt kaabliruumi. Kui ta on käe otsas, on ta osa tööriistast. Mõlemal juhul: voolik ei tee kiirliitmiku juures järsku nurka (murdunud voolik on kinni voolik), klapi mähise ümber käib õhk, ja juhe on kinni nii, et tõmme ei jõua klemmideni.

Kirjuta üles: proovikloti tasku mõõdud ja peatuse kõrgus, ja mis esimesel korral valesti läks; klapi kinnituse peatuse kõrgused; kuidas polt kihtide suhtes käib; klapi temperatuur pärast kümmet minutit voolu all, käega või termomeetriga; foto kinnitusest koos voolikutega.

#### 3. Tööriist

Nüüd see, mille pärast labor olemas on: üks tööriist, neli asja. Napp, süstal, UV-lamp ja kaamera.

Laboris 2 jäi olemasolev tööriistahoidik puutumata, et õpetatud punktid kehtiksid edasi. Nüüd on see sinu otsus: ehitad olemasoleva külge või teed uue. Kui teed uue, tuleb punktid uuesti õpetada. Arvesta sellega enne, mitte pärast.

**Kes on millal all.** See on selle osa päris küsimus. Kui napp võtab klaasi, ei tohi süstla otsik millegi vastu minna. Kui süstal doseerib, ei tohi napp ees olla ega detaili pihta käia. Kui lamp kõvendab, peab ta olema õigel kaugusel. Selleks on mitu teed: otsikud on eri kõrgusel, otsikud on külgsuunas nihkes, või J4 pöörab tööriista nii, et õige otsik tuleb õige koha peale. Proovi oma lahendus Fusionis läbi kõigi kolme töökohaga — sisend, töökoht, väljund — ja kõigi hoidikutega, mis Laboris 2 tegid. Hoidiku sein, mis nappa ei seganud, võib süstla otsikut segada.

**Süstal.** Hoidik hoiab süstalt nii, et otsik on iga kord samas kohas. Sama reegel, mis hoidikul ruudustikus: asendi annab kuju, mitte hõõrdumine. Krae toetub, toru on juhitud, ja pärast vahetust on otsik seal, kus ta oli. Süstal vahetub **ühe käega ja ilma tööriistadeta** — teises käes on sul uus süstal. See on klamber, mis paindub ja tuleb tagasi, ja Laboris 1 mõõtsid sa täpselt selle: kuhu maani tükk paindub ja tuleb tagasi, ja kust alates ei tule. Klamber töötab esimese numbri sees, varuga. Süstla suurus on parameeter.

**UV-lamp.** LED on jahutusradiaatori peal ja radiaator on põhjusega: LED läheb kuumaks. PLA hakkab pehmenema 60 °C kandis. Radiaator vajab õhku enda ümber, mitte plastist karpi. Lamp on süstla otsikust vähemalt 30 mm kaugusel ja suunatud nii, et **valguskoonus läheb otsikust mööda**. Liim, mis kõveneb otsiku sees, on ummistunud otsik, ja see lõpetab tööpäeva. Joonista koonus Fusionis kehana ja vaata, kas ta lõikub otsikuga. Siis kontrolli laual: prillid ette, LED kõige väiksema vooluga, valge paber liimi kohale. Laik peab olema paberil ja otsik varjus. Kui lambi ümber on vari, mis valgust suunab, on ta must või seest tume.

**Kaamera** jääb. Ta peab endiselt nägema seda, mis otsiku all toimub, ja nüüd on otsikuid kaks. Otsusta, kumba ta vaatab, või kas ta näeb mõlemat.

**Voolikud ja juhtmed.** Kaks voolikut, kaamera toide, LED-i juhe, võib-olla klapi juhe. Kõik nad käivad käega kaasa. Tõmbetõke on osa prindist, mitte kleeplint.

Lõpuks mõõda iga otsiku koht flantsi suhtes: napa keskpunkt, süstla otsiku tipp, lambi laigu keskpunkt. Kolm nihet, millimeetrites. Jaam liidab need õpetatud punktile, ja siis ei pea iga kohta kolm korda õpetama.

Kirjuta üles: kuidas sa lahendasid, kes millal all on, ja mis sind teistest lahendustest loobuma pani; süstla vahetuse aeg ja otsiku koht pärast vahetust võrreldes enne (viis vahetust, nihikuga või kaameraga); klambri paindumine ja Labori 1 number, mille pealt see tuli; lambi kaugus otsikust, foto laigust paberil; radiaatori temperatuur pärast kavandatud kõvendusaega; tööriista kaal tühja ja täis süstlaga; kolm nihet failis `docs/tool_offsets.md`; foto tööriistast kahest küljest.

#### 4. Õhk peab pidama

Süstlasse tuleb õhk tagant, kolvi poolt. Õhuvoolik peab süstla külge käima nii, et ta peab +110 kPa juures ja tuleb ära, kui süstalt vahetad.

Eelmise aasta korgid on vanade asjade kastis ja nad lekkisid. Võta üks, pane rõhu alla ja otsi seebiveega üles, kust. Enamasti on vastus üks kahest. Kas õhk läks **läbi seina**: prinditud sein on kihtide virn ja rõhk leiab kihtide vahelt tee, kui sein on õhuke või perimeetreid on vähe. Või läks ta **tihendi kõrvalt**: O-rõngas tihendab ainult siis, kui ta on soones, mis teda parasjagu kokku surub — liiga sügavas soones ta ei puuduta, liiga madalas ei mahu kork peale. Soone mõõdud arvutatakse rõnga mõõtudest, mitte ei pakuta.

Tee oma. Või leia valmis adapter ja pane see tellimusse — ka see on vastus, kui sa ütled, miks.

**Lekkekatse.** Süstla otsikul kork peal. Pump puhuma, klapp süstla harule, pump seisma. Vaata Andmehõive anduri pealt, kui palju rõhk viie minutiga langeb. Siis seebivesi igale liitekohale: voolik, kiirliitmikud, klapp, kork. Mullid näitavad kohta. Paranda ja korda. Seejärel sada klapi lülitust ja sama katse uuesti, sest liitekoht, mis pidas esimesel päeval, ei pruugi pidada pärast sadat tõmblust.

Kirjuta üles: kust vana kork lekkis; sinu korgi või adapteri lahendus, ja kui O-rõngas, siis soone mõõdud ja kust need tulid; read failis `docs/leak_test.csv` (katse number, rõhk alguses, rõhk 5 minuti pärast, kus lekkis, mis parandas); tulemus enne ja pärast sadat lülitust.

#### 5. Katse

Doseerimine tahab ruudustikus kahte kohta juurde, ja mõlemad on Gridfinity hoidikud.

* **Prügitops.** Enne iga tööd lastakse otsikust üks tilk topsi, et otsikus oleks värske liim. Tops on koht, kuhu robot ulatub ja kust inimene ta tühjendamiseks kätte saab.
* **Otsiku parkimiskoht.** Kui robot seisab, ei tohi otsik olla valguse käes: päevavalguses on piisavalt UV-d, et liim otsikus aegamisi kõveneks. Koht, kus otsik on pimedas ja kinni.

Pane mõlemad Labori 2 paigutusele (`layout.md`) juurde ja vaata, kas käe tee jääb ikka ühesuunaliseks.

Siis kuiv läbijooks. Süstal on tühi, LED on väljas, klapp lülitab. Robot võtab klaasi sisendist, läheb töökoha kohale doseerimise asendisse, siis kõvendamise asendisse, paneb klaasi väljundisse. 20 korda järjest, kõigepealt 20 % kiirusel. Vaata nelja asja: kas mõni voolik või juhe jääb kuhugi taha; kas mõni otsik käib hoidiku vastu; kas J4 pööramisel läheb midagi pingule; ja kas kaamera näeb endiselt seda, mida peab.

Siis võta tööriist flantsi küljest maha ja pane tagasi. Kas kolm nihet kehtivad veel? See on sama küsimus, mis hoidikul ruudustikus, ja sama mõõtmine.

Kirjuta üles: uuendatud `layout.md` prügitopsi ja parkimiskohaga; read failis `docs/cycle_test.csv` (ring, kas tõstis, kas jõudis doseerimise asendisse, kas jõudis kõvendamise asendisse, kas pani, mis haakis); mitu kahekümnest läks puhtalt läbi; nihked enne ja pärast tööriista mahavõtmist.

**KAARDISTA ISE — vastused.** Iga osa kohta: numbrid, ühikud, kus fail on. Tegemata asja kohta üks rida, miks.

### Ohutus

* **405 nm valgus ja silmad.** LED-i ei vaadata, ei varjuga ega ilma. Kui LED on draiveri küljes, on kõigil laua ääres 405 nm kaitseprillid ees. Laigu katse käib kõige väiksema vooluga, lamp suunatud laua poole, mitte kunagi silmade kõrgusele.
* **Selles laboris vaiku süstlas ei ole.** Lekkekatse käib õhu ja seebiveega. Kui laual on süstal vaiguga, on otsikul kork peal ja käes nitriilkindad: kõvenemata vaik ärritab nahka.
* **Rõhk.** Korgiga süstal +110 kPa all on suletud anum. Katse ajal on ta hoidikus, mitte käes. Enne kui süstla ära võtad, lase rõhk klapi kaudu välja.
* Lahtine voolik +110 kPa juures lendab; ära suuna kellegi poole.
* LED-i radiaator ja klapi mähis lähevad kuumaks. Mõõda, ära katsu.
* **Roboti alus peab jääma vabaks**, nagu Laboris 2. Klapi hoidik ja prügitops ei ulatu aluse vastu.
* Uue tööriista esimene jooks käib 20 % kiirusel ja otsikud jäävad 20 mm kõrgemale, õhku. Tööriist on nüüd pikem ja laiem kui see, millega punktid õpetati.
* Hoidikuid ja süstalt vahetatakse siis, kui robot on keelatud.
* Printeri otsik on 200–230 °C. Kui paned mutrit peatatud prindi sisse, on otsik sealsamas: kasuta pintsette.
* Robot: käed ei ole laua kohal, kui robot on sisse lülitatud. Hädastopp käeulatuses.

### Komponendid selle labori jaoks

Tellimus läheb välja 06.11.26 ja jõuab kohale enne kaitsmist. Valmis nimekirja ei ole: meeskond paneb tellimuse ise kokku faili `docs/bom.md`, iga rea juures üks lause, milline osa seda küsib.

Tellimine käib ühisest tellimistabelist: [https://moodle.ut.ee/mod/url/view.php?id=1535601](https://moodle.ut.ee/mod/url/view.php?id=1535601). Kanna oma read sinna enne tellimise kuupäeva; mida tabelis ei ole, seda ei tellita. Fail `docs/bom.md` jääb sinu reposse põhjenduseks, miks sa just neid asju küsisid.

Mõtle näiteks: mis mõõdus O-rõngast su soone arvutus tahab, kui sa korgi ise teed, või kas valmis adapter on mõistlikum; mis polte ja mutreid klapi kinnitusaugud küsivad ja kas neid on varuks, sest mõni jääb proovikloti sisse; kas 4 mm voolikut ja kiirliitmikke jätkub mõlema haru jaoks; kas LED-i ja klapi juhe on piisavalt pikk ja pehme, et käega kaasa käia; ja kas PLA peab radiaatori ja klapi kõrval vastu või küsib see koht teist materjali.

### Hindamiskriteeriumid

| Kategooria | Punktid |
| :--- | :--- |
| Tööfailid — parameetritega tööriist ja klapi kinnitus koos sisse modelleeritud osadega, prügitopsi ja parkimiskoha hoidikud, STL ja 3MF iga prindi kohta, peatuse kõrgused 3MF-is | 5 p |
| Analüüs — osade mõõdud ja kaalueelarve, õhu skeem, klapi asukoha valik, klambri paindumine Labori 1 numbri vastu, lambi koonus, lekkekatse tabel, kolm nihet | 5 p |
| Prototüüp — tööriist roboti küljes alla 500 g, süstal vahetub ühe käega, lamp tabab liimi kohta ja mitte otsikut, süstla haru peab rõhku, 20 kuiva ringi ilma haakumata | 5 p |
| Dokumentatsioon — README, arenduspäevik, `tool_layout.md`, `tool_offsets.md`, `leak_test.csv`, `cycle_test.csv`, `bom.md`, AGENTS.md | 5 p |
| **Kokku** | **20 p** |

### Kaitsmine

Link git repole, tag `3d-print-lab3`.

Kaitsmine on lihtne suuline 15 minuti jutuajamine. Vahetad süstla ühe käega. Robot teeb ühe kuiva ringi: tõstab klaasi, läheb doseerimise asendisse, läheb kõvendamise asendisse, paneb klaasi ära. Näitad paberil, kuhu lambi laik langeb. Avad oma arenduspäeviku. Õppejõud küsib umbes viis küsimust selle kohta, kuidas sa selle tegid. Kui esimesel korral ei õnnestu, tuled uuesti.

Repos on kaustas `3d-print/lab3/`: lähtefailid, STL ja `.3mf` iga prindi kohta, `docs/` kaustas `tool_layout.md`, `tool_offsets.md`, `leak_test.csv`, `cycle_test.csv`, `bom.md` ja fotod, `README.md` selle labori kohta, ja `AGENTS.md` uuendatud.

### Arenduspäevik

**KAARDISTA ISE — päevik.** Üks sissekanne iga töösessiooni kohta, kirjutatud iseendale, nii et inimene, kes seal ei olnud, saab aru. Sissekandeid lisatakse, mitte ei muudeta.

**PP.KK.AA — kes olid kohal**
* Tegime:
* Juhtus (numbrid):
* Otsustasime, ja miks:
* Lahti järgmiseks korraks:

### Väljundid ja tulemused

**Väljundid**
* Andmehõive L3: tööriist, mille süstla haru peab rõhku ja mille voolikute pikkused on teada — tilga suurust saab mõõta päris tööriistaga, mitte käes hoitud süstlaga.
* Nutikad Lahendused L3: kolm nihet, mille järgi jaam teab, kus napp, otsik ja lamp õpetatud punkti suhtes on.
* 3D printimine L4: tööriist ja klapi kinnitus, millest üks detail tehakse ühe mõõdiku järgi paremaks.

**KAARDISTA ISE, lõpus.**
* Git repo ja tag:
* Numbrid, mille see labor andis, ühikutega:
* Mida me teeksime teisiti:
* Mida järgmine labor peaks enne alustamist teadma:

### Tagasiside
