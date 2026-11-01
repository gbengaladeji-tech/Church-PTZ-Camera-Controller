# Reference review and limitations

Review date: 2026-11-01. Personal engineering sources were read-only. No
Obsidian note, VS Code history file, PDF, workbook, or handoff document was
modified or copied into the repository.

## Local sources inspected

| Source | Result and use |
|---|---|
| Repository and Git history | Inspected branches, commits, remote, tracked/untracked files, original simulations/tests |
| `software/controller_v1.py` | Recovered prototype; hash matches newest VS Code snapshot |
| VS Code `entries.json` + 38 snapshots | Timestamps/content compared; newest clean snapshot identified |
| `Church_PTZ_Complete_Handoff_2026-10-27.md` | Most recent external baseline before the current instruction; exposed historical contradictions and serial/pin risks |
| `Church_PTZ_Master_Execution_Prompt_2026-10-27.md` | Workflow/context only; not treated as proof of hardware receipt |
| `Church_PTZ_R5_Engineering_Review.md` | Earlier electrical risks, BOM maturity, and verification gates |
| `Church_PTZ_Master_BOM_R5.xlsx` | All sheet names/rows inspected through the XLSX XML; outdated 27-button/six-encoder baseline marked superseded |
| `Church_PTZ_R5_Unresolved_Parts.csv` | Open connector, power, PCB, protection, display, and test-fixture gaps reviewed |
| Obsidian Church PTZ folder | Eight project notes inspected; useful August learning/prototype history, superseded for hardware choices |
| Datavideo VISCA PDF | File present (V2.7-E4 family); local text extraction unavailable |
| Engineering handoff R0 PDF | File present; local text extraction unavailable and later Markdown sources supersede much of it |

## PDF limitation

The environment had no `pdftotext`, PyPDF, or similar parser. LibreOffice could
import the PDFs internally but had no working text export filter. Therefore no
claim is made that every PDF table was independently transcribed. Protocol
claims were limited to the original code/evidence and current official Datavideo
product/protocol pages. Exact packet ranges and connector details remain
verification tasks.

## Conflict resolution

From newest to oldest:

1. current explicit user instruction (2026-11-01);
2. complete Markdown handoff (2026-10-27), where it does not conflict;
3. R5 review/BOM (2026-10-10/11);
4. August repository and Obsidian learning notes;
5. older PDF handoff.

Examples:

- current 28 Omron switches overrides 27 APEM/Omron mixed controls;
- current three encoders overrides six;
- current 13 separate LEDs overrides 27 illuminated keys;
- W55RP20 overrides W5500/Arduino/Raspberry Pi deployment concepts;
- four physical RS-422 ports remain; ten front positions do not create six more;
- focus/iris/WB stay unqualified despite appearing in generic VISCA references.

## Official web sources checked

- [WIZnet W55RP20-EVB-PICO](https://docs.wiznet.io/Product/Chip/MCU/W55RP20/w55rp20-evb-pico)
- [WIZnet W55RP20 overview and examples](https://docs.wiznet.io/Product/Chip/MCU/W55RP20)
- [Datavideo PTR-10 MARK II](https://datavideo.com/global/product/PTR-10%2BMark%2BII)
- [Datavideo VISCA protocol page](https://datavideo.com/us/protocol/182/ptr-10t-mark-ii-visca-control-protocol)

No unrelated personal folders, email, Onshape document, purchasing system, or
other conversation was accessed.
