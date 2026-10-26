# Contributing to nano24

Useful contributions include circuit/package reviews, order-specific DFM feedback, firmware target packaging, antenna measurements and assembled-board test results.

For a hardware issue, include the board revision or git commit, the affected references/nets, evidence and a proposed correction where possible. For test results, use the record fields in [TESTING.md](TESTING.md). Identify actual measurements separately from simulations, estimates and CAD checks.

For CAD changes:

1. Edit the native KiCad project and keep project-relative library paths.
2. Update the schematic, PCB and affected local library definitions together.
3. Run ERC, PCB DRC and schematic-parity checks; explain any remaining findings.
4. Regenerate affected fabrication files, BOM/CPL, previews and audit reports.
5. Update the antenna/fabrication/firmware notes when the change affects them.
6. Include a concise description of the trigger, resulting behavior and validation in the pull request.

Keep credentials, Wi-Fi passwords, personal binding phrases, KiCad session files and temporary work out of commits. Preserve source attribution and applicable license notices. The current design is an untested prototype; passing CAD checks alone should not be described as working hardware.
