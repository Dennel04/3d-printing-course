# 3D printimine ja CAD · Labor 4 — Üks detail paremaks, kolmel moel

**Maht** 30 tundi · **Hindamine** 20 punkti · **Ülesandel märgitud väljastamine** 17.11.2026 · **Tellimine** 27.11.2026 · **Esimene kaitsmine** 10.12.2026 veebis

Lühenda ühe kasutuses oleva prinditud detaili prindiaega või paranda üht teist ülesandes lubatud mõõdikut. Võrdle sama detaili originaali, käsitsi ümber tehtud versiooni ja Fusioni generatiivset versiooni. Kinnita valik meeskonnaga esimesel tööpäeval. [Kohalik ülesandekoopia](assignment-EST.md) · [Täielik ametlik ülesanne](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/3D%20printing/3D%20Printing%20%5BLab%204%5D%20EST.md) · [Ametlik kokkuvõte](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/3D%20printing/3D%20Printing%20%5BLabor%204%20kokkuv%C3%B5te%5D%20EST.md)

## Seis 15.11.2026

Soovitus on **Lab 2 klaasi 2 × 2 Gridfinity sisendhoidik** (`glass-input-holder`, v3) ja mõõdik **lühem prindiaeg sama tugevuse juures**. Hoidikul on Fusioni lähtefail, STL ja PrusaSliceri projekt ning robot on nelja pesa kaudu klaasi teisaldanud. Valik on esialgne, kuni meeskond on tuvastanud füüsilise v3, mõõtnud töökoormuse suuruse ja suuna, teinud originaalil pilootkatse ning kinnitanud Fusionis Generative Designi tööruumi ja uuringu lahendamise ligipääsu. [Kandidaadid ja originaal](docs/analysis_original.md) · [Fusioni ligipääs](docs/generative_setup.md)

**TODO.** Kinnitada detail, mõõdik, katsepiirid ja tellimisvajadus. Teha Lab 4 füüsilised mõõtmised, piloot, mõlemad uued disainid, kolme versiooni simulatsioonid ja kaheksa ülejäänud viilutust. Printida ja katsetada üheksa eksemplari ning valida ja paigaldada võitja. Vahetuse aeg ja andmevorming ootavad seotud meeskondade kokkulepet.

## Kontrollnimekiri

