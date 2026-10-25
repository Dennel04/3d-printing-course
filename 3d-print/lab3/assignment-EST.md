## 3D printimine ja CAD: Labor 3 — Tööriist: napp, süstal ja UV-lamp

**Töömaht:** 28 tundi | **Hindamine:** 20 punkti | **Meeskond:** 3 tudengit | **Välja antud:** 27.10.26 | **Tellimise kuupäev:** 06.11.26 | **Esimene kaitsmine:** 19.11.26, veebis

### Kuidas see dokument töötab

* Repo ja töökord on Laborist 1 olemas ja samad.
* Too sellest dokumendist oma projekti repo juurde see, mida vaja: selle labori kaust, `README.md`, kuhu lähevad su enda numbrid, otsused ja KAARDISTA ISE vastused, ja failid, mida kontrollnimekiri nimetab. Tervet dokumenti üle kopeerida ei ole vaja.

### Eesmärk

Laud on valmis ja hoidikud on ruudustikus. Käe otsas on napp ja kaamera, ja sellega saab tõsta. Aga silt ei saa kokku ainult tõstmisega: klaas **liimitakse** Atomi ekraani peale.

Liim on 3D-printeri vaik, mis kõveneb 405 nm valguse käes. Seega peab robot oskama kolme asja:

* **tõsta** — iminapp, nagu seni;
* **doseerida** — süstal, millest õhurõhk surub tilga välja;
* **kõvendada** — UV LED, mis valgustab liimi läbi klaasi.

Käsi on üks ja tööriista keegi vahepeal ei vaheta. Kõik kolm on ühes tööriistas, koos kaameraga, mis seal Laborist 2 juba on.

Pumpa on samuti üks, ja tal on üks voolik. Pumbakast kas imeb või puhub. Imedes hoiab napp klaasi, puhudes surub õhk süstlast tilga välja. Mõlemat korraga ta ei tee, ja seepärast tehakse tilk enne, kui klaas võetakse. Puhumise ajal on napp lahti ja liigne õhk läheb sealt välja.

Tilga algust ja lõppu otsustab **solenoidklapp** süstla ees: kolme avaga klapp, mis voolu all laseb pumba õhu süstlasse ja vooluta laseb vedrul ta tagasi, nii et süstla rõhk läheb õhku. Napp klapi kaudu ei käi: ta on Y-liitmikuga otse pumba voolikus, enne klappi. Klapp tuleb kuhugi kinnitada, ja voolikud peavad kuhugi minema.

See on esimene detail sellel kursusel, millel on korraga kolm vaenlast. **Rõhk** leiab üles iga prao kihtide vahel. **Kaal** on piiratud: käsi tõstab 500 g, ja sinna sisse läheb tööriist koos kõige raskema koormaga — täis süstal ja klaas napa küljes korraga. Ja **geomeetria**: kolm otsikut ühes tööriistas segavad üksteist, kui sa ei ole läbi mõelnud, kes millal all on.

Selles laboris on viis asja:

1. **Mõõda ja paiguta.** Kõik osad nihikuga, õhu teekond skeemina, kaal kokku arvutatuna — enne kui Fusioni avad.
2. **Klapi kinnitus.** Kinnitus on Fusionis olemas: prindi, pane kokku ja pane ta süsteemi külge.
3. **Tööriist.** Napp, süstal, UV-lamp ja kaamera ühes tükis, nii et ükski ei sega teist.
4. **Õhk peab pidama.** Süstla päis lõpuni, O-rõngaga, ja survekatse pumba täie rõhuga.
5. **Katse.** Kogu liigutus kuivalt läbi, ja kohad ruudustikus, mida doseerimine juurde tahab.

Esimesel päeval uusi osi ei ole. Ehita sellest, mis riiulil on, ja kirjuta puuduv tellimuseks, mis läheb välja 06.11.

*See on elav dokument. Uuenda eesmärke, kui need töö käigus muutuvad — uued teadmised teevad vanad eesmärgid vahel mõttetuks. Mõte on hoida meeskond kogu aeg sihil, et ei eksitaks detailide metsa ja põhiprobleem ei jääks lahendamata.*

**KAARDISTA ISE — eesmärk nii, nagu ta tegelikult välja tuli.**

### Kontrollnimekiri

**Peab olema tehtud**

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

**KAARDISTA ISE — kuupäevad ja sinu enda sammud.**

### Sisendid

