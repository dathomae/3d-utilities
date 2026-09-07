"""Tests for the scaffold.example make_box builder (TDD test-first)."""

import pytest
from build123d import Compound, Part

from scaffold.example import PARTS, make_assembly, make_box


def test_make_box_returns_part():
    """make_box() must return a build123d Part."""
    box = make_box()
    assert isinstance(box, Part)


def test_make_box_bounding_box_size():
    """Default make_box() is a 10 mm cube: bounding box size (10, 10, 10)."""
    box = make_box()
    # build123d Vector is not a tuple subclass; convert for pytest.approx.
    size = tuple(box.bounding_box().size)
    assert size == pytest.approx((10, 10, 10))


def test_make_box_centered_at_origin():
    """Default box spans -5..5 in each axis (centered at the origin)."""
    box = make_box()
    bb = box.bounding_box()
    assert tuple(bb.min) == pytest.approx((-5, -5, -5))
    assert tuple(bb.max) == pytest.approx((5, 5, 5))


def test_parts_registry_contains_box():
    """PARTS registers the box under the name 'box'."""
    assert "box" in PARTS
    assert isinstance(PARTS["box"], Part)


def test_make_assembly_is_compound_of_parts():
    """make_assembly() returns a Compound with the box's geometry."""
    assembly = make_assembly()
    assert isinstance(assembly, Compound)
    size = tuple(assembly.bounding_box().size)
    assert size == pytest.approx((10, 10, 10))
