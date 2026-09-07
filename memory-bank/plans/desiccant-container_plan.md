# Desiccant Container Plan

## Objective

1. **Establish a project convention**: every new utility lives in its own directory under `src/` (e.g. `src/<utility_name>/`), containing that utility's source code plus a `README.md` that explains what the utility is and how to use it. The convention applies to **new utilities only**; the existing `src/scaffold/` package is left as-is (grandfathered) for now.
2. **Build the desiccant container** as the first utility created under that convention.

## Background

The container holds filament desiccant at the bottom of a clear cereal storage box. It is a two-compartment tray:

- **Large compartment** (~2/3 of the length, at the 75 mm end) holds **activated alumina** desiccant.
- **Small compartment** (~1/3 of the length, at the 65 mm end) holds **color-changing silica gel**.

The two desiccants require very different recharge temperatures (alumina ~200–250 °C, silica ~120 °C), so they must stay physically separate during filling and removal. The container therefore has **two independent lids**, one per compartment, so each desiccant can be refilled/recharged without opening the other. The container is printed in **clear PLA** so the color-change indicator is visible through the container and the cereal box. Desiccant is always removed and dried separately at room temperature; the PLA container is never oven-dried.

## Design Specification

### Shape and dimensions

Top view is an **isosceles trapezoid**, symmetric about its long centerline. All dimensions in millimeters; coordinate origin at the trapezoid's center on the bottom face, X along length, Y across width, Z up.

