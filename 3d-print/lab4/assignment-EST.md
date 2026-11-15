## 3D printimine ja CAD: Labor 4 — Üks detail paremaks, kolmel moel

**Töömaht:** 30 tundi | **Hindamine:** 20 punkti | **Meeskond:** 3 tudengit | **Välja antud:** 17.11.26 | **Tellimise kuupäev:** 27.11.26 | **Esimene kaitsmine:** 10.12.26, veebis

### Kuidas see dokument töötab

* Repo ja töökord on Laborist 1 olemas ja samad.
* Too sellest dokumendist oma projekti repo juurde see, mida vaja: selle labori kaust, `README.md`, kuhu lähevad su enda numbrid, otsused ja KAARDISTA ISE vastused, ja failid, mida kontrollnimekiri nimetab. Tervet dokumenti üle kopeerida ei ole vaja.
* Skeemid ja simulatsioonid lähevad dokumenti pildina, pildi juurde link elavale failile, et teine saaks selle lahti teha ja edasi muuta.

### Eesmärk

Laua peal on nüüd kolme labori jagu detaile, ja neid on nädalaid kasutatud: hoidikud ruudustikus Laborist 2, tööriist napi, süstla, lambi ja kaameraga, klapi kinnitus ja süstla päis Laborist 3. Iga detail joonistati üks kord ja prinditi kohe, kui ta töötas. Keegi ei küsinud, kas ta võiks olla kergem, kiirem printida või kauem vastu pidada.

Selles laboris võtad ühe neist detailidest ja teed ta **ühe mõõdiku järgi paremaks**. Mõõdikuid on neli, ja valid ühe:

* **Prindiaeg** sama tugevuse juures.
* **Tugevus** sama prindiaja juures (±5 %).
* **Kaal** sama tugevuse juures — tööriista detailil, sest käsi tõstab 500 g koos kõige raskema koormaga.
* **Kasutuskorrad**: mitu süstla vahetust, hoidiku väljavõtmist või klambri painutust, enne kui mõõdetud omadus läheb tolerantsist välja.

Ja sa teed seda **kolmel moel**, et näha, milline võitis:

1. **Originaal**, nii nagu ta on.
2. **Käsitsi ümber tehtud**: ribid sinna, kus jõud käib, seinad otsiku laiuse kordsed, kaldserv toe asemel, poldid Labori 3 reegli järgi.
3. **Generatiivne disain** Fusionis: samad kinnituskohad, samad koormused, samad kohad, kuhu materjali panna ei tohi — ja kuju otsib arvuti.

Kõik kolm lähevad enne printimist läbi simulatsiooni, ja simulatsiooni ennustus kirjutatakse üles enne, kui esimene eksemplar printerist tuleb. Siis kõik kolm prinditakse, ja kõik kolm läbivad sama katse roboti peal. Tulemus on tabel ja vastus ühele küsimusele: **kas sellise detaili puhul on käsitsi tehtud disain parem kui generatiivne, ja miks?**

Selles laboris on viis asja:

1. **Vali detail ja mõõdik.** Ja koormus ühe lausega: kust jõud tuleb, mis suunas, kui suur.
2. **Originaal ja katse.** Kuidas originaal on tehtud ja kus ta nõrk on. Katse on paigas ja läbi proovitud enne, kui midagi ümber joonistad.
3. **Kaks uut versiooni.** Käsitsi ja generatiivne, samade liidestega.
4. **Simulatsioon enne printi.** Sama koormus, samad kinnitused, ennustus kirjas.
5. **Katse ja võrdlus.** Kolm eksemplari igast versioonist, üks tabel, üks võitja, mis läheb lauale.

Esimesel päeval uusi osi ei ole. Ehita sellest, mis riiulil on, ja kirjuta puuduv tellimuseks, mis läheb välja 27.11.

*See on elav dokument. Uuenda eesmärke, kui need töö käigus muutuvad — uued teadmised teevad vanad eesmärgid vahel mõttetuks. Mõte on hoida meeskond kogu aeg sihil, et ei eksitaks detailide metsa ja põhiprobleem ei jääks lahendamata.*

