"""Mounting-hole pattern for the vertical mill bed.

The vertical mill bed carries M5 threaded holes used to mount jigs. This module
captures that pattern as code so jig programs can place the standardized
countersunk mounting holes without re-deriving the grid.

The machine, screw, and hole conventions are documented in
`resources/modeling/vertical_mill_jigs.md` and `resources/modeling/screws.md`.
"""

#: Number of hole columns (x direction) and rows (y direction).
COLUMNS = 7
ROWS = 5

#: Distance of the left column and bottom row from the bed edges (mm).
LEFT_OFFSET = 26.0
BOTTOM_OFFSET = 16.0

#: Center-to-center spacing between columns and rows (mm).
X_SPACING = 40.0
Y_SPACING = 45.0


def mounting_hole_locations() -> list[tuple[float, float]]:
    """Return the bed's M5 mounting-hole centers as ``(x, y)`` tuples.

    Positions are measured from the bed origin at the lower-left corner. The
    result is a 7 × 5 grid ordered bottom-to-top, left-to-right, minus the
    lower-left hole, which the bed does not carry.
    """
    columns = [LEFT_OFFSET + X_SPACING * i for i in range(COLUMNS)]
    rows = [BOTTOM_OFFSET + Y_SPACING * j for j in range(ROWS)]
    locations = [(x, y) for y in rows for x in columns]
    locations.remove((LEFT_OFFSET, BOTTOM_OFFSET))  # the lower-left hole is absent
    return locations