| Parameter | Symbol | Value |
|-----------|--------|-------|
| Length (X, between the two end walls) | `LENGTH` | 185.0 |
| Short end width (Y, at the 65 mm end) | `SHORT_END` | 65.0 |
| Long end width (Y, at the 75 mm end) | `LONG_END` | 75.0 |
| Assembled height (Z) | — | 15.0 |
| Body total height | `BODY_HEIGHT` | 13.0 |
| Bottom plate thickness | `BOTTOM_THICKNESS` | 2.0 |
| Outer wall thickness | `WALL_THICKNESS` | 4.0 |
| Internal dividing-wall thickness | `DIVIDER_THICKNESS` | 8.0 |
| Lid total height | `LID_HEIGHT` | 4.0 |
| Lid top-plate thickness | `LID_TOP_THICKNESS` | 2.0 |
| Rim height (vertical engagement) | `RIM_HEIGHT` | 2.0 |
| Rim inset (from the wall's outer face) | `RIM_INSET` | 2.0 |
| Radial clearance, lid skirt ↔ rim (ooze allowance) | `OOZE_CLEARANCE` | 0.2 |
| Divider position (fraction of `LENGTH` from the short end) | `DIVIDER_RATIO` | 1/3 |

The taper is intentional and matches the cereal container's floor. The short end (65 mm) is the silica/small compartment; the long end (75 mm) is the alumina/large compartment. The taper is gentle (~1.5° per side) and presents no meaningful overhang.

### Body (one part)

- Outer footprint: the trapezoid above, centered on the origin.
- Bottom plate 2 mm; interior cavity depth 11 mm; body total height 13 mm.
- Outer walls 4 mm thick.
- **Internal dividing wall**: 8 mm thick, **solid** (no vents), placed so its centerline is `DIVIDER_RATIO` (1/3) of the length from the short end's outer face. It keeps the two desiccants apart.
- **Rim**: on top of every wall (outer perimeter **and** the divider), 2 mm tall, inset 2 mm from the wall's outer face. For the outer walls this yields a 2 mm rim flush with the interior face and a 2 mm shelf on the exterior. For the 8 mm divider it steps 2 mm in from **both** faces, leaving a 4 mm rim in the middle with a 2 mm shelf on each side. Rim height is uniform everywhere.

### Lids (two parts)

- **`lid_small`** covers the silica compartment (65 mm end); **`lid_large`** covers the alumina compartment (75 mm end). The two lids differ in footprint because the compartments differ in length.
- Each lid: 2 mm top plate + 2 mm skirt = 4 mm tall. Skirt is 2 mm thick (nominal) and drops over the rim with its outer face flush with the body's outer face and a **0.2 mm radial clearance** to the rim's outer face.
- The two lids are separated along the top by the divider's 4 mm rim ridge, which keeps each compartment independently openable and gives each lid a positive grip.

### Vents

- Rectangular through-slots **5 mm long × 1 mm tall**, oriented with the 5 mm dimension horizontal and the 1 mm dimension vertical.
- **1 mm solid margin** between adjacent slots and from all edges.
- Placed on: both lids' top plates and the four outer side walls (both compartments).
- **Not** on: the bottom plate or the internal dividing wall.

### Embossing

- Raised text **`SILICA`** on the interior floor of the small compartment and **`ALUMINA`** on the interior floor of the large compartment (build123d `Text`, ~0.5 mm tall), so the compartments are identifiable when opened for refill.

### STEP exports

Three files written to `manufacture/` (gitignored artifacts):

| File | Part |
|------|------|
| `desiccant_body.step` | Body (tray with divider and rim) |
| `desiccant_lid_small.step` | Small (silica) compartment lid |
| `desiccant_lid_large.step` | Large (alumina) compartment lid |

## Convention Specification

New utilities follow this layout:

```
src/<utility_name>/
    __init__.py
    <utility_name>.py      # or <module>.py: parametric geometry + STEP-export CLI
    README.md              # what the utility is, how to build/export/print/use it
tests/
    test_<utility_name>.py # pytest tests (top-level tests/ dir, as today)
manufacture/               # generated .step files (gitignored)
```

Notes:

- Each utility directory is a Python **package** so tests import `from <utility_name> import ...`; `[tool.setuptools.packages.find]` with `where = ["src"]` already discovers it, so no `pyproject.toml` change is required for a new utility.
- Tests continue to live in the top-level `tests/` directory, matching the existing `tests/test_example.py` / `tests/test_mill_bed.py` pattern.
- The existing `src/scaffold/` package (including the shared `mill_bed.py` reference data and its consumers) is left untouched by this plan.

## Impacted files

### Create

| Path | Purpose |
|------|---------|
| `src/desiccant_container/__init__.py` | Package marker; re-exports the part builders. |
| `src/desiccant_container/container.py` | Parametric geometry for body + both lids, `PARTS` dict, STEP-export CLI. |
| `src/desiccant_container/README.md` | Utility description, dimensions, desiccant usage, recharge temperatures, build/export/print instructions. |
| `tests/test_desiccant_container.py` | pytest tests for body, lids, vents, and fit clearance. |

### Update

| Path | Change |
|------|--------|
| `README.md` | Repository layout: describe `src/<utility>/` per-utility directories instead of "one module per utility". |
| `memory-bank/brief.md` | Update "Individual utilities add one module under `src/scaffold/`" to the per-directory convention. |
| `memory-bank/requirements.md` | Update functional requirement 1 to "each as its own directory under `src/`". |
| `memory-bank/design/design.md` | Update the "one module per utility" statement and add the desiccant container to the parts list. |
| `memory-bank/concepts.md` | Update the "Utility project" concept to "one directory under `src/`". |

## Design decisions (resolved)

1. **Two lids, not one** — desiccants recharge at different temperatures and must be kept separate; each compartment opens independently.
2. **Dividing wall 8 mm** (double a 4 mm wall) — it carries a rim + shelf on both faces (`2+2+2+2`).
3. **Rim engagement 2 mm**, uniform on outer walls and divider; lid 2 mm top + 2 mm skirt.
4. **Body 13 mm + lid 4 mm = 15 mm assembled** (the lid's 2 mm skirt overlaps the body rather than stacking).
5. **Ooze allowance 0.2 mm** radial clearance (0.4 mm nozzle / 0.2 mm layer height).
6. **Vents** = 5 mm × 1 mm rectangular slots, 1 mm solid margin on all sides, on lids + four outer walls, none on bottom/divider.
7. **Material**: clear PLA; desiccant removed and recharged separately; container never oven-dried.
8. **Embossing**: `SILICA` / `ALUMINA` on the interior floor.
9. **Three STEP files**: body, small lid, large lid.
10. **Convention scope**: new utilities only; `src/scaffold/` grandfathered; tests stay in `tests/`.

## Steps

### Step 1: Document the per-utility directory convention

**Goal**: the repository documentation consistently describes each utility as its own `src/<name>/` directory (source + README), applied to new utilities going forward.

**Completion criteria**: `README.md`, `brief.md`, `requirements.md`, `design/design.md`, and `concepts.md` all state the new convention; a grep for the old "one module under `src/scaffold/`" phrasing returns no stale statements (the `scaffold` package itself may still be mentioned as the grandfathered/placeholder package).

- (a) Update `README.md` repository-layout table and prose.
- (b) Update `memory-bank/brief.md` (Key Design Considerations → Self-containment and the overview).
- (c) Update `memory-bank/requirements.md` functional requirement 1.
- (d) Update `memory-bank/design/design.md` project-design bullet and parts-list intro.
- (e) Update `memory-bank/concepts.md` "Utility project" concept row.

### Step 2: Body geometry (test-first)

**Goal**: `make_body()` returns a valid build123d `Part` for the trapezoidal tray with two compartments, the 8 mm solid divider, and the 2 mm rim.

**Completion criteria**: tests asserting (1) `Part` return type and validity, (2) overall bounding box `185 × 75 × 13` mm, (3) 4 mm outer wall / 8 mm divider / 2 mm rim thicknesses, (4) divider centerline at 1/3 of length from the short end, and (5) a closed interior cavity, all pass before and after implementation.

- (a) Write `tests/test_desiccant_container.py` body tests first (per the Logical TDD Lifecycle: structural definition → tests → implementation).
- (b) Implement `make_body()` in `src/desiccant_container/container.py` using the dimension parameters above.

### Step 3: Lid geometry (test-first)

**Goal**: `make_lid_small()` and `make_lid_large()` return valid parts that mate with the body's rim at 0.2 mm clearance.

**Completion criteria**: tests asserting each lid's footprint matches its compartment, 2 mm top plate, 2 mm skirt, and that the skirt-to-rim radial gap equals 0.2 mm, pass.

- (a) Write lid tests first.
- (b) Implement the two lid builders with the `OOZE_CLEARANCE` parameter.

### Step 4: Vents, embossing, STEP-export CLI, and utility README

**Goal**: the container has its vent slots and embossed labels, exports three STEP files, and is documented.

**Completion criteria**: tests for vent-slot count/geometry and the presence of embossed text pass; running the CLI writes `desiccant_body.step`, `desiccant_lid_small.step`, and `desiccant_lid_large.step` into `manufacture/`; `src/desiccant_container/README.md` explains the utility (dimensions, desiccant fill, recharge temperatures, build/export/print/view).

- (a) Add vent-slot geometry to the body side walls and both lid top plates (5 × 1 mm slots, 1 mm margins).
- (b) Add `SILICA`/`ALUMINA` embossing to the interior floor.
- (c) Add the `PARTS` dict and the `main()` STEP-export CLI (mirroring the `scaffold.example` CLI: `-o/--outdir`, `--show`).
- (d) Write `src/desiccant_container/README.md`.
- (e) Write any additional tests for the CLI export behavior (test-first where practical).

### Step 5: End-to-end verification

**Goal**: a fresh environment can build, test, and export the utility.

**Completion criteria**: `python -m pytest` is green; `python -m desiccant_container.container` (or the documented CLI) writes all three `.step` files; `git status` shows only the intended new/changed files.

- (a) Run `python -m pytest`.
- (b) Run the CLI and confirm the three STEP files appear in `manufacture/`.
- (c) Optionally view body and lids with `ocp_vscode` (`--show`).
- (d) Review `git status` for unintended changes.

## Story-Writer Guidance

This plan is intended to be turned into **one story** via `scripts/add-new-story.pdd.script.md`. The executor (technical-writer + architect-for-story-planning) supplies the parameters and decomposes the steps into test-first tasks.

- **story_name**: `desiccant-container`
- **description**: "Establish the per-utility directory convention and build the two-compartment desiccant container: a trapezoidal tray with separate silica and alumina lids, vents, and STEP export."

### Architect-for-story-planning review (incorporated)

- **Keep the ventless-then-vented split**: build body and lid base geometry first, then add vents + embossing as an additive detail pass. Do **not** fold vents/embossing into the base-geometry tasks — that would oversize them. The envelope/rim/clearance tests from the base tasks are invariant under perforation, so the seam is natural.
- **Split the original Task 4** at the geometry-vs-infrastructure seam: vents + embossing (4), then CLI + export tests + README (5).
- **Fold end-to-end verification (Step 5) into task completion criteria** — no standalone verification task; attach the terminal full-suite `python -m pytest` + CLI `.step` export + `git status` check to the last task in the chain.
- **No coding task is `[Small]`**; all route to `code-for-story-implementor` (each introduces net-new builders or multi-cycle geometry).

### Suggested task decomposition (all tasks `Not Started`)

1. **Document the per-utility directory convention** — Step 1. Docs-only (`README.md`, `brief.md`, `requirements.md`, `design/design.md`, `concepts.md`). Route to `technical-writer-for-story-implementor`. No TDD.
2. **Body geometry (test-first)** — Step 2. New `src/desiccant_container/container.py` with `make_body()`; tests first. Route to `code-for-story-implementor`.
3. **Lid geometry (test-first)** — Step 3. `make_lid_small()` + `make_lid_large()`; tests first. Route to `code-for-story-implementor`. Sequential after task 2.
4. **Vents and embossing (test-first)** — Step 4 geometry. 5 × 1 mm slots + `SILICA`/`ALUMINA` embossing on body and lids; tests first. Route to `code-for-story-implementor`. Sequential after task 3.
5. **STEP-export CLI, export tests, and utility README** — Step 4 infrastructure. `PARTS` dict + `main()` CLI + export tests + `src/desiccant_container/README.md`. Route to `code-for-story-implementor`; the README prose may route to `technical-writer-for-story-implementor`. Sequential after task 4; carries the folded end-to-end verification.

All coding tasks follow the Logical TDD Lifecycle with the test-and-implement cycle integrated inside each task, never as a separate "write tests" task. The chain 2 → 3 → 4 → 5 is strictly sequential (shared `container.py` / test file plus a semantic dependency).

### Parallelism

- **Group A (tasks 1, 2)**: parallelizable — disjoint file sets (docs vs. new package). Merge any order. After merging run `python -m pytest` (new `tests/test_desiccant_container.py` alongside the pre-existing `tests/test_example.py` / `tests/test_mounting_sheet.py`; no new failures). Watch for conflicts in `memory-bank/context.md` (implementing agents update it at task start/end in both worktrees).
- No other parallel groups: the coding chain shares `container.py` and the test file and is sequential.

## Completion criteria (overall)

- `README.md`, `brief.md`, `requirements.md`, `design/design.md`, and `concepts.md` document the per-utility-directory convention; no stale "one module under `src/scaffold/`" phrasing remains.
- `src/desiccant_container/` contains `__init__.py`, `container.py`, and `README.md`; `tests/test_desiccant_container.py` exists and passes.
- The geometry matches the dimension table (185 × 75 × 13 mm body, 65/75 mm ends, 8 mm divider at 1/3, 2 mm rim, 0.2 mm lid clearance, 5 × 1 mm vents with 1 mm margins, `SILICA`/`ALUMINA` embossing).
- `python -m pytest` passes; the CLI exports `desiccant_body.step`, `desiccant_lid_small.step`, and `desiccant_lid_large.step` to `manufacture/`.
