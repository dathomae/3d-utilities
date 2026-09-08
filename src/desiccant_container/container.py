"""Parametric geometry for the desiccant container body and lids.

The body is a trapezoidal tray: an isosceles trapezoid in plan view,
symmetric about its long centerline, centered on the origin (X along length,
Y across width, Z up).  It holds two compartments of desiccant:

* the small (silica) compartment at the 65 mm short end, and
* the large (alumina) compartment at the 75 mm long end.

It consists of a 2 mm bottom plate, 4 mm outer walls, a solid 8 mm internal
dividing wall (no vents) that keeps the two desiccants apart, and a
``RIM_HEIGHT``-tall rim stepped ``RIM_INSET`` inward on the top of every wall
(outer perimeter and divider).  All dimensions are module-level parameters in
millimetres.

Two separate lids close the compartments: each is a 2 mm top plate plus a
``RIM_HEIGHT``-tall skirt, with the skirt's outer face flush with the body's
outer face and a ``OOZE_CLEARANCE`` radial gap to the rim's outer face so the
lids mate without binding.

Ventilation: 5 x 1 mm rectangular through-slots (``VENT_SLOT_LENGTH`` x
``VENT_SLOT_HEIGHT``) with 1 mm solid margins (``VENT_MARGIN``) perforate
the four outer side walls below the rim and both lids' top plates - never the
bottom plate, the rim, or the internal dividing wall.  Cutting boxes extend
slightly past the faces they pierce (``VENT_OVERCUT``, ``LID_SLOT_OVERCUT``)
so the booleans stay clean.

The interior cavity is formed by offsetting each of the four outer faces
inward by ``WALL_THICKNESS`` perpendicular to that face (a true polygon
offset), so the slanted side walls - like the end walls - are exactly
``WALL_THICKNESS`` thick measured normal to the face.  The same
perpendicular offset (by ``RIM_INSET``) defines the rim step on the top of
every wall.

The two compartments are identified by ``SILICA`` and ``ALUMINA`` lettering
inlaid flush into the interior floor.  The lettering is a separate part
(``make_labels``) printed in a contrasting filament and pressed into matching
``LABEL_DEPTH``-deep recesses cut into the bottom plate, so its top face
sits level with the floor.
"""

import argparse
import math
from pathlib import Path

from build123d import (
    Align,
    Box,
    BuildPart,
    BuildSketch,
    Compound,
    Location,
    Locations,
    Mode,
    Part,
    Plane,
    Polygon,
    Rectangle,
    Shape,
    Text,
    Vector,
    export_step,
    extrude,
)

# --- Body dimensions (mm) ---
LENGTH = 185.0
SHORT_END = 65.0
LONG_END = 75.0
BODY_HEIGHT = 23.0
BOTTOM_THICKNESS = 2.0
WALL_THICKNESS = 4.0
DIVIDER_THICKNESS = 8.0
# The rim is the lip the lids grip.  The full-thickness wall below it is
# ``BODY_HEIGHT - RIM_HEIGHT`` tall and carries the vent slots.
RIM_HEIGHT = 12.0
RIM_INSET = 2.0
DIVIDER_RATIO = 1 / 3

# --- Lid dimensions (mm) ---
# The skirt is ``LID_HEIGHT - LID_TOP_THICKNESS`` tall and grips the full
# ``RIM_HEIGHT`` of the rim.
LID_HEIGHT = 14.0
LID_TOP_THICKNESS = 2.0
OOZE_CLEARANCE = 0.2

# --- Vent dimensions (mm) ---
VENT_SLOT_LENGTH = 5.0
VENT_SLOT_HEIGHT = 1.0
VENT_MARGIN = 1.0
VENT_OVERCUT = 1.0
# Lid slots use a smaller overcut than the body-wall slots so the cutting box
# barely leaves the top plate: a larger overcut would notch the skirt wall
# where the outermost slots meet it.
LID_SLOT_OVERCUT = 0.4

