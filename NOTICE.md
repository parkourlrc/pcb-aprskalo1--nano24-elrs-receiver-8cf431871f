# Provenance and modifications

This personal receiver schematic and compact PCB are adapted from the OpenDrone OpenRX Lite-UFL hardware project, under CERN-OHL-S-2.0. The upstream license is retained in `LICENSE`. This is a derivative prototype, not a RadioMaster design or an official OpenDrone product release.

Reference revision: `b8c35f6de77468bdd4c66319bc5ced1b88bc6ef6` of https://github.com/OpenDrone-hw/OpenRX-Lite-UFL . Circuit source: `hardware/esp32c3_sx1281_lite.kicad_sch`. The associated component-library snapshot was `fdf8319b3512925a7566532ae4b38a298cf54c24` of https://github.com/OpenDrone-hw/KiCad-Library .

Changes made 26 October 2026:

1. Created a separate flat KiCad 10 schematic/project and local symbol/footprint library tables; upstream sources are unchanged.
2. Replaced upstream branding/artwork and placeholder comments with project title, revision, wiring, firmware mapping and prototype notes. Attribution and license are retained.
3. Made the MCU's required ESP32-C3FH4 variant explicit in the displayed component value.
4. Corrected local symbol electrical pin types for radio, regulator, clock, LED, filter and antenna using the component roles in their documentation. The MCU's VDD_SPI pin is power input in this externally supplied circuit mode, which Espressif permits. Pin numbering and symbol geometry are retained.
5. Moved the redundant regulator-output PWR_FLAG to the filtered MCU RF supply after L3; this models a supply reached through a passive inductor. It does not add a physical component.
6. Snapped L3 and both connected wire endpoints onto the schematic connection grid, preserving connectivity.
7. Removed the unused GPIO10-to-ground tie and marked that pin NC. All other physical pin/net memberships match the reference in the automated comparison.
8. Excluded bare copper test/solder pads from purchased-parts BOM and pick/place files. Physical parts and reference supplier fields are otherwise retained.

Custom reference footprints retain their upstream names. Standard symbol shapes are derived from KiCad library symbols embedded in the upstream schematic; the KiCad libraries use the Creative Commons CC-BY-SA-4.0 license with their library exception, described at https://www.kicad.org/libraries/license/ . No claim of exclusive authorship over those source assets is made.

No assembled hardware, RF performance qualification or manufacturing release is implied by this revision.

Compact PCB prototype 0.3 was added on 26 October 2026 in a separate project. Unlike the earlier 37 x 28 mm four-layer experiment, this revision derives its dense two-sided core placement and portions of its six-layer routing from upstream `hardware/OpenRX-Lite-UFL.kicad_pcb` at the pinned revision above. RadioMaster RP1 photographs provided an additional visual benchmark; no RadioMaster netlist or proprietary PCB file was used.

The compact derivative uses a 13 x 14 mm outline, corrected 3.7 mm C3 exposed-pad footprint and ground stitching, new two-sided cable/BOOT pads, a relocated MCU-side crystal circuit, a relocated ceramic Wi-Fi antenna and matching parts, an all-layer antenna clearance region, revised reset-component placement, renewed digital/power routes, ground/power pours and a proposed six-layer stack. Local `RX_Compact` footprints retain source copper geometry except for the documented corrected MCU footprint and new bare pads. Silkscreen/mask drawing artefacts were removed and assembly references, model paths and circuit metadata were reconciled with the schematic. The native final CAD files are the authoritative editable design; intermediate layout scripts are not a fabrication release workflow.

Available upstream custom 3D models are included with the hardware sources under the existing license. The generic KiCad QFN32 footprint and other standard-library-derived assets retain the KiCad library licensing described above. Local footprint names are unique to this derivative so the delivered library definitions match the board.

Revision 0.4, 26 October 2026, replaces the ceramic Wi-Fi antenna with an original parameterized B.Cu meandered-monopole prototype, its one-feed schematic symbol and compact all-layer plane/via clearance strip. The geometry is not a recovered or validated RadioMaster antenna. RP1 photographs guided packaging only. Initial C21/C22/L2 values are retained as provisional tuning populations. AE1 is excluded from purchased BOM/CPL data. The board is shortened to 13 x 11.1 mm with chamfered corners, four wide castellated bottom-edge cable pads and aligned RX/TX/+/- labels. The MCU crystal cluster moves to the front with two signal escape vias; EN/BOOT and power/UART routing are renewed. Schematics, local footprints, BOM/CPL, firmware notes, fabrication exports and previews are revised together. All prior attribution and license terms remain applicable. RF validation and final fabrication/assembly approval remain outstanding.

Branding update: the product/board name is nano24. The visible C3/version marking is replaced by the lowercase nano24 name. Electrical design is unchanged. Revision metadata remains for engineering traceability.
