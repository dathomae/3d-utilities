"""Tests for the desiccant_container body, lids, vent slots, and label inlays (TDD test-first).

The body is a 185 x (65/75) x 23 mm trapezoidal tray: a 2 mm bottom plate,
4 mm outer walls, a solid 8 mm internal dividing wall at 1/3 of the length
from the short end, and a 12 mm rim stepped 2 mm into the top of every wall.
Vent slots (5 x 1 mm, 1 mm margins) perforate the four outer side walls below
the rim and both lids' top plates - never the bottom plate, the rim, or the
internal dividing wall.
Two snap-fit lids cover the short and long chambers, and the interior floor
carries recessed "SILICA" and "ALUMINA" label inlays (a separate, contrasting
part pressed flush into the floor).

Wall, divider, rim, lid, vent-slot, and label-inlay properties are probed with
small axis-aligned boxes boolean-intersected with the part: the intersection
volume equals the probe volume when the probe lies entirely inside solid, and
~0 when in void.
"""

import math

import pytest
from build123d import Align, Box, Location, Part

from desiccant_container import (
    ALUMINA_LABEL,
    BODY_HEIGHT,
    BOTTOM_THICKNESS,
    DIVIDER_RATIO,
    DIVIDER_THICKNESS,
    LABEL_DEPTH,
    LENGTH,
    LID_HEIGHT,
    LID_TOP_THICKNESS,
    LONG_END,
    OOZE_CLEARANCE,
    RIM_HEIGHT,
    RIM_INSET,
    SHORT_END,
    SILICA_LABEL,
    VENT_MARGIN,
    VENT_SLOT_HEIGHT,
    VENT_SLOT_LENGTH,
    WALL_THICKNESS,
    make_body,
    make_body_assembly,
    make_labels,
    make_lid_large,
    make_lid_small,
)

from desiccant_container.container import _slot_centers


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


def _outer_half_width(x: float) -> float:
    """Half-width of the body's outer trapezoid at a given X, in mm."""
    slope = (LONG_END - SHORT_END) / (2 * LENGTH)
    return SHORT_END / 2 + slope * (x + LENGTH / 2)


def _interior_half_width(x: float) -> float:
    """Half-width of the body's interior cavity at a given X, in mm."""
    slope = (LONG_END - SHORT_END) / (2 * LENGTH)
    perp = math.sqrt(1 + slope * slope)
    outer_half = SHORT_END / 2 + slope * (x + LENGTH / 2)
    return outer_half - WALL_THICKNESS * perp


def test_make_body_returns_part():
    """make_body() must return a valid build123d Part."""
    body = make_body()
    assert isinstance(body, Part)
    assert body.is_valid


def test_bounding_box_size():
    """The body spans 185 (X) x 75 (Y) x 23 (Z) mm."""
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
    """The short-end wall is WALL_THICKNESS (4 mm) thick in X.

    The probe band is z in [6, 7] mm, a solid gap between the vent-slot rows
    (which span z in [1,2], [3,4], [5,6], [7,8], [9,10] below the rim).
    """
    body = make_body()
    probe = _probe(
        WALL_THICKNESS, 40, 1, (-LENGTH / 2 + WALL_THICKNESS / 2, 0, 6)
    )
    assert _intersect_volume(body, probe) == pytest.approx(
        WALL_THICKNESS * 40 * 1
    )


