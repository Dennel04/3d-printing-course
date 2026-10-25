# Ühised komponendimudelid

Ostetud komponentide 3D-mudelid, mida kasutavad kõik laborid (hoidikud, kinnitused, kokkupaneku kontroll Fusionis). Laboripõhised osad jäävad oma `labN/` kausta.

Fusionis: **Insert → Insert Mesh** (STL/OBJ) või **Insert → Insert into Current Design / Upload** (STEP, f3d). Mesh-mudelid sobivad kokkupõrke ja paigutuse kontrolliks; täpsed pesamõõdud võta nihikuga mõõdetud väärtustest (`3d-print/lab2/docs/measurements.md`), mitte võrgust.

| Kaust | Failid | Allikas | Mõõdud mudelis | Märkus |
|---|---|---|---|---|
| `m5stack-atoms3/` | `AtomS3.stl`, `AtomS3R.stl` | M5Stack [M5_Hardware](https://github.com/m5stack/M5_Hardware) `Products/C123_AtomS3` ja `C126_AtomS3R`, laaditud 24.10.2026 | korpus 24,0 × 24,0 × 12,9 mm (failis on mitu detaili kõrvuti, kogulaius 95,3 mm) | mõlemad failid on baithaaval identsed; mõõdetud 24 × 24 × 12,9 mm (`nominal`); kaksik (`sim/`) kasutab kokkupandud paari (x < 30 mm) |
| `m5stack-atomic-battery-base/` | `Atomic_Battery_Base_Bottom_Shell.obj`, `Atomic_Battery_Base_Face_Shell.stl` | M5Stack M5_Hardware `Products/A151_Atomic_Battery_Base`, laaditud 24.10.2026 | põhi 24,0 × 24,0 × 18,0 mm, kate 23,2 × 21,6 × 2,5 mm | meie akumoodul mõõdeti 24,04 × 24,01 × 21,97 mm — et see on Atomic Battery Base, on kinnitamata; kaksik (`sim/`) kasutab töökohal seda mudelit |
| `xiao-esp32s3-sense/` | `xiao-esp32s3-sense.step`, `.f3d` | Seeed Studio XIAO ESP32S3 (Sense) ametlik mudel (kaameramoodul + Sense laiendusplaat), eksporditud Fusioni dokumendist `lab2-cameras-reference` | 24,4 × 14,0 × 17,8 mm | kasutatud `lab2/camera-mounts/xiao-square-mount-v2` jaoks; kaksikus (`sim/`) kinnituse sees |
| `verbatim-awc03-webcam/` | `verbatim-awc03-webcam.step`, `.f3d` | lihtsustatud mudel (Claude, 23.10.2026) mõõtude järgi, eksporditud `lab2-cameras-reference`-ist | 106 × 55 × 42,5 mm | ainult välisgabariit; klambri jala mõõdud vt `lab2/veebikaamera-post/` |
