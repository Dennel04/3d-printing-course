# 23.10.2026 — komponentide mõõtude mõju Lab 2 CAD-ile

Lähteandmed ja olekud: [`measurements.md`](measurements.md), Maksimi `Measurements.xlsx` ning meeskonna kinnitus. Füüsiline klaas on **30 × 30 × 2 mm** (`confirmed`), AtomS3 **24 × 24 × 12,9 mm** (`nominal`). Geomeetriat ei muudetud. Allpool olevad STL-mõõdud on eksporditud võrgu analüüs, mitte prinditud detaili mõõtmine ega Fusioni parameetrite kinnitus.

## Olemasolevate failide kontroll

STL-i binaarsete kolmnurkade tipud ja telgedega paralleelsed tasapinnad loeti millimeetrites; lähtecommit `acd3d5c`. Mudeli kohalik Z ei ole roboti Z. F3D parameetreid ega 3MF-i vastavust ei ole Fusionis / PrusaSliceris kontrollitud.

| Mudel ja allikas | Kontrollitud CAD-geomeetria | Mõju ja vajalik tegevus |
|---|---|---|
| `glass-input-holder/stl/glass-input-holder.stl` | Väljast 83,5 × 83,5 mm. Klaasipesade sirgseinad X/Y = −36,3 / −5,7 ja +5,7 / +36,3 mm: vahe 30,6 mm, keskmed ±21 mm. Pesa põhi kohalikul Z = 4 mm, ülaserv Z = 5,5 mm. Z = −4,75…5,5 mm (standardne Gridfinity jalg). | Need pole 24 mm klaasipesad. 30 mm klaasi arvutuslik täislaiuse varu 0,6 mm ehk 0,3 mm külje kohta; füüsilist lõtku pole mõõdetud. 2 mm klaas ulatuks nimetatud põrandast 0,5 mm ülaservast kõrgemale. Kontrollida nurkade kuju, sissejuhtimist, klaasi tegelikku suurust, kõiki nelja pesa ja iminapa ligipääsu. |
| `valjundhoidik/stl/valjundhoidik-v1.stl` | Välismõõt 83,2 × 83,2 mm, Z = −4,65…16,5 mm: kogukõrgus 21,15 mm. Sirged siseseinad X/Y = ±39,1 mm: 78,2 × 78,2 mm. Põhi Z = 2,5 mm, sügavus ülaservani 14 mm. | Varasem kogukõrgus 24,15 mm kirjeldab pikemate jalgade seisu; praegune STL on 21,15 mm kõrge. Neli 30 mm klaasi vajavad pööramata 2 × 2 paigutuses vähemalt 60 × 60 mm, lisaks vahed; sirgete seinte järgi jääb kokku 18,2 mm varu kummalgi teljel. See ei tõenda mahtumist ümardatud nurkades ega robotiga asetamist. Määrata neli sihtpunkti, servade/klaaside vahed ja pöördevahemik. Kontrollida F3D/STL/3MF omavahelist vastavust. |
| `ready-parts-input-holder` — aku sisend, töökoht ja eraldi praagi koht vastavalt varasemale otsusele | Aku lähteväärtus 24,04 × 24,01 × 21,97 mm (`measured`), AtomS3 24 × 24 × 12,9 mm (`nominal`). Pesade mõõdud ja koostu tegelik kõrgus pole selles ülevaates kinnitatud. | 30 mm klaas ulatub keskse 24 mm Atomi gabariidist 3 mm külje kohta üle; kontrollida hoidiku seinu, naaberpesasid ja valmis koostu eemaldamist. Aku kontaktid üles, Atom ekraan üles (`planned`). Aku + Atom + klaas annaks lihtsa kõrguste summana 36,87 mm; see pole koostu mõõt, sest ühenduse kattuvus ja sisestussügavus on teadmata. Kasutada trajektoori jaoks mõõdetud koostu, mitte seda summat. Praagi sihtkoht vajab eraldi kinnitamist. |
| `atoms3-input-holder` | AtomS3 füüsilised gabariidid endiselt mõõtmata; Exceli 24 × 24 × 12,9 mm on nimimõõt. | Kontrollida pesa füüsilist lõtku ja orientatsiooni. USB-C keskjoone 11,4 mm lähteserv tuleb fotol või skeemil määrata enne avause või sihtpunkti kasutamist. |
| `camera-mounts/.../xiao-square-mount-v1` | XIAO põhiplaat 17,74 × 21,33 × 1,21 mm (`measured`); kaameralaiendus, objektiivi asukoht ja antenni vaba ala puuduvad. | Võrrelda põhiplaadi renne mõõduga, jättes komponentidele ja USB-C-le ruumi. 1,21 mm on põhiplaadi mõõt, mitte kaamerakoostu kogukõrgus. Ligikaudne 90° alla on `planned`. Uus kaamerapesa vajab kaameraplaadi mõõtmisi; olemasolev pilt ei tõenda 30 × 30 mm klaasi täielikku nähtavust. |

