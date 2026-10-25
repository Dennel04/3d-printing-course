# Labori 3 esimese füüsilise töökorra katsejuhend

Kasuta seda järjekorras. Mõõda enne CAD-i alustamist. Kõik tegelikud tulemused
kirjuta kohe vastavasse faili; ebaõnnestunud katseid ei kustutata ega peideta.

## A. Inventuur ja füüsilised mõõtmised

1. Kontrolli olemasolu: 3/2 klapp, liitmikud, 4 mm voolik, süstal/süstlad,
   otsik/otsikud, 405 nm UV LED koos jahutusradiaatoriga, draiver, iminapp,
   kaamera, vajalikud kruvid/mutrid/seibid, kaal, nihik ja printer.
   Õpetajalt tulevad klapp, kaks 4 mm Y-kiirliitmikku, Metcal 910-B 10 cc
   mustad süstlad, otsikud, O-rõngaste komplekt ja kaitseprillid.
   LED-i ja draiveri valib meeskond Mouserist; kontrolli ka musta PLA,
   silikooni ja hambaorkide olemasolu.
2. Anna igale kasutatavale süstlale ja otsikule ID.
3. Täida `measurements.md`: mõõda nihikuga, kaalu kavandatud komplektid ja
   fotografeeri vajaduse korral mõõtmise nullpunkt.
4. Märgi puuduv `bom.md` faili. Ära vali CAD-i lõppmõõte enne mõõtmist.

### A1. Fusioni kontroll enne printi

