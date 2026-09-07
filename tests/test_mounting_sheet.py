"""Tests for the scaffold.mounting_sheet test sheet builder."""

import pytest
from build123d import GeomType, Part

from scaffold.mill_bed import COLUMNS, ROWS
from scaffold.mounting_sheet import (
    SHEET_HEIGHT,
    SHEET_LENGTH,
    SHEET_THICKNESS,
    make_mounting_sheet,
)


def test_make_mounting_sheet_returns_part():
    """make_mounting_sheet() must return a build123d Part."""
    assert isinstance(make_mounting_sheet(), Part)


def test_sheet_dimensions():
    """The sheet is 340 × 225 × 1 mm."""
    sheet = make_mounting_sheet()
    size = tuple(sheet.bounding_box().size)
    assert size == pytest.approx((SHEET_LENGTH, SHEET_HEIGHT, SHEET_THICKNESS))


def test_sheet_has_one_hole_per_mounting_location():
    """Each mounting location gets one through-hole: 34 cylindrical faces."""
    sheet = make_mounting_sheet()
    holes = sheet.faces().filter_by(GeomType.CYLINDER)
    assert len(holes) == COLUMNS * ROWS - 1