Täida punktid koos kuupäeva ja tõendiviitega. Allolevad 14 punkti järgivad [ametlikku kontrollnimekirja](assignment-EST.md#kontrollnimekiri).

- [ ] Vali esimesel päeval detail ja üks mõõdik, põhjenda valikut. Kirjelda ühes lauses mõõdetud jõu päritolu, suunda ja suurust.
- [ ] Analüüsi originaali prindiaega, kaalu, tugesid, orientatsiooni ja selle põhjendust, nõrka kohta ning materjali, mis koormust ei kanna. [Originaali analüüs](docs/analysis_original.md)
- [ ] Proovi enne ümberjoonistamist katse originaalil läbi. Fikseeri rakis, jõu suund, roboti kiirus ja rikke või tolerantsist väljumise piir. [Katsejuhend](docs/test-procedure.md)
- [ ] Tee käsitsi versioon originaaliga samas Fusioni failis ja kontrolli kõiki liidesemõõte. [Disainide võrdlus](docs/design_comparison.md)
- [ ] Seadista generatiivse uuringu kinnitused, keelualad, koormus ja tootmispiirangud. Vali mõõdiku järgi üks tulemus, puhasta see prinditavaks kehaks ja kontrolli tugede vajadust. [Fusioni uuring](docs/generative_setup.md)
- [ ] Simuleeri kolme versiooni sama koormuse, kinnituste ja võrgusilmaga. Salvesta kuupäevaga ennustus enne võrdlusseeria printi. [Simulatsioon](docs/simulation.md)
- [ ] Viiluta iga versioon kolmes orientatsioonis, täida üheksa rida ja põhjenda asendivalikut mõõdiku järgi. [Orientatsioonitabel](notebooks/README.md)
- [ ] Prindi samal printeril ja sama filamendiga igast versioonist kolm eksemplari. Kaalu ja mõõda kõik üheksa.
- [ ] Katseta kõik üheksa eksemplari läbisegi, arvuta versioonide keskmised ja vahemikud. [Katsetabel](data/test.csv)
- [ ] Võrdle prindiaega, massi, tugesid ja katsetulemust, kõrvuta ennustust mõõtmisega. [Võrdlustabel](docs/design_comparison.md#tulemused)
- [ ] Paigalda võitja ja kontrolli sõltuvaid liideseid, hoidiku asendit, roboti punkte ning vastavalt valitud detailile tööriista nihkeid ja süstlavahetust. [Integratsioon](docs/integration.md)
- [ ] Märgi 27.11 tellimus või kinnitatud nullvajadus BOM-i. [Komponendid](docs/bom.md)
- [ ] Ekspordi kõik Fusioni disainid repos avatavate `.f3d` arhiividena või lingitud osadega disaini puhul `.f3z` arhiividena. Lisa iga prindi STL ja 3MF.
- [ ] Täida README ja arenduspäevik, kontrolli AGENTS.md ning lisa esitamise ajal tag `3d-print-lab4`. Valmista kaitsmiseks ette kolm detaili, võrdlustabel, üks roboti katse ja selgitus, miks käsitsi või generatiivne variant võitis.

## Mida varasematest laboritest kasutada

| Allikas | Kasuta otse | Täienda | Mõõda või valmista uuesti |
| --- | --- | --- | --- |
| [Lab 1 lõtk ja PLA paindekatse](../lab1/README.md#osad) · [paindekehade 3MF](../lab1/flex-piece/3mf/flex-piece-thickness-test.3mf) | 0,2 mm juures kiilus, 0,4 mm juures liikus. 1,2 / 1,5 / 2,0 mm PLA paindekehad näitavad paksuse mõju paindumisele. | Otsi meeskonnalt või õppejõult arvuline piki kihti ja kihtide vahelise tugevuse suhe ning tõmberakise meetod ja jõupiir. Olemasolev paindetabel annab paindevaatlused, jõusuhe ja roboti tõmbepiir puuduvad. | Kui mõõtandmeid pole, lepi kokku ühine jõumõõtmine ja vajaduse korral suunakatse eraldi PLA-proovidel. |
| [Lab 2 mõõdud 13.11.2026](../lab2/docs/measurements.md#13112026--atoms3-ja-klaas-nihikuga) · [paigutus](../lab2/docs/layout.md) · [sobituskatse CSV](../lab2/docs/refit_test.csv) | Gridfinity samm 42 mm, nihikuga mõõdetud klaas 30 × 30 × 1,2 mm ja õpetatud punktid. 12/12 klaasiülekannet kolmes toimivuskatses, sh 13.11 viimases ringis 4/4 pärast hoidikute tagasipanekut ja punkte ümber õpetamata. | Tuvasta tegelik detailiversioon ja rakis. Lab 2-l jäid ringid 4–5, 42 mm füüsiline ümberpaigutus ja tagasipaneku arvuline viga lahtiseks. | Füüsiline pesade, jalgade ja istumiskõrguse mõõt, koormus ning originaali piloot. Tugevuse kohta annab andmed Lab 4 jõukatse. Korda toimivuskontrolli valitud võitjaga. |
| [Lab 3 mõõtmised 15.11](../lab3/docs/measurements.md#mõõtmised-15112026) · [kuivsobitus](../lab3/docs/test-procedure.md#kordusproov-ja-leitud-süstlapäis-15112026) · [kaalueelarve](../lab3/docs/tool_layout.md) | Mõõdetud on klapi koost 68,84 g, tühi süstlakorpus 6,33 g, klaas 1,70 g, napa koost 42,03 g ja XIAO moodul 4,05 g. C-klamber hoidis sügavamal istuvat süstalt kordusproovis, eemaldamisel oli jõudu vaja. Leitud 24,05 g süstlapäis sobis kuivalt referentsiks. | Seo iga mass tegeliku tööriistaversiooni ja koostisega. Verbatim on laual eraldi postil. Klambri korduvus, vahetusjõud ja päise hermeetilisus on veel lahtised. | Kaalu lõplik liikuv tööriist suurima koormaga. Tööriistadetaili valikul mõõda mõjutatud koormus ja neli nihet ning tee asjakohased Lab 3 korduskontrollid. |
| [MG400 digitaalne kaksik](../sim/README.md) · [Station Hub](../hub/README.md) · [Lab 2 salvestatud simulatsioon](../lab2/docs/sim_dry_run_full.txt) | Kasuta olemasolevat URDF-i, ruudustikku, kalibreerimist ja paigutust ulatuse, teekonna ning kokkupõrke eelkontrolliks. | Lisa tegelik detailiümbris, rakis ja tööriistaversioon siis, kui mõõdud on käes. 15.11 Hubi Jog-täiendus puudutab tööala õpetamist. | Tõenda sobivus, haare, jõud ja koordinaadid päris jaamas. Digitaalne kaksik annab geomeetrilise kontrolli ja Fusion annab tugevuse prognoosi. |

## Tööjärjekord

1. **Lab 4 esimene tööpäev.** Kontrolli Fusioni ligipääsu ja riiulivarusid ning märgi puudujäägid. Mõõda originaal ja töökoormus ning tee pilootkatse. Kinnita saadud andmete põhjal detail ja mõõdik. Lepi kokku katseseeria aeg ja võimalik hilisem vahetus. [Katse](docs/test-procedure.md) · [BOM](docs/bom.md) · [Integratsioon](docs/integration.md)
2. **Kodus, pärast pilooti.** Ava Fusioni töökoopia, lukusta liidesed ja tee käsitsi variant ning generatiivne uuring. Käivita kolme versiooni võrreldav simulatsioon. PrusaSliceris viiluta 3 × 3 orientatsiooni ja salvesta valikud koos 3MF-idega. Kirjuta ennustused enne võrdlusseeria printi. Pythonis/Jupyteris valmista ette failide ja arvutuste kontroll. [Disainid](docs/design_comparison.md) · [Analüüs](notebooks/README.md)
3. **Laboris.** Prindi, kaalu ja mõõda üheksa eksemplari ning katseta neid samas rakises. Võrdle prognoosi ja mõõtmist. Paigalda võitja kokkulepitud ajal, kontrolli sõltuvusi ja teavita seotud laborite meeskondi.
4. **Kaitsmine.** Lisa allikfailid, viilutusprojektid ja pildid. Lingi skeemi või simulatsioonipildi juurest muudetava lähtefailini. Näita 15 minuti jooksul kolme versiooni ja tee üks katse robotil.

## Tulemused

**KAARDISTA ISE.** Lisa kinnitatud valik, koormus N ja suund, kuupäevadega katse- ning ennustusviited, võitja või otsuse edasilükkamise põhjus ja uuesti kontrollitud liidesed. Kaitsmise eel lisa repo ja tag, üks lõik käsitsi ning generatiivse variandi erinevusest, töö käigus õpitu ja järgmise labori sisend. [Võrdlustabel](docs/design_comparison.md#tulemused)

## Arenduspäevik

Lisa iga töösessiooni järel uus sissekanne koos kuupäeva, osalejate, töö, arvude, otsuste ja järgmiste sammudega.

**15.11.2026 · dokumentatsiooni ettevalmistus (Codex)**

- Kontrollisime GitHubi `main` seisu `7f92370`, kohalikke tööfaile ja ülesande täisteksti. Ülesandekoopia Git blob on `30e3f5eac2c95b3277d42cbb1466d2e65b3e4729`.
- Panime kirja v3 klaasihoidiku soovituse ja üheksa proovikeha katseplaani. Algse 3MF-i viilutus andis hinnanguks 41 min 58 s ja 28,19 g ning hoiatuse pikkade sildade kohta. Ülejäänud kaheksa orientatsiooni ootavad viilutamist.
- Järgmine samm on meeskonna otsus ja labori piloot. Fikseerida mõõdetud koormus, jõupiir, vastuvõtupiirid ning riiuli jääk enne tellimist.

**15.11.2026 · avaldamiseelne audit (Codex)**

- Võrdlesin 14 kontrollpunkti õppejõu täistekstiga ja täpsustasin Fusioni ligipääsu kontrolli, viilutuse hinnangute ning lõpetamata tööde seisu.