1. Ava [README-s viidatud õpetaja mudelid](../README.md#õpetaja-cad-referentsid);
   kontrolli eriti uuendatud `Süstla päis poolik.f3z` blob SHA-d.
2. Vii päris süstla mõõdud kasutajaparameetritesse; mudeli hinnanguline mõõt
   ei ole füüsiline mõõtmine. Enne LED-i saabumist kasuta selgelt märgitud
   andmelehekeha; hiljem mõõda LED üle.
3. Uues MG400 tööriistahoidiku koostus on iga osa oma komponent.
   Kasuta `Design → Solid → Assemble → Joint` osade ja roboti nina ühendamiseks.
4. Ava `Assemble → Motion Study`; käi läbi doseerimiskoht, klaasi sisend,
   kõvendamiskoht ja väljund koos kõigi Lab 2 hoidikutega.
5. Tee `Inspect → Interference` koostule, päisele ja O-rõngale ning
   valguskoonuse/otsiku geomeetriale. Salvesta konfliktid ja põhjendatud
   parandused; arvutatud läbimine ei kinnita füüsilist sobivust.

## B. Mutritasku katse

Tee siis, kui klapikinnituse süsteemiadapter vajab sisseprinditud mutrit.

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

Enne suure tööriista printi ava `Solenoidklapi kinnitus.f3z`, prindi õpetaja
kaks tükki ja pane klapp kokku seibide ning kolme M4 poldi ja mutriga.
Voolik läheb otse klapini, hambaork lukustab ta ja silikoon tihendab.
Kontrolli:

- klapi sobivust ning kinnitusavade joondust;
- liitmike paigaldamist ja eemaldamist;
- ühendatud vooliku paindumist ilma murdumiseta;
- elektripistiku ja kruvide ligipääsu;
- klapi eemaldamise ja hooldamise võimalust.

Rõhu all kontrolli prindikihtide mõrasid poldi juures, vooliku libisemist,
silikooni lahtitulekut ja seebimulle. Kirjuta iga rike ning parandus üles.
Paigalda kinnitus valitud laua- või tööriistaadapterisse; taga mähise ümber
õhuruum ja juhtme tõmbetõke. Mõõda mähise temperatuur 10 min voolu all
olemise järel termomeetriga (°C); ära puuduta kuuma mähist.

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
   Kontrolli suurimat koormust: täis süstal ja klaas napa küljes korraga,
   lisaks kõik kinnitused, päis, kaamera, lamp, liikuvad voolikud ja juhtmed.
   Täis süstla kaalumise korraldus kooskõlasta õppejõuga; kuivkatse jääb tühjaks.
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
8. Mõõda neljanda nihkena kaamera pildi keskpunkt samal määratud tööpinnal;
   märgi töökaugus, kaader ja J4/R. Korda ka seda pärast taaspaigaldust.
   Lab 2 R = 33° napa kalibreerimist ei kanta uuele hoidikule automaatselt üle.

### F1. Süstla päise tihend

1. Vaata õpetaja pooleli päist ja päise/süstla koostu; seal olev rõngas on
   kandidaat, mitte kinnitatud valik.
2. Mõõda päris süstal ja vali komplektist O-rõngas. Kirjuta rõnga mõõdud,
   materjal ja allikas; arvuta venitus, kokkusurumine ning soone täitumine
   valitud rõnga ning süstla mõõtude põhjal.
3. Kontrolli soont Interference'iga ja väikesel proovikehal, seejärel päisel.
   Märgi prindi sein, perimeetrid ja kõik ebaõnnestumised mõõtelehele.
4. Alles kokkupandud ja kinnitatud päisega tee surve- ning lekkekatse.

## G. Pumba suurima rõhu katse ja viieminutine lekkekatse

1. Kontrolli skeemi `pump → Y → napp / klapp → süstal` ja klapi kolmandat
   atmosfääriava. Kinnita Andmehõive valitud anduriasukoht ja kalibreerimine.
   Enne maksimaalset rõhku tuvasta klapi pumba-, süstla- ja atmosfääriport
   märgistuse ning füüsilise ühenduskontrolliga. Kontrolli esmalt madala
   katserõhuga, et klapi vooluta lülitamisel süstlaharu rõhk päriselt atmosfääri
   vabaneb; pumba poolne andur üksi seda ei tõenda. Enne survekatset kontrolli,
   et süstal ja päis on hoidikus ohutult fikseeritud ega saa välja liikuda.
   Portide, rõhuvabastuse ja fikseerimise tulemused:
   `TODO — waiting for physical test`. Maksimaalse rõhu katset alusta alles
   pärast nende kontrollide läbimist ja tulemuste kirjapanekut.
2. Kinnita tühi süstal hoidikusse, sulge otsik ja napi haru. Klapp on voolu all.
3. Survekatsel lase pumbal puhuda täisvõimsusel kuni rõhk enam ei tõuse.
   Kirjuta anduri tegelik suurim rõhk (kPa), päise tulemus ja rikked
   `measurements.md` ning `leak_test.csv` faili; rõhku ei eeldata.
4. Eraldi lekkekatsel suru süsteem rõhu alla, peata pump, kirjuta algrõhk ja
   hoia 5 minutit. **Klapp jääb kogu viieminutise katse ajaks voolu alla**;
   vooluta klapp tühjendaks süstla atmosfääri. Napi haru jääb suletuks.
5. Kirjuta 5 minuti lõpp-rõhk, tegelik kestus ja anduri asukoht; kontrolli
   seebiveega voolikut, vooliku otsa klapikinnituses, klappi ja süstla päist.
6. CSV-s märgi testiliik, klapi olek, suletud napi haru, rõhk, aeg, mullid,
   lekkekoht, pass/fail ja parandus. Säilita ebaõnnestunud read.
7. Tee 100 klapilülitust ja korda sama lekkekatset; erista enne/pärast
   lülitusi tehtud jooksud. Lülituste arv on nõue, mitte juba tehtud tulemus.
8. Enne lahtivõtmist peata pump, vii klapp vooluta olekusse ning kinnita
   süstlaharu rõhu vabanemine. Enne klappi paiknev andur ei näita vooluta
   klapiga eraldatud süstla rõhku; kontrolli kasutatava mõõtepunkti tähendust.
   Suletud süstalt ei hoita katse ajal käes.

## H. UV-geomeetria katse

1. Ära kasuta päris vaiku.
2. Pane kõigile laua ääres viibijatele 405 nm kaitseprillid.
3. Suuna LED väikseima vajaliku vooluga valgele paberile, mitte silmade
   kõrgusele; ka laigu katse tehakse musta katte all.
4. Märgi paberi kaugus ja tööriista asend.
5. Kontrolli, kus on valgustatud laik süstla/otsiku suhtes ning et otsik ei
   varjaks valgusteed.
6. Dokumenteeri geomeetria ja tulemus; ära eelda valguskoonuse nurka.
7. Kontrolli nõutud vähemalt 30 mm kaugust lambist otsikuni; otsik jääb varju.
8. Must PLA-kate peab piirama kogu valguse; radiaator jääb välja õhu kätte.
   Kirjuta seina paksus (mm), perimeetrite arv ja täidis (%).
9. Pimedas ruumis pane katte ümber UV all helendav paber/kleebis, prillid ette,
   LED väikseimale voolule. Salvesta iga lekkekoht, parandus ja korduskatse.
   Käsi ega nahka katte alla ei panda.
10. Mõõda radiaatori temperatuur kavandatud kõvendusaja järel; salvesta
    aeg (s), temperatuur (°C), vool (mA) ja foto mõõtelehel.

## I. Gridfinity abiosad

Kontrolli eraldi prügitopsi hoidikut ja pimedat otsiku parkimiskohta:

- füüsiline Gridfinity sobivus;
- inimese ja roboti ligipääs;
- et otsik ei saastaks lauda;
- et parkimisgeomeetria kaitseks otsikut soovimatu UV-valguse eest.

## J. 20 tsükli kuivkatse

Süstal on tühi ja LED väljas.
Uue hoidikuga õpeta punktid uuesti. Esimene jooks tee ülesande järgi 20 %
kiirusel ja otsikud 20 mm kõrgemal õhus; alles kontrolli järel tegelikul teel.
Iga tsükli järjekord:

1. liigu doseerimisasendisse (kuivalt, süstal tühi);
2. tõsta klaas sisendist;
3. liigu kõvendamisasendisse;
4. pane klaas väljundisse.

Täida `cycle_test.csv` kõik 20 rida. Iga tsükli juures märgi
doseerimisasendisse jõudmine, klaasi tõstmine, kõvendamisasendisse jõudmine,
väljundisse panek, haakumine/kokkupõrge, pass/fail ning
märkused. Ühtegi tulemust ei täideta ette. Kontrolli J4 pöördel voolikute ja
juhtmete pinget ning kaamera vaadet. Lab 2 slot-pickeri klaasitsükkel ei
sisalda seda uut järjekorda; selles dokumentatsiooniülesandes programmi ei muudeta.

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
