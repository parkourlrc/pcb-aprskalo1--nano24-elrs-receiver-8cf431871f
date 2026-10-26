# Revision 0.4 - prototype fabrication review

The native project describes a **13 x 11.1 mm, six-layer, nominal 1.0 mm PCB**. Dimensions use Edge.Cuts centre lines. This is an unpackaged, double-sided precision assembly with 0201 parts, QFN/X2SON packages and a small RGB LED. Agree panel rails, tooling, fiducials, stencil/reflow treatment and inspection with the assembler; a production panel is not included.

## Cable pads and holes

Four bottom-edge cable lands are **1.8 mm wide x 1.6 mm long**, exposed on both faces. Their centres are X 101.25, 104.55, 107.85, 111.15 mm at Y 110.30 mm, in RX/TX/+5V/GND order from the front. Each land has a **0.60 mm plated hole centred on the routed board edge**, producing a castellation/half-hole. Native pads are explicitly marked castellated. Confirm 0.60 mm castellations, panel support, edge routing sequence, plating quality and burr control with the fabricator.

Each land also contains two small 0.20 mm plated stitching holes. These small holes, and the SMD via-in-pad holes elsewhere, require filled/copper-capped processing. **The four 0.60 mm castellated edge holes must remain open.** Selective filling/capping and castellations must be confirmed for the final order. Ordinary tenting does not replace via filling. Nine ground vias sit within the C3 exposed-pad region. Provide cable strain relief after soldering.

The front BOOT pad is 0.8 mm diameter. Cable-pad silk labels are 0.7 mm high with 0.10 mm strokes; agree the legibility of these fine markings with the fabricator.

## Proposed stack

| Layer / dielectric | Thickness | Role |
| --- | --- | --- |
| F.Cu | 0.035 mm | Components, ELRS RF, local routes and 40 MHz crystal |
| Dielectric 1 | 0.100 mm | Ground reference spacing |
| In1.Cu | 0.0175 mm | Ground, no signal tracks |
| Dielectric 2 | 0.140 mm | Prepreg |
| In2.Cu | 0.0175 mm | 3.3 V distribution and limited signal routes |
| Dielectric 3 | 0.380 mm | Core |
| In3.Cu | 0.0175 mm | Signal routes and ground fill |
| Dielectric 4 | 0.140 mm | Prepreg |
| In4.Cu | 0.0175 mm | Ground, no signal tracks |
| Dielectric 5 | 0.100 mm | Ground reference spacing |
| B.Cu | 0.035 mm | MCU, Wi-Fi matching/feed and printed antenna |

Nominal FR4 epsilon-r is 4.2. This proposed stack is recorded in the PCB but is not a confirmed fabricator stack/order code. Confirm actual dielectric properties, thicknesses and RF feed impedance before manufacture. The antenna requires tuning for the final stack. The [JLCPCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities) are a starting point for quotation, not approval of this particular geometry/process combination.

## RF and assembly review

AE1 is an integral, mask-covered B.Cu printed radiator; **do not fit the former ceramic antenna**. Do not put plane copper, vias or unrelated traces in its 2.05 x 5.7 mm all-layer clearance strip. Do not add paste or a component at AE1. The printed antenna is unmeasured and custom: read `ANTENNA-DESIGN.md`. C21/C22/L2 are provisional values requiring RF tuning.

The SX1281/filter/U.FL feed remains on F.Cu without signal vias. The 40 MHz crystal cluster moves to F.Cu and has two MCU pin escape vias in this revision. Clock accuracy and RF performance have not been measured.

Declared minimum track/space is 0.09 mm. New digital routes generally use 0.10 mm tracks. Most through vias have 0.20 mm drills and 0.35-0.45 mm copper diameters. Minimum annular width is 0.075 mm, hole-to-copper clearance 0.20 mm, hole-to-hole clearance 0.25 mm and routed-edge copper clearance 0.20 mm, with native castellated-pad edge treatment. No DRC exclusions are used.

The BOM/CPL contains 41 purchased parts across both faces. Positions/rotations are native KiCad values: approve the assembler's placement preview, particularly bottom-side and polarized parts. Confirm the RF filter's legacy `2450FM07D0034T` procurement replacement and the RGB LED's value/MPN spelling and 3.3 V suitability. Supplier selections are inherited references, not verified current stock or approved substitutes.

## Manufacturing files and coordinates

Gerbers, drills and CPL share the lower-left plot origin at absolute KiCad X 99.7 mm, Y 110.3 mm. Output X increases rightward and Y upward. Bottom-side coordinates use the same board frame, with no additional X mirroring. Drill coordinates are checked against the 13 x 11.1 mm extents; the castellated holes lie at Y=0.

`exports/pcb/manufacturing/` contains six copper layers, both masks, pastes and silkscreens, outline, job file and separate plated/non-plated drill files. The empty NPTH file is intentional. These files are packaged as `nano24-Gerbers-PROTOTYPE.zip` for review/quotation.

Final ERC, DRC, airwire and schematic-parity counts are zero. Before ordering a usable receiver, complete order-specific DFM/assembly review, antenna matching/efficiency work and prototype tests for supply, UART/BOOT recovery, Wi-Fi updates, CRSF, ELRS binding, sensitivity, telemetry and failsafe.
