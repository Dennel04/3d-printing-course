# Slot picker

Veebiaken, kus ruudustiku lahtrile klõpsates viib MG400 iminapa selle lahtri kohale. Režiimis **Edit layout** saab hoidikuid lisada, nimetada, neile tüüpi anda, nihutada ja kustutada. Kasutab `mg400-base` serverit (`http://127.0.0.1:8000`), mis peab olema ühendatud ja lubatud (enabled).

```bash
python slot_picker.py          # ava http://127.0.0.1:8010
python slot_picker.py --check  # prindi G-1, E+3, D-2, B+5, F-4 arvutatud X/Y
```

Ainult Pythoni standardteek, lisapakette pole vaja.

## Kuidas liigub

Iga klõps teeb kolm liigutust ja ootab pärast igaüht, kuni käsi kohale jõuab:

1. üles `travel_z`-ni samas X/Y-s;
2. üle `travel_z` kõrgusel lahtri keskpunkti kohale;
3. alla hõljumiskõrgusele (Hover Z).

Pessa ei laskuta: ruudustiku pinna Z puudutus on veel tegemata. R on alati `tool_r` (33), sest napp ei ole J4 teljel ja X/Y sõltub R-ist.

## Kaitsed

- Liikumine ainult siis, kui "Motion enabled" on märgitud; STOP katkestab ja peatab käe (`/api/stop`).
- Kiirus mg400-base-s peab olema ≤ `max_speed_ratio` (30 %); esimene jooks 20 %.
- Lahtrid väljaspool `radius_min`–`radius_max` ja `no_go` hoidikud (veebikaamera post) on hallid.
- Kui mg400-base piirab sihtpunkti (clamp) või robotil on viga/alarm, liikumine peatub.
- Hover Z lubatud vahemik on `min_hover_z` … `travel_z`.

## Paigutuse redaktor (Edit layout)

- **Lohistamine**: vajuta hoidiku lahtrile ja lohista — kogu hoidik liigub kursori/sõrmega kaasa (teise hoidiku peale või ruudustikust välja ei lähe, jääb viimasesse lubatud kohta). Tühjal lahtril vajutades ja lohistades valitakse ristkülik.
- Klõps lahtril valib/eemaldab selle (sinine raam). Nimi + tüüp + **Add holder from selection** lisab hoidiku.
- Hoidiku real: nime ja tüübi muutmine, nooled nihutavad kogu hoidikut ühe lahtri võrra (← → numbrite, ↑ ↓ tähtede suunas), **Use selection** asendab hoidiku lahtrid valitutega, **Delete** kustutab.
- Lahter saab kuuluda ainult ühele hoidikule; ruudustikust välja nihutada ei saa.
- Midagi ei salvestata enne **Save layout**; server kontrollib (nimi olemas ja kordumatu, tüüp tuntud, lahtrid olemas, kattuvusi pole) ja kirjutab `layout.json`-i. Salvestamata muudatustega Drive-režiimis ei liiguta.
- Tüübid on `layout.json` → `types` (glass, atom, battery, workstation, output, reject, calibration, camera_post, other): nimi ja värv; `no_go: true` (veebikaamera post) teeb lahtrid sõiduks keelatuks. Uue tüübi jaoks lisa sinna rida.

## Kaamera (View)

**View** teeb XIAO tööriistakaameraga (`camera_port`, COM5) kaadri kausta `frames/` (gitignore); leht näitab alati kõige uuemat kaadrit sellest kaustast — ka neid, mille sinna salvestab Claude.

## Seaded — `layout.json`

- `calibration` — ainult `tool_r` (33). Lahtrite X/Y tuleb failist [`../calibration/cells.py`](../calibration/cells.py) (24.10.26 kolme ruudu sobitus, pööre +0,87°); uue kalibreerimise järel muuda seal `MEASURED`.
- `motion` — kõrgused, kiiruse piir, ulatus.
- `types` — hoidikute tüübid (nimi, värv, `no_go`).
- `holders` — hoidikud: `name`, `type`, `cells`, `status`. Muuda redaktoriga. Praegused read on **ettepanek**, mitte kinnitatud paigutus (`docs/layout.md`); 24.10.26 oli klaas tegelikult B+5 hoidikus.

Testitud ainult simuleeritud mg400-base API-ga. Päris robotiga: TODO — waiting for physical test.
