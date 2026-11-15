# Fusion Generative Design

**TODO enne detaili valiku kinnitamist.** Kontrolli hariduslitsentsi, Generative Designi tööruumi ja uuringu lahendamise ligipääsu. Seadista uuring pärast [originaali mõõtmist ja pilooti](test-procedure.md#2-koormus-ja-originaali-piloot). Salvesta kasutatud Fusioni versioon, uuringu ID ja arhiiv.

| Sisend | Klaasihoidiku v3 seadistus |
| --- | --- |
| Preserve Geometry | Säilita nelja pesa põrandad, seinte kontaktvööd ja sissejuhtivad servad ning kõigi jalgade kontaktpinnad. Jäta säilitatavale geomeetriale piisav materjalikiht ja piisav ühenduspind uue kehaga. Seo need [liidesemõõtudega](analysis_original.md#klaasihoidiku-lähtegeomeetria-ja-print). |
| Obstacle Geometry | Modelleeri klaaside täisümbrised koos paigalduseks vajaliku vaba ruumiga, iminapa liikumisümbris, ruudustiku soklid, naaberhoidikud ja ligipääs detaili väljatõstmiseks. Kui detailivalik muutub, lisa vastava tööriista süstla vahetustee, voolikud, UV-koonuse vaba ruum ja kaamera vaateväli. |
| Lubatud kuju | Kontrolli uuringu väljundeid originaali paigaldusümbrise suhtes ja kasuta vajaduse korral ümbrist piiravaid keelukehi. Lähtemahu võib teha originaali liideste vahelisest põhjast. |
| Kinnitused ja jõud | Kanna tegeliku koormuse vektorid ja kontaktalad säilitatavale geomeetriale. Seo piirangud ruudustiku kontaktide ja katses kasutatava rakisega. Kasuta igas koormusjuhus mõõdetud jõudu (N) ning seadista **Safety Factor = 2**. Märgi, kuidas varutegurit rakendasid. Sama mõõdetud jõu korrutamine kahega koos Safety Factor 2 seadistusega loeks varu kaks korda. |
| Materjal | Kasuta prindiga kooskõlas PLA omadusi. Kui Fusion pakub ainult sobivat lähendit, salvesta materjalikaart ja selle allikas ning kontrolli lõpptulemust ühises [simulatsioonis](simulation.md). |
| Tootmine | Vali **Additive**. Määra prindisuunad samas mudeli teljestikus kui viilutustabelis. Kasuta 45° esialgse üleulatuva nurga kandidaadina ja kontrolli seda tegeliku profiiliga. Vali väikseim paksus tegeliku ekstrusioonilaiuse, vajaliku perimeetrite arvu ja mõõdetud koormuse järgi. Algse 3MF-i perimeetrirada on 0,45 mm, kahe raja nimilaius on 0,90 mm. Kinnita valitud paksusega seinad PrusaSliceri rajavaates. |
| Eesmärk Fusionis | **Minimize Mass** on viis saada vähem materjali sisaldavaid kandidaate varuteguriga 2. Lab 4 mõõdik on **lühem prindiaeg sama tugevuse juures**. Vali nõuetele vastavate prinditavate kandidaatide seast viilutaja järgi kiireim. |

[Autodesk · säilitatav geomeetria](https://help.autodesk.com/cloudhelp/ENU/Fusion-GenerativeDesign/files/GD-PRESERVE-GEOM.htm) · [Tootmispiirangud](https://help.autodesk.com/cloudhelp/ENU/Fusion-GenerativeDesign/files/GD-ADDITIVE-REF.htm) · [Eesmärgid ja varutegur](https://help.autodesk.com/cloudhelp/ENU/Fusion-GenerativeDesign/files/GD-OBJECTIVES.htm)

1. Salvesta seadistuse pilt koos liideste, keelualade, jõu noolte, kinnituste ja parameetritega. Kirjuta üles lahendi kuupäev ja saadud kandidaatide arv.
2. Jäta võrdlusse kandidaadid, mis mahuvad lubatud ümbrisesse, säilitavad liidesed ja vastavad uuringu tugevuspiirile. Kontrolli prinditavust, toe ligipääsu, pesade puhtust ja hinnangulist prindiaega. Kui tuge kulub massilt rohkem kui detailile, lükka tulemus tagasi.
3. Vali tingimustele vastav lühima hinnangulise prindiajaga tulemus. Märgi tulemi ID, võrdluse alused ja tagasilükatud kuju põhjused.
4. Ekspordi valitud tulemus Fusioni disainina. Viimistle liited ja tee tulemist prinditav keha. Kontrolli ristlõikeid ja liideseid ning käivita lõplik simulatsioon ja viilutus just sellel kehal. Salvesta lähteuuring, lõppkeha, STL, 3MF ja pildid.

**Täita pärast uuringut.** Kuupäev, uuringu ID, kandidaate kokku, valitud ID, prindiaeg ja tugi, kontrollitud liidesed, puhastamisel tehtud muudatused ning arhiivi ja piltide viited.
