# Desiccant Container — Split Design Plan

## Objective

Replace the single-tray-with-shared-divider design with two independent containers rising from a common monolithic base plate. Each container has a full-perimeter rim on all four walls and the containers are separated by a 5 mm gap. The total footprint (length = 185 mm) is preserved.

## Background

The current design has a single trapezoidal body with an 8 mm solid internal dividing wall. The new design changes to two completely independent containers that share a common base:

- Each container has its own full perimeter walls (4 mm thick) on all four sides
- Each container has a full perimeter rim (2 mm inset, 12 mm tall) on all four sides
- The containers are separated by a 5 mm gap between their adjacent outer wall faces
- The existing 8 mm divider wall is eliminated
- The existing divider rim ridge and lid-seat slot boxes are eliminated
- Total interior capacity loss: ~5 mm (the gap width), under 3%
- DIVIDER_RATIO is re-interpreted to set the gap center position

## Design decisions (resolved)

1. **No divider**: the shared 8 mm wall is replaced by two independent 4 mm walls (one per container) separated by a 5 mm gap. Total wall material at boundary unchanged (8 mm).
2. **Gap center = old divider center**: `DIVIDER_RATIO = 1/3` from short end now positions the center of the 5 mm gap.
3. **Full perimeter rim on each container**: no need for lid-seat slot boxes or divider rim ridge — each container's rim is a simple contiguous ring.
4. **Vent slots**: generated on all four side walls of each container via the existing slot-generation logic. The adjacent (gap-facing) walls receive vents naturally; no special-casing.
5. **Total length = 185 mm**: unchanged from current design. Small container interior ≈ 51.2 mm, large container interior ≈ 112.8 mm (was 53.7 / 115.3).
6. **Labels unchanged**: SILICA on small container floor, ALUMINA on large container floor.
7. **Lids unchanged in construction**: each lid matches its container's outer trapezoidal footprint. No need for the lid-seat slot.

## Impacted files

### Modify

| Path | Change |
|------|--------|
| `src/desiccant_container/container.py` | Structural rewrite of `make_body()` and helper functions; remove divider-related code; reinterpret `DIVIDER_RATIO` |
| `src/desiccant_container/README.md` | Update description, dimensions table (add `GAP`, remove `DIVIDER_THICKNESS`), rim description |
| `tests/test_desiccant_container.py` | Update test expectations for new geometry (no divider, different compartment sizes, gap) |

### Remove from code

- `_lid_seat_slot_boxes()` function
- `_interior_half_width()` function (no longer needed externally — vent calc will call it differently)
- `DIVIDER_THICKNESS` constant
- All divider construction logic in `make_body()`
- Divider rim shelf cutting in `make_body()`

### Add to code

- `GAP = 5.0` constant
- Helper: `_container_vertices(outer_left_x, outer_right_x)` — returns tuple of (outer_vertices, inner_vertices) for a trapezoidal container between two X stations
- Helper: `_container_slot_boxes(left_x, right_x)` — returns vent slot boxes for all four walls of a container

### Regenerate

- `manufacture/desiccant_body.step`
- `manufacture/desiccant_lid_small.step`
- `manufacture/desiccant_lid_large.step`

## Steps

### Step 1: Update tests to reflect new split-container geometry

**Goal**: Tests are updated to expect the new geometry before any code changes (red phase).

**Completion criteria**: Running tests fails against current code (tests expect new geometry, code still has old design).

- (a) Update `tests/test_desiccant_container.py`:
  - Remove tests asserting divider thickness / divider centerline / divider rim ridge
  - Update bounding-box assertions: body height unchanged (23 mm), Z bounds unchanged (0 to 23 mm)
  - Update compartment interior length assertions: small ≈ 51.2 mm, large ≈ 112.8 mm
  - Add test asserting 5 mm gap between container outer walls
  - Add test asserting each container has a full perimeter rim (no shared wall)
  - Update vent slot tests: both inner walls (gap-facing) should have slots
  - Keep all other tests (wall thickness 4 mm, rim inset 2 mm, rim height 12 mm, bottom thickness 2 mm, label positions, lid clearances)

