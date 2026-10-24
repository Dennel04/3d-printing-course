# Slot picker

Veebiaken, kus ruudustiku lahtrile klõpsates viib MG400 iminapa selle lahtri kohale. Kasutab `mg400-base` serverit (`http://127.0.0.1:8000`), mis peab olema ühendatud ja lubatud (enabled).

```bash
python slot_picker.py          # ava http://127.0.0.1:8010
python slot_picker.py --check  # prindi G-1, E+3, E+2, E+4 arvutatud X/Y
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

## Seaded — `layout.json`

- `calibration` — 24.10.26 kalibreerimine (`docs/measurements.md`): pööre +1,82°, G-1/E+3 pöördepunkt mudelis ja mõõdetud. Uue kalibreerimise järel muuda siin.
- `motion` — kõrgused, kiiruse piir, ulatus.
- `holders` — hoidikute lahtrid. Praegu **ettepanek**, mitte kinnitatud paigutus (`docs/layout.md`).

Testitud ainult simuleeritud mg400-base API-ga. Päris robotiga: TODO — waiting for physical test.