Kõigi ülaltoodud füüsiliste sobivus- ja trajektoorikontrollide tulemus: `TODO — waiting for physical test`.

## 24.10.2026 — uus füüsiline tõend ja olemasolevate failide kontroll

Eelnev tabel ja allpool olevad kontrollülesanded kirjeldavad 23.10 ülevaadet. **24.10 täiendus:** kasutaja kinnitas aku, AtomS3 ja klaasi sobivuse vastavates prinditud sisendhoidikutes: detailid jõuavad põhjani, liiguvad lõtku piires vabalt, tulevad sõrmedega välja ega kiilunud. See täpsustab varasemat üldist sobivuse TODO-d ainult kontrollitud ulatuses. Täielik tulemus, allikas ja piirangud on [`measurements.md` 24.10 kirjes](measurements.md); kontrollitud pesade arvu ja klaasihoidiku versiooni ei täpsustatud. Prinditud pesade arvulised nihikumõõdud ja lõtk (mm) on endiselt `TODO — waiting for physical test`.

Kontrollitud repo seisus `36d6bc5` olemasolevaid lähtefaile `ready-parts-input-holder/src/ready-parts-input-holder-v1.f3d`, `atoms3-input-holder/src/atoms3-input-holder-v1.f3d` ning `glass-input-holder/src/glass-input-holder.f3d`: failid ja Fusioni arhiivikirjed on olemas. Kasutatud ZIP-lugeja ei toeta nende Zstandard-pakkimist (meetod 93), seega Fusioni parameetrite, lähtegeomeetria ja STL-iga vastavuse täielikku kontrolli ei kinnitata. Uusi mudeleid ei loodud ja olemasolevaid faile ei muudetud.

Vastavate olemasolevate binaarsete STL-ide tipud ja tasapinnad kontrolliti uuesti. **CAD dimensions**, mitte prinditud pesa mõõtmised:

| STL `stl/` alamkaustas | Pesa sirgseinte vahe X × Y | Põhi / ülaserv kohalikus Z-s | Arvutuslik sügavus |
|---|---|---|---|
| `ready-parts-input-holder-v1.stl` | 24,6 × 24,6 mm | 3 / 31 mm | 28 mm |
| `atoms3-input-holder-v1.stl` | 24,6 × 24,6 mm | 3 / 11 mm | 8 mm |
| `glass-input-holder.stl` | 30,6 × 30,6 mm | 4 / 5,5 mm | 1,5 mm |

Eraldi kummist iminapa D41 ja H1 on nüüd nihikuga mõõdetud (`measured`), kuid selle samasus robotil oleva eksemplariga pole kinnitatud. Seetõttu jäävad paigaldatud tööriista gabariitide, tihenduspinna ja liikumistee kontrollid avatuks. Kaalu puudumisel antud tööriista massihinnang on `estimated, not measured`; tegelik kaalumine enne/pärast kaamerat jääb TODO-ks. Kvalitatiivne pesasobivus ei kinnita kõigi pesade robotiga ligipääsu, Gridfinity jalgade kordustäpsust ega kogu tsükli tulemust. Varasemad katsed ja ebaõnnestumised jäävad alles.

## MG400 haaramise ja trajektoori kontroll

