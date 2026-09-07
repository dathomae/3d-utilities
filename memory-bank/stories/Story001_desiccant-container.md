# Story001: Desiccant Container

## Goal

Establish the per-utility directory convention and build the two-compartment desiccant container: a trapezoidal tray with separate silica and alumina lids, vents, and STEP export.

This story does two things. First, it documents a new repository convention: every new utility lives in its own directory under `src/` (e.g. `src/<utility_name>/`) containing that utility's source code plus a `README.md`, applied to **new utilities only** (the existing `src/scaffold/` package is grandfathered). Second, it builds the desiccant container as the first utility under that convention: a two-compartment trapezoidal tray that holds filament desiccant at the bottom of a clear cereal storage box, with an independent lid per compartment (the two desiccants recharge at very different temperatures), vent slots for airflow, embossed `SILICA`/`ALUMINA` labels on the interior floors, and STEP export of three parts. The full specification is in the [plan](../plans/desiccant-container_plan.md).

## References

- [Plan: desiccant container](../plans/desiccant-container_plan.md)
- [Requirements](../requirements.md)
- [Design](../design/design.md)
- [Concepts](../concepts.md)
- [Brief](../brief.md)

## Dependencies

None — this is the first story for the project. It builds on the existing `src/scaffold/` package (which is left untouched) but has no prior story dependencies.

## Dependent Stories

None.

## Tasks

### Task Sizing

- No tasks are annotated `[Small]`; all coding tasks (2, 3, 4a, 4b, 5) route to `code-for-story-implementor`.
- Task 4b (embossing) was evaluated as borderline-small but is routed to `code-for-story-implementor` per the when-in-doubt rule (build123d `Text` placement and extrusion onto a face have non-obvious API details that a limited-context agent may not resolve).
- Writing tasks (1, 6) route to `technical-writer-for-story-implementor`.

### Task 1: Document the per-utility directory convention — Completed

Route: `technical-writer-for-story-implementor` (docs-only; no TDD).

Update the repository documentation so that each utility is consistently described as its own `src/<name>/` directory (source + `README.md`), replacing the current "one module per utility" / "one module under `src/scaffold/`" phrasing. The `src/scaffold/` package itself may still be mentioned as the grandfathered placeholder package.

   a. Update `README.md` (repo root): rewrite the repository-layout table and prose so modeling code lives in per-utility directories under `src/<utility_name>/`, with `src/scaffold/` called out as the grandfathered placeholder — Not Started
   b. Update `memory-bank/brief.md`: change the overview sentence ("Individual utilities add one module under `src/scaffold/`") and the "Self-containment" bullet in Key Design Considerations to the per-directory convention — Not Started
   c. Update `memory-bank/requirements.md`: change functional requirement 1 from "each as its own module under `src/scaffold/`" to "each as its own directory under `src/`" — Not Started
   d. Update `memory-bank/design/design.md`: update the "one module per utility" project-design bullet to the per-directory convention, and add the desiccant container to the parts list — Not Started
   e. Update `memory-bank/concepts.md`: update the "Utility project" concept row from "one Python module" to "one directory under `src/`" — Not Started

Completion criteria: all five files state the per-directory convention; a grep for the stale "one module under `src/scaffold/`" phrasing returns no matches (the `scaffold` package may still be mentioned as the grandfathered placeholder).

### Task 2: Body geometry (test-first) — Completed

Route: `code-for-story-implementor` (Logical TDD Lifecycle: write tests, then implement).

