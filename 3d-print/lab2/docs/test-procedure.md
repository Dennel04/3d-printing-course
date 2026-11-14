# Lab 2 katseprotseduur roboti juures

Kõik mõõtmata tulemused ja katsed on olekus `TODO — waiting for physical test`. Enne katseid ava ka [`MG 400 rakis.md`](MG%20400%20rakis.md), [`measurements.md`](measurements.md) ja [`refit_test.csv`](refit_test.csv).

**Lõppseis:** 24.10 ring 1 andis varasemas paigutuses 4/4. 13.11 andsid lõpppaigutuses ringid 2 ja 3 mõlemad 4/4; ring 3 järgnes kolme hoidiku eemaldamisele ja samadesse ruutudesse tagasipanekule, punkte ümber õpetamata. Meeskond lõpetas CAD-etapi 12/12 füüsilise ülekandega. Ringe 4–5 ja 42 mm füüsilist ümberpaigutuskatset ei tehtud. Allpool kirjeldatud [ametliku ülesande](../assignment-EST.md) täielik katsemaht jääb seega täitmata.

## A. Gridfinity kalibreerimine

Ruudustik on lükatud roboti platvormi (pesa) vastu. Kõik punktid R 33 juures.

### A1. Kahe kauge ruudu meetod

1. Keela robot ja pane 1 × 1 kalibreerimiskast `gridfinity-calibration` kaugesse ruutu `F-2`; kontrolli, et kast istub täielikult põhjas. (`B-2` ei sobi: napp ei ulatu seal kasti põhja, J3 piir.)
2. Luba robot, vii napp väikese kiirusega kasti kohale ja sea see silmaga pesa keskele (risti kohale).
3. Lase napp aeglaselt kasti põhjani (puudutus). Kirjuta X/Y/Z faili [`calibration.csv`](calibration.csv).
4. Korda teises kauges ruudus `C+4` — kaks kaugel asuvat punkti annavad ruudustiku pöörde.
5. Lisa punktid `calibration/cells.py`-sse (`MEASURED`); sobitus arvutab pöörde ja nihke. Kontrolli, et mõõdetud ja CAD-i kauguse vahe on alla 1 mm.
6. Kontroll kolmandas ruudus (nt `D+3`): slot picker viib napa arvutatud keskpunkti, napp peab olema pesa keskel.

## B. Hoidiku sobivuskatse

1. Kontrolli, et hoidiku Gridfinity jalg istub täielikult ruudustikus.
2. Kontrolli ja dokumenteeri loks.
3. Kontrolli, et inimene saab detaili ohutult sisestada ja eemaldada.
4. Kontrolli sissejuhtivat kaldserva või faasi.
5. Kontrolli, et iminapp pääseb detailile vertikaalselt ligi ja miski ei ulatu liikumisteele.

## C. Klaasi teisalduskatse

Lõppseisu klaas on **30 × 30 × 1,2 mm** (Denysi 13.11 nihikumõõt). 23.10 kinnitatud 30 × 30 × 2 mm jääb [mõõteregistrisse](measurements.md) varasema Exceli lähteväärtusena. Enne uue trajektoori kasutamist läbi [CAD-i kontrollülesanded](cad-measurement-review.md). Tehtud klaasitsüklite tulemused on [katsetabelis](refit_test.csv).

1. Lae sisendhoidikusse neli klaasi.
2. Paigalda töökoha hoidikusse Atomi mannekeen.
   - 23.10.26: mannekeeni asemel kasutame päris AtomS3-t (ekraan üleval).
3. Õpeta vajalikud võtmise ja asetamise punktid.
4. Teisalda iga klaas järjest: `sisend → töökoht → heade väljund`.
5. Ära sekku käsitsi nelja klaasi vahel.
6. Kirjuta iga ebaõnnestumine nähtava põhjusega üles; ära peida ebaõnnestunud katseid.

## D. Eemaldamise ja tagasipaneku katse

13.11 ring 3 läbis selle kontrolli ühe korduspaigalduse järel. Allpool on täieliku protokolli juhis; ringe 4–5 ei tehtud.

