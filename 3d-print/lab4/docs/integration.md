# Integratsioon Andmehõive ja Nutikate Lahendustega

## Detail ja liidesed

Muudatusettepanek puudutab klaasi sisendhoidikut `glass-input-holder` v3. Meeskonna otsus ja vahetus on ootel. Säilita 2 × 2 Gridfinity jalad ja 42 mm samm, nelja pesa keskmed, põhja ja serva kõrgus, kontaktpinnad, klaasi istumine ja napa vaba liikumisruum. Kui meeskond valib tööriistadetaili, fikseeri selle flantsi-, poldi-, vooliku- ja vastasdetaili liidesed [enne ümberjoonistamist](analysis_original.md).

[Lab 2 paigutus](../../lab2/docs/layout.md) annab lähtepunktid D−1, D−2, E−1, E−2, E+2 ja väljund D/E +3/+4. Eelmise tööriista puhul on dokumenteeritud R = 33°. Kontrolli tegelikku ruudustiku referentsi, kõigi nelja pesa X/Y keskpunkti, võtu- ja asetuskõrgusi, lähenemis- ja taganemiskõrgusi, J4/R-i, töökaugusi ja teekonda. Kui Andmehõive töövoog vahetab sisendi ja väljundi rollid, kontrolli mõlema suuna koordinaadid ja kinnita viienda klaasi jaoks tegelik paigutus. Lab 2 nelja pesa plaan üksi ei määra viienda klaasi asukohta.

Kui flantsi küljes tööriist vahetub, mõõda samast referentsist **iminapa keskpunkt**, **süstla otsiku tipp**, **UV-laigu keskpunkt** ja **kaamera pildi keskpunkt** tööpinnal. Märgi X/Y/Z, J4/R ja tööpind. Ainult lauahoidiku vahetuse korral kontrolli napa ulatust ja kinnita, milline tööriista ning nihkekomplekti versioon parasjagu kehtib. Vajaduse korral kontrolli ka kaamera vaatevälja ja tilgaplaadi kõrgust. [Lab 3 nihked](../../lab3/docs/tool_offsets.md) · [Kaksik](../../sim/README.md)

## Vahetuse ajastus

1. Lepi enne esimest Andmehõive kirjet kokku versioonitunnus ja selle sidumine tsükliga. Planeeri vahetus mõõteseeriate vahele. Säilita soovitusliku detaili korral lähteviide `glass-input-holder-v3`. Uue paigalduse versioon võiks olla `glass-input-holder-lab4-h-v1` või `glass-input-holder-lab4-g-v1`. Seo paigaldatud eksemplari ID Fusioni arhiivi, STL-i, 3MF-i ning kontrolltõendiga.
2. Lõpeta või peata käimasolev töövoog ning fikseeri vana versiooni viimane lõpetatud tsükkel. Kohalik operaator keelab roboti enne füüsilist vahetust ja hoiab operaatori luku kontrolli all. Märgi tegelik vahetuse hetk ISO 8601 kujul koos ajavööndi nihkega (Europe/Tallinn), jaama ning meeskonna tunnus ja vahetuse teinud isik. Kui tsükkel katkeb, märgi selle ID ja staatus.
3. Tee esmane kontroll aeglaselt, fikseeri katselised kontrolltsüklid ja leia uue versiooni esimene heaks kiidetud tsükkel pärast kontrolli. Lisa vahetuslogisse paigutuse, kalibreerimise, tööriista ja töövoo tunnused ning kõik muutunud koordinaadid. Jätka andmekogumist pärast osapoolte kinnitust.

## Andmehõive L4 · „Masin, mis mõõdab ise“

Ülesanne ütleb, et üks tsükkel annab ühe kirje ja vähemalt 300 tsüklit jõuab andmestikku. Tilgad lähevad tilgaplaadile ja viis klaasi ringlevad hoidikute vahel. Anna Andmehõivele meeskond, jaam, vana ja uus detailiversioon, vahetuse aeg, vana konfiguratsiooni viimane ja uue esimene kehtiv `cycle`, kontroll- või katkestatud tsüklid ning muutunud tööriista, kaamera ja paigutuse andmed. Märgi samal ajal toimunud otsiku, süstla, rõhu, retsepti või töövoo muudatused. Säilita rõhukõverate, piltide ja märgete seosed. Võrdluses rühmita kirjed versiooni järgi ning jäta ümberseadistuse tsüklid eraldi. [Andmehõive ametlik Lab 4](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/Data%20Acquisition/Data%20Acquisition%20%5BLab%204%5D%20EST.md)

## Nutikad Lahendused L4

Lepi Andmehõive ja Nutikate Lahendustega enne esimese kirje saatmist kokku `docs/record.md` kirje kuju. Ülesandes kasutatud väljad `team`, `cycle` ja `t` annavad seosele lähtepunkti. Töövoo salvestaja, operaatori lukk, puhver ja ühine andmebaas peavad säilitama selle seose ka hilinenud kirjete ja kordussaatmise puhul. Kasuta kirje tsükli aega ning kokkulepitud tsüklivõtit. Andmebaasi saabumisaeg võib olla hilisem. [Nutikate Lahenduste ametlik Lab 4](https://github.com/KKallas/Narva-subjects/blob/main/EST/2026-27/Smart%20Solutions/Smart%20Solutions%20%5BLab%204%5D%20EST.md)

**Ettepanek ühisele kirjeldusviisile.** Pea vahetuslogi ja seo see kirjetega kokkulepitud meeskonna/jaama/tsükli võtmega. Kasuta igal tsüklil detailiversiooni välja ainult siis, kui osapooled lisavad selle ühisesse skeemi enne selle lukustamist. Vahetuslogis võiksid olla järgmised väljad.

| Väli | Sisu |
| --- | --- |
| `team`, `station_id`, `part_id` | Meeskond, jaam ja vahetatud osa püsitunnus |
| `old_revision`, `new_revision`, `sample_id` | Vana ja uus versioon ning paigaldatud eksemplar |
| `changed_at`, `operator` | Tegelik vahetushetk koos ajavööndi nihkega ja teostaja |
| `last_old_cycle`, `first_new_cycle`, `check_cycles` | Andmeseeriate piir ning kontrolli või katkestuse tsüklid |
| `workflow_id`, `layout_ref`, `offsets_ref`, `verification_ref` | Töövoo versioon, ruudustiku ja õpetatud punktide viide, nihkekirje ning kontrolltõend |

Kinnita koos vahetusaken, viienda klaasi paigutus, tsüklivõti ja ajavööndi kuju, versiooni sidumine ühise kirjega ning see, kes peatab ja taaskäivitab töövoo.