**KAARDISTA ISE — eesmärk nii, nagu ta tegelikult välja tuli.**

### Kontrollnimekiri

**Peab olema tehtud**

- [ ] Detail ja mõõdik valitud esimesel päeval, põhjus kirjas. Koormus ühe lausega, suund ja suurus mõõdetud, mitte oletatud.
- [ ] Originaali analüüs failis `docs/analysis_original.md`: prindiaeg, mass, tugi, orientatsioon ja miks, nõrk koht, kus materjal ei kanna midagi.
- [ ] Katse kirjeldatud ja originaali peal läbi proovitud enne ümberjoonistamist: rakis, jõu suund, roboti kiirus, mis on "katki" või "tolerantsist väljas".
- [ ] Käsitsi versioon Fusionis samas failis kui originaal; iga liidese mõõt sama.
- [ ] Generatiivne versioon: kinnituskohad, keelualad, koormus ja tootmise piirangud seadistatud, üks tulemus valitud mõõdiku järgi, puhastatud kehaks, prinditav ilma tugede metsata.
- [ ] Simulatsioon kõigil kolmel versioonil sama koormuse, samade kinnituste ja sama võrgusilmaga. Ennustus kirjas enne printimist.
- [ ] Iga versioon kolmes orientatsioonis läbi slaiseri, üheksa rida tabelis, orientatsioon valitud mõõdiku järgi.
- [ ] Iga versioon prinditud kolm korda samal printeril, kaalutud, mõõdetud.
- [ ] Katse tehtud: kolm eksemplari versiooni kohta, keskmine ja vahemik. Tulemus failis `data/test.csv`.
- [ ] Võrdlustabel: prindiaeg, mass, tugi, tugevus või kasutuskorrad, ennustus mõõdetu kõrval.
- [ ] Võitja laual, ja kõik, mis temast sõltub, töötab: tööriista nihked, hoidiku asend, süstla vahetus.
- [ ] Tellimus 27.11 failis `docs/bom.md`.
- [ ] Iga Fusioni disain on repos Fusioni arhiivina (File → Export: `.f3d`, lingitud osadega disainil `.f3z`), et õppejõud saaks ta lahti teha.
- [ ] Repo ja arenduspäevik täidetud, tag `3d-print-lab4`.

**KAARDISTA ISE — kuupäevad ja sinu enda sammud.**

### Sisendid

* 3D printimise L1-st: lõtk, kihtide vahelise ja piki kihti murdumise suhe, painde- ja murdumise numbrid, roboti tõmbekatse meetod.
* 3D printimise L2-st: hoidikud ja ruudustik, tagasipanemise katse ja selle numbrid. Ümber tehtud hoidik peab need numbrid säilitama.
* 3D printimise L3-st: tööriist, klapi kinnitus, süstla päis, kaalueelarve ja kolm nihet failis `tool_offsets.md`. Ümber tehtud tööriista detail peab nihked säilitama või uuesti mõõtma.
* Andmehõive L4-st: laud teeb samal ajal sadu tsükleid originaaldetailidega. Lepi kokku, millal detail vahetatakse, et nende andmed ei läheks pooleks.

### Vahendid

1. Fusion, hariduslitsents, simulatsiooni ja generatiivse disaini tööruumiga
2. PrusaSlicer, üks ja sama printer kõigi versioonide jaoks, PLA
3. Nihik, köögikaal (1 g)
4. MG400 jaamaga, tõmbekatse jõu mõõtmine Laborist 1, konks ja rakis
5. Originaaldetail nii, nagu ta prinditi; kui ta on katki, prindi ta uuesti sama `.3mf`-ist muutmata kujul
6. Kasutuskordade mõõdikuks: vastasdetailid (süstlad, klaasid, klapp) ja loendur
7. Jupyter Lab

*Kui plaan muutub, uuenda ka vahendeid, või tee draw.io skeem, mis näitab, kuidas asjad omavahel töötavad.*

**KAARDISTA ISE — mida sa päriselt kasutasid.**

### Taustainfo