1. Keela robot, eemalda hoidikud ja paigalda need tagasi samadesse ruutudesse.
2. Ära muuda õpetatud punkte.
3. Lae neli klaasi uuesti.
4. Tee viis ringi, igas neli klaasi: kokku `5 × 4 = 20` läbimist.
5. Märgi iga etapp eraldi faili `refit_test.csv`: sisendist võtmine, töökohale asetamine, töökohalt võtmine ja väljundisse asetamine.
6. Kirjuta kõik vead ja ebaõnnestumised märkuste veergu.

## E. 42 mm ümberpaigutuskatse

Seda katset ei tehtud füüsiliselt. Hoidikute tagasipanek samadesse ruutudesse ringiks 3 on eraldi kontroll.

1. Keela robot ja tõsta hoidik teise Gridfinity ruutu.
2. Tuleta uus sihtpunkt algsest õpetatud punktist, liites vastaval teljel ruutude täisarvu × `42 mm`.
3. Tee katse väikese kiirusega.
4. Kirjuta üles, kas arvutatud punkt töötas. Kui ei töötanud, mõõda ja kirjuta tegelik X/Y/Z viga millimeetrites.

## F. Tööriistakaamera katse

CAD-etapis paigaldati XIAO kinnitus ja saadi USB kaudu [töökoha kaader](photos/tool-camera-workstation-2026-10-24.jpg). [Wi-Fi HTTP püsivara](https://github.com/Dennel04/smart-solutions-course/tree/main/smart-solutions/lab2/firmware-xiao-camera/), mõlema kaamera lõplik Stationi integratsioon, FPS-i, viite ja võrguliikluse mõõtmine ning toite, kaablite ja liikumisulatuse täielik kontroll jäävad Smart Solutionsi jätkutööks.

1. Kinnita kaamera olemasoleva iminapa kõrvale.
2. Kontrolli, et iminapa vertikaalne tee ja hoidikutesse laskumine on vabad.
3. Kontrolli, et kaadris on töökoht ning USB-C pesa jääb ligipääsetavaks.
4. Sõida väikese kiirusega läbi kogu kavandatud käe liikumine ja J4 pöördevahemik.
5. Kontrolli, et kaabel ei jää käe ega hoidikute taha kinni ja tõmbetõke töötab.
6. Kirjuta valitud toide, pinge, vool ja põhjendus faili `measurements.md`.
7. Ära ühenda midagi roboti tööriistatoitesse enne pinge mõõtmist ja õppejõu kontrolli.

## G. Üldvaatekaamera katse

Verbatim AWC-03 on postil ja ühendatud USB kaudu. [25.10 kaadris](photos/veebikaamera-kaader-2026-10-25.jpg) on ruudustik, hoidikud ja robot. Allpool jäävad avatuks liikumisvaru, kaabli, vibratsiooni ja kaamera korduspaigalduse kontrollid.

1. Paiguta kaamera kõrgemale roboti mõõdetud maksimaalsest trajektoorist.
2. Kontrolli, et kogu ruudustik ja robot on kaadris.
3. Tee väikese kiirusega kokkupõrkekontroll kaamerapostile lähimas asendis.
4. Kinnita USB-kaabel nii, et see ei ripu üle tööala.
5. Mõõda pildi vibratsioon roboti liikumise ajal pikslites või millimeetrites laua pinnal.
6. Eemalda kinnitus, paigalda see tagasi ning mõõda pildi kordustäpsus.

## Ohutusmeeldetuletused

- Roboti alus, süvend ja 20° kaldsein peavad jääma täiesti vabaks.
- Hoidikuid tõsta ja laadida ainult siis, kui robot on keelatud; enne iga jooksu kontrolli, et hoidikud istuvad põhjas.
- Kui robot on sisse lülitatud, hoia käed laualt eemal. Esimene jooks tee aeglaselt, hädastopp käeulatuses.
- Uue hoidiku esimene tõstmine tee `20%` kiirusel ja iminapaga `20 mm` kõrgemal, õhus.
- Kontrolli kaameraposti ja kaablite kokkupõrkeid väikese kiirusega; liikuval kaablil peab olema tõmbetõke.
- Roboti tööriistatoidet kasuta alles pärast pinge mõõtmist ja õppejõu kontrolli.
- Printeri otsik on `200–230 °C`; eemalda jahtunud detail spaatliga. Küljelõikuritega lõika näost eemale.
