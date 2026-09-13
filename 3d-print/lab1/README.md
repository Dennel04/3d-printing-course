## 3D printimine ja CAD: Labor 1 — Printer, ja tööriist, mis annab järele

**Töömaht:** 30 tundi | **Hindamine:** 20 punkti | **Meeskond:** 3 tudengit | **Välja antud:** 11.09.26 | **Tellimise kuupäev:** 22.09.26 | **Esimene kaitsmine:** 06.10.26, veebis

### Kuidas see dokument töötab

* Kopeeri see fail esimesel päeval oma repo laborikausta `README.md`-ks ja täida seal, töö käigus.
* **ANTUD** on see, mida õppejõud teab. **KAARDISTA ISE** on tühi, sest vastust ei tea veel keegi. Sina mõõdad ja kirjutad numbri koos põhjusega siia.
* Midagi ei kustutata. Vale number jääb, kuupäevaga, parandus tuleb tema alla.
* Kirjuta nii, et meeskonnakaaslane, kes sel päeval ruumis ei olnud, saab aru: päris failinimed, päris numbrid, ühikud.
* Tähtaeg ei ole tähtis. Tähtis on, et asi saab tehtud ja sa saad aru. Ei tulnud esimesel korral välja, tule homme tagasi ja proovi uuesti. Kaitsta saab nii mitu korda, kui vaja.

### Eesmärk

Aasta lõpuks paneb MG400 kokku sildi: AtomS3, mille ekraani peale on liimitud polükarbonaatklaas. Iga detail, mis roboti külge kinnitub või elektroonikat hoiab, tuleb selles ruumis printerist välja. See labor räägib sellest printerist ja lõpeb esimese tööriistaga roboti küljes: pastakahoidikuga. Sama meeskond teeb kõiki kolme ainet: sina kirjutad programmi ja sina teed pastaka otsiku. Kolm ainet, üks demo: **vajuta tähte, robot joonistab selle.**

Selles laboris on kolm asja:

1. **Kuup.** 5 × 5 × 5 cm, sees silinder raadiusega 2 cm. Ütleb, kui suur lõtk sellel printeril päriselt on.
2. **Paindlik tükk.** Ütleb, kust ta murdub ja kuhu maani ta plastiliselt paindub.
3. **Pastakahoidik.** Roboti otsa läheb kuulpastakas, seega on ta Z vigade suhtes väga tundlik. Hoidik peab järele andma.

Esimesel päeval uusi osi ei ole. Ehita sellest, mis riiulil on, ja kirjuta puuduv tellimuseks, mis läheb välja 22.09.

*See on elav dokument. Uuenda eesmärke, kui need töö käigus muutuvad — uued teadmised teevad vanad eesmärgid vahel mõttetuks. Mõte on hoida meeskond kogu aeg sihil, et ei eksitaks detailide metsa ja põhiprobleem ei jääks lahendamata.*

**KAARDISTA ISE — eesmärk nii, nagu ta tegelikult välja tuli.**

### Kontrollnimekiri

**Peab olema tehtud**

- [x] Kuup prinditud, lõtk teada (vahemik 0.2–0.4 mm, vt allpool).
- [x] Paindlik tükk prinditud, murdumise koht ja plastilise paindumise piir teada.
- [ ] Pastakahoidik roboti küljes, annab järele. Robot joonistab sellega tähe, mida ESP32 näitab.
- [ ] Repo ja arenduspäevik täidetud, tag `3d-print-lab1`.

**KAARDISTA ISE — kuupäevad ja sinu enda sammud.**

### Sisendid

* Riiulilt: printerid, PLA, nihik, kuulpastakad, marker, maalriteip, paber.
* Vanade asjade kastist, kui see on: eelmise aasta hoidikud, et elu lihtsam oleks. Kui ei ole, ei ole midagi puudu.
* Õppejõult: MG400 baaspakett Pythonis.

### Vahendid

1. Fusion 360, hariduslitsents (aktiveeritakse tunnis)
2. Hoidiku jaoks tarkvara sinu valikul: Fusion, Blender või muu, mis annab STL-i
3. PrusaSlicer, labori printerid, PLA
4. Nihik, kuulpastakas, marker, maalriteip, paber
5. MG400 koos baaspaketiga
6. Git, üks repo meeskonna kohta, `AGENTS.md` juurkaustas

