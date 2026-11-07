# Labori 3 komponentide inventuur ja võimalik tellimus

Kontrolli osade olemasolu füüsilisel töökorral. Põhjenda tellimisvajadus ja
kasuta tootekoodi kinnitamiseks tellimistabelit ning tarnija allikat.

Tellimuse tähtaeg oli 06.11.2026; esimene kaitsmine on 19.11.2026.
[Õppejõu ühine tellimistabel](https://docs.google.com/spreadsheets/d/11Wf7WONugjfL77vNTto1eWfUyokqos01xseWcNSE6f4/edit?gid=0#gid=0)
on tellimuse oleku allikas.
Õpetaja antavat osa ei loeta automaatselt puudu olevaks: kontrolli üleandmist
ja riiulivaru. LED-i ja draiveri valib meeskond, õppejõud ostab Mouserist.
Mõlema kinnitatud valiku juurde on vaja Mouseri tootekoodi ja põhjendust.
LED-i kiirgusnurk, vool, soojuskoormus ja mõõdud võetakse valitud osa
andmelehelt märgitud allikaga, hilisem füüsiline kontroll jääb eraldi.

| Vastutus / tarneallikas | Komponendid | Inventuuri / valiku olek |
|---|---|---|
| Õpetaja annab | 3/2 klapp; kaks 4 mm Y-kiirliitmikku; Metcal 910-B 10 cc mustad süstlad ja otsikud; O-rõngaste komplekt; 405 nm kaitseprillid | TODO — waiting for physical test |
| Õpetaja CAD-allikad, meeskond prindib | Klapikinnituse valmis koost ja lõpetatav süstla päis; allikad README-s | TODO — waiting for physical test |
| Meeskond valib, õpetaja ostab Mouserist | 405 nm LED, draiver ja UV-toite tarvikud | LED ja draiver on valitud ning ühises tabelis; vt allpool. |
| Riiulivaru kontroll / põhjendatud lisavajadus | Must PLA, muu PLA, voolik, silikoon, hambaorgid, poldid, mutrid, seibid, juhtmed, seebivesi | TODO — waiting for physical test |

| Komponent | Kogus | Nõude allikas | Laos? | Tellida? | Põhjus / täpsustus |
|---|---:|---|---|---|---|
| PLA, sh must PLA UV-kattele | TODO — waiting for physical measurement | Lab 3 printdetailid ja must kate | TODO — waiting for physical test | TODO — waiting for physical test | Kontrollida sobiva materjali ja koguse olemasolu. |
| 3/2 solenoidklapp | TODO — waiting for physical measurement | `assignment-EST.md`, õpetaja annab | TODO — waiting for physical test | TODO — waiting for physical test | Voolu all pump süstlasse, vooluta süstal atmosfääri; napp on eraldi Y-harus. |
| Kaks 4 mm Y-kiirliitmikku | 2 tk (ülesande sisend, mitte inventuuritulemus) | `assignment-EST.md`, õpetaja annab | TODO — waiting for physical test | TODO — waiting for physical test | Napi haru ja rõhuanduri ühendus; puudumist ei eeldata. |
| Kiirliitmikud | TODO — waiting for physical measurement | Pneumaatika teekond | TODO — waiting for physical test | TODO — waiting for physical test | Tüüp ja kogus selguvad olemasolevate osade inventuuril. |
| 4 mm voolik | TODO — waiting for physical measurement | `assignment-EST.md`, sisendid | TODO — waiting for physical test | TODO — waiting for physical test | Vajalik mõlemale harule; pikkus mõõta tegelikul marsruudil. |
| Metcal 910-B mustad süstlad, 10 cc | TODO — waiting for physical measurement | `assignment-EST.md`, õpetaja annab | TODO — waiting for physical test | TODO — waiting for physical test | ID ja kogus kinnitada inventuuril. |
| Otsikud | TODO — waiting for physical measurement | `assignment-EST.md`, sisendid | TODO — waiting for physical test | TODO — waiting for physical test | ID, kinnitus ja kogus kinnitada inventuuril. |
| 405 nm LED ja jahutusradiaator | Kumbagi 1 tk tellimistabelis | Meeskonna valik, õpetaja ostab Mouserist | TODO — waiting for physical test | `submitted`; ost kinnitamata | New Energy LED ja Würth Elektronik 40905112092424 radiaator (read 10 ja 14). Jahutus vajab kontrolli. |
| LED-i draiver | 1 tk tellimistabelis | Meeskonna valik, õpetaja ostab Mouserist | TODO — waiting for physical test | `submitted`; ost kinnitamata | RECOM 350 mA nimiväljundiga; elektriline sobivus vajab kontrolli. |
| O-rõngaste komplekt / lisarõngas | TODO — waiting for physical measurement | Õpetaja komplekt; võimalik lisavajadus päise arvutusest | TODO — waiting for physical test | TODO — waiting for physical test | Enne ostuvajadust vali komplektist ja arvuta soon; mõõtu ei oletata. |
| Silikoon ja hambaorgid | TODO — waiting for physical measurement | Õpetaja klapikinnituse kokkupanek | TODO — waiting for physical test | TODO — waiting for physical test | Tihendus ja vooliku mehaaniline lukustus. |
| Nõelventiil, kui Andmehõive valib | TODO — waiting for physical measurement | Tingimuslik valik napi harus | TODO — waiting for physical test | TODO — waiting for physical test | Tüüp ja vajadus kooskõlastada enne tellimist. |
| 405 nm kaitseprillid | TODO — waiting for physical measurement | `assignment-EST.md`, ohutus | TODO — waiting for physical test | TODO — waiting for physical test | Kõigile UV-katse ajal laua ääres viibijatele. |
| Poldid, mutrid ja seibid | TODO — waiting for physical measurement | Klapikinnitus ja mutritasku katse | TODO — waiting for physical test | TODO — waiting for physical test | Suurus ja kogus määratakse tegelike kinnitusavade järgi. |
| Keermesisud, kui hilisem disain need valib | TODO — waiting for physical measurement | Tingimuslik CAD-otsus | TODO — waiting for physical test | TODO — waiting for physical test | Ei tellita enne, kui disainivalik ja mõõt on kinnitatud. |
| Seebivee pihustipudel | TODO — waiting for physical measurement | `assignment-EST.md`, lekkekatse | TODO — waiting for physical test | TODO — waiting for physical test | Iga pneumaatilise liitekoha kontrolliks. |

## UV-komponentide valik ja tellimisolek

Kontroll 07.11.2026: [tellimistabeli read 10–15](https://docs.google.com/spreadsheets/d/11Wf7WONugjfL77vNTto1eWfUyokqos01xseWcNSE6f4/edit?gid=0#gid=0&range=D10:J15),
aine „3D printimine ja CAD”. `selected` tähendab mudeli valikut; `submitted`
tähendab rea kandmist ühisesse tabelisse. `ordered` vajab ostukinnitust,
`received` kättesaamise kinnitust ja `physically tested` katsekirjet.

| Komponent | Mudel | Mouseri kood | `selected` | `submitted` | `ordered` | `received` | `physically tested` |
|---|---|---|---|---|---|---|---|
| 405 nm LED (rida 10) | New Energy LST1-01G01-UV04-00 | [416-LST101G01UV04](https://www.mouser.com/en/ProductDetail/New-Energy/LST1-01G01-UV04-00?qs=wd5RIQLrsJhXFj3vG5W5hQ%3D%3D) | Jah | Jah | Kinnitamata | Kinnitamata | TODO |
| LED-draiver (rida 11) | RECOM RCD-24-0.35/W/X3 | [919-RCD-24-0.35/W/X3](https://eu.mouser.com/en/ProductDetail/RECOM-Power/RCD-24-0.35-W-X3?qs=XF8hdbuHJAWtxpFzhhVydw%3D%3D) | Jah | Jah | Kinnitamata | Kinnitamata | TODO |

LED-i ja draiveri tellimise ning kättesaamise kuupäevad olid tabelis tühjad.
Andmehõive Lab 3 BOM-is olid sama valiku Mouseri koodid veel TODO.

Elektriliste andmete allikad ja tähendus:

- [New Energy LED-i andmeleht](https://www.mouser.com/datasheet/3/1525/1/NewEnergy_StarBoard_Horticulture_Luminus_DataSheet.pdf) annab 405 nm ja tüüpilise päripinge 3,4 V võrdlustingimusel 500 mA, `Tj = 25 °C`. See vool on andmelehe võrdlustingimus.
- [RECOM RCD-24 andmeleht](https://recom-power.com/pdf/Lightline_DC-DC/RCD-24.pdf) annab valitud draiveri nimiväljundiks 350 mA. Nimiväljund on kavandatud LED-i toitevool, kui draiver töötab täisvoolul; tegelikku LED-i voolu pole mõõdetud.
- [M5Stack U023 andmed](https://docs.m5stack.com/en/unit/Unit_Relay) annavad kontaktide nimikoormuseks 3 A pingel 30 V DC. Tabeli rida 15 käsitleb UV-toite lisareleed; kontaktide nimikoormusest ei saa tuletada LED-i voolu ega draiveri sisendvoolu.

**TODO:** dokumenteeri LED-i päripinge ja jahutus 350 mA juures, draiveri
vajalik pingevaru 12 V toitega ning relee sobivus draiveri sisendi püsi- ja
käivitusvoolule. Elektriline sobivus ja füüsiline katse on kinnitamata.
**TODO:** kontrolli UV ohutut väljalülitumist tavaseiskamisel ja juhtsignaali
kadumisel.
