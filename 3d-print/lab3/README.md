# 3D printimine ja CAD: Labor 3 - Tööriist: napp, süstal ja UV-lamp

**Maht:** 28 tundi | **Hindamine:** 20 punkti | **Meeskond:** 3 tudengit | **Välja antud:** 27.10.26 | **Tellimine:** 06.11.26 | **Esimene kaitsmine:** 17.11.26, veebis

See on meeskonna tööpäevik ja otsuste register. Täielik ülesanne on failis [`assignment-EST.md`](assignment-EST.md) (originaal, muutmata). Hoia mõõtmised koos ühikutega, lisa iga töökorra kohta uus päevikusissekanne ning jäta varasemad tulemused alles.

## Eesmärk

Üks tööriist MG400 käe otsas: iminapp, süstal, UV-lamp (405 nm) ja kaamera, nii et ükski ei sega teist. Pumba õhku jagab 3/2 solenoidklapp: voolu all süstlale, vooluta napale. Piirangud: rõhk (+110 kPa), kaal (käsi tõstab 500 g koos tööriistaga) ja geomeetria (kes on millal all).

**KAARDISTA ISE — eesmärk nii, nagu ta tegelikult välja tuli.**

## Kontrollnimekiri

- [ ] Kõik osad mõõdetud nihikuga ja Fusionis kehadena olemas: klapp koos liitmikega, süstal, süstla otsikud, UV LED jahutusradiaatoril, napp, kaameramoodul.
- [ ] Õhu teekond skeemina ja kaalueelarve tabelina failis `docs/tool_layout.md`.
- [ ] Klapi kinnitus valmis: klapp on kinni oma kinnitusaukudest, mutrid on prindi sisse pandud, voolikud ei murdu.
- [ ] Tööriist roboti küljes: napp, süstal, UV-lamp ja kaamera. Kaal alla 500 g koos täis süstlaga.
- [ ] Süstal vahetub ühe käega, ilma tööriistadeta. 20 vahetust järjest, klamber terve.
- [ ] UV-lambi koonus tabab liimi kohta ja läheb süstla otsikust mööda. Kontrollitud Fusionis ja valge paberiga laual.
- [ ] Iga otsiku nihe flantsi suhtes mõõdetud ja kirjas failis `docs/tool_offsets.md`.
- [ ] Lekkekatse: süstla haru hoiab rõhku 5 minutit, iga liitekoht seebiveega üle käidud. Tulemus failis `docs/leak_test.csv`.
- [ ] Prügitopsi hoidik ja otsiku parkimiskoht ruudustikus.
- [ ] Kuiv läbijooks: tõsta klaas, mine doseerimise kohta, mine kõvendamise kohta, 20 korda. Miski ei haagi. Tulemus failis `docs/cycle_test.csv`.
- [ ] Tellimus 06.11 failis `docs/bom.md`.
- [ ] Repo ja arenduspäevik täidetud, tag `3d-print-lab3`.

## Teadaolevad lähteandmed

### Varasematest laboritest

- Lab 1 lõtk: `0,4 mm` liikus vabalt, `0,2 mm` kiilus; lõpptulemus vahemik `0,2–0,4 mm` (vt `../lab1/README.md`).
- Lab 1 paindumise ja murdumise numbrid flex-tükist — vaja süstla klambri jaoks (vt `../lab1/README.md`).
- Lab 2: hoidikud ruudustikus, paigutus `../lab2/docs/layout.md`, kaamera kinnitus ja toide, olemasolev iminapa tööriistahoidik.

### Teistest ainetest

- Andmehõive L3: kus andur voolikus istub ja kui pikk voolik klapi ja süstla vahel olla tohib — `TODO — küsida`.
- Nutikad Lahendused L1: jaam punktide õpetamiseks ja ülemängimiseks.

### Tegelikku mõõtmist või katset vajavad väärtused

Klapi, liitmike, süstla, otsikute, LED-i koos radiaatoriga, napa ja kaameramooduli mõõdud ja kaalud; klapi asukoht (käe otsas või laual); mutritasku mõõdud ja peatuse kõrgus; kolm nihet flantsi suhtes; lekkekatse ja kuiva läbijooksu tulemused. Kõigi olek: `TODO — waiting for physical test`.

## Tööfailid

- [`docs/tool_layout.md`](docs/tool_layout.md) — osade mõõdud ja kaalud, õhu skeem, kaalueelarve, klapi asukoha otsus.
- [`docs/tool_offsets.md`](docs/tool_offsets.md) — napa, süstla otsiku ja lambi laigu nihked flantsi suhtes.
- [`docs/leak_test.csv`](docs/leak_test.csv) — lekkekatsed.
- [`docs/cycle_test.csv`](docs/cycle_test.csv) — 20 kuiva ringi.
- [`docs/bom.md`](docs/bom.md) — tellimus 06.11.26, iga rea põhjendus.
- `docs/photos/` — fotod.

## CAD-failid

Iga detail eraldi kaustas, `src/` (Fusion), `stl/`, `3mf/`, versioonid `-v1`, `-v2`, ...; 3MF-is on mutrite peatuse kõrgused.

- `nut-pocket-test/` — väike prooviklots mutritasku ja printimise peatuse jaoks.
- `valve-mount/` — solenoidklapi kinnitus.
- `tool/` — tööriist: napp, süstal, UV-lamp, kaamera.
- `purge-cup-holder/` — prügitopsi Gridfinity hoidik.
- `nozzle-park/` — otsiku parkimiskoht (pimedas ja kinni).

## Arenduspäevik

Lisa iga töökorra lõppu uus sissekanne; ära kirjuta varasemaid sissekandeid ümber.

**PP.KK.AA — kes olid kohal**
- Tegime:
- Juhtus (numbrid):
- Otsustasime, ja miks:
- Lahti järgmiseks korraks:
