# Vertical Mill Jig Mounting

This document is the reference for creating jigs that mount to the vertical mill bed. It ties together the standardized mounting screw, the hole feature cut for it, and the bed's mounting-hole pattern. Consult this file whenever a vertical mill jig is being created.

## Standardized mounting screw

All jigs mount with a single standardized screw, documented in full in [screws.md](screws.md) (section 8):

| Property | Value |
|----------|-------|
| Thread | M5 (coarse, 0.80 mm pitch) |
| Length | 30 mm |
| Thread coverage | Full thread |
| Head style | Flat head (countersunk / conical), hex socket |
| Head diameter | 10 mm |
| Countersink angle | 90° (included, ISO metric standard) |
| Head height (cone depth) | ~2.5 mm |

## Mounting hole feature

Each mounting location gets a countersunk through-hole sized for the screw. The through-hole clears the M5 shank and threads, and the countersink buries the conical head below the working face. In build123d this is a single `CounterSinkHole` operation (see [screws.md](screws.md) section 9):

- Clearance (through-hole) radius: 5.8 / 2 = **2.9 mm**
- Countersink (head) radius: 10 / 2 = **5.0 mm**
- Countersink angle: **90°**

```python
from build123d import *

clearance_radius = 5.8 / 2  # 2.9 mm
head_radius = 10 / 2        # 5.0 mm

with BuildPart() as base:
    Box(50, 50, 4)  # jig base
    with Locations((0, 0, 2)):  # top face
        CounterSinkHole(
            radius=clearance_radius,
            counter_sink_radius=head_radius,
            counter_sink_angle=90,
        )
```

## Jig base thickness

The base must be at least **4 mm** thick. The 90° head cone is ~2.5 mm tall (a 10 mm head over a 5 mm thread), so 4 mm buries the head below the working face with ~1.5 mm of material to spare.

## Bed mounting-hole pattern

The bed's M5 mounting holes form a grid measured from the bed origin at the **lower-left** corner.

| Parameter | Value |
|-----------|-------|
| Columns (x direction) | 7 |
| Rows (y direction) | 5 |
| Left column offset from left edge | 26 mm |
| Bottom row offset from bottom edge | 16 mm |
| Horizontal spacing between column centers | 40 mm |
| Vertical spacing between row centers | 45 mm |

**Exception:** the lower-left hole is missing — the bed carries no hole at (26, 16).

The hole centers are:

| y \ x | 26 | 66 | 106 | 146 | 186 | 226 | 266 |
|-------|----|----|-----|-----|-----|-----|-----|
| **196** | (26, 196) | (66, 196) | (106, 196) | (146, 196) | (186, 196) | (226, 196) | (266, 196) |
| **151** | (26, 151) | (66, 151) | (106, 151) | (146, 151) | (186, 151) | (226, 151) | (266, 151) |
| **106** | (26, 106) | (66, 106) | (106, 106) | (146, 106) | (186, 106) | (226, 106) | (266, 106) |
| **61** | (26, 61) | (66, 61) | (106, 61) | (146, 61) | (186, 61) | (226, 61) | (266, 61) |
| **16** | — (missing) | (66, 16) | (106, 16) | (146, 16) | (186, 16) | (226, 16) | (266, 16) |

That is 34 holes total: the regular 7 × 5 grid minus the missing lower-left hole at (26, 16).

## Using the pattern in a jig

To mount a jig, cut a countersunk M5 hole at each bed location the jig covers. The pattern is regular with a single missing hole, so generate the locations from the parameters above rather than hard-coding 34 coordinates:

```python
def mounting_hole_locations():
    columns = [26 + 40 * i for i in range(7)]
    rows = [16 + 45 * j for j in range(5)]
    locations = [(x, y) for y in rows for x in columns]
    locations.remove((26, 16))  # the lower-left hole is missing
    return locations
```

This helper is the canonical source of the grid. The reusable, importable version of it lives in the package as `scaffold.mill_bed`:

```python
from scaffold.mill_bed import mounting_hole_locations

for x, y in mounting_hole_locations():
    ...
```

Jig programs should import `mounting_hole_locations` from there rather than re-deriving the pattern.
