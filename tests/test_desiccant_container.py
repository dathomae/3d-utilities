"""Tests for the desiccant_container body geometry (TDD test-first).

The body is a 185 x (65/75) x 13 mm trapezoidal tray: a 2 mm bottom plate,
4 mm outer walls, a solid 8 mm internal dividing wall at 1/3 of the length
from the short end, and a 2 mm rim stepped 2 mm into the top of every wall.

Wall, divider, and rim thicknesses are probed with small axis-aligned boxes
boolean-intersected with the part: the intersection volume equals the probe
volume when the probe lies entirely inside solid, and ~0 when in void.
"""

import pytest
from build123d import Align, Box, Location, Part

from desiccant_container import (
    BODY_HEIGHT,
    BOTTOM_THICKNESS,
    DIVIDER_RATIO,
    DIVIDER_THICKNESS,
    LENGTH,
    LONG_END,
    RIM_HEIGHT,
    RIM_INSET,
    SHORT_END,
    WALL_THICKNESS,
    make_body,
)


def _probe(width, depth, height, center):
    """Return an axis-aligned probe Box at ``center`` with its base at Z=0."""
    return Box(
        width,
        depth,
        height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ).moved(Location(center))


def _intersect_shapes(body, probe):
    """The boolean intersection of ``body`` and ``probe`` as a list of Shapes.

    build123d ``Shape.intersect`` returns a ``ShapeList`` (or ``None`` when
    the shapes are disjoint), so normalise both cases to a plain list.
    """
    result = body.intersect(probe)
    return [] if result is None else list(result)


def _intersect_volume(body, probe):
    """Total volume of the intersection (0.0 when the probe is in void)."""
    return sum(shape.volume for shape in _intersect_shapes(body, probe))


def test_make_body_returns_part():
    """make_body() must return a valid build123d Part."""
    body = make_body()
    assert isinstance(body, Part)
    assert body.is_valid


def test_bounding_box_size():
    """The body spans 185 (X) x 75 (Y) x 13 (Z) mm."""
    body = make_body()
    size = tuple(body.bounding_box().size)
    assert size == pytest.approx((LENGTH, LONG_END, BODY_HEIGHT))


def test_body_centered_on_origin():
    """The trapezoid is centered on the origin, sitting on the Z=0 plane."""
    body = make_body()
    bb = body.bounding_box()
    assert tuple(bb.min) == pytest.approx((-LENGTH / 2, -LONG_END / 2, 0))
    assert tuple(bb.max) == pytest.approx((LENGTH / 2, LONG_END / 2, BODY_HEIGHT))


def test_outer_wall_thickness():
    """The short-end wall is WALL_THICKNESS (4 mm) thick in X."""
    body = make_body()
    probe = _probe(
        WALL_THICKNESS, 40, 7, (-LENGTH / 2 + WALL_THICKNESS / 2, 0, 3)
    )
    assert _intersect_volume(body, probe) == pytest.approx(
        WALL_THICKNESS * 40 * 7
    )


def test_side_wall_thickness_at_midpoint():
    """The side wall is nominally 4 mm thick (horizontally) at mid-length."""
    body = make_body()
    # At x=0 the wall spans Y in [31, 35]; probe Y in [32, 34].
    probe = _probe(2, 2, 7, (0, LONG_END / 2 - 4.5, 3))
    assert _intersect_volume(body, probe) == pytest.approx(2 * 2 * 7)


def test_divider_thickness_and_position():
    """The divider is DIVIDER_THICKNESS (8 mm) thick, with its centerline at
    DIVIDER_RATIO (1/3) of LENGTH from the short end's outer face."""
    body = make_body()
    probe = _probe(20, 2, 7, (-30, 0, 3))  # X in [-40, -20] on the centerline
    section = _intersect_shapes(body, probe)
    assert len(section) == 1  # a single solid chunk: the divider
    bb = section[0].bounding_box()
    assert bb.size.X == pytest.approx(DIVIDER_THICKNESS)
    center_x = (bb.min.X + bb.max.X) / 2
    assert center_x - (-LENGTH / 2) == pytest.approx(LENGTH * DIVIDER_RATIO)


def test_divider_is_solid_across_the_interior():
    """The divider fills the whole interior width, so the two compartments
    cannot communicate through it."""
    body = make_body()
    divider_center_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    probe = _probe(DIVIDER_THICKNESS, 50, 7, (divider_center_x, 0, 3))
    assert _intersect_volume(body, probe) == pytest.approx(
        DIVIDER_THICKNESS * 50 * 7
    )


def test_rim_thickness():
    """The top 2 mm of the short-end wall is a 2 mm rim (solid between
    X=-90.5 and X=-88.5), with the 2 mm exterior shelf cut away."""
    body = make_body()
    rim_probe = _probe(
        RIM_INSET,
        40,
        RIM_HEIGHT,
        (-LENGTH / 2 + WALL_THICKNESS - RIM_INSET / 2, 0,
         BODY_HEIGHT - RIM_HEIGHT),
    )
    assert _intersect_volume(body, rim_probe) == pytest.approx(
        RIM_INSET * 40 * RIM_HEIGHT
    )
    shelf_probe = _probe(
        RIM_INSET,
        40,
        RIM_HEIGHT,
        (-LENGTH / 2 + RIM_INSET / 2, 0, BODY_HEIGHT - RIM_HEIGHT),
    )
    assert _intersect_volume(body, shelf_probe) == pytest.approx(0, abs=1e-6)


def test_divider_rim_ridge_and_shelves():
    """The divider's top has a 4 mm centered rim ridge and 2 mm shelves."""
    body = make_body()
    center_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    ridge_probe = _probe(
        DIVIDER_THICKNESS - 2 * RIM_INSET,
        40,
        RIM_HEIGHT,
        (center_x, 0, BODY_HEIGHT - RIM_HEIGHT),
    )
    assert _intersect_volume(body, ridge_probe) == pytest.approx(
        (DIVIDER_THICKNESS - 2 * RIM_INSET) * 40 * RIM_HEIGHT
    )
    shelf_probe = _probe(
        RIM_INSET,
        40,
        RIM_HEIGHT,
        (center_x - DIVIDER_THICKNESS / 2 + RIM_INSET / 2, 0,
         BODY_HEIGHT - RIM_HEIGHT),
    )
    assert _intersect_volume(body, shelf_probe) == pytest.approx(0, abs=1e-6)


def test_interior_cavity_hollow_with_solid_bottom():
    """The interior is a hollow basin sealed by a 2 mm bottom plate."""
    body = make_body()
    # Void in the small (silica) compartment, away from walls and divider.
    void_probe = _probe(35, 20, 7, (-62.5, 0, 6.5))
    assert _intersect_volume(body, void_probe) == pytest.approx(0, abs=1e-6)
    # The bottom plate under the same footprint is solid BOTTOM_THICKNESS.
    bottom_probe = _probe(35, 20, BOTTOM_THICKNESS, (-62.5, 0, 0))
    assert _intersect_volume(body, bottom_probe) == pytest.approx(
        35 * 20 * BOTTOM_THICKNESS
    )


def test_large_compartment_is_hollow():
    """The large (alumina) compartment is a separate void beyond the divider."""
    body = make_body()
    center_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    probe = _probe(20, 30, 7, (center_x + 22, 0, 6.5))
    assert _intersect_volume(body, probe) == pytest.approx(0, abs=1e-6)


def test_body_is_single_closed_shell():
    """The body boundary is one closed shell: no open or split surfaces."""
    body = make_body()
    assert len(body.shells()) == 1