def test_side_wall_thickness_at_midpoint():
    """The side wall is solid at mid-length between the two vent-slot rows."""
    body = make_body()
    # At x=0 the wall spans Y in [31, 35]; probe Y in [32, 34].  The probe is
    # 0.8 mm wide in X, fully inside the 1.14 mm solid gap between the slanted
    # side-wall vent rows that straddle x=0.
    probe = _probe(0.8, 2, 7, (0, LONG_END / 2 - 4.5, 3))
    assert _intersect_volume(body, probe) == pytest.approx(0.8 * 2 * 7)


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
        1,
        (-LENGTH / 2 + WALL_THICKNESS - RIM_INSET / 2, 0,
         BODY_HEIGHT - 1),
    )
    assert _intersect_volume(body, rim_probe) == pytest.approx(
        RIM_INSET * 40 * 1
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
    # The bottom plate away from the label inlays is solid BOTTOM_THICKNESS.
    bottom_probe = _probe(20, 20, BOTTOM_THICKNESS, (70, 0, 0))
    assert _intersect_volume(body, bottom_probe) == pytest.approx(
        20 * 20 * BOTTOM_THICKNESS
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


# --- Lid geometry tests ---


def test_make_lid_small_returns_part():
    """make_lid_small() must return a valid build123d Part."""
    lid = make_lid_small()
    assert isinstance(lid, Part)
    assert lid.is_valid


def test_make_lid_large_returns_part():
    """make_lid_large() must return a valid build123d Part."""
    lid = make_lid_large()
    assert isinstance(lid, Part)
    assert lid.is_valid


def test_lid_small_bounding_box():
    """The small lid footprint spans the silica compartment up to the divider rim ridge."""
    lid = make_lid_small()
    divider_centerline = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    rim_ridge_half_width = DIVIDER_THICKNESS / 2 - RIM_INSET
    right_edge = divider_centerline - rim_ridge_half_width
    expected_x_size = right_edge - (-LENGTH / 2)
    expected_y_size = 2 * _outer_half_width(right_edge)
    size = tuple(lid.bounding_box().size)
    assert size == pytest.approx((expected_x_size, expected_y_size, LID_HEIGHT))


def test_lid_large_bounding_box():
    """The large lid footprint spans the alumina compartment from the divider rim ridge."""
    lid = make_lid_large()
    divider_centerline = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    rim_ridge_half_width = DIVIDER_THICKNESS / 2 - RIM_INSET
    left_edge = divider_centerline + rim_ridge_half_width
    expected_x_size = LENGTH / 2 - left_edge
    size = tuple(lid.bounding_box().size)
    assert size == pytest.approx((expected_x_size, LONG_END, LID_HEIGHT))


def test_lids_are_separated_by_divider_rim_ridge():
    """The two lids straddle the divider's 4 mm rim ridge without overlap."""
    small_lid = make_lid_small()
    large_lid = make_lid_large()
    gap = large_lid.bounding_box().min.X - small_lid.bounding_box().max.X
    assert gap == pytest.approx(DIVIDER_THICKNESS - 2 * RIM_INSET)
    assert small_lid.bounding_box().max.X < large_lid.bounding_box().min.X


def _lid_top_holes(lid: Part) -> list[object]:
    """The inner wires (vent-slot holes) of the lid's top-plate surface."""
    top = max(
        (f for f in lid.faces() if f.normal_at().Z > 0.99),
        key=lambda f: f.area,
    )
    return top.inner_wires()


def test_lid_top_plates_have_a_grid_of_vent_slots():
    """Both lids' top plates are perforated by a full-width grid of slots.

    The slots must cover most of the lid width, not just a single centerline
    row (which was the bug being fixed).
    """
    for lid in (make_lid_small(), make_lid_large()):
        holes = _lid_top_holes(lid)
        assert len(holes) > 100
        ys = [w.bounding_box().center().Y for w in holes]
        assert max(ys) - min(ys) > 0.8 * lid.bounding_box().size.Y


def test_lid_small_skirt_is_hollow():
    """The bottom 2 mm of the small lid is hollow except for the skirt wall."""
    lid = make_lid_small()
    right_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO - (
        DIVIDER_THICKNESS / 2 - RIM_INSET
    )
    center_x = (-LENGTH / 2 + right_x) / 2
    probe = _probe(
        20,
        20,
        LID_HEIGHT - LID_TOP_THICKNESS,
        (center_x, 0, 0),
    )
    assert _intersect_volume(lid, probe) == pytest.approx(0, abs=1e-6)


def test_lid_large_skirt_is_hollow():
    """The bottom 2 mm of the large lid is hollow except for the skirt wall."""
    lid = make_lid_large()
    left_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO + (
        DIVIDER_THICKNESS / 2 - RIM_INSET
    )
    center_x = (left_x + LENGTH / 2) / 2
    probe = _probe(
        20,
        20,
        LID_HEIGHT - LID_TOP_THICKNESS,
        (center_x, 0, 0),
    )
    assert _intersect_volume(lid, probe) == pytest.approx(0, abs=1e-6)


def test_lid_small_skirt_wall_thickness():
    """The small lid's short-end skirt fills the wall thickness below the
    vent-slot overcut zone (z in [0, 1.5])."""
    lid = make_lid_small()
    wall_thickness = RIM_INSET - OOZE_CLEARANCE
    probe = _probe(
        wall_thickness,
        40,
        1.5,
        (-LENGTH / 2 + wall_thickness / 2, 0, 0),
    )
    assert _intersect_volume(lid, probe) == pytest.approx(
        wall_thickness * 40 * 1.5
    )


def test_lid_large_skirt_wall_thickness():
    """The large lid's long-end skirt fills the wall thickness below the
    vent-slot overcut zone (z in [0, 1.5])."""
    lid = make_lid_large()
    wall_thickness = RIM_INSET - OOZE_CLEARANCE
    probe = _probe(
        wall_thickness,
        40,
        1.5,
        (LENGTH / 2 - wall_thickness / 2, 0, 0),
    )
    assert _intersect_volume(lid, probe) == pytest.approx(
        wall_thickness * 40 * 1.5
    )


def test_lid_small_skirt_to_rim_clearance():
    """The small lid's short-end skirt leaves a 0.2 mm gap to the body rim."""
    lid = make_lid_small()
    gap_center_x = -LENGTH / 2 + RIM_INSET - OOZE_CLEARANCE / 2
    probe = _probe(
        OOZE_CLEARANCE,
        40,
        LID_HEIGHT - LID_TOP_THICKNESS,
        (gap_center_x, 0, 0),
    )
    assert _intersect_volume(lid, probe) == pytest.approx(0, abs=1e-6)


def test_lid_large_skirt_to_rim_clearance():
    """The large lid's long-end skirt leaves a 0.2 mm gap to the body rim."""
    lid = make_lid_large()
    gap_center_x = LENGTH / 2 - RIM_INSET + OOZE_CLEARANCE / 2
    probe = _probe(
        OOZE_CLEARANCE,
        40,
        LID_HEIGHT - LID_TOP_THICKNESS,
        (gap_center_x, 0, 0),
    )
    assert _intersect_volume(lid, probe) == pytest.approx(0, abs=1e-6)


def test_lid_slanted_side_skirt_to_rim_clearance():
    """The lid skirt clears the slanted side-wall rim by 0.2 mm radially."""
    lid = make_lid_large()
    slope = (LONG_END - SHORT_END) / (2 * LENGTH)
    perp = math.sqrt(1 + slope * slope)
    y_outer = _outer_half_width(0)
    gap_center_y = y_outer - (RIM_INSET - OOZE_CLEARANCE / 2) * perp
    probe = _probe(
        0.1,
        0.1,
        LID_HEIGHT - LID_TOP_THICKNESS,
        (0, gap_center_y, 0),
    )
    assert _intersect_volume(lid, probe) == pytest.approx(0, abs=1e-6)


def test_lid_small_is_single_closed_shell():
    """The small lid boundary is one closed shell."""
    lid = make_lid_small()
    assert len(lid.shells()) == 1


def test_lid_large_is_single_closed_shell():
    """The large lid boundary is one closed shell."""
    lid = make_lid_large()
    assert len(lid.shells()) == 1


# --- Vent-slot tests ---


def _slot_count_and_gap(span: float) -> tuple[int, float]:
    """Expected number of slots and the gap between them for a span."""
    n = int((span - VENT_MARGIN) // (VENT_SLOT_LENGTH + VENT_MARGIN))
    used = 2 * VENT_MARGIN + n * VENT_SLOT_LENGTH
    gap = (span - used) / (n - 1) if n > 1 else 0.0
    return n, gap


def _end_wall_slot_centers(span: float) -> list[float]:
    """Centred Y positions of the slots on an end wall of width ``span``."""
    n, gap = _slot_count_and_gap(span)
    first = VENT_MARGIN + VENT_SLOT_LENGTH / 2
    centers = [first + i * (VENT_SLOT_LENGTH + gap) for i in range(n)]
    return [c - span / 2 for c in centers]


def test_short_end_wall_has_vent_slots():
    """The short end wall carries 5 x 1 mm through-slots with 1 mm margins."""
    body = make_body()
    z = VENT_MARGIN + VENT_SLOT_HEIGHT / 2
    centers = _end_wall_slot_centers(SHORT_END)
    assert len(centers) == 10

    # The 1 mm bottom slot row (z in [1, 2]) is probed over the central band
    # |y| <= 26 mm.  The band excludes the corners, where the adjacent
    # slanted-side-wall slots legitimately cut into the shared corner mass.
    band = 26.0
    band_centers = [
        y for y in centers if abs(y) + VENT_SLOT_LENGTH / 2 <= band
    ]
    assert len(band_centers) == 8
    probe = _probe(
        WALL_THICKNESS,
        2 * band,
        VENT_SLOT_HEIGHT,
        (-LENGTH / 2 + WALL_THICKNESS / 2, 0, VENT_MARGIN),
    )
    expected = (
        2 * band * VENT_SLOT_HEIGHT * WALL_THICKNESS
        - len(band_centers)
        * VENT_SLOT_LENGTH
        * VENT_SLOT_HEIGHT
        * WALL_THICKNESS
    )
    assert _intersect_volume(body, probe) == pytest.approx(expected, abs=1e-5)

    # The two outermost slots (against the 1 mm Y-edge margins) are also
    # carved.
    for y in (centers[0], centers[-1]):
        void_probe = Box(
            WALL_THICKNESS - 0.1,
            VENT_SLOT_LENGTH - 0.1,
            VENT_SLOT_HEIGHT - 0.1,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((-LENGTH / 2 + WALL_THICKNESS / 2, y, z)))
        assert _intersect_volume(body, void_probe) == pytest.approx(0, abs=1e-5)


def test_long_end_wall_has_vent_slots():
    """The long end wall carries 5 x 1 mm through-slots with 1 mm margins."""
    body = make_body()
    z = VENT_MARGIN + VENT_SLOT_HEIGHT / 2
    centers = _end_wall_slot_centers(LONG_END)
    assert len(centers) == 12

    # The 1 mm bottom slot row (z in [1, 2]) is probed over the central band
    # |y| <= 31 mm.  The band stays inside the trapezoid footprint (half-width
    # at the wall's inner face is ~37.39 mm) and excludes the corners, where
    # the adjacent slanted-side-wall slots cut into the shared corner mass.
    band = 31.0
    band_centers = [
        y for y in centers if abs(y) + VENT_SLOT_LENGTH / 2 <= band
    ]
    assert len(band_centers) == 10
    probe = _probe(
        WALL_THICKNESS,
        2 * band,
        VENT_SLOT_HEIGHT,
        (LENGTH / 2 - WALL_THICKNESS / 2, 0, VENT_MARGIN),
    )
    expected = (
        2 * band * VENT_SLOT_HEIGHT * WALL_THICKNESS
        - len(band_centers)
        * VENT_SLOT_LENGTH
        * VENT_SLOT_HEIGHT
        * WALL_THICKNESS
    )
    assert _intersect_volume(body, probe) == pytest.approx(expected, abs=1e-5)

    # The two outermost slots (against the 1 mm Y-edge margins) are also
    # carved.
    for y in (centers[0], centers[-1]):
        void_probe = Box(
            WALL_THICKNESS - 0.1,
            VENT_SLOT_LENGTH - 0.1,
            VENT_SLOT_HEIGHT - 0.1,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((LENGTH / 2 - WALL_THICKNESS / 2, y, z)))
        assert _intersect_volume(body, void_probe) == pytest.approx(0, abs=1e-5)


def test_slanted_side_walls_have_vent_slots():
    """Both slanted outer side walls carry 5 x 1 mm through-slots."""
    body = make_body()
    slope = (LONG_END - SHORT_END) / (2 * LENGTH)
    angle = math.atan(slope)
    wall_len = math.sqrt(LENGTH ** 2 + ((LONG_END - SHORT_END) / 2) ** 2)
    n, gap = _slot_count_and_gap(wall_len)
    first_s = VENT_MARGIN + VENT_SLOT_LENGTH / 2
    z = VENT_MARGIN + VENT_SLOT_HEIGHT / 2

    for y_sign in (1, -1):
        angle_deg = (
            math.degrees(angle) if y_sign > 0 else math.degrees(-angle)
        )

        # Void probe inside the first slot.
        s = first_s
        x = -LENGTH / 2 + s * math.cos(angle)
        outer_y = y_sign * _outer_half_width(x)
        inner_y = y_sign * _interior_half_width(x)
        mid_y = (outer_y + inner_y) / 2
        void_probe = Box(
            VENT_SLOT_LENGTH - 0.1,
            WALL_THICKNESS - 0.1,
            VENT_SLOT_HEIGHT - 0.1,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((x, mid_y, z), (0, 0, angle_deg)))
        assert _intersect_volume(body, void_probe) == pytest.approx(0, abs=1e-5)

        # Solid probe in the gap between the first two slots.
        s_mid = first_s + VENT_SLOT_LENGTH / 2 + gap / 2
        x_mid = -LENGTH / 2 + s_mid * math.cos(angle)
        outer_y = y_sign * _outer_half_width(x_mid)
        inner_y = y_sign * _interior_half_width(x_mid)
        mid_y = (outer_y + inner_y) / 2
        solid_probe = Box(
            gap - 0.1,
            WALL_THICKNESS - 0.1,
            VENT_SLOT_HEIGHT - 0.1,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((x_mid, mid_y, z), (0, 0, angle_deg)))
        expected = (gap - 0.1) * (WALL_THICKNESS - 0.1) * (VENT_SLOT_HEIGHT - 0.1)
        assert _intersect_volume(body, solid_probe) == pytest.approx(expected, abs=1e-5)

        # Bottom-margin probe: the wall is solid in the 1 mm margin below the
        # first slot row (z in [0, 1]) at the first slot's position.
        s_margin = first_s
        x_margin = -LENGTH / 2 + s_margin * math.cos(angle)
        outer_y = y_sign * _outer_half_width(x_margin)
        inner_y = y_sign * _interior_half_width(x_margin)
        mid_y = (outer_y + inner_y) / 2
        margin_probe = Box(
            VENT_SLOT_LENGTH - 0.1,
            WALL_THICKNESS - 0.1,
            VENT_MARGIN - 0.1,
            align=(Align.CENTER, Align.CENTER, Align.CENTER),
        ).moved(Location((x_margin, mid_y, VENT_MARGIN / 2),
                         (0, 0, angle_deg)))
        expected_margin = (
            (VENT_SLOT_LENGTH - 0.1)
            * (WALL_THICKNESS - 0.1)
            * (VENT_MARGIN - 0.1)
        )
        assert _intersect_volume(body, margin_probe) == pytest.approx(
            expected_margin, abs=1e-5
        )


def _lid_slot_grid(lid: Part) -> list[tuple[float, float]]:
    """Recompute the (x, y) vent-slot centers of a lid's top-plate grid."""
    slope = (LONG_END - SHORT_END) / (2 * LENGTH)
    perp = math.sqrt(1 + slope * slope)
    skirt_inset = RIM_INSET - OOZE_CLEARANCE
    bb = lid.bounding_box()
    left_x = bb.min.X
    span = bb.size.X
    x_centers, _ = _slot_centers(span, VENT_SLOT_LENGTH, VENT_MARGIN)
    centers: list[tuple[float, float]] = []
    for x_rel in x_centers:
        x = left_x + x_rel
        inner_half = _outer_half_width(x) - skirt_inset * perp
        y_centers, _ = _slot_centers(
            2 * inner_half, VENT_SLOT_HEIGHT, VENT_MARGIN
        )
        for y_rel in y_centers:
            centers.append((x, y_rel - inner_half))
    return centers


def test_lid_small_top_plate_has_vent_slots():
    """The small lid top plate carries a grid of 5 x 1 mm through-slots."""
    lid = make_lid_small()
    centers = _lid_slot_grid(lid)
    assert len(centers) > 100
    z = LID_HEIGHT - LID_TOP_THICKNESS / 2

    # A computed slot center is a through-hole (void).
    x, y = centers[0]
    void_probe = Box(
        VENT_SLOT_LENGTH - 0.1,
        VENT_SLOT_HEIGHT - 0.1,
        LID_TOP_THICKNESS - 0.1,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((x, y, z)))
    assert _intersect_volume(lid, void_probe) == pytest.approx(0, abs=1e-5)

    # The X-edge margin before the first column is solid plate.
    left_x = lid.bounding_box().min.X
    edge_probe = Box(
        VENT_MARGIN - 0.1,
        VENT_SLOT_HEIGHT - 0.1,
        LID_TOP_THICKNESS - 0.1,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((left_x + VENT_MARGIN / 2, 0, z)))
    expected = (
        (VENT_MARGIN - 0.1)
        * (VENT_SLOT_HEIGHT - 0.1)
        * (LID_TOP_THICKNESS - 0.1)
    )
    assert _intersect_volume(lid, edge_probe) == pytest.approx(expected, abs=1e-5)


def test_lid_large_top_plate_has_vent_slots():
    """The large lid top plate carries a grid of 5 x 1 mm through-slots."""
    lid = make_lid_large()
    centers = _lid_slot_grid(lid)
    assert len(centers) > 100
    z = LID_HEIGHT - LID_TOP_THICKNESS / 2

    x, y = centers[0]
    void_probe = Box(
        VENT_SLOT_LENGTH - 0.1,
        VENT_SLOT_HEIGHT - 0.1,
        LID_TOP_THICKNESS - 0.1,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((x, y, z)))
    assert _intersect_volume(lid, void_probe) == pytest.approx(0, abs=1e-5)

    left_x = lid.bounding_box().min.X
    edge_probe = Box(
        VENT_MARGIN - 0.1,
        VENT_SLOT_HEIGHT - 0.1,
        LID_TOP_THICKNESS - 0.1,
        align=(Align.CENTER, Align.CENTER, Align.CENTER),
    ).moved(Location((left_x + VENT_MARGIN / 2, 0, z)))
    expected = (
        (VENT_MARGIN - 0.1)
        * (VENT_SLOT_HEIGHT - 0.1)
        * (LID_TOP_THICKNESS - 0.1)
    )
    assert _intersect_volume(lid, edge_probe) == pytest.approx(expected, abs=1e-5)


def test_bottom_plate_has_no_vent_slots():
    """The bottom plate remains solid (away from label inlays); no slots cut it."""
    body = make_body()
    probe = _probe(20, 20, BOTTOM_THICKNESS, (70, 0, 0))
    assert _intersect_volume(body, probe) == pytest.approx(
        20 * 20 * BOTTOM_THICKNESS, abs=1e-5
    )


def test_divider_has_no_vent_slots():
    """The internal dividing wall remains solid; no slots cut into it."""
    body = make_body()
    divider_center_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    probe = _probe(DIVIDER_THICKNESS, 50, 7, (divider_center_x, 0, 3))
    assert _intersect_volume(body, probe) == pytest.approx(
        DIVIDER_THICKNESS * 50 * 7, abs=1e-5
    )


# --- Label inlay tests ---


def _label_center_x(is_small: bool) -> float:
    """X center of a label on a compartment floor.

    The label is centered between the inner face of the relevant end wall and
    the inner face of the divider.
    """
    divider_center_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    if is_small:
        left = -LENGTH / 2 + WALL_THICKNESS
        right = divider_center_x - DIVIDER_THICKNESS / 2
    else:
        left = divider_center_x + DIVIDER_THICKNESS / 2
        right = LENGTH / 2 - WALL_THICKNESS
    return (left + right) / 2


def test_labels_part_is_flush_with_the_floor():
    """The labels span LABEL_DEPTH below the floor, with their top flush at it."""
    labels = make_labels()
    bb = labels.bounding_box()
    assert bb.min.Z == pytest.approx(BOTTOM_THICKNESS - LABEL_DEPTH, abs=1e-6)
    assert bb.max.Z == pytest.approx(BOTTOM_THICKNESS, abs=1e-6)


def test_labels_have_glyphs_in_both_compartments():
    """The labels part has lettering in both the small and large compartments."""
    labels = make_labels()
    small_x = _label_center_x(is_small=True)
    large_x = _label_center_x(is_small=False)
    xs = [s.bounding_box().center().X for s in labels.solids()]
    assert any(abs(x - small_x) < 20 for x in xs)
    assert any(abs(x - large_x) < 20 for x in xs)


def test_labels_fill_the_floor_recesses():
    """The labels exactly fill the recesses cut into the body floor (flush)."""
    body = make_body()
    labels = make_labels()
    for is_small in (True, False):
        x = _label_center_x(is_small)
        probe = _probe(30, 10, LABEL_DEPTH, (x, 0, BOTTOM_THICKNESS - LABEL_DEPTH))
        full = 30 * 10 * LABEL_DEPTH
        assert _intersect_volume(body, probe) + _intersect_volume(
            labels, probe
        ) == pytest.approx(full, rel=1e-3)


def test_body_assembly_contains_body_and_labels():
    """The body assembly holds the body and its labels as separate solids."""
    assembly = make_body_assembly()
    assert len(assembly.solids()) == len(make_body().solids()) + len(
        make_labels().solids()
    )


def test_labels_are_confined_to_compartments():
    """The label inlays stay on their own side of the divider."""
    labels = make_labels()
    divider_center_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    small_max = max(
        s.bounding_box().max.X
        for s in labels.solids()
        if s.bounding_box().center().X < 0
    )
    large_min = min(
        s.bounding_box().min.X
        for s in labels.solids()
        if s.bounding_box().center().X > 0
    )
    assert small_max < divider_center_x
    assert large_min > divider_center_x
