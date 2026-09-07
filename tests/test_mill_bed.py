"""Tests for the scaffold.mill_bed mounting-hole pattern."""

from scaffold.mill_bed import (
    BOTTOM_OFFSET,
    COLUMNS,
    LEFT_OFFSET,
    ROWS,
    X_SPACING,
    Y_SPACING,
    mounting_hole_locations,
)


def test_returns_34_holes():
    """The bed has a 7 × 5 grid minus the missing lower-left hole: 34 holes."""
    assert len(mounting_hole_locations()) == COLUMNS * ROWS - 1


def test_x_positions_match_seven_columns():
    """Distinct x positions are the 7 columns spaced 40 mm apart from 26 mm."""
    xs = sorted({x for x, _ in mounting_hole_locations()})
    assert xs == [LEFT_OFFSET + X_SPACING * i for i in range(COLUMNS)]


def test_rows_spaced_45_mm():
    """The five rows start at 16 mm and step by 45 mm."""
    ys = sorted({y for _, y in mounting_hole_locations()})
    assert ys == [BOTTOM_OFFSET + Y_SPACING * j for j in range(ROWS)]


def test_lower_left_hole_is_missing():
    """The lower-left hole (26, 16) is absent from the pattern."""
    assert (LEFT_OFFSET, BOTTOM_OFFSET) not in mounting_hole_locations()


def test_bottom_row_has_six_holes():
    """The bottom row holds 6 holes (the leftmost is missing)."""
    bottom = [(x, y) for x, y in mounting_hole_locations() if y == BOTTOM_OFFSET]
    assert len(bottom) == COLUMNS - 1