### Step 2: Implement split-container `make_body()`

**Goal**: `make_body()` produces two independent riser boxes on a shared base, with full perimeter rims.

**Completion criteria**: All body geometry tests pass.

- (a) Add `GAP = 5.0` constant; remove `DIVIDER_THICKNESS = 8.0`
- (b) Compute gap center from `DIVIDER_RATIO`; derive container X bounds
- (c) Implement `_container_vertices(outer_left_x, outer_right_x)`:
  - Returns (outer_vertices, inner_vertices) as lists of Vector for a trapezoidal container segment
  - Outer: trapezoid with left half-width at `_outer_half_width(left_x)` and right half-width at `_outer_half_width(right_x)`, centered at `(left_x + right_x) / 2`
  - Inner: same but inset by `WALL_THICKNESS` perpendicular to each face
- (d) Rewrite `make_body()`:
  - Step 1: extrude full 185 mm outer trapezoid to `BOTTOM_THICKNESS` (shared base)
  - Step 2: extrude small container outer footprint from base top to `BODY_HEIGHT`; hollow out interior
  - Step 3: extrude large container outer footprint from base top to `BODY_HEIGHT`; hollow out interior
  - Step 4: cut perimeter rim ring for small container (outer-minus-RIM_INSET trapezoid, BODY_HEIGHT - RIM_HEIGHT to BODY_HEIGHT)
  - Step 5: cut perimeter rim ring for large container
  - Step 6: cut SILICA and ALUMINA label recesses (update label center computation for new compartment bounds)
  - Step 7: cut vent slots on all four walls of each container (use `_container_slot_boxes()` helper)
- (e) Remove all divider-related code: divider wall solid, divider rim shelves, `_lid_seat_slot_boxes()`

### Step 3: Update lid builders for new container footprints

**Goal**: `make_lid_small()` and `make_lid_large()` match the new independent container outer footprints.

**Completion criteria**: Lid geometry tests pass; each lid's outer footprint matches its container's outer footprint within tolerance.

- (a) Update `make_lid_small()`: lid covers from `-LENGTH/2` to `gap_center_x - GAP/2`, outer widths at each end from `_outer_half_width()`
- (b) Update `make_lid_large()`: lid covers from `gap_center_x + GAP/2` to `LENGTH/2`
- (c) `_make_lid()` internals unchanged (uses trapezoid vertices + top plate + skirt + vent grid on top)

### Step 4: Update README documentation

**Goal**: `README.md` reflects the split-container design.

**Completion criteria**: README accurately describes two independent containers on a shared base, corrects the dimensions table, and removes references to divider/lid-seat-slots.

- (a) Replace dimension table entry for `DIVIDER_THICKNESS` (8.0) with `GAP` (5.0)
- (b) Update body description: two independent containers sharing a monolithic base, full perimeter rims
- (c) Remove references to divider ridge, lid-seat slots from rim and lid descriptions
- (d) Update interior fill dimensions (compartment lengths change by ~2.5 mm each)
- (e) Update assembled height if any change (no change expected — BODY_HEIGHT and LID_HEIGHT unchanged)

### Step 5: Regenerate STEP exports and verify

**Goal**: Fresh STEP files exported; all tests pass.

**Completion criteria**: `python -m pytest` is green; `python -m desiccant_container.container` exports three STEP files to `manufacture/`; visual inspection of assembly confirms gap between containers.

- (a) Run `python -m pytest tests/test_desiccant_container.py`
- (b) Run `python -m desiccant_container.container`
- (c) Verify three STEP files exist in `manufacture/`
- (d) Optionally: `python -m desiccant_container.container --show assembly` to visually verify gap

## Completion criteria (overall)

- `GAP = 5.0` present; `DIVIDER_THICKNESS` removed; `DIVIDER_RATIO` now defines gap center
- `_lid_seat_slot_boxes()` removed entirely
- `make_body()` builds two independent containers on shared base with full perimeter rims
- No shared wall between containers; 5 mm gap between adjacent wall outer faces
- Each lid matches its container's independent outer footprint
- `README.md` accurately describes the new design
- All tests pass; STEP files export correctly