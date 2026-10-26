# AE1 printed Wi-Fi antenna - v0.4 prototype

AE1 serves the ESP32-C3's 2.4 GHz Wi-Fi for configuration and firmware access. It does not replace the external ELRS link antenna connected to J1.

## Circuit and BOM change

- Removed the physical Johanson `2450AT18A100E` ceramic antenna.
- Replaced its two-terminal schematic symbol with `RX_Parts:PCB_Meander_2G4`, a one-feed printed antenna symbol. Removed the obsolete pin-2 no-connect marker.
- AE1 uses `RX_V04:PCB_Meander_2G4_v04`, one connected custom B.Cu copper pad on `/WIFI`, with solder mask covering it and no solder paste or 3D component.
- AE1 is excluded from the purchased BOM and pick/place data. `PCB_FEATURE` is a fabrication description, not an orderable component MPN. Purchased component count decreases from 42 to 41.
- C21, C22 and L2 remain the C-L-C matching network. **C21 = 1.2 pF, C22 = 1.2 pF, L2 = 2.5 nH are initial reference populations only. They have not been matched to this radiator.** Their schematic/BOM `TuningNote` fields require prototype retuning.
- No MCU, CRSF or SX1281 firmware pins changed.

## Geometry

| Item | Specification |
| --- | --- |
| Antenna type | Custom meandered monopole prototype; single feed, no ground short |
| Copper layer | B.Cu |
| Feed, absolute KiCad coordinates | X 111.0 mm, Y 105.0 mm |
| Trace width | 0.18 mm |
| Traverse width / pitch | 1.20 mm / 0.30 mm |
| Traverses | 16 |
| Copper centreline length | 25.10 mm including feed and open tip |
| Antenna copper bounding box | X 110.91-112.29 mm, Y 99.81-105.09 mm |
| All-layer clearance region | X 110.65-112.70 mm, Y 99.45-105.15 mm |
| Clearance-region dimensions | 2.05 x 5.70 mm |

The exact generated path is in `references/antenna-geometry.json`. The native footprint and Gerbers are authoritative. The 0.12 mm gaps between neighbouring radiator runs and the small ground/edge distances are intentional prototype geometry and require fabrication review.

All six layers have a native rule area preventing plane fills and vias in the strip. Only AE1 and its intended feed enter the region. The rest of the PCB retains ground references. Keep metal, batteries, flight-controller ground planes and wires away from this strip in the installed assembly.

## Evidence and limits

[RadioMaster RP1 product photographs](https://radiomasterrc.com/products/rp1-expresslrs-2-4ghz-nano-receiver) show a compact edge antenna arrangement. They guide placement and packaging only: photographs do not establish hidden layer geometry, feed topology, dielectric properties or tuning values. This design is not a RadioMaster layout reconstruction.

The [TI AN043 antenna reference](https://www.ti.com/lit/pdf/swra117) describes a substantially larger 15.2 x 5.7 mm inverted-F antenna. Its validated performance cannot be transferred to this smaller custom monopole. This project does not claim that reference's measured performance.

[Espressif's ESP32-C3 RF guidance](https://espressif.github.io/esp32-c3-book-en/chapter_5/5.2/5.2.5.html) discusses the matching network and the need to match the actual antenna/PCB. Existing ceramic-antenna component values are not proof of a suitable printed-antenna match.

## Required prototype work

Measure antenna input impedance/return loss with a suitable calibrated VNA fixture and de-embed the feed as appropriate. Tune radiator length and C21/C22/L2 for the actual fabricated stack-up, board and enclosure. Check the Wi-Fi operating band, radiated efficiency/range and sensitivity to installed wires/metal. A good return loss alone does not establish radiation efficiency. Then test firmware access, CRSF, ELRS sensitivity/telemetry and failsafe on assembled hardware.

No antenna simulation, VNA measurements, efficiency measurements or receiver range tests have been performed. KiCad ERC/DRC establishes connectivity and geometry, not RF performance. If prototype measurements are unsatisfactory, the radiator or matching network will need a further revision.