# --- Label inlay dimensions (mm) ---
LABEL_DEPTH = 0.8
LABEL_FONT_SIZE = 10.0
SILICA_LABEL = "SILICA"
ALUMINA_LABEL = "ALUMINA"


def _trapezoid_vertices(
    length: float,
    short_end: float,
    long_end: float,
    inset: float = 0.0,
) -> list[Vector]:
    """Corner vertices of an isosceles trapezoid centered on the origin.

    X spans ``+/- length/2`` along the length; Y spans ``+/- short_end/2``
    at the short (silica) end and ``+/- long_end/2`` at the long (alumina)
    end.  ``inset`` offsets each of the four faces inward by that amount
    PERPENDICULAR to the face (a true polygon offset), so an inset face is
    exactly ``inset`` away from its outer counterpart everywhere and the
    slanted side walls keep the outer taper.  ``inset=0`` yields the outer
    footprint.
    """
    slope = (long_end - short_end) / (2 * length)
    perp = math.sqrt(1 + slope * slope)
    x_end = length / 2 - inset
    short_half = short_end / 2 + slope * inset - perp * inset
    long_half = long_end / 2 - slope * inset - perp * inset
    return [
        Vector(-x_end, -short_half),
        Vector(-x_end, +short_half),
        Vector(+x_end, +long_half),
        Vector(+x_end, -long_half),
    ]


def _interior_half_width(x: float) -> float:
    """Interior (cavity) half-width in Y at a given X, in mm.

    The cavity profile is the outer trapezoid with each face offset inward by
    ``WALL_THICKNESS`` perpendicular to that face, so every wall (end walls
    and slanted side walls) is exactly ``WALL_THICKNESS`` thick measured
    normal to its face.
    """
    slope = (LONG_END - SHORT_END) / (2 * LENGTH)
    perp = math.sqrt(1 + slope * slope)
    outer_half = SHORT_END / 2 + slope * (x + LENGTH / 2)
    return outer_half - WALL_THICKNESS * perp


def _outer_half_width(x: float) -> float:
    """Outer trapezoid half-width in Y at a given X, in mm."""
    slope = (LONG_END - SHORT_END) / (2 * LENGTH)
    return SHORT_END / 2 + slope * (x + LENGTH / 2)


def _wall_angle() -> float:
    """Angle (radians) of the slanted side walls relative to the X axis."""
    return math.atan2(LONG_END - SHORT_END, 2 * LENGTH)


def _wall_length() -> float:
    """Length of one slanted side wall along its face, in mm."""
    return math.sqrt(LENGTH ** 2 + ((LONG_END - SHORT_END) / 2) ** 2)


