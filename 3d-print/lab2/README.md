# 3D printimine ja CAD: Labor 2 - Sisend, töökoht, väljund

**Maht:** 30 tundi | **Hindamine:** 20 punkti | **Meeskond:** 3 tudengit

See on meeskonna tööpäevik ja otsuste register. Hoia mõõtmised koos ühikutega, lisa iga töökorra kohta uus päevikusissekanne ning jäta varasemad tulemused alles. Täielikku töölehte ei kopeerita.

## Eesmärk

Kavandada MG400 töölauale Gridfinity hoidikud sisenditele, töökohtadele ning heade ja praakdetailide väljundile. Hoidik peab pärast ruudustikust eemaldamist ja tagasipanekut jääma roboti suhtes samasse kohta. Kaamerad peavad nägema töökohta ja kogu lauda.

## Kontrollnimekiri

- [ ] `docs/layout.md`: töövoog, ruutude paigutus ja skeem mõõdetud laua järgi.
- [ ] 1 x 1 Gridfinity kalibreerimishoidik testitud ruudustikus ja robotiga.
- [ ] Kolm sisendhoidikut, igaühes vähemalt neli mõõdetud pesa.
- [ ] Töökoha hoidik ja heade ning praakdetailide väljundikohad.
- [ ] Iga pesa mõõt ja roboti sihtpunkt dokumenteeritud ruudu ning nihkega.
- [ ] Klaasiga tehtud viis korduskatset ja tulemused failis `docs/refit_test.csv`.
- [ ] XIAO ESP32S3 Sense kaamera kinnitus ning valitud ja katsetatud toide.
- [ ] USB UHD veebikaamera jäik post; mõõdetud pildikõikumine roboti liikumise ajal.
- [ ] `docs/bom.md` sisaldab iga tellitava rea põhjendust.
- [ ] Iga prindi lähtefail, STL ja 3MF on versioonitud.
- [ ] Arenduspäevik täidetud; esitamisel lisatud tag `3d-print-lab2`.

## Teadaolevad lähteandmed

- Gridfinity ruudustik: 7 x 10 ruutu, samm 42 mm. Kontrolli füüsiliselt ruutude tähistus ja koordinaatide suund.
- Lab 1 printerikatse: 0,4 mm lõtkuga detail liikus vabalt; 0,2 mm lõtkuga detail kiilus. Seni kasutatav vahemik on 0,2-0,4 mm, mitte lõplikult kalibreeritud väärtus.
- Materjal: PLA.
- Töökoha täpsusala, detailide mõõdud, ruutude asukohad ja kaamerate toide tuleb meeskonnal mõõta või katsetada.

## CAD-failid

- `src/gridfinity-calibration-v1.scad` - esmane 1 x 1 kalibreerimismudel. Enne printi kontrolli jala sobivus ruudustikku.
- `src/gridfinity-tray-v1.scad` - nelja pesaga mitmeruuduline alustusmudel. Vaheta näidismõõdud mõõdetud detailide vastu.

Need lähtefailid ei ole veel füüsiliselt sobivaks kinnitatud. Iga print vajab PrusaSlicerist eksporditud STL-i ja 3MF-i, uue versiooninime ning mõõtmistulemuste dokumenteerimist.

## Arenduspäevik

Lisa iga töökorra lõppu uus sissekanne; ära kirjuta varasemaid sissekandeid ümber.

**Kuupäev - osalejad**
- Tegime:
- Mõõtmised ja tulemused koos ühikutega:
- Otsused ja põhjendused:
- Failid ja versioonid:
- Järgmiseks:
