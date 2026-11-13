# Lab 2 katseprotseduur roboti juures

Kõik mõõtmata tulemused ja katsed on olekus `TODO — waiting for physical test`. Enne katseid ava ka [`MG 400 rakis.md`](MG%20400%20rakis.md), [`measurements.md`](measurements.md) ja [`refit_test.csv`](refit_test.csv).

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

23.10.2026 lähteandmete parandus: kasuta meie **30 × 30 × 2 mm** klaasi (`confirmed`, Maksimi Excel `Measurements!D8:E19` ja meeskonna kinnitus). Ametliku ülesande 24 × 24 × 2 mm on säilitatud ajalooline nominaal. Enne uue trajektoori kasutamist läbi [`CAD-i kontrollülesanded`](cad-measurement-review.md): kõik neli pesa, klaasi üleulatus ja pöörded, iminapa ligipääs, töökoht, neli väljundpunkti ja praak. Uusi sihtpunkte ei tuletata üksnes USB-C 11,4 mm mõõdust. Katsetulemus: `TODO — waiting for physical test`.

1. Lae sisendhoidikusse neli klaasi.
2. Paigalda töökoha hoidikusse Atomi mannekeen.
   - 23.10.26: mannekeeni asemel kasutame päris AtomS3-t (ekraan üleval).
3. Õpeta vajalikud võtmise ja asetamise punktid.
4. Teisalda iga klaas järjest: `sisend → töökoht → heade väljund`.
5. Ära sekku käsitsi nelja klaasi vahel.
6. Kirjuta iga ebaõnnestumine nähtava põhjusega üles; ära peida ebaõnnestunud katseid.

## D. Eemaldamise ja tagasipaneku katse

1. Keela robot, eemalda hoidikud ja paigalda need tagasi samadesse ruutudesse.
2. Ära muuda õpetatud punkte.
3. Lae neli klaasi uuesti.
4. Tee viis ringi, igas neli klaasi: kokku `5 × 4 = 20` läbimist.
5. Märgi iga etapp eraldi faili `refit_test.csv`: sisendist võtmine, töökohale asetamine, töökohalt võtmine ja väljundisse asetamine.
6. Kirjuta kõik vead ja ebaõnnestumised märkuste veergu.

## E. 42 mm ümberpaigutuskatse

1. Keela robot ja tõsta hoidik teise Gridfinity ruutu.
2. Tuleta uus sihtpunkt algsest õpetatud punktist, liites vastaval teljel ruutude täisarvu × `42 mm`.
3. Tee katse väikese kiirusega.
4. Kirjuta üles, kas arvutatud punkt töötas. Kui ei töötanud, mõõda ja kirjuta tegelik X/Y/Z viga millimeetrites.

## F. Tööriistakaamera katse

23.10.2026 arhitektuur: XIAO USB Serial diagnostika on kontrollitud COM5 kaudu (OV3660, JPEG 1600 × 1200 px, [`tegelik foto`](photos/tool-camera-first-frame.jpg)). Lõppvariandi Wi-Fi HTTP püsivara asub [Smart Solutionsi repos](https://github.com/Dennel04/smart-solutions-course/tree/main/smart-solutions/lab2/firmware-xiao-camera/); siinset USB-püsivara säilitatakse diagnostikaks. Enne lõppvariandi vastuvõtmist kontrolli Wi-Fi HTTP pilti tegelikult XIAO-lt station PC-sse ning salvesta terav töökoha kaader terve 30 × 30 mm klaasi ja Atomiga. Seejärel kontrolli allolevate sammudega toidet, kaablimarsruuti, tõmbetõket ning MG400 kogu kavandatud liikumisvahemikku ja J4 pööret. Kõik need lõppvariandi füüsilised kontrollid: `TODO — waiting for physical test`.

1. Kinnita kaamera olemasoleva iminapa kõrvale.
2. Kontrolli, et iminapa vertikaalne tee ja hoidikutesse laskumine on vabad.
3. Kontrolli, et kaadris on töökoht ning USB-C pesa jääb ligipääsetavaks.
4. Sõida väikese kiirusega läbi kogu kavandatud käe liikumine ja J4 pöördevahemik.
5. Kontrolli, et kaabel ei jää käe ega hoidikute taha kinni ja tõmbetõke töötab.
6. Kirjuta valitud toide, pinge, vool ja põhjendus faili `measurements.md`.
7. Ära ühenda midagi roboti tööriistatoitesse enne pinge mõõtmist ja õppejõu kontrolli.

## G. Üldvaatekaamera katse

Valitud üldvaatekaamera on Verbatim AWC-03, ühendus USB kaudu station PC-ga. MG400 saab käsud Etherneti kaudu; Atom kasutab USB Serialit ja Wi-Fi-t. Need ühendused ei asenda allolevaid kaamera- ja liikumiskatseid.

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
