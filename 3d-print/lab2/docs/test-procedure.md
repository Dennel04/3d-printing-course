# Lab 2 katseprotseduur roboti juures

Kõik mõõtmata tulemused ja katsed on olekus `TODO — waiting for physical test`. Enne katseid ava ka [`MG 400 rakis.md`](MG%20400%20rakis.md), [`measurements.md`](measurements.md) ja [`refit_test.csv`](refit_test.csv).

## A. Gridfinity kalibreerimine

1. Keela robot ja paigalda 1 × 1 kalibreerimishoidik ruutu `B-2`; kontrolli, et hoidik istub täielikult põhjas.
2. Luba robot ning vii tööriista tipp väikese kiirusega hoidiku keskpunkti.
3. Kirjuta roboti X/Y/Z koordinaadid faili `measurements.md`.
4. Arvuta sama ruudu koordinaadid ametliku lauavalemiga. Arvuta nihe: mõõdetud koordinaat miinus arvutatud koordinaat.
5. Rakenda sama nihet kaugele kontrollruudule, näiteks `E+3`, ja mõõda tegelik viga.
6. Kui viga on üle `1 mm`, kontrolli telgede suunda, pöördenurka ja võimalikku telgede vahetust; ära kohanda hoidikut oletuse põhjal.
7. Määra Z üks kord ruudustiku pealispinna suhtes ja kirjuta mõõteviis üles.

## B. Hoidiku sobivuskatse

1. Kontrolli, et hoidiku Gridfinity jalg istub täielikult ruudustikus.
2. Kontrolli ja dokumenteeri loks.
3. Kontrolli, et inimene saab detaili ohutult sisestada ja eemaldada.
4. Kontrolli sissejuhtivat kaldserva või faasi.
5. Kontrolli, et iminapp pääseb detailile vertikaalselt ligi ja miski ei ulatu liikumisteele.

## C. Klaasi teisalduskatse

1. Lae sisendhoidikusse neli klaasi.
2. Paigalda töökoha hoidikusse Atomi mannekeen.
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

1. Kinnita kaamera olemasoleva iminapa kõrvale.
2. Kontrolli, et iminapa vertikaalne tee ja hoidikutesse laskumine on vabad.
3. Kontrolli, et kaadris on töökoht ning USB-C pesa jääb ligipääsetavaks.
4. Sõida väikese kiirusega läbi kogu kavandatud käe liikumine ja J4 pöördevahemik.
5. Kontrolli, et kaabel ei jää käe ega hoidikute taha kinni ja tõmbetõke töötab.
6. Kirjuta valitud toide, pinge, vool ja põhjendus faili `measurements.md`.
7. Ära ühenda midagi roboti tööriistatoitesse enne pinge mõõtmist ja õppejõu kontrolli.

## G. Üldvaatekaamera katse

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