Create the `src/desiccant_container/` package and implement `make_body()`, the trapezoidal tray. The tray is an isosceles trapezoid in plan view, symmetric about its long centerline, centered on the origin (X along length, Y across width, Z up). Dimensions (mm): `LENGTH = 185.0`, `SHORT_END = 65.0` (silica/small compartment), `LONG_END = 75.0` (alumina/large compartment), `BODY_HEIGHT = 13.0`, `BOTTOM_THICKNESS = 2.0`, `WALL_THICKNESS = 4.0`, `DIVIDER_THICKNESS = 8.0`, `RIM_HEIGHT = 2.0`, `RIM_INSET = 2.0`, `DIVIDER_RATIO = 1/3`. The solid (unvented) internal dividing wall's centerline sits at `DIVIDER_RATIO` of `LENGTH` from the short end's outer face. A 2 mm rim sits on top of every wall (outer perimeter and divider), inset 2 mm from the wall's outer face.

   a. Write `tests/test_desiccant_container.py` body tests first, asserting: (1) `make_body()` returns a build123d `Part`; (2) overall bounding box is `185 × 75 × 13` mm; (3) 4 mm outer wall / 8 mm divider / 2 mm rim thicknesses; (4) divider centerline at 1/3 of `LENGTH` from the short end; (5) a closed interior cavity split into two compartments — Not Started
   b. Create `src/desiccant_container/__init__.py` (package marker re-exporting `make_body`) — Not Started
   c. Implement `make_body()` in `src/desiccant_container/container.py` using the dimension parameters above — Not Started
   d. Run `python -m pytest`; the body tests pass — Not Started

Completion criteria: `make_body()` returns a valid `Part` meeting the assertions above; `python -m pytest` is green.

### Task 3: Lid geometry (test-first) — Completed

Route: `code-for-story-implementor` (Logical TDD Lifecycle). Depends on Task 2 (body rim geometry).

Implement `make_lid_small()` (covers the 65 mm silica compartment) and `make_lid_large()` (covers the 75 mm alumina compartment). Each lid is a 2 mm top plate plus a 2 mm skirt (4 mm total), with the skirt dropping over the body's rim; the skirt's outer face is flush with the body's outer face with an `OOZE_CLEARANCE = 0.2` mm radial clearance to the rim's outer face. The two lids differ in footprint because the compartments differ in length; they are separated along the top by the divider's 4 mm rim ridge.

   a. Write lid tests first, asserting: each lid returns a `Part`; each lid's footprint matches its compartment; 2 mm top plate and 2 mm skirt; the skirt-to-rim radial gap equals 0.2 mm — Not Started
   b. Implement `make_lid_small()` and `make_lid_large()` in `src/desiccant_container/container.py` using the `OOZE_CLEARANCE` parameter — Not Started
   c. Re-export the lid builders from `src/desiccant_container/__init__.py` — Not Started
   d. Run `python -m pytest`; the lid tests pass — Not Started

Completion criteria: both lid builders return valid `Part`s that mate with the body's rim at the specified 0.2 mm clearance; `python -m pytest` is green.

### Task 4a: Add vent slots to the body walls and lid top plates (test-first) — Not Started

Route: `code-for-story-implementor` (Logical TDD Lifecycle). Depends on Tasks 2 and 3.

Add rectangular through-slots `5 mm long × 1 mm tall` (5 mm dimension horizontal, 1 mm vertical), with a `1 mm` solid margin between adjacent slots and from all edges. Slots go on the four outer side walls (both compartments) and on both lids' top plates — never on the bottom plate or the internal dividing wall.

   a. Write vent tests first, asserting slot count and geometry (5 × 1 mm slots, 1 mm margins) on the outer walls and lid top plates — Not Started
   b. Implement the vent-slot geometry in `src/desiccant_container/container.py`, cutting slots into the body's four outer side walls and both lid top plates — Not Started
   c. Run `python -m pytest`; the vent tests pass — Not Started

Completion criteria: the container and lids carry the specified vent slots with 1 mm margins, absent from the bottom plate and divider; `python -m pytest` is green.

### Task 4b: Add SILICA / ALUMINA floor embossing (test-first) — Not Started

Route: `code-for-story-implementor` (Logical TDD Lifecycle). Depends on Task 2 (and runs after 4a, sharing the same files).

Add raised build123d `Text` — `SILICA` (~0.5 mm tall) on the interior floor of the small compartment and `ALUMINA` on the interior floor of the large compartment — so each compartment is identifiable when opened for refill.

   a. Write embossing tests first, asserting the presence of raised text on each interior floor — Not Started
   b. Implement the embossing in `src/desiccant_container/container.py` using build123d `Text` extruded ~0.5 mm on each interior floor — Not Started
   c. Run `python -m pytest`; the embossing tests pass — Not Started