* **Generatiivne disain Fusionis**
  [https://www.youtube.com/watch?v=PSSt8wswNJQ](https://www.youtube.com/watch?v=PSSt8wswNJQ)
  Lühidalt: mis peab jääma ja kuhu materjali panna ei tohi
  [https://www.youtube.com/watch?v=lbDFC0oD-e0](https://www.youtube.com/watch?v=lbDFC0oD-e0)
* **Staatiline simulatsioon Fusionis** — koormus, kinnitus, võrgusilm
  [https://www.youtube.com/watch?v=qXljJk7TZZE](https://www.youtube.com/watch?v=qXljJk7TZZE)
  Sama pikemalt
  [https://www.youtube.com/watch?v=wsF_tEp_4tE](https://www.youtube.com/watch?v=wsF_tEp_4tE)
* **Disain FDM printimiseks** — ribid, seina paksus, kaldserv toe asemel
  [https://www.youtube.com/watch?v=_R2E8VwyNz0](https://www.youtube.com/watch?v=_R2E8VwyNz0)
  Ja detailid, mis tuge ei vaja
  [https://www.youtube.com/watch?v=RPijCjz9G1w](https://www.youtube.com/watch?v=RPijCjz9G1w)
* **Topoloogia optimeerimine** — mida generatiivne disain kapoti all teeb
  [https://www.youtube.com/watch?v=_erS8dRxILM](https://www.youtube.com/watch?v=_erS8dRxILM)

*Lisa siia oma allikaid ja kasulikku infot, mis aitaks sul projektist aru saada ka aastaid hiljem, kui selle uuesti lahti teed.*

**KAARDISTA ISE — sinu allikad.**

### Osad

#### 1. Vali detail ja mõõdik

Vali detail, mille paremaks tegemine midagi päriselt muudab. Tööriista detail, mis on kerge, on terve labori kasu: iga gramm, mis tööriistast ära tuleb, on gramm koormust juurde. Hoidik, mis kulub, on kasu sellele, kes laudu igal nädalal kokku paneb. Klamber, mis väsib, on süstla vahetus, mis ühel päeval ei õnnestu.

Siis koormus. Kust jõud tuleb, mis suunas, ja kui suur ta on? Ära paku. Mõõda: napi tõmbejõud klaasilt, süstla vahetamise jõud, klapi kaal korda kiirendus, mida robot liigutamisel annab. Kui jõudu mõõta ei saa, kirjuta, miks, ja kust su number tuli.

Kirjuta üles: detail, mõõdik ja põhjus; koormus ühe lausega, suund ja suurus, ja kuidas sa selle said.

#### 2. Originaal ja katse

Enne, kui midagi ümber joonistad, tea, mis sul on.

**Originaal.** Prindiaeg ja mass slaiserist ja kaalult, tugi grammides, orientatsioon ja miks just see. Nõrk koht: kus ta Labori 1–3 katsetes murdus või kus tal on kulumise jälg. Ja kus materjal ei tee midagi: seinad, mis on paksemad, kui vaja, täidis, mis ei kanna, kohad, kust jõud läbi ei käi. Labori 1 kihtide pindala kõver Z suunas näitab, kuhu prindiaeg läheb.

**Katse.** Sama katse käib kõigi kolme versiooni peal, nii et ta peab olema korratav: rakis, mis hoiab detaili alati samamoodi, jõu suund, roboti kiirus, ja mis on "katki" või "tolerantsist väljas". Tugevuse mõõdikul tõmbab robot Labori 1 meetodiga, kolm eksemplari versiooni kohta. Kasutuskordade mõõdikul käib robot vastasdetailiga läbi kuni sada korda või seni, kuni mõõdetud omadus tolerantsist välja läheb.

Proovi katse originaali peal läbi, enne kui joonistad. Katse, mida esimest korda proovitakse uue detaili peal, mõõdab katset, mitte detaili.

Kirjuta üles: `docs/analysis_original.md`; katse kirjeldus ja originaali tulemus kolme eksemplariga.

#### 3. Kaks uut versiooni

Mõlemal uuel versioonil on täpselt samad liidesed kui originaalil: kinnitusaugud, süstla krae, hoidiku jalg, klapi poldid. Kui liides muutub, ei ole see enam sama detail, ja võrdlus ei kehti.

**Käsitsi.** Tee koopia samas Fusioni failis ja hoia liidesed lukus visandis. Siis ribid sinna, kust jõud läbi käib, seinad otsiku laiuse kordsed, kaldserv toe asemel, poldid Labori 3 reegli järgi: polt kannab tõmmet, plast ainult survet.

**Generatiivne.** Fusion vajab neli asja: mis peab jääma (liidesed), kuhu materjali panna ei tohi (süstal, voolikud, lambi koonus, napi tee, hoidiku pesad), koormused varuteguriga 2, ja tootmise piirangud (lisatootmine, üleulatuv nurk, väikseim paksus). Tulemusi annab ta nii palju, kui mitu materjali, tootmisviisi ja printimissuunda sa talle ette annad. Vali üks mõõdiku järgi, tee temast keha ja kontrolli, et ta prindib ilma tugede metsata. Generatiivne tulemus, mis vajab rohkem tuge kui detaili ennast, ei ole võit.

Kirjuta üles: mõlema versiooni Fusioni fail ja ekraanipilt; generatiivse uuringu seadistus; mitu tulemust ta andis ja miks sa valisid selle.

#### 4. Simulatsioon enne printi

Kõik kolm versiooni lähevad läbi sama simulatsiooni: sama koormus, samad kinnitused, sama võrgusilma suurus. Kirjuta iga versiooni kohta ennustus — kus ta murdub ja millise jõu juures — **enne**, kui esimene eksemplar printerist tuleb.

Simulatsioon arvestab materjali, mis on igas suunas ühesugune. Prinditud detail ei ole: kihtide vahelt on ta mitu korda nõrgem. Labori 1 suhe ütleb, kui palju. Kirjuta üles, kuidas sa selle ennustusse tõid.

Siis orientatsioon: iga versioon kolmes asendis läbi slaiseri. Üheksa rida tabelis — prindiaeg, tugi, ja kus kihid on jõu suhtes. Vali iga versiooni asend mõõdiku järgi: prindiaja mõõdikul kiireim, tugevuse ja kasutuskordade mõõdikul see, kus kihid jäävad jõuga risti.

Kirjuta üles: simulatsiooni seadistus ja pildid; ennustus iga versiooni kohta kuupäevaga; üheksa orientatsiooni tabel ja valik.

#### 5. Katse ja võrdlus

Prindi iga versioon kolm korda samal printeril, sama filamendiga. Kaalu ja mõõda iga eksemplar. Siis katse, kõik eksemplarid samas järjekorras segamini, mitte esimesena kõik originaalid — muidu mõõdad ka seda, kuidas robot või rakis päeva jooksul muutus.

Võrdlustabel: prindiaeg, mass, tugi, tugevus või kasutuskorrad keskmise ja vahemikuga, ja ennustus mõõdetu kõrval. Kus ennustus eksis, ja miks?

Võitja läheb lauale. Kontrolli kõik, mis temast sõltub: kas tööriista nihked kehtivad, kas hoidik tuleb samasse kohta tagasi, kas süstal vahetub ühe käega.

Kirjuta üles: `data/test.csv` (versioon, eksemplar, prindiaeg, mass, tulemus, mis juhtus); võrdlustabel; üks lõik vastusega küsimusele, kas käsitsi oli parem kui generatiivne ja miks; mis lauale läks ja mis selle järel üle mõõdeti.

**KAARDISTA ISE — vastused.** Iga osa kohta: numbrid, ühikud, kus fail on. Tegemata asja kohta üks rida, miks.

### Ohutus

* **Tõmbekatse.** Prinditud detail murdub äkki ja tükid lendavad. Kaitseprillid ees, käed eemal, robot tõmbab 20 % kiirusel.
* **Roboti jõud.** Robot ei ole tõmbemasin: tema jõud on piiratud ja kokkupõrke tuvastus peatab ta. Ära tõsta jõudu üle selle, mida Labori 1 mõõtmine lubas.
* **Laud ja Andmehõive tsüklid.** Detaili vahetus käib siis, kui robot on keelatud ja Andmehõive meeskond teab.
* Printeri otsik on 200–230 °C. Pintsetid, mitte sõrmed.
* Robot: käed ei ole laual, kui robot on sisse lülitatud. Hädastopp käeulatuses.

### Komponendid selle labori jaoks

Tellimus läheb välja 27.11.26 ja jõuab kohale enne kaitsmist. Valmis nimekirja ei ole: meeskond paneb tellimuse ise kokku faili `docs/bom.md`, iga rea juures üks lause, milline osa seda küsib.

Tellimine käib ühisest tellimistabelist: [https://moodle.ut.ee/mod/url/view.php?id=1535601](https://moodle.ut.ee/mod/url/view.php?id=1535601). Kanna oma read sinna enne tellimise kuupäeva; mida tabelis ei ole, seda ei tellita.

Mõtle näiteks: kas filamenti jätkub vähemalt üheksa prindi ja paari ebaõnnestumise jaoks; millest teed konksu ja rakise, mis hoiab detaili tõmbel alati samamoodi; kas polte ja mutreid jätkub uute versioonide jaoks; ja kas kasutuskordade katse kulutab vastasdetaile — süstlaid, klaase —, mida tuleb juurde.

### Hindamiskriteeriumid

| Kategooria | Punktid |
| :--- | :--- |
| Tööfailid — kolm versiooni Fusionis samade liidestega, generatiivse uuringu seadistus, simulatsioon, slaiseri projektid, STL ja 3MF iga prindi kohta | 5 p |
| Analüüs — originaali analüüs, koormus mõõdetud, ennustus enne printi, üheksa orientatsiooni tabel, võrdlustabel keskmise ja vahemikuga, ennustus mõõdetu kõrval | 5 p |
| Prototüüp — kõik kolm versiooni prinditud ja katsetatud sama katsega, võitja laual ja kõik temast sõltuv töötab | 5 p |
| Dokumentatsioon — README, arenduspäevik, `analysis_original.md`, `test.csv`, `bom.md`, AGENTS.md | 5 p |
| **Kokku** | **20 p** |

### Kaitsmine

Link git repole, tag `3d-print-lab4`.

Kaitsmine on lihtne suuline 15 minuti jutuajamine. Näitad kolme versiooni kõrvuti ja võrdlustabelit. Robot teeb ühe katse otse. Ütled, kumb võitis, käsitsi või generatiivne, ja miks, ja kus simulatsioon eksis. Avad oma arenduspäeviku. Õppejõud küsib umbes viis küsimust selle kohta, kuidas sa selle tegid. Kui esimesel korral ei õnnestu, tuled uuesti.

Repos on kaustas `3d-print/lab4/`: kolm versiooni lähtefailidena (Fusioni disainid arhiivina, `.f3d` või `.f3z`), STL ja `.3mf` iga prindi kohta, `notebooks/` orientatsiooni ja võrdlusega, `data/test.csv`, `docs/` kaustas `analysis_original.md`, simulatsiooni pildid, `bom.md` ja fotod, `README.md` selle labori kohta, ja `AGENTS.md` uuendatud.

### Arenduspäevik

**KAARDISTA ISE — päevik.** Üks sissekanne iga töösessiooni kohta, kirjutatud iseendale, nii et inimene, kes seal ei olnud, saab aru. Sissekandeid lisatakse, mitte ei muudeta.

**PP.KK.AA — kes olid kohal**
* Tegime:
* Juhtus (numbrid):
* Otsustasime, ja miks:
* Lahti järgmiseks korraks:

### Väljundid ja tulemused

**Väljundid**
* Integratsiooniprojekt: parem detail koos põhjusega, miks ta parem on.
* Andmehõive L4: kuupäev, millal detail laual vahetus, et andmed jaguneksid õigesti.
* 3D printimine L5: harjumus vaadata, kuhu tolerants ja materjal lähevad — joonise jaoks, mis läheb tellimusena välja.

**KAARDISTA ISE, lõpus.**
* Git repo ja tag:
* Numbrid, mille see labor andis, ühikutega:
* Mida me teeksime teisiti:
* Mida järgmine labor peaks enne alustamist teadma:

### Tagasiside