- Klaas suureneb varasema vale lähteväärtusega võrreldes 6 mm kummalgi teljel; keskse haarde korral ulatub serv 3 mm kaugemale. Pööratud 30 mm ruudu suurim teljesuunaline ulatus on `30 × √2 ≈ 42,43 mm` ehk poolulatus 21,21 mm; 24 mm ruudu puhul oli see 16,97 mm. Neid arvutuslikke ümbriseid tuleb võrrelda seina, naaberdetaili, kaabli, kaamerakinnituse ja transporditeega.
- Sama keskme korral ei tulene mõõduparandusest automaatselt uut X/Y sihtpunkti. Servapõhise referentsi korral võib keskpunkt muutuda 3 mm telje kohta; suund ja nullpunkt tuleb esmalt kinnitada. USB-C 11,4 mm ei ole haardekeskme koordinaat.
- Kontrollida kõigi nelja sisendpesa tegelik põrandakõrgus ja istumine. V2 jala alumise Z muutus STL-is on 3 mm; sellest ei saa ilma laua ja hoidiku mõõtmiseta järeldada roboti võtukõrguse muutust. Klaasi paksus jääb kinnitatud 2 mm, kuid see ei kinnita Z-sihtpunkti.
- Iminapa läbimõõt, tihenduspind ja kogu tööriista gabariidid tuleb füüsiliselt mõõta. G-1 kalibreerimisel saadud ligikaudne efektiivne Ø22 mm pole iminapa mõõteprotokoll ega vaakumhaarde tõend. Kontrollida keskset haaret, klaasi püsimist ja tööriista vertikaalset ligipääsu.
- Lõpetada G-1 neljas nurk, korrata eri Z-l mõõdetud nurk ja kontrollruut. Praegust ligikaudset kalibreerimisnihet ei loeta kinnitatud teisenduseks. Seejärel kontrollida võtmine, tõstmine, transport, töökoht, väljund ja praak koos 30 mm klaasi ning vajaduse korral kogu koostuga.
- Katsetada [`test-procedure.md`](test-procedure.md) ohutusreeglite järgi: hoidikute laadimisel robot keelatud, käed töötamise ajal eemal, esimene uus trajektoor aeglaselt ja hädastopp käeulatuses. Uue hoidiku esimene õhusõit 20% kiirusel ja 20 mm kõrgemal vastavalt olemasolevale juhendile. Katsetulemus: `TODO — waiting for physical test`.

## Fusion 360 kontrollülesanded enne võimalikku ümbertegemist

1. Ava vastav versioonitud `.f3d`: **File → Open → Open from my computer**. Vali millimeetrid (**Browser → Document Settings → Units → Change Active Units → Millimeter**).
2. Ava **Design → Solid → Modify → Change Parameters**. Kontrolli, kas detaili X/Y/Z, pesa lõtk külje kohta ja põranda kõrgus on **User Parameters**. Planeeritud klaasi lähteparameetrid on 30 mm, 30 mm, 2 mm; ära nimeta 0,3 mm arvutuslikku külgvaru mõõdetud sobivuseks.
3. Vali **Inspect → Measure**, mõõda vastasseinad, põrand–serv, faasid ja nurgad kõigis neljas pesas ning kontrolli vastavust ülalolevale STL-ile. Kasuta **Inspect → Section Analysis** istumissügavuse ja klaasi üleulatuse kontrolliks.
4. Lisa eraldi kontrollkomponendina 30 × 30 × 2 mm klaasi ümbris ning mõõdetud või selgelt nimimõõduga komponendid. Paiguta need kavandatud asenditesse; kasuta **Inspect → Interference**. Kontrolli eraldi lubatud klaasipöördeid ja kogu transporditeed; ühe staatilise asendi nullinterferents ei kinnita trajektoori.
5. Kui klaas nurka ei mahu, lõtk ei sobi või sein jääb haardeteele, pane kirja konkreetne vastuolu ja parameetrimuutus. Alles kontrolli järel loo uus versioon **File → Save As**; ära kirjuta prinditud iteratsiooni üle. Ekspordi uue versiooni STL ning salvesta vastav PrusaSliceri 3MF. Praeguses sessioonis ei muudetud geomeetriat ega loodud printi.