Completion criteria: `SILICA` and `ALUMINA` are embossed on the correct interior floors; `python -m pytest` is green.

### Task 5: STEP-export CLI and PARTS dict (test-first) — Not Started

Route: `code-for-story-implementor` (Logical TDD Lifecycle). Depends on Tasks 2, 3, 4a, 4b.

Add the `PARTS` dict keyed by name and a `main()` STEP-export CLI mirroring `src/scaffold/example.py` (`-o/--outdir` defaulting to `manufacture`, and `--show`). Exporting writes three files: `desiccant_body.step`, `desiccant_lid_small.step`, `desiccant_lid_large.step`.

   a. Add the `PARTS` dict registering `body`, `lid_small`, and `lid_large` — Not Started
   b. Implement `main()` (argparse `-o/--outdir`, `--show`) in `src/desiccant_container/container.py`, exporting the three parts to the outdir — Not Started
   c. Write CLI/export tests first where practical: running the CLI writes the three `.step` files into `manufacture/` (use a temp dir in tests) — Not Started
   d. Run `python -m pytest` and confirm running the CLI (`python -m desiccant_container.container`) writes all three `.step` files — Not Started

Completion criteria: `python -m pytest` is green; the CLI writes `desiccant_body.step`, `desiccant_lid_small.step`, and `desiccant_lid_large.step` into `manufacture/`.

### Task 6: Utility README — Not Started

Route: `technical-writer-for-story-implementor` (docs-only). Depends on Tasks 2–5 (describes the final geometry and CLI).

Write `src/desiccant_container/README.md` explaining the utility: what it is, its dimensions, how to fill it with activated alumina (large compartment) and color-changing silica gel (small compartment), the differing recharge temperatures (alumina ~200–250 °C, silica ~120 °C), that desiccant is always removed and dried separately (the PLA container is never oven-dried), and build/export/print/view instructions.

   a. Write `src/desiccant_container/README.md` covering dimensions, desiccant fill, recharge temperatures, and build/export/print/view instructions — Not Started

Completion criteria: `src/desiccant_container/README.md` exists and covers the utility's purpose, dimensions, desiccant usage, recharge temperatures, and build/export/print/view steps.

### Parallel Execution

- **Group A: Tasks 1 and 2 (parallel).** Task 1 (documentation) is file-disjoint from the entire coding chain (Tasks 2–5) and launches in parallel with Task 2, the chain's first task.
- The coding chain is strictly sequential: Task 2 → Task 3 → Task 4a → Task 4b → Task 5. Tasks 3, 4a, 4b, and 5 each modify `src/desiccant_container/container.py` and `tests/test_desiccant_container.py` (Tasks 3 and 5 also touch `__init__.py`), so none may run concurrently.
- Task 6 depends semantically on the coding chain (it documents the final CLI and geometry) and runs serially after Task 5.

No other parallel groups.

### Execution Order

1. **Group A** — Task 1 ∥ Task 2 (parallel)
2. Task 3 (sequential)
3. Task 4a (sequential)
4. Task 4b (sequential)
5. Task 5 (sequential)
6. Task 6 (sequential)

### Reintegration

**Group A (Tasks 1 and 2):**

- Merge order: any order — the file sets are fully disjoint (Task 1 touches only `README.md` and the five memory-bank docs; Task 2 touches only `src/desiccant_container/*` and `tests/test_desiccant_container.py`), with no shared infrastructure.
- Integration tests:
  - `python -m pytest` — confirms the merged tree is green (new package and tests present, existing `tests/test_example.py`, `tests/test_mill_bed.py`, `tests/test_mounting_sheet.py` still pass).
  - `grep -rn "one module under \`src/scaffold/\`" README.md memory-bank/ || true` — Task 1's doc-side acceptance check; expect no matches.
