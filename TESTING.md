# nano24 validation plan

**No physical hardware tests have been completed.** This file separates recorded CAD checks from work that requires assembled hardware and RF measurements. CAD renders are not evidence of an assembled board.

## Recorded CAD checks

KiCad 10.0.7 reports zero ERC violations, PCB DRC violations, unconnected items and schematic-parity findings. The independent audit checks component counts, physical net membership, firmware pins, antenna clearance, cable-pad order, nine MCU exposed-pad ground vias and the near-surface ground-reference layers.

Reports: [ERC](exports/ERC.json), [DRC](exports/pcb/DRC.json), [geometry/connectivity audit](exports/verification.json).

## Before prototype fabrication

- [ ] Review ESP32-C3 package/pin numbering, power, strapping and exposed-pad implementation against component documentation.
- [ ] Review SX1281 power, matching, filter and TCXO interface.
- [ ] Resolve RF filter procurement replacement, RGB LED selection and actual component availability.
- [ ] Confirm fabricator stack-up and RF feed geometry.
- [ ] Obtain order-specific DFM approval for castellations, annular rings, via filling/capping and fine silkscreen.
- [ ] Confirm panel support, both-side assembly, stencil treatment, polarized-part orientation and CPL rotations.
- [ ] Agree a practical RF measurement fixture and antenna matching/tuning procedure.

## Initial power-up and clocks

- [ ] Inspect assembly and check supply resistance/shorts before applying power.
- [ ] Power from a suitable current-limited regulated supply and record startup/idle current.
- [ ] Measure the 3.3 V rail during startup, radio activity and Wi-Fi activity.
- [ ] Verify MCU enable/reset and boot-strap levels.
- [ ] Check the 40 MHz MCU clock and 52 MHz radio TCXO using suitable low-loading measurement methods.
- [ ] Check regulator/component temperatures and supply stability.

## Firmware and interfaces

- [ ] Build a version-pinned complete ELRS UART flash package with the nano24 hardware map.
- [ ] Verify GPIO9 BOOT-pad entry, UART download and normal restart after removing the BOOT connection.
- [ ] Confirm MCU boot, radio detection and RGB LED behavior.
- [ ] Verify CRSF channels and telemetry over the four-wire FC interface.
- [ ] Verify binding phrase, initial unbound startup, FC `bind_rx` and three-power-cycle binding.
- [ ] Verify binding persistence after power cycling.
- [ ] Verify UART recovery, Betaflight passthrough and Wi-Fi update paths.

## RF and system behavior

- [ ] Measure and tune the printed Wi-Fi antenna and C21/C22/L2 for the actual fabricated board.
- [ ] Measure radiated efficiency or suitable comparative over-the-air performance; a good return loss alone is insufficient.
- [ ] Verify Wi-Fi configuration/update reliability across the intended operating band.
- [ ] Characterize ELRS receiver sensitivity and telemetry output power with the intended external antenna.
- [ ] Test packet modes and behavior across intended supply and operating conditions.
- [ ] Verify failsafe, link loss, recovery and model-match behavior on a bench setup.
- [ ] Evaluate installed cable, metal and enclosure effects on both antennas.

Flight testing and any production-readiness claim come after suitable bench/RF validation and review of the results.

## Measurement record template

For each test, record:

| Field | Value to record |
| --- | --- |
| Board identity | Hardware revision, git commit, board serial/marking |
| Fabrication | Manufacturer, order, actual stack, finish and assembly changes |
| Firmware | ELRS source revision, target, settings and binary checksum |
| Setup | Instrument models, calibration, fixtures, antennas, supply and environment |
| Method | Procedure, limits and the reason those limits were chosen |
| Result | Measured values, logs/plots, pass/fail and observed anomalies |
| Follow-up | Required changes, retest conditions and outstanding questions |

Submit results with enough detail to reproduce the observation. Keep failed results and changed matching populations in the record.
