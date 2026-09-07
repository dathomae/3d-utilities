# Context

Records the task or story currently in progress. Updated at the start and end of every task; completed entries are removed. Not a historical log.

## Active Tasks

- **Capture the repository purpose** — updating `README.md` and the `memory-bank/` documents (`brief.md`, `requirements.md`, `context.md`, `concepts.md`, `terms.md`, `design/design.md`) to describe `3d-utilities` as a collection of small parametric utilities for 3D printing and milling.

## Recently Completed

- **Base repository setup** — the repository was converted from a generic template into this project's home, with the Python package layout, `setup.sh`, and the memory-bank skeletons in place (see `memory-bank/plans/base-repository-setup_plan.md`).
- **Initial mill-bed utilities** — `src/scaffold/mill_bed.py` encodes the vertical mill bed's M5 mounting-hole pattern, and `src/scaffold/mounting_sheet.py` builds a test sheet to verify that pattern against the machine.
