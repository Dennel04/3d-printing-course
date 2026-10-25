# Komponentide nimekiri

Lisa tellimusse ainult meeskonna kinnitatud kogus. Iga rea põhjendus seostub konkreetse hoidiku, kaamera või toitekatsega. Kontrolli enne tellimist, mida laboris juba olemas on.

| Kogus | Komponent / spetsifikatsioon | Mille jaoks ja miks seda vaja on | Olek / link |
|---:|---|---|---|
| | PLA | Gridfinity hoidikute, kaamera kinnituste ja jäiga postiosa printimiseks; kontrollida olemasolevat varu. | kontrollimata |
| | XIAO ESP32S3 Sense | Tööriistakaamera on olemas; USB Serial pildi saamine COM5 kaudu on kinnitatud (OV3660, JPEG 1600 × 1200 px, foto README-s). | olemas; uut tellimust ega kogust ei kinnitata |
| | XIAO ESP32S3 Sense kaamerale sobiv toide ja kaabel | Tööriistal oleva kaamera toitevalik tuleb enne tellimist läbi proovida ning pinge ja vool kinnitada. | katsetada |
| | Verbatim AWC-03 (49580) USB veebikaamera | Tuvastatud üldvaatekaamera, ühendatakse USB kaudu station PC-ga; posti klambri mõõtmine on kirjeldatud README-s. | mudel tuvastatud; uut ostu ega tellimust ei kinnitata |
| | Üldvaatekaamera USB-kaabel / vajaduse korral pikendus | Ühendus Verbatim AWC-03 ja station PC vahel; tegelik vajalik pikkus ja olemasolev kaabel tuleb kontrollida. | kogus, pikkus ja tellimisvajadus kinnitamata |
| | Kinnitusvahendid, tüüp ja mõõt pärast prototüüpi | Kaamera kinnitamiseks iminapa tööriistahoidikule ja/või postiosade ühendamiseks; valida pärast liideste mõõtmist. | määramata |
| 8 | M3 × 6 sisekuuskantpeaga kruvi (DIN 912 / ISO 4762) | Haarats (`gripper-attachment`): 4 tk flantsi külge, 4 tk iminapa külge. Pea all 2 mm prinditud materjali, keermesse ~4 mm. | ootel — haaratsi arendus peatatud 23.10.26, Lab 2-s ei telli |
| 1 | Vertikaalne toru 16 mm, pikkus 458 mm | Veebikaamera post: toru läheb prinditud nurga (`veebikaamera-post-v1-nurk`) ja ülemise osa vahele, kaamera jääb ~470 mm laua kohale (README kontrollnimekiri). | olemasolu ja materjal kinnitamata; pikkus kinnitada enne lõikamist |
| | 1,75 mm PLA filamendi tükk (tihvt) | Lukustab XIAO kaameramooduli `xiao-square-mount-v2` pesas (ava Ø1,85 mm). | olemas (kulumaterjal), ei telli |

25.10.2026 täiendus: XIAO toide on valitud — **USB-C kaabel** arvutisse (sama kaabel annab pildi), vt README kontrollnimekirja XIAO punkt. Rida „XIAO ESP32S3 Sense kaamerale sobiv toide ja kaabel“ ei vaja seega eraldi toiteallikat; kaabli pikkus kogu MG400 liikumisel jääb kontrollida. XIAO kinnitus kasutab J4 kaane olemasolevaid M2,5 kruve, uusi kruve ei telli.

23.10.2026 täiendus: XIAO olemasolu ja USB-katse ning Verbatimi mudel põhinevad meeskonna kinnitatud seisul ja README varasematel kirjetel. Tühjad koguseväljad ei tähenda nulli ega ostukogust. XIAO Wi-Fi HTTP valik ei määra toiteallikat ega kaablite arvu. Kaamera mass (g), lõpliku toite pinge/vool ja kaablite sobivus kogu MG400 liikumisel: `TODO — waiting for physical test`. Tellimuse tegemist siin ei kinnitata.
