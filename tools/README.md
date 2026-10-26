# CAD export and audit helpers

The native KiCad files are the editable design source. Intermediate migration/layout-generation scripts are not included as a reconstruction workflow; they depended on earlier local revisions. The helpers here operate on the delivered project.

## Export

Run `python tools/export_release.py` with KiCad 10 installed. The script finds `kicad-cli` on PATH, accepts a `KICAD_CLI` environment override, and otherwise checks the KiCad 10 default Windows location. It uses the Python standard library.

It runs ERC and PCB DRC with schematic parity, then exports the netlist, BOM, six-layer Gerbers/drills, both-side placements, assembler BOM/CPL, SVG plots and native 3D renders. It checks the purchased-part count and drill extents and builds `exports/pcb/nano24-Gerbers-PROTOTYPE.zip`.

The schematic PNG is a convenience raster preview of the schematic SVG. Regenerate it from the newly exported SVG when the schematic appearance changes; the export script updates the SVG, not that PNG.

## Independent audit

Run `audit_final.py` with a Python environment that can import KiCad 10's `pcbnew` and `wx`. On the development PC:

```powershell
& 'C:\Program Files\KiCad\10.0\bin\python.exe' tools/audit_final.py
```

The script compares the current board, netlist and report files against the expected physical connectivity and known geometry constraints. It writes `exports/verification.json`. The dimensions/count assertions describe the current hardware revision and must be reviewed deliberately if the design changes.

`expected-connectivity.json` is the physical-net membership baseline for this revision. It is not a simulated or measured electrical test. The audit does not establish RF impedance, antenna efficiency, clock accuracy, power integrity, sourcing correctness or receiver operation.