def _slot_centers(span: float, slot_size: float, margin: float) -> tuple[list[float], float]:
    """Return equally spaced slot centers and the gap between them within ``span``.

    Edge margins are exactly ``margin``. The gap between adjacent slots is always
    >= ``margin`` (any leftover span is distributed evenly as extra gap).
    """
    if span < 2 * margin + slot_size:
        return [], 0.0
    n = int((span - margin) // (slot_size + margin))
    if n < 1:
        return [], 0.0
    used = 2 * margin + n * slot_size
    gap = (span - used) / (n - 1) if n > 1 else 0.0
    first = margin + slot_size / 2
    return [first + i * (slot_size + gap) for i in range(n)], gap


def _body_vent_slot_boxes() -> list[Part]:
    """Positioned through-slot boxes for the four outer walls of the body.

    The boxes are returned as a list of un-cut shapes so ``make_body`` can
    subtract them from the base tray in a single fused boolean operation
    (hundreds of sequential ``Mode.SUBTRACT`` boxes would take minutes).
    Slots perforate only the full-thickness wall below the rim (the rim the
    lids grip is left solid), and never the bottom plate or the internal
    dividing wall.  Each box extends slightly beyond the wall faces
    (``VENT_OVERCUT``) to avoid coplanar boolean issues.
    """
    boxes: list[Part] = []
    overcut = VENT_OVERCUT
    z_centers, _ = _slot_centers(
        BODY_HEIGHT - RIM_HEIGHT, VENT_SLOT_HEIGHT, VENT_MARGIN
    )
    if not z_centers:
        return boxes

    # Short end wall (X = -LENGTH/2).  ``_slot_centers`` returns positions in
    # ``[0, span]``, so recentre them about the wall: subtract SHORT_END / 2.
    y_centers, _ = _slot_centers(SHORT_END, VENT_SLOT_LENGTH, VENT_MARGIN)
    for y_rel in y_centers:
        y = y_rel - SHORT_END / 2
        for z in z_centers:
            boxes.append(
                Box(
                    WALL_THICKNESS + overcut,
                    VENT_SLOT_LENGTH,
                    VENT_SLOT_HEIGHT,
                    align=(Align.CENTER, Align.CENTER, Align.CENTER),
                ).moved(Location((-LENGTH / 2 + WALL_THICKNESS / 2, y, z)))
            )

    # Long end wall (X = +LENGTH/2).
    y_centers, _ = _slot_centers(LONG_END, VENT_SLOT_LENGTH, VENT_MARGIN)
    for y_rel in y_centers:
        y = y_rel - LONG_END / 2
        for z in z_centers:
            boxes.append(
                Box(
                    WALL_THICKNESS + overcut,
                    VENT_SLOT_LENGTH,
                    VENT_SLOT_HEIGHT,
                    align=(Align.CENTER, Align.CENTER, Align.CENTER),
                ).moved(Location((LENGTH / 2 - WALL_THICKNESS / 2, y, z)))
            )

    # Slanted side walls (both Y signs).
    angle = _wall_angle()
    wall_len = _wall_length()
    s_centers, _ = _slot_centers(wall_len, VENT_SLOT_LENGTH, VENT_MARGIN)
    for y_sign in (1, -1):
        angle_deg = (
            math.degrees(angle) if y_sign > 0 else math.degrees(-angle)
        )
        for s in s_centers:
            x = -LENGTH / 2 + s * math.cos(angle)
            outer_y = y_sign * _outer_half_width(x)
            inner_y = y_sign * _interior_half_width(x)
            mid_y = (outer_y + inner_y) / 2
            for z in z_centers:
                boxes.append(
                    Box(
                        VENT_SLOT_LENGTH,
                        WALL_THICKNESS + overcut,
                        VENT_SLOT_HEIGHT,
                        align=(Align.CENTER, Align.CENTER, Align.CENTER),
                    ).moved(Location((x, mid_y, z), (0, 0, angle_deg)))
                )

    return boxes


def _label_centers() -> tuple[float, float]:
    """X centers of the SILICA (small) and ALUMINA (large) label inlays.

    Each label is centered between the inner face of its end wall and the
    inner face of the divider, on the interior floor.
    """
    divider_center_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    small = (
        -LENGTH / 2 + WALL_THICKNESS + divider_center_x - DIVIDER_THICKNESS / 2
    ) / 2
    large = (
        divider_center_x + DIVIDER_THICKNESS / 2 + LENGTH / 2 - WALL_THICKNESS
    ) / 2
    return small, large


def make_body() -> Part:
    """Return the desiccant container body as a build123d Part.

    Construction:
    1. extrude the outer trapezoid footprint to ``BODY_HEIGHT``,
    2. cut the interior cavity (outer faces offset inward by
       ``WALL_THICKNESS`` perpendicular to each face) from the top of the
       ``BOTTOM_THICKNESS`` bottom plate up to the body top,
    3. add the solid ``DIVIDER_THICKNESS`` dividing wall at ``DIVIDER_RATIO``
       of the length from the short end's outer face, spanning the full
       interior width so the two compartments are sealed from each other,
    4. step the top ``RIM_HEIGHT`` mm of every wall inward by ``RIM_INSET``:
       a ring around the outer perimeter (rim flush with the interior face,
       leaving a 2 mm exterior shelf) and two 2 mm shelves on the divider,
       leaving the 4 mm centered divider rim ridge,
    5. cut ``LABEL_DEPTH``-deep recesses for the SILICA and ALUMINA label
       inlays into the interior floor (see ``make_labels``),
    6. cut the vent slots (5 x 1 mm, 1 mm margins, see
       ``_body_vent_slot_boxes``) through the four outer side walls below the
       rim in a single fused boolean operation; the bottom plate, the rim, and
       the internal dividing wall carry no vents.
    """
    divider_center_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    # The interior narrows toward the short end, so the divider must span the
    # interior width at its widest (long-end) face to seal both compartments.
    divider_half_span = _interior_half_width(
        divider_center_x + DIVIDER_THICKNESS / 2
    )

    with BuildPart() as body:
        # 1. Outer trapezoid footprint, full height.
        with BuildSketch(Plane.XY):
            Polygon(_trapezoid_vertices(LENGTH, SHORT_END, LONG_END))
        extrude(amount=BODY_HEIGHT)

        # 2. Interior cavity, from the bottom plate top to the body top.
        with BuildSketch(Plane.XY.offset(BOTTOM_THICKNESS)):
            Polygon(
                _trapezoid_vertices(LENGTH, SHORT_END, LONG_END, WALL_THICKNESS)
            )
        extrude(amount=BODY_HEIGHT - BOTTOM_THICKNESS, mode=Mode.SUBTRACT)

        # 3. Solid internal dividing wall (no vents), bottom to top.
        with Locations((divider_center_x, 0, 0)):
            Box(
                DIVIDER_THICKNESS,
                2 * divider_half_span,
                BODY_HEIGHT,
                align=(Align.CENTER, Align.CENTER, Align.MIN),
            )

        # 4a. Perimeter rim: remove the outer RIM_INSET ring from the top
        #     RIM_HEIGHT mm, leaving a 2 mm rim flush with the interior face
        #     and a 2 mm shelf on the exterior.
        with BuildSketch(Plane.XY.offset(BODY_HEIGHT - RIM_HEIGHT)):
            Polygon(_trapezoid_vertices(LENGTH, SHORT_END, LONG_END))
            Polygon(
                _trapezoid_vertices(LENGTH, SHORT_END, LONG_END, RIM_INSET),
                mode=Mode.SUBTRACT,
            )
        extrude(amount=RIM_HEIGHT, mode=Mode.SUBTRACT)

        # 4b. Divider rim: remove the two 2 mm shelves, leaving a 4 mm ridge
        #     centered on the divider (inset 2 mm from both faces).
        for shelf_center_x in (
            divider_center_x - DIVIDER_THICKNESS / 2 + RIM_INSET / 2,
            divider_center_x + DIVIDER_THICKNESS / 2 - RIM_INSET / 2,
        ):
            with BuildSketch(Plane.XY.offset(BODY_HEIGHT - RIM_HEIGHT)):
                with Locations((shelf_center_x, 0)):
                    Rectangle(RIM_INSET, 2 * divider_half_span)
            extrude(amount=RIM_HEIGHT, mode=Mode.SUBTRACT)

        # 5. Label-inlay recesses: cut LABEL_DEPTH-deep pockets for the
        #    separate SILICA and ALUMINA inlay part into the interior floor.
        small_center_x, large_center_x = _label_centers()
        with BuildSketch(Plane.XY.offset(BOTTOM_THICKNESS)):
            with Locations((small_center_x, 0)):
                Text(SILICA_LABEL, font_size=LABEL_FONT_SIZE)
            with Locations((large_center_x, 0)):
                Text(ALUMINA_LABEL, font_size=LABEL_FONT_SIZE)
        extrude(amount=-LABEL_DEPTH, mode=Mode.SUBTRACT)

    # 6. Vent slots on the four outer side walls below the rim (never on the
    #    bottom plate, the rim, or the divider): cut the fused slot tool from
    #    the tray in a single boolean operation.
    return Part([body.part.cut(*_body_vent_slot_boxes())])


def _make_lid(left_x: float, right_x: float) -> Part:
    """Return a lid covering the trapezoidal footprint between two X stations.

    The lid is a 2 mm top plate plus a 2 mm skirt.  The skirt wall is
    inset from the outer footprint by ``RIM_INSET - OOZE_CLEARANCE`` so it
    clears the body's 2 mm rim by ``OOZE_CLEARANCE`` radially while the
    skirt's outer face stays flush with the body's outer face.

    The top plate carries a grid of vent slots (5 x 1 mm, 1 mm margins):
    columns run along the lid's length and rows across its width, following
    the taper so the grid covers the whole top while staying clear of the
    skirt.  Each slot's cutting box extends just past the plate's underside
    by ``LID_SLOT_OVERCUT`` for a clean boolean.
    """
    lid_length = right_x - left_x
    center_x = (left_x + right_x) / 2
    left_width = 2 * _outer_half_width(left_x)
    right_width = 2 * _outer_half_width(right_x)
    skirt_inset = RIM_INSET - OOZE_CLEARANCE

    outer = _trapezoid_vertices(lid_length, left_width, right_width)
    outer = [v + Vector(center_x, 0) for v in outer]
    inner = _trapezoid_vertices(lid_length, left_width, right_width, skirt_inset)
    inner = [v + Vector(center_x, 0) for v in inner]

    with BuildPart() as lid:
        # Top plate plus skirt outer wall.
        with BuildSketch(Plane.XY):
            Polygon(outer)
        extrude(amount=LID_HEIGHT)

        # Hollow out the underside to leave a 2 mm skirt around the rim.
        with BuildSketch(Plane.XY):
            Polygon(inner)
        extrude(amount=LID_HEIGHT - LID_TOP_THICKNESS, mode=Mode.SUBTRACT)

    # Vent slots on the top plate (5 x 1 mm, 1 mm margins, through-cut),
    # arranged as a grid: one row of slots across the width for every column
    # along the length.  Rows follow the lid's taper (the interior width
    # inside the skirt shrinks toward the short end), so the grid covers the
    # whole top without cutting into the skirt.  All slot boxes are fused
    # into a single boolean operation.
    slot_boxes: list[Part] = []
    x_centers, _ = _slot_centers(lid_length, VENT_SLOT_LENGTH, VENT_MARGIN)
    z = LID_HEIGHT - LID_TOP_THICKNESS / 2
    perp = math.sqrt(1 + ((LONG_END - SHORT_END) / (2 * LENGTH)) ** 2)
    for x_rel in x_centers:
        x = left_x + x_rel
        # Half-width of the top-plate region inside the skirt at this X.
        inner_half = _outer_half_width(x) - skirt_inset * perp
        y_centers, _ = _slot_centers(
            2 * inner_half, VENT_SLOT_HEIGHT, VENT_MARGIN
        )
        for y_rel in y_centers:
            slot_boxes.append(
                Box(
                    VENT_SLOT_LENGTH,
                    VENT_SLOT_HEIGHT,
                    LID_TOP_THICKNESS + LID_SLOT_OVERCUT,
                    align=(Align.CENTER, Align.CENTER, Align.CENTER),
                ).moved(Location((x, y_rel - inner_half, z)))
            )

    return Part([lid.part.cut(*slot_boxes)])


def make_lid_small() -> Part:
    """Return the lid for the small (silica) compartment."""
    divider_center_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    right_x = divider_center_x - (DIVIDER_THICKNESS / 2 - RIM_INSET)
    return _make_lid(-LENGTH / 2, right_x)


def make_lid_large() -> Part:
    """Return the lid for the large (alumina) compartment."""
    divider_center_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    left_x = divider_center_x + (DIVIDER_THICKNESS / 2 - RIM_INSET)
    return _make_lid(left_x, LENGTH / 2)


def make_labels() -> Part:
    """Return the SILICA and ALUMINA label inlays as a part.

    The labels are printed in a contrasting filament and pressed into the
    matching ``LABEL_DEPTH``-deep recesses cut into the body's interior
    floor.  Each glyph is ``LABEL_DEPTH`` tall with its top face level with
    the floor (Z = ``BOTTOM_THICKNESS``).  They are exported inside the body
    assembly (``make_body_assembly``) rather than as their own STEP file.
    """
    small_center_x, large_center_x = _label_centers()
    with BuildPart() as labels:
        with BuildSketch(Plane.XY.offset(BOTTOM_THICKNESS - LABEL_DEPTH)):
            with Locations((small_center_x, 0)):
                Text(SILICA_LABEL, font_size=LABEL_FONT_SIZE)
            with Locations((large_center_x, 0)):
                Text(ALUMINA_LABEL, font_size=LABEL_FONT_SIZE)
        extrude(amount=LABEL_DEPTH)
    return labels.part


def make_body_assembly() -> Compound:
    """Return the body plus its label inlays as a single multi-material part.

    The labels stay as separate solids (not fused to the body) so a slicing
    tool can assign them a contrasting filament.  The body and labels are
    exported together in one STEP file (``desiccant_body.step``).
    """
    return Compound([make_body(), make_labels()])


#: The parts this module builds, keyed by the name a `--show` call uses.
#: ``body`` is the body-plus-labels assembly; the lids are single parts.
PARTS: dict[str, Shape] = {
    "body": make_body_assembly(),
    "lid_small": make_lid_small(),
    "lid_large": make_lid_large(),
}


#: Mapping from part registry name to the STEP file name written by ``main``.
_STEP_NAMES: dict[str, str] = {
    "body": "desiccant_body.step",
    "lid_small": "desiccant_lid_small.step",
    "lid_large": "desiccant_lid_large.step",
}


def make_assembly() -> list[Part]:
    """Return the assembled container as a list of separately positioned parts.

    The body sits at the origin, the label inlays sit in the floor at their
    natural positions, and each lid is raised so its skirt overlaps the rim
    (lifted by ``BODY_HEIGHT - RIM_HEIGHT``).  The parts are returned
    individually (not fused into a ``Compound``) so the viewer can show them
    as distinct, selectable objects.
    """
    lift = Location((0, 0, BODY_HEIGHT - RIM_HEIGHT))
    return [
        make_body(),
        make_labels(),
        make_lid_small().moved(lift),
        make_lid_large().moved(lift),
    ]


def show_part(name: str) -> None:
    """Show a part by name, or the full assembly, in the ocp_vscode viewer."""
    if name != "assembly" and name not in PARTS:
        known = ", ".join(sorted(PARTS)) + ", or assembly"
        raise SystemExit(f"unknown part {name!r}; choose from: {known}")

    from ocp_vscode import show

    if name == "assembly":
        show(
            *make_assembly(),
            names=["body", "labels", "lid_small", "lid_large"],
        )
    else:
        show(PARTS[name])


def main(argv: list[str] | None = None) -> None:
    """Export the desiccant container parts to STEP files and optionally show one."""
    parser = argparse.ArgumentParser(
        description="Export the desiccant container parts to STEP files."
    )
    parser.add_argument(
        "-o",
        "--outdir",
        default="manufacture",
        help="Output directory for the STEP files (default: manufacture)",
    )
    parser.add_argument(
        "--show",
        nargs="?",
        const="body",
        metavar="PART",
        help="Show a part (or 'assembly') in ocp_vscode after export; "
        "with no value, shows the primary part (default: body)",
    )
    args = parser.parse_args(argv)

    if args.show and args.show != "assembly" and args.show not in PARTS:
        known = ", ".join(sorted(PARTS)) + ", or assembly"
        parser.error(f"unknown part {args.show!r}; choose from: {known}")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for name, part in PARTS.items():
        outpath = outdir / _STEP_NAMES[name]
        export_step(part, str(outpath))
        print(f"wrote {outpath}")

    if args.show:
        show_part(args.show)


if __name__ == "__main__":
    main()