- Watch for conflicts in: none within the group (disjoint files). Spot-check at merge that the parts-list row Task 1 adds to `memory-bank/design/design.md` still names the builders/STEP files the chain implements (`make_body`, `make_lid_small`, `make_lid_large`, and the three `.step` files).

Note: Task 6 is not in a parallel group (semantic dependency on the code chain); its worktree merges serially after Task 5.

## Test-First Development

This project follows the Logical TDD Lifecycle. Coding tasks 2, 3, 4a, 4b, and 5 each integrate the test-and-implement cycle within the task (tests written before implementation), never as a separate "write tests" task. Writing tasks 1 and 6 do not require tests.

## Constraints

- Geometry is defined with build123d only; the sole third-party dependencies remain build123d, pytest, and ocp_vscode (no `pyproject.toml` change is required — `[tool.setuptools.packages.find]` with `where = ["src"]` already discovers the new package).
- Units are millimeters. Dimensions are Python parameters, never hard-coded literals.
- Material is clear PLA; desiccant is removed and recharged separately; the container is never oven-dried.
- STEP files are written to `manufacture/` and are gitignored artifacts.
- Tests live in the top-level `tests/` directory; the new package is imported as `from desiccant_container import ...`.
- The existing `src/scaffold/` package is left untouched by this story.

### Key dimensions

| Parameter | Value |
|-----------|-------|
| `LENGTH` | 185.0 |
| `SHORT_END` (silica/small compartment) | 65.0 |
| `LONG_END` (alumina/large compartment) | 75.0 |
| `BODY_HEIGHT` | 13.0 |
| `BOTTOM_THICKNESS` | 2.0 |
| `WALL_THICKNESS` | 4.0 |
| `DIVIDER_THICKNESS` | 8.0 |
| `LID_HEIGHT` (2 mm top + 2 mm skirt) | 4.0 |
| `RIM_HEIGHT` | 2.0 |
| `RIM_INSET` | 2.0 |
| `OOZE_CLEARANCE` | 0.2 |
| `DIVIDER_RATIO` (from the short end) | 1/3 |
| Assembled height | 15.0 |
| Vent slots | 5 mm × 1 mm, 1 mm margins |

## Intent

- **Task 1**: Make the repository documentation consistently describe the per-utility directory convention so future utilities follow it.
- **Task 2**: Produce a valid parametric body (tray with two compartments, solid divider, rim) matching the dimension table.
- **Task 3**: Produce two lids that mate with the body's rim at the specified clearance.
- **Task 4a**: Perforate the body and lids with the specified vent slots for desiccant airflow.
- **Task 4b**: Emboss compartment labels so each compartment is identifiable when opened.
- **Task 5**: Provide a CLI that exports the three parts to STEP, mirroring the scaffold's export workflow.
- **Task 6**: Document the utility so a new user can build, export, print, fill, and recharge it.

## Acceptance Criteria

- `README.md`, `brief.md`, `requirements.md`, `design/design.md`, and `concepts.md` document the per-utility-directory convention; no stale "one module under `src/scaffold/`" phrasing remains.
- `src/desiccant_container/` contains `__init__.py`, `container.py`, and `README.md`; `tests/test_desiccant_container.py` exists and passes.
- The geometry matches the dimension table (185 × 75 × 13 mm body; 65/75 mm ends; 8 mm divider at 1/3; 2 mm rim; 0.2 mm lid clearance; 5 × 1 mm vents with 1 mm margins; `SILICA`/`ALUMINA` embossing).
- `python -m pytest` passes; the CLI exports `desiccant_body.step`, `desiccant_lid_small.step`, and `desiccant_lid_large.step` to `manufacture/`.

## Requesting Clarification

If at any point during implementation there is confusion or ambiguity about the goal or how to accomplish it, stop and ask the user for clarification.

## Notes

- **End-to-end verification** (plan Step 5) is folded into Task 5's completion criteria and the overall Acceptance Criteria rather than a standalone task.
- The geometry spec is intentionally concise here; the authoritative dimension table and design decisions are in [the plan](../plans/desiccant-container_plan.md).
