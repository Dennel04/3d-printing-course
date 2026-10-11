# Labori 3 esimese füüsilise töökorra katsejuhend

Kasuta seda järjekorras. Mõõda enne CAD-i alustamist. Kõik tegelikud tulemused
kirjuta kohe vastavasse faili; ebaõnnestunud katseid ei kustutata ega peideta.

## A. Inventuur ja füüsilised mõõtmised

1. Kontrolli olemasolu: 3/2 klapp, liitmikud, 4 mm voolik, süstal/süstlad,
   otsik/otsikud, 405 nm UV LED koos jahutusradiaatoriga, draiver, iminapp,
   kaamera, vajalikud kruvid/mutrid/seibid, kaal, nihik ja printer.
2. Anna igale kasutatavale süstlale ja otsikule ID.
3. Täida `measurements.md`: mõõda nihikuga, kaalu kavandatud komplektid ja
   fotografeeri vajaduse korral mõõtmise nullpunkt.
4. Märgi puuduv `bom.md` faili. Ära vali CAD-i lõppmõõte enne mõõtmist.

## B. Mutritasku katse

1. Mõõda tegelik mutter ja polt.
2. Tee ainult väike nummerdatud prooviklots.
3. Slice'i mudel ning lisa selgelt kontrollitud paus õigel kihil.
4. Prindi prooviklots.
5. Pausi ajal järgi printeri ohutusjuhiseid: hoia käed kuumast otsikust ja
   alusplaadist eemal ning sisesta mutter pintsettidega ilma prindipead
   nihutamata.
6. Jätka printi.
7. Kontrolli poldi keermestumist.
8. Kontrolli, kas mutter pöörleb või tuleb pesast välja.
9. Kirjuta täpne tulemus `measurements.md` faili.
10. Muudatuse korral tee uus versioon; vana füüsilist printi ja selle faile ei
    kirjutata üle.

## C. Klapikinnituse valideerimine

Enne suure tööriista printi paigalda klapp proovikinnitusse ja kontrolli:

- klapi sobivust ning kinnitusavade joondust;
- liitmike paigaldamist ja eemaldamist;
- ühendatud vooliku paindumist ilma murdumiseta;
- elektripistiku ja kruvide ligipääsu;
- klapi eemaldamise ja hooldamise võimalust.

Kõik tulemused: `TODO — waiting for physical test` kuni katse on tehtud.

## D. Süstla kiirvahetuse katse

Pärast töötava klambri printimist tee 20 järjestikust ühe käega sisestamist ja
eemaldamist ilma tööriistadeta. Nummerda katsed 1–20 ning kirjuta iga
ebaõnnestumine, jääv deformatsioon või asendimuutus üles. Kriteeriumi ei märgita
valmis enne, kui kõik 20 füüsilist vahetust on päriselt tehtud.

| Vahetused | Klambri versioon | Ebaõnnestumised / deformatsioon | Tulemus |
|---|---|---|---|
| 1–20 | TODO — waiting for physical test | TODO — waiting for physical test | TODO — waiting for physical test |

## E. Tööriista kuiv sobitus enne robotit

1. Paigalda kuivalt iminapp, süstal, UV-lamp, kaamera, voolikud ja juhtmed.
2. Määra füüsiliselt, milline osa on napa-, doseerimis- ja kõvendusasendis
   kõige madalam.
3. Kontrolli voolikute, juhtmete, pistikute ja hoolduskohtade vaba ruumi.
4. Kaalu kogu tööriist kavandatud tööolekus enne robotile paigaldamist.
5. Kui kogumass on `≥ 500 g`, ära paigalda tööriista robotile.

## F. Tööriista nihked

1. Vali ja märgi üks ühine flantsi/tool'i koordinaatide referents ning telgede
   positiivsed suunad.
2. Paigalda valmis tööriist alati samas orientatsioonis.
3. Mõõda samast referentsist napa tipu keskpunkti X/Y/Z.
4. Mõõda samast referentsist süstla otsiku tipu X/Y/Z.
5. Kaitseprillidega tehtud paberikatses mõõda samast referentsist UV-laigu
   keskpunkti X/Y/Z ja kirjuta kasutatud tööriistaasend.
6. Korda mõõtmist pärast tööriista eemaldamist ja tagasipanekut; kirjuta
   kordustäpsus ja mõõtemääramatus, kui neid saab mõõta.
7. Sisesta ainult füüsilised tulemused faili `tool_offsets.md`.

## G. Pneumaatiline lekkekatse

1. Kinnita süstal hoidikusse ja sulge otsik.
2. Ühenda süstlaharu, suru süsteem katseks rõhu alla ning kirjuta tegelik
   algrõhk faili `leak_test.csv`.
3. Peata pump ja hoia süsteemi 5 minutit.
4. Kontrolli seebiveega iga liitekohta: voolik, kiirliitmikud, klapp ja kork või
   adapter.
5. Kirjuta lõpp-rõhk, aeg, mullide tulemus, testitud haru/liide ja pass/fail.
6. Lekke korral dokumenteeri asukoht ning parandus; jäta ebaõnnestunud rida
   alles ja tee uus test uue run ID-ga.
7. Enne lahtivõtmist vabasta rõhk klapi kaudu.

## H. UV-geomeetria katse

1. Ära kasuta päris vaiku.
2. Pane kõigile laua ääres viibijatele 405 nm kaitseprillid.
3. Suuna LED väikseima vajaliku vooluga valgele paberile, mitte silmade
   kõrgusele.
4. Märgi paberi kaugus ja tööriista asend.
5. Kontrolli, kus on valgustatud laik süstla/otsiku suhtes ning et otsik ei
   varjaks valgusteed.
6. Dokumenteeri geomeetria ja tulemus; ära eelda valguskoonuse nurka.

## I. Gridfinity abiosad

Kontrolli eraldi prügitopsi hoidikut ja pimedat otsiku parkimiskohta:

- füüsiline Gridfinity sobivus;
- inimese ja roboti ligipääs;
- et otsik ei saastaks lauda;
- et parkimisgeomeetria kaitseks otsikut soovimatu UV-valguse eest.

## J. 20 tsükli kuivkatse

Süstal on tühi ja LED väljas, kui õppejõud ei nõua selgesõnaliselt teisiti.
Alusta MG400-ga aeglaselt. Iga tsükli järjekord:

1. tõsta klaas;
2. liigu doseerimisasendisse;
3. liigu kõvendamisasendisse;
4. tagasta detail või vii nõutud väljundisse.

Täida `cycle_test.csv` kõik 20 rida. Iga tsükli juures märgi klaasi tõstmine,
doseerimis- ja kõvendusasendisse jõudmine, haakumine/kokkupõrge, pass/fail ning
märkused. Ühtegi tulemust ei täideta ette.

## K. Ohutus

- MG400 esimene käik tehakse aeglaselt; hädastopp peab olema käeulatuses.
- Käed hoitakse roboti tööalast väljas, kui robot on lubatud.
- UV LED-i kasutades kantakse 405 nm kaitseprille ja LED-i ei vaadata.
- Kuivkatses ei kasutata päris vaiku, kui õppejõud ei nõua teisiti.
- Survestatud pneumaatilisi liiteid kontrollitakse ettevaatlikult; suletud
  süstalt ei hoita käes ja rõhk vabastatakse enne lahtivõtmist.
- Mutri sisestamisel peatatud printi kasutatakse printeri ohutut protseduuri
  ja pintsette; kuuma otsikut ega alusplaati ei puudutata.
- Tööriista 500 g kogukoormuse piiri ei ületata.