* Õppejõult: 3/2 solenoidklapp, kaks 4 mm Y-kiirliitmikku (napi haru ja rõhuandur), tühjad 10 cc mustad süstlad [Metcal 910-B](https://www.farnell.com/datasheets/3919444.pdf) ja otsikud, kaitseprillid 405 nm jaoks.
* Meeskonnalt endalt: 405 nm LED ja draiver. Valid ise, õppejõud ostab Mouserist.
* Õppejõult: klapi kinnitus Fusionis, `Solenoidklapi kinnitus.f3z` selles kaustas; pooleli süstla päis, `Süstla päis poolik.f3z` selles kaustas; O-rõngaste komplekt; 10 cc süstla mudel parameetritega, `Metcal 910 süstal 10cc.f3d`; Metcali enda mudelid süstlast ja kolvist, `Metcal 910-N süstal 10cc.f3d` ja `Metcal 910-WW kolb 10cc.f3d`; ja päis koos süstlaga, `Süstla päis ja süstal 10cc.f3d`; kõik selles kaustas.
* Vanade asjade kastist: mõned eelmise aasta süstlahoidikud. Igaüks on omamoodi veider ja ükski üksi ei ole hea eeskuju; vaata neid koos, enne kui oma hoidiku teed. Süstla päis oli eelmisel aastal valmis Metcali oma; sel aastal teed päise ise. Metcali päis on selles kaustas mudelina, `Metcal 910-3RHB.f3d`.
* 3D printimise L1-st: lõtk, paindumise ja murdumise numbrid.
* 3D printimise L2-st: hoidikud ruudustikus, kaamera kinnitus ja toide, olemasolev iminapa tööriistahoidik (eeskujuks, kuidas hoidik nina külge käib), tööriista kaal.
* Andmehõive L3-st: kus andur voolikus istub ja kui pikk voolik klapi ja süstla vahel olla tohib.
* Nutikate Lahenduste L1-st: jaam, millega punkte õpetada ja üle mängida.

### Vahendid

1. Fusion 360, hariduslitsents
2. PrusaSlicer, labori printerid, PLA
3. Nihik, 300 mm joonlaud, köögikaal (1 g)
4. MG400 koos baaspaketi, pumbakasti ja iminapaga
5. 3/2 solenoidklapp kinnitusega, 4 mm voolik, kaks 4 mm Y-kiirliitmikku, hambaorgid, silikoon
6. 10 cc süstlad (Metcal 910-B) ja otsikud; tühjad, selles laboris vaiku süstlas ei ole
7. 405 nm LED jahutusradiaatoril ja draiver (sinu valitud, Mouserist), kaitseprillid 405 nm jaoks
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
* **Jointid: osad kokku nii, et nad liiguvad**
  [https://www.youtube.com/watch?v=z5gs2_SV5Ao](https://www.youtube.com/watch?v=z5gs2_SV5Ao)
* **Liikumise uuring (Motion Study)**
  [https://www.youtube.com/watch?v=eXEQuWMAEsM](https://www.youtube.com/watch?v=eXEQuWMAEsM)
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

**Osad.** Mõõda nihikuga kõik, mis tööriista sisse või külge läheb: klapp koos kinnitusega, süstal (läbimõõt, krae, pikkus koos otsikuga), iga otsik, LED koos jahutusradiaatoriga, napp, kaameramoodul. Kaalu igaüks, ja kaalu ka klaas, mida napp tõstab, ning süstal tühjana ja UV-liimiga täis. Fusionis on iga osa lihtne keha õigete mõõtudega — mitte ilus, vaid õige suurusega. Siis näed enne printimist, mis millest läbi läheb. LED-i sul alguses ei ole: sa valid ta ise ja ta tuleb tellimusega. Kuni ta kohale jõuab, on ta Fusionis keha andmelehe mõõtude järgi; kui ta tuleb, mõõda üle.

**Õhk.** Joonista teekond: pump → Y-liitmik → üks haru napale, teine klapile, ja klapist süstlale. Klapi kolmas ava läheb õhku. Märgi peale, kuhu süstal on ühendatud, kui klapil voolu ei ole. See peab olema õhk: kui midagi läheb valesti ja vool kaob, ei tohi süstlast midagi välja tulla. Märgi peale ka rõhuandur: ta käib teise Y-kiirliitmikuga voolikusse, kas pumba voolikusse enne klappi või klapi ja süstla vahele, nagu Andmehõive valis. Kui Andmehõive paneb napi harusse nõelventiili, märgi ka see. Märgi peale iga vooliku pikkus. Voolik klapi ja süstla vahel on ruum, mis tuleb enne täis pumbata, kui tilk liikuma hakkab, ja pärast tühjaks lasta, kui tilk peab lõppema — mida pikem, seda laisemalt tilk algab ja lõpeb. Andmehõive mõõdab seda; küsi neilt, kui pikk ta olla tohib.

**Kaal.** Liida kokku. Käsi tõstab 500 g, ja see on kõik, mis flantsi küljes ripub, siis kui ripub kõige rohkem: tööriist, süstal UV-liimiga täis ja klaas napa küljes, kõik korraga. Täis süstal on raskem kui tühi, ja klaas on käe otsas kogu tõstmise ja kõvendamise aja. Mis jääb üle, on see, mida su prinditud osad kaaluda tohivad. Kui number on negatiivne, ei käi klapp käe otsa.

Siit tuleb selle labori esimene päris otsus: **kas klapp elab käe otsas või laua peal?** Käe otsas on voolik süstlani lühike ja tilk algab ja lõpeb teravalt, aga klapp on kaal ja tema juhe peab käega kaasa käima. Laua peal on käsi kerge, aga voolik on pikk. Mõlemad on kaitstavad. Vali numbritega.

Kirjuta üles failis `docs/tool_layout.md`: iga osa mõõdud ja kaal; õhu skeem voolikute pikkustega; kaalueelarve tabelina; kus klapp elab ja miks.

#### 2. Klapi kinnitus

Klapi kinnitust sa ise ei joonista. See on olemas, failis `Solenoidklapi kinnitus.f3z` selle dokumendi kõrval: klapp, kaks prinditud tükki, seibid ning kolm M4 polti mutritega. Ava see enne, kui midagi teed, ja vaata, kuidas ta töötab, sest samad mõtted lähevad sinu enda osadesse.

**Poldid tõmbavad kihid kokku.** Poldid käivad läbi mõlema prinditud tüki ja tõmbavad nad seibidega klapi ümber kokku. Kihid on kogu aeg surve all, mitte ei kisu lahti. Reegel, mis kehtib sellest laborist alates iga poldi kohta: **polt kannab tõmmet, plast kannab ainult survet.** Labori 1 murdumise number ütleb sulle, miks: kihtide vahelt on prinditud detail mitu korda nõrgem kui piki kihti.

**Õhk ei käi läbi prindi.** Voolik läheb läbi prinditud tüki otse klapi juurde, nii lähedale kui saab. Suruõhk puutub ainult voolikut ja klappi, mitte prinditud kihte. Prinditud sein rõhu all leiab kihtide vahelt prao üles (vt osa 4); siin hoiab print ainult voolikut paigal.

**Hambaork ja silikoon.** Kaks tööd, kaks eri asja. Külgaugud on hambaorkude jaoks: hambaork läheb august läbi, surub vastu voolikut ja hoiab teda hõõrdumisega paigal, nii et voolik rõhu all välja ei libise. Hambaork annab tugevuse. Silikoon annab tiheduse: ta liimib vooliku ja prindi vahe hermeetiliselt kinni. Vahe on nii väike kui võimalik, aga nii paks, et silikoon sinna sisse mahub ja rõhk teda vahelt välja ei lükka. Silikoon üksi ei hoiaks voolikut paigal, ja hambaork üksi ei peaks õhku.

See on selle kinnituse õppetund. PLA-st võib teha osa, mis töötab rõhu all, kui kõik tema piirangud on teada ja kinnitus on nende järgi planeeritud: kihid on poltidega kokku surutud, õhk ei käi kihtide vahelt, jõudu kannab hambaork ja tihendab silikoon. Iga piirangu jaoks on oma lahendus, ja ükski lahendus ei pea tegema kahte tööd korraga.

**Prindi ja pane kokku.** Valmis kinnitusi kastis ei ole: prindi kinnitus failist, poldid läbi, hambaork ja silikoon. Siis rõhk peale ja vaata üle: kas print on poldi juurest kihtide vahelt mõranenud, kas voolik liigub hambaorgist hoolimata, kas silikoon on lahti tulnud, kas seebivesi näitab mulle. Kirjuta üles, mis läks katki ja mis sa parandasid, sest see näitab, kus kinnitus on kõige nõrgem.

**Süsteemi külge.** Sinu töö on kinnitus süsteemi külge panna, ja kuidas, sõltub osa 1 otsusest. Kui klapp on laua peal, tee talle Gridfinity hoidik, mis käib ruudustiku peale nagu kõik teised hoidikud, ja juhe läheb ruudu alt kaabliruumi. Kui klapp on käe otsas, käib ta tööriistahoidiku külge, ja tööriistahoidik käib praegu roboti nina külge. Kinnitust ennast muutma ei pea; tee hoidik või adapter, mis teda hoiab. Mõlemal juhul: voolik ei tee klapi juures järsku nurka (murdunud voolik on kinni voolik), klapi mähise ümber käib õhk, ja juhe on kinni nii, et tõmme ei jõua klemmideni.

Kui adapter vajab mutrit, ei käi see plasti keermesse ega liimiga tagaküljele. **Mutter prinditakse sisse.** Sa jätad mudelisse tasku, peatad printeri õigel kihil, paned mutri taskusse ja lased printeril edasi minna, üle mutri. Tasku on mutrist natuke suurem (kui palju, ütleb Labori 1 lõtk) ja natuke sügavam, nii et otsik üle sõites vastu ei lähe, ja peatus on esimesel kihil pärast tasku ülaserva. Proovi kõigepealt väikese klotsi peal, mis prindib kümme minutit, mitte adapteri peal.

Kirjuta üles: mis kokkupanekul või rõhu all katki läks ja mis sa parandasid; kuidas adapter kinnitust hoiab ja kuidas tema poldid kihtide suhtes käivad; kui mutter läks prindi sisse, siis proovikloti tasku mõõdud ja peatuse kõrgus; klapi temperatuur pärast kümmet minutit voolu all, käega või termomeetriga; foto kinnitusest koos voolikutega süsteemi küljes.

#### 3. Tööriist

Nüüd see, mille pärast labor olemas on: üks tööriist, neli asja. Napp, süstal, UV-lamp ja kaamera.

Laboris 2 jäi olemasolev tööriistahoidik puutumata, et õpetatud punktid kehtiksid edasi. Nüüd tuleb sinna nii palju juurde, et vanast hoidikust ei jää midagi alles: tee uus tööriistahoidik, mis käib roboti nina külge. Uue hoidikuga tuleb punktid uuesti õpetada. Arvesta sellega enne, mitte pärast.

**Kes on millal all.** See on selle osa päris küsimus. Kui napp võtab klaasi, ei tohi süstla otsik millegi vastu minna. Kui süstal doseerib, ei tohi napp ees olla ega detaili pihta käia. Kui lamp kõvendab, peab ta olema õigel kaugusel. Selleks on mitu võimalust: otsikud on eri kõrgusel, otsikud on külgsuunas nihkes, või J4 pöörab tööriista nii, et õige otsik tuleb õige koha peale. Pane kogu tööriist Fusionis kokku: iga osa on oma komponent, ja osad on omavahel ja roboti nina küljes jointidega (Joint). Siis tee liikumise uuring (Motion Study): tööriist käib läbi kõigi kolme töökoha — sisend, töökoht, väljund — ja kõigi hoidikute kohalt, mis Laboris 2 tegid. Nii näed enne printimist, mis kuhu vastu läheb. Hoidiku sein, mis nappa ei seganud, võib süstla otsikut segada.

**Süstal.** Hoidik hoiab süstalt nii, et otsik on iga kord samas kohas. Sama reegel, mis hoidikul ruudustikus: asendi annab kuju, mitte hõõrdumine. Krae toetub, toru on juhitud, ja pärast vahetust on otsik seal, kus ta oli. Süstal vahetub **ühe käega ja ilma tööriistadeta** — teises käes on sul uus süstal. See on klamber, mis paindub ja tuleb tagasi, ja Laboris 1 mõõtsid sa täpselt selle: kuhu maani tükk paindub ja tuleb tagasi, ja kust alates ei tule. Klamber töötab esimese numbri sees, varuga. Süstal on 10 cc [Metcal 910-B](https://www.farnell.com/datasheets/3919444.pdf): andmelehel on joonis, kus on sisediameeter 15,72 mm, välisdiameeter 18,26 mm, krae 22,6 × 34,0 mm ja 3,3 mm paks, pikkus 90,9 mm. Selle järgi on tehtud mudel `Metcal 910 süstal 10cc.f3d` selles kaustas: iga mõõt on kasutaja parameeter ja kolm neist (Luer-krae diameeter ja sein, koonuse pikkus) on hinnangud, sest andmelehel neid ei ole. Metcali enda mudel samast süstlast on kõrval, `Metcal 910-N süstal 10cc.f3d`, ja kolb `Metcal 910-WW kolb 10cc.f3d`: nendega saad kontrollida, kas su päis istub päris süstla kuju peal. Andmeleht ütleb ise, et mõõdud on viiteks: mõõda päris süstal nihikuga üle ja pane enda numbrid parameetritesse. Süstla suurus jääb parameetriks. Vanade asjade kastis on mõned eelmise aasta hoidikud. Ükski neist ei ole eeskuju; vaata neid koos ja otsi, mis on neil kõigil olemas ja mis igaühel valesti on.

**UV-lamp.** LED on jahutusradiaatori peal ja radiaator on põhjusega: LED läheb kuumaks. PLA hakkab pehmenema 60 °C kandis. Radiaator vajab õhku enda ümber, mitte plastist karpi. Lamp on süstla otsikust vähemalt 30 mm kaugusel ja suunatud nii, et **valguskoonus läheb otsikust mööda**. Liim, mis kõveneb otsiku sees, on ummistunud otsik, ja see lõpetab tööpäeva. Joonista koonus Fusionis kehana ja vaata, kas ta lõikub otsikuga. Siis kontrolli laual: prillid ette, LED kõige väiksema vooluga, valge paber liimi kohale. 405 nm paistab valgel koopiapaberil tuhmi violetse laiguna, ja see laik on su laik. Ta on eredam, kui paistab, nii et vaata prillidega. Laik peab olema paberil ja otsik varjus. Kui lambi ümber on vari, mis valgust suunab, on ta must või seest tume.

**Kate.** Valgustamine käib katte all, nii et valgus välja ei paista. Kate võib olla tööriista küljes, töökoha hoidiku küljes või mõlemas: näiteks must põll ümber lambi, mis laskub kõvendamise asendis töökoha hoidiku serva peale, nii et valgus jääb nende vahele kinni. Radiaator jääb katte välja, õhu kätte.

Kate prinditakse **musta** PLA-ga. 405 nm on UV ja nähtava valguse piiril: silm näeb teda tuhmina, palju nõrgemana, kui ta on, nii et lekkivat valgust on kerge alahinnata, aga silmad saavad sellest ikkagi kahju. Hele või naturaalne PLA laseb osa sellest läbi ja hajutab. Must pigment neelab UV ära ja kaitseb ühtlasi plasti ennast: UV vanandab PLA-d pinnalt, ta läheb kollaseks ja rabedaks, ja must kate peab sellele kõige kauem vastu. Kui ta kevadeks rabedaks läheb, prindid uue. Ohtlikum on soojus, sest LED on katte kõrval ja PLA pehmeneb 60 °C kandis.

Katte seinal on **sügavust**: mitu perimeetrit ja täidis vahel, mitte üks õhuke sein. Prinditud sein on kihtide virn, ja üks halvasti kinni jäänud kiht, esimene kiht või auk perimeetris on pragu, kust valgus otse välja pääseb. Paksu seina ja täidisega peab valgus läbima mitu kihti ja põrkama täidise vastu, ja sinna ta jääbki. Kontrolli: paber, mis UV all helendab (markeriga üle tõmmatud valge paber või helendav kleebis), katte ümber, pime ruum, prillid ees, LED kõige väiksema vooluga katte all. Kus paber helendab, sealt valgus välja pääseb.

**Kaamera** jääb. Ta peab endiselt nägema seda, mis otsiku all toimub, ja nüüd on otsikuid kaks. Otsusta, kumba ta vaatab, või kas ta näeb mõlemat.

**Voolikud ja juhtmed.** Kaks voolikut, kaamera toide, LED-i juhe, võib-olla klapi juhe. Kõik nad käivad käega kaasa. Tõmbetõke on osa prindist, mitte kleeplint.

Lõpuks mõõda iga otsiku koht flantsi suhtes: napa keskpunkt, süstla otsiku tipp, lambi laigu keskpunkt ja kaamera pildi keskpunkt. Neli nihet, millimeetrites. Kaamera nihet vajab Andmehõive: robot viib kaamera iga tilga kohale ja pildistab ta. Jaam liidab need õpetatud punktile, ja siis ei pea iga kohta kolm korda õpetama.

Kirjuta üles: kuidas sa lahendasid, kes millal all on, ja mis sind teistest lahendustest loobuma pani; liikumise uuring Fusionis ja mis seal kuhu vastu läks; süstla vahetuse aeg ja otsiku koht pärast vahetust võrreldes enne (viis vahetust, nihikuga või kaameraga); klambri paindumine ja Labori 1 number, mille pealt see tuli; lambi kaugus otsikust, foto laigust paberil; radiaatori temperatuur pärast kavandatud kõvendusaega; katte seina paksus, perimeetrid ja täidis, ja kust helendav paber esimesel korral valgust näitas; tööriista kaal tühja süstlaga ning täis süstla ja klaasiga korraga; neli nihet failis `docs/tool_offsets.md`; foto tööriistast kahest küljest.

#### 4. Õhk peab pidama

Süstlasse tuleb õhk tagant, kolvi poolt. Selleks on süstla päis: prinditud tükk, mis käib süstla tagumise otsa peale ja kuhu voolik sisse läheb. Ta peab vastu kogu rõhu, mida pump anda jõuab, ja tuleb ära, kui süstalt vahetad.

**Pooleli päis.** Failis `Süstla päis poolik.f3z` selle dokumendi kõrval on päis, mis on poolel teel. Ta on joonistatud 10 cc süstlale (Metcal 910, sisediameeter 15,72 mm), nagu ka Metcali päis: kuju on olemas ja kaks M4 polti hoiavad teda koos, aga tihendit ei ole. Selline päis lekib. Sinu töö on ta lõpuni teha.

Failis `Süstla päis ja süstal 10cc.f3d` on päis ja süstla mudel koos, lukus. Päis on keeratav lukk: süstla krae läheb kanalisse, ja 60° pööret viib krae otsad riiulite alla, kuni nad jäävad vastu piirajaid. Fusionis läheb see läbi ilma, et miski teineteisest läbi läheks. Aga Fusionis on lõtk null, ja päris printeril ei ole: krae on 3,3 mm paks ja tema pilu riiuli all on 3,4 mm kõrge, ja tropp läheb süstla sisse 15,72 mm avasse 14,66 mm suurusena. Kas see mahub ja kas krae ei loksu, ütleb Labori 1 lõtk, mitte joonis. Mõõda oma süstal nihikuga, pane numbrid süstla mudeli parameetritesse ja vaata, kas päis sobib ikka.

Tropil on soon (põhi 11,94 mm, laius 2 mm), ja koostus on sinna pandud üks rõngas komplektist, 11 × 2,5, nii nagu ta päriselt istuks: soone põhja peale venitatud. Pane Fusionis koostusele interference-kontroll peale ja vaata, mida see ütleb. Õppejõult saad O-rõngaste komplekti: vali sealt rõngas, arvuta, kas soon surub teda õigesti kokku ja kas tal on soones ruumi, ja muuda soont, kui ei ole. Kas 11 × 2,5 on üldse õige valik, otsustad ka sina.

Eelmisel aastal käis süstla peale valmis päis (Metcal), ja tema mudel on selles kaustas, `Metcal 910-3RHB.f3d`. Kui tahad pooleli päise asemel oma päise teha, on see parem eeskuju: vaata, kuidas tema süstla külge käib ja kus ta tihendab. Sel aastal on päis prinditud, ja prinditud päisest pääseb õhk välja kahte teed. Kas **läbi seina**: prinditud sein on kihtide virn ja rõhk leiab kihtide vahelt tee, kui sein on õhuke või perimeetreid on vähe. Või **tihendi kõrvalt**: O-rõngas tihendab ainult siis, kui ta on soones, mis teda parasjagu kokku surub — liiga sügavas soones ta ei puuduta, liiga madalas ei mahu päis peale. Soone mõõdud arvutatakse rõnga mõõtudest, mitte ei pakuta.

Seega: sein, mis on rõhu all, on piisavalt paks ja perimeetreid on piisavalt, ja rõngas istub soones, mis teda õigesti kokku surub. Proovi soont kõigepealt väikese klotsi peal, mitte terve päise peal.

**Survekatse.** Päis peab vastu pumba täie rõhu, mitte ainult doseerimise rõhu. Otsikul kork, napi haru kinni, et õhk sealt välja ei läheks, klapp voolu all, pump puhub täisvõimsusel, kuni rõhk enam ei tõuse. Selle numbri näitab Andmehõive andur, ja see on pumba suurim rõhk. Kui päis selle välja kannatab, kannatab ta ka doseerimist.

**Lekkekatse.** Süstla otsikul kork peal, napi haru kinni. Pump puhuma, klapp voolu alla, pump seisma. Klapp jääb voolu alla kogu katse ajaks: vooluta laseb ta süstla õhku. Vaata Andmehõive anduri pealt, kui palju rõhk viie minutiga langeb. Siis seebivesi igale liitekohale: voolik, vooliku ots klapi kinnituses, klapp, süstla päis. Mullid näitavad kohta. Paranda ja korda. Seejärel sada klapi lülitust ja sama katse uuesti, sest liitekoht, mis pidas esimesel päeval, ei pruugi pidada pärast sadat tõmblust.

Kirjuta üles: kust su päis esimesel korral lekkis ja mis selle parandas; mis rõnga valisid komplektist, soone mõõdud ja kust need tulid; pumba suurim rõhk ja kas päis selle välja kannatas; read failis `docs/leak_test.csv` (katse number, rõhk alguses, rõhk 5 minuti pärast, kus lekkis, mis parandas); tulemus enne ja pärast sadat lülitust.

#### 5. Katse

Doseerimine tahab ruudustikus kahte kohta juurde, ja mõlemad on Gridfinity hoidikud.

* **Prügitops.** Enne iga tööd lastakse otsikust üks tilk topsi, et otsikus oleks värske liim. Tops on koht, kuhu robot ulatub ja kust inimene ta tühjendamiseks kätte saab.
* **Otsiku parkimiskoht.** Kui robot seisab, ei tohi otsik olla valguse käes: päevavalguses on piisavalt UV-d, et liim otsikus aegamisi kõveneks. Koht, kus otsik on pimedas ja kinni.

Pane mõlemad Labori 2 paigutusele (`layout.md`) juurde ja vaata, kas käe tee jääb ikka ühesuunaliseks.

Siis kuiv läbijooks. Süstal on tühi, LED on väljas, klapp lülitab. Robot läheb töökoha kohale doseerimise asendisse, siis võtab klaasi sisendist, toob ta töökohale kõvendamise asendisse ja paneb klaasi väljundisse. Doseerimine on enne tõstmist, sest kui pump imeb klaasi kinni, ei saa ta süstlasse puhuda. 20 korda järjest, kõigepealt 20 % kiirusel. Vaata nelja asja: kas mõni voolik või juhe jääb kuhugi taha; kas mõni otsik käib hoidiku vastu; kas J4 pööramisel läheb midagi pingule; ja kas kaamera näeb endiselt seda, mida peab.

Siis võta tööriist flantsi küljest maha ja pane tagasi. Kas neli nihet kehtivad veel? See on sama küsimus, mis hoidikul ruudustikus, ja sama mõõtmine.

Kirjuta üles: uuendatud `layout.md` prügitopsi ja parkimiskohaga; read failis `docs/cycle_test.csv` (ring, kas jõudis doseerimise asendisse, kas tõstis, kas jõudis kõvendamise asendisse, kas pani, mis haakis); mitu kahekümnest läks puhtalt läbi; nihked enne ja pärast tööriista mahavõtmist.

**KAARDISTA ISE — vastused.** Iga osa kohta: numbrid, ühikud, kus fail on. Tegemata asja kohta üks rida, miks.

### Ohutus

* **405 nm valgus ja silmad.** Valgustamine käib katte all, nii et valgus välja ei paista. 405 nm on UV ja nähtava valguse piiril: silm näeb teda tuhmi violetsena, palju nõrgemana, kui ta tegelikult on, ja võrkkest saab kahju enne, kui valgus ere tundub. LED-i ei vaadata, ei varjuga ega ilma, ja käsi ega nahka katte alla ei panda. Kui LED on draiveri küljes, on kõigil laua ääres kaitseprillid 405 nm jaoks ees. Laigu katse käib samuti katte all, kõige väiksema vooluga, lamp suunatud laua poole, mitte kunagi silmade kõrgusele.
* **Selles laboris vaiku süstlas ei ole.** Lekkekatse käib õhu ja seebiveega. Kui laual on süstal vaiguga, on otsikul kork peal ja käes nitriilkindad: kõvenemata vaik ärritab nahka.
* **Rõhk.** Korgiga süstal pumba täie rõhu all on suletud anum. Katse ajal on ta hoidikus, mitte käes. Vooluta klapp laseb süstla rõhu ise õhku: enne kui süstla ära võtad, on klapp vooluta.
* Lahtine voolik rõhu all lendab; ära suuna kellegi poole.
* LED-i radiaator ja klapi mähis lähevad kuumaks. Mõõda, ära katsu.
* **Roboti alus peab jääma vabaks**, nagu Laboris 2. Klapi hoidik ja prügitops ei ulatu aluse vastu.
* Uue tööriista esimene jooks käib 20 % kiirusel ja otsikud jäävad 20 mm kõrgemale, õhku. Tööriist on nüüd pikem ja laiem kui see, millega punktid õpetati.
* Hoidikuid ja süstalt vahetatakse siis, kui robot on keelatud.
* Printeri otsik on 200–230 °C. Kui paned mutrit peatatud prindi sisse, on otsik sealsamas: kasuta pintsette.
* Robot: käed ei ole laua kohal, kui robot on sisse lülitatud. Hädastopp käeulatuses.

### Komponendid selle labori jaoks

Tellimus läheb välja 06.11.26 ja jõuab kohale enne kaitsmist. Valmis nimekirja ei ole: meeskond paneb tellimuse ise kokku faili `docs/bom.md`, iga rea juures üks lause, milline osa seda küsib.

Tellimine käib ühisest tellimistabelist: [https://moodle.ut.ee/mod/url/view.php?id=1535601](https://moodle.ut.ee/mod/url/view.php?id=1535601). Kanna oma read sinna enne tellimise kuupäeva; mida tabelis ei ole, seda ei tellita. Fail `docs/bom.md` jääb sinu reposse põhjenduseks, miks sa just neid asju küsisid.

**LED-i ja draiveri valid ise.** Õppejõud ostab need Mouserist, nii et tabelisse läheb Mouseri tootekood ja `docs/bom.md`-sse põhjendus. Liim on [Anycubic Standard Resin](https://www.photopoint.ee/en/printers-accessories/5160735-anycubic-standard-resin-grey), mis kõveneb 365–405 nm all. Valime 405 nm, sest polükarbonaatklaas neelab tavaliselt suure osa 365 nm valgusest, aga 405 nm laseb paremini läbi. Mõtle: kas LED-i lainepikkus on tõesti 405 nm; kui lai on kiirgusnurk, sest sellest tuleb lambi koonus ja laigu suurus; kui palju valgust ta annab ja kui palju sooja tuleb sellega kaasa; kas ta on juba tähekujulisel alusel või tuleb see eraldi; mis voolu ta tahab ja milline draiver selle annab; ja kas mõõdud on andmelehel, et saaksid ta Fusionisse joonistada enne, kui ta kohale jõuab.

Mõtle näiteks: kas O-rõngaste komplektis on rõngas, mida su soone arvutus tahab, või tuleb mõni juurde tellida; kas polte, mutreid ja seibe jätkub klapi kinnituse ja adapteri jaoks, ja kas neid jääb varuks, sest mõni jääb proovikloti sisse; kas silikooni on; kas 4 mm voolikut jätkub mõlema haru jaoks; kas LED-i ja klapi juhe on piisavalt pikk ja pehme, et käega kaasa käia; ja kas PLA peab radiaatori ja klapi kõrval vastu või küsib see koht teist materjali.

### Hindamiskriteeriumid

| Kategooria | Punktid |
| :--- | :--- |
| Tööfailid — parameetritega tööriist, klapi kinnituse adapter ja lõpuni tehtud süstla päis koos sisse modelleeritud osadega, prügitopsi ja parkimiskoha hoidikud, STL ja 3MF iga prindi kohta, peatuse kõrgused 3MF-is | 5 p |
| Analüüs — osade mõõdud ja kaalueelarve, õhu skeem, klapi asukoha valik, klambri paindumine Labori 1 numbri vastu, lambi koonus, O-rõnga soone arvutus, survekatse ja lekkekatse tabel, neli nihet | 5 p |
| Prototüüp — tööriist roboti küljes alla 500 g koos täis süstla ja klaasiga, süstal vahetub ühe käega, lamp tabab liimi kohta ja mitte otsikut, süstla haru peab rõhku, 20 kuiva ringi ilma haakumata | 5 p |
| Dokumentatsioon — README, arenduspäevik, `tool_layout.md`, `tool_offsets.md`, `leak_test.csv`, `cycle_test.csv`, `bom.md`, AGENTS.md | 5 p |
| **Kokku** | **20 p** |

### Kaitsmine

Link git repole, tag `3d-print-lab3`.

Kaitsmine on lihtne suuline 15 minuti jutuajamine. Vahetad süstla ühe käega. Robot teeb ühe kuiva ringi: läheb doseerimise asendisse, tõstab klaasi, läheb kõvendamise asendisse, paneb klaasi ära. Näitad paberil, kuhu lambi laik langeb. Avad oma arenduspäeviku. Õppejõud küsib umbes viis küsimust selle kohta, kuidas sa selle tegid. Kui esimesel korral ei õnnestu, tuled uuesti.

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
* Nutikad Lahendused L3: neli nihet, mille järgi jaam teab, kus napp, otsik, lamp ja kaamera õpetatud punkti suhtes on.
* 3D printimine L4: tööriist ja klapi kinnitus, millest üks detail tehakse ühe mõõdiku järgi paremaks.

**KAARDISTA ISE, lõpus.**
* Git repo ja tag:
* Numbrid, mille see labor andis, ühikutega:
* Mida me teeksime teisiti:
* Mida järgmine labor peaks enne alustamist teadma:

### Tagasiside