*Kui plaan muutub, uuenda ka vahendeid, või tee draw.io skeem, mis näitab, kuidas asjad omavahel töötavad.*

**KAARDISTA ISE — mida sa päriselt kasutasid.**

### Taustainfo

* **Fusion 360 mudeldamine FDM printimise jaoks**
  [https://www.youtube.com/watch?v=5hComh1hFzY](https://www.youtube.com/watch?v=5hComh1hFzY)
  Või print in place
  [https://www.youtube.com/watch?v=vHHMwpaIrco](https://www.youtube.com/watch?v=vHHMwpaIrco)
* **3D mudelite harjutused**
  Too Tall Toby
  [https://www.tootalltoby.com/](https://www.tootalltoby.com/)
* **3D prinditavad vedrud**
  [https://www.youtube.com/watch?v=wpriGP45Unw](https://www.youtube.com/watch?v=wpriGP45Unw)
  Või print-in-place hinged
  [https://www.youtube.com/watch?v=fYDJLdOV_zE](https://www.youtube.com/watch?v=fYDJLdOV_zE)
* **Prusa**
  Printer: [https://www.prusa3d.com/product/prusa-core-one/](https://www.prusa3d.com/product/prusa-core-one/)
  Slicer: [https://www.prusa3d.com/page/prusaslicer_424/](https://www.prusa3d.com/page/prusaslicer_424/)
* **MG400 mount**
  Fusion360: [https://a360.co/4nruicX](https://a360.co/4nruicX)

*Lisa siia oma allikaid ja kasulikku infot, mis aitaks sul projektist aru saada ka aastaid hiljem, kui selle uuesti lahti teed.*

**KAARDISTA ISE — sinu allikad.**

### Osad

#### 1. Kuup

Fusionis. 5 × 5 × 5 cm, sees silinder raadiusega 2 cm. Lõtk silindri ja seina vahel on parameeter. Kui print võtab liiga kaua aega, tee kuup madalamaks.

Kirjuta üles: mis lõtkuga silinder pöörleb ja mis lõtkuga on kinni sulanud. See number on iga hilisema detaili jaoks.

#### 2. Paindlik tükk

Sinu disain, sinu tarkvara. Prindi ja painuta.

Kirjuta üles: kuhu maani ta paindub ja tuleb tagasi, kust alates jääb plastiliselt kõveraks, kus murdub. Need numbrid lähevad hoidiku vedrutavasse ossa.

#### 3. Pastakahoidik

Tarkvaras, mille ise valid. Toru kuulpastaka jaoks ja kinnitus MG400 flantsi külge. Vedrutav osa nii, et kui õpetatud kõrgus on paar millimeetrit paigast ära, jääb pastakas terveks ja joon on ikka paberil.

Vedrutav osa võtab mõned proovimised. Iga print on uus versioon ja uus fail. Kirjuta iga versiooni juurde, mis muutus ja miks. Pane tähele, kui kaua muudatus tarkvaras võtab: see on koht, kus sa tunned, miks Fusionit kasutada.

Pane hoidik roboti külge. Robot joonistab tähe, mida ESP32 näitab.

**KAARDISTA ISE — vastused.** Iga osa kohta: numbrid, ühikud, kus fail on. Tegemata asja kohta üks rida, miks.

**1. Kuup.** Testis Raimo, tulemus jagatud kogu meeskonnaga (üks ühine tulemus, mitte iga liige eraldi). Printimise kiirendamiseks vähendati kuubi kõrgust 50 mm → **20 mm** (alus jäi 50×50 mm). Testiti kaht lõtku:
- **Lõtk 0.4 mm** — silinder liigub/pöörleb vabalt, ei ole kinni.
- **Lõtk 0.2 mm** — silinder jäi peale printimist kinni; tuli terava tööriistaga kaapida, et leida koht, kust see läbi ei mahtunud. Lõpuks õnnestus silinder ikkagi liikuma saada (väiksema lõtkuga detaili ümbris muutus peale demonteerimist kasutuskõlbmatuks)
- **Tähelepanek:** prinditud silinder ei tulnud täiesti ümmargune — kohati veidi ebatäpne/mitte-ümmargune kuju, mis tõenäoliselt seletab, miks 0.2 mm lõtk osadest kohtadest ei mahtunud, kuigi arvutuslikult oleks pidanud.( seam- ehk koht kus 3D printer alustab ja lõpetab kihi printimist jääb pisut rohkem välja ulatuma, kui ülejäänud kihi serv)
- **Järeldus (lõplik):** meeskond otsustas 0.3 mm versiooni mitte printida ja teema siin sulgeda — selle printeri lõtkeks võtame vahemiku **0.2–0.4 mm** (täpsemat väärtust rohkem ei testita). Hilisemate detailide (paindlik tükk, pastakahoidiku vedrutav osa) puhul arvestame selle vahemikuga.
- **Failid:** minu (Denys) versioon `cube/src/cube-tolerance-v1.f3d` / `cube/stl/cube-tolerance-v1.stl` / `cube/3mf/cube-tolerance-v1.3mf` (50 mm kõrgus, lõtk 0.2 mm). Raimo 20 mm kõrgusega versioonide ekspordid on repos: `cube/stl/Kuubikud_auguga.stl` ja `cube/3mf/kuubikud.3mf`. Nende versioonide lähte-/F3D-faili repos ei ole: TODO.

**2. Paindlik tükk.** Otsustasime paindliku tüki arendamise asemel kasutada pastaka vedru.

**3. Pastakahoidik.** Pastaka hoidiku otsustasime teha kahest 3D prinditud detailist, mis on ühendatud keermeliitega omavahel ja kinnitatud 4 M3 kruviga roboti külge. Detaili disanimisel lähtusime sellest, et arendus protsessis on hea kui asjad on reguleeritavad. Me ei tea kui palju jõudu on vaja, et pastakas kirjutaks ja samal ajal pastaka süsi otsas olev kuul kinni ei kiiluks ja auku paberisse ei kraabiks. Keermeliite abil on võimalik lisada eelpinget vedrule, pastaka süsi saab liikuda kuskil 5mm sissepoole. 2 versiooni kokku panemisel vähendasime sisemise keerme paksus 0.15mm et anda rohkem lõtku keerme kokku keermaisel, kuid sellest ei piisanud ja sisemise keerme lühendamisel saime töötava detaili.

Tähelepanek -- 3D printida sisemisi keermeid on oluliselt raskem, kui välimisi( prinditav materjal võib sisemise keerme puhul hüpata ja põhjustada ebaühtlaseid keermeid). Pastaka süsi enda mõõtmed on suhteliselt väiksed, kuid pastaka süsi hoidiku puhul täpsus pole väga kriitiline, seega võiks lõtk suurem olla.
Järeldus -- pastaka hoidiku disainiimine õnnestus suurepäraselt. Teise versiooniga õnnestus töötav detail kokkupanna. 

### Ohutus

* Printeri otsik on 200–230 °C. Detailid spaatliga, kui laud on jahtunud.
* Robot: käed ei ole laual, kui robot on sisse lülitatud. Esimene jooks aeglaselt, hädastopp käeulatuses.
* Küljelõikurid lõikavad näost eemale.

### Komponendid järgmiseks laboriks

Tellimuse paneb kokku meeskond ise, jagatud Google Sheetis. Tellimus läheb välja 22.09.26.

Mida võib vaja minna: PLA, PETG, M5 poldid ja mutrid (laua augud on 5 mm), M3 kuumsisestused, magnetid. Kirjuta sinna see, mida sul selle labori järgi päriselt puudu jäi.

### Hindamiskriteeriumid

| Kategooria | Punktid |
| :--- | :--- |
| Tööfailid — kuup, paindlik tükk, hoidiku versioonid, STL ja 3MF | 5 p |
| Analüüs — lõtk, paindumise ja murdumise numbrid | 5 p |
| Prototüüp — hoidik roboti küljes annab järele, robot joonistab tähe, mida ESP32 näitab | 5 p |
| Dokumentatsioon — README, arenduspäevik, AGENTS.md | 5 p |
| **Kokku** | **20 p** |

### Kaitsmine

Link git repole, tag `3d-print-lab1`.

Kaitsmine on lihtne suuline 15 minuti jutuajamine. Näitad, kuidas robot joonistab tähte, mida ESP32 näitab, ja avad oma arenduspäeviku. Õppejõud küsib umbes viis küsimust selle kohta, kuidas sa selle tegid. Kui esimesel korral ei õnnestu, tuled uuesti.

Repos on kaustas `3d-print/lab1/`: lähtefailid, STL ja `.3mf` iga prindi kohta, see fail kui `README.md`, ja `AGENTS.md` uuendatud.

### Arenduspäevik

**KAARDISTA ISE — päevik.** Üks sissekanne iga töösessiooni kohta, kirjutatud iseendale, nii et inimene, kes seal ei olnud, saab aru. Sissekandeid lisatakse, mitte ei muudeta.

**11.09.26 — Denys, Nikita, Raimo**
* Tegime: Esimene loeng — tutvusime, õppejõud selgitas, mis aine see on ja mida õpime. Näidati näidisena väikest seadet, mida me selle aasta jooksul ehitada suudame. Anti esimene laboratoorne töö (see, Lab 1). Pärast loengut seadsin üles töökeskkonna: GitHub repo (`3d-printing-course`), meili, Claude (AI) abilise, logisin sisse Fusion 360-sse. Lugesin läbi juhendi — esimesel lugemisel ei saanud kohe aru, mida täpselt teha tuleb. Pärast ettevalmistust alustasin koos AI abilisega Fusionis: eskiis, ekstrusioon, tegin kuubi, siis auk (silinder) kuubi sees — sain aru, kuidas neid samme teha. Tegin kuubi + eraldi silindri (vahega 0.2 mm) samasse auku, salvestasin kõik versioonid (`.f3d`, `.stl`, `.3mf`), kontrollisin PrusaSlicer'is, et kaks keha on eraldi objektid, ja saatsin printima.
* Juhtus (numbrid): kuup 50×50×50 mm, auk/silinder ⌀40 mm, esimene testitav vahe (gap) = 0.2 mm. Printimise tulemus (kas silinder keerleb või on kinni sulanud) on veel teadmata — selgub pärast printi.
* Otsustasime, ja miks: alustasime vahega 0.2 mm kesksest väärtusest, et esimese prindi järgi otsustada, kas järgmisena proovida väiksemat või suuremat vahet.
* Lahti järgmiseks korraks: oodata prindi tulemust, mõõta/katsetada, kas 0.2 mm vahe keerleb vabalt või on kinni; kirjutada tulemus siia juurde; vajadusel teha uus versioon (v2) teise vahega.

**11.09.26 (jätk) — Raimo tegi prindi- ja lõtketesti, tulemus ühine kogu meeskonnale**
* Tegime: Raimo printis kuubi kiiremini, vähendades kõrgust 50 mm → 20 mm (alus 50×50 mm samaks jäi). Testis kaht lõtku: 0.4 mm ja 0.2 mm. 0.4 mm juures liigub silinder vabalt. 0.2 mm juures jäi silinder kinni — tuli terava tööriistaga kaapida, et leida koht, kust läbi ei mahtunud; lõpuks õnnestus paika saada, aga detail kahjustus kergelt selle käigus.
* Juhtus (numbrid): kõrgus 20 mm, lõtk 0.4 mm → vaba pöörlemine; lõtk 0.2 mm → kinni, vajas jõudu/kaapimist. Lisaks: prinditud silinder ei tulnud täiesti ümmargune (kohati veidi ebatäpne kuju) — see selgitab osaliselt, miks 0.2 mm kohati üldse kinni kiilus.
* Otsustasime, ja miks: reaalne lõtke piir jääb 0.2–0.4 mm vahele; järgmisena proovime vahepealset väärtust (nt 0.3 mm), et piiri täpsemalt paika panna.
* Lahti järgmiseks korraks: lisada Raimo failid (f3d/stl/3mf) reposse, kui ta on GitHubis kaastöötajana lisatud; alustada paindliku tükiga.

**11.09.26 (jätk 2) — otsus: kuubi teema suletud**
* Tegime: arutasime, kas printida ka lõtkuga ~0.3 mm täpsema piiri jaoks.
* Otsustasime, ja miks: ei prindi 0.3 mm versiooni, sulgeme kuubi teema praeguse tulemusega (lõtk 0.2–0.4 mm vahemikus). Ajapiirang / soov edasi liikuda järgmiste osade juurde.
* Lahti järgmiseks korraks: alustada paindliku tükiga (osa 2).

**12.09.26 — pastakahoidiku katse MG400-l**
* Tegime: paigaldasime pastakahoidiku MG400 roboti külge ja kontrollisime kinnitust ning vedru tööd.
* Juhtus (vaatlus): pastakahoidik püsib roboti küljes kindlalt. Hoidiku sisemine vedru töötab Z-suunas korrektselt ja pehmendab kontakti paberiga nii, et pastakas ei suru paberilehte läbi.
* Otsustasime, ja miks: kinnitus ja Z-suunaline vedrumehhanism töötavad ettenähtud viisil. Kogu prototüübi kriteeriumi ei märgi veel täidetuks, sest praegu saab robotiga joonistada ainult käsitsi juhituna ehk käsirežiimis; ESP32 näidatava tähe automaatset joonistamist ei ole veel saavutatud.
* Lahti järgmiseks korraks: ühendada roboti joonistamine ESP32 juhtimisega ja katsetada automaatset tähe joonistamist.

**13.09.26 — paindliku tüki paksusekatse**
* Tegime: modelleerisime Fusion 360-s parameetrilise paindekatsekeha ning printisime sama geomeetriaga kolm varianti. Ainus muudetud parameeter oli paksus: `1,2 mm`, `1,5 mm` ja `2,0 mm`. Katsekehad prinditi ühe partiina samade printimisseadetega. Katsetamisel fikseeriti üks ots ning vaba otsa painutati järk-järgult; pärast iga sammu kontrolliti, kas detail taastub või jääb püsivalt deformeerunuks.
* Juhtus (numbrid):

  | Paksus | Suurim kõrvalekalle, mille järel detail taastus | Püsiv deformatsioon algas | Murdumine | Murdumiskoht |
  |---|---:|---:|---|---|
  | `1,2 mm` | `50 mm` | `60 mm` | Tavalisel painutamisel ei murdunud; detaili sai täielikult kokku painutada nii, et otsad puutusid kokku, kui painutada mõlemas suunas | keskelt |
  | `1,5 mm` | `40 mm` | `50 mm` | Tavalisel painutamisel ei murdunud; detaili sai täielikult kokku painutada nii, et otsad puutusid kokku, kui painutada mõlemas suunas | keskelt |
  | `2,0 mm` | `20 mm` | `25 mm` | Murdus ligikaudu `330°` painutuse juures | keskelt |

* Tähelepanek: õhemad katsekehad talusid suuremat läbipainet enne püsiva deformatsiooni tekkimist. `2,0 mm` variant oli jäigem ning murdus suure painutuse korral. Kõigi variantide suurim deformatsioon või murdumine toimus keskmises kitsamas tsoonis, nagu mudeli geomeetriaga ette nähtud.
* Otsustasime, ja miks: paindliku tüki ülesande jaoks on nüüd olemas reaalsed paindumise, püsiva deformatsiooni ja murdumise tulemused. Pastakahoidiku lõplikus mehhanismis jääme siiski metallist kuulpastaka vedru juurde, sest see lahendus on MG400-l juba töötanud ja võimaldab Z-suunalist järeleandmist.
* Failid:
  - `flex-piece/stl/flex-piece-1.2mm.stl`
  - `flex-piece/stl/flex-piece-1.5mm.stl`
  - `flex-piece/stl/flex-piece-2.0mm.stl`
  - `flex-piece/3mf/flex-piece-thickness-test.3mf`
* Lahti järgmiseks korraks: jätkata ESP32 ja MG400 automaatse tähe joonistamise ühendamisega ning lisada puuduvad pastakahoidiku ja kuubi tööfailid, kui need on meeskonnakaaslase arvutist kättesaadavad.

### Väljundid ja tulemused

**Väljundid**
* Nutikad Lahendused L1: pastakahoidik, mis demopäeval tähe joonistab.
* 3D printimine L2, L3, L4: lõtk ja paindumise numbrid iga hilisema detaili jaoks.

**KAARDISTA ISE, lõpus.**
* Git repo ja tag:
* Numbrid, mille see labor andis, ühikutega:
* Mida me teeksime teisiti:
* Mida järgmine labor peaks enne alustamist teadma:

### Tagasiside
