"""Parametric geometry for the desiccant container body and lids.

The body is a monolithic 185 x (65/75) mm base plate with two independent
trapezoidal containers rising from it, separated by a 5 mm gap centred at
``DIVIDER_RATIO`` of the length from the short end.  Each container has 4 mm
walls on all four sides, a full-perimeter ``RIM_HEIGHT``-tall rim stepped
``RIM_INSET`` inward on every wall, a 2 mm bottom plate, and carries one
desiccant:

* the small (silica) container at the 65 mm short end, and
* the large (alumina) container at the 75 mm long end.

Two separate lids close the containers: each is a 2 mm top plate plus a
``RIM_HEIGHT``-tall skirt, with the skirt's outer face flush with the
container's outer face and a ``OOZE_CLEARANCE`` radial gap to the rim's outer
face so the lids mate without binding.

Ventilation: 5 x 1 mm rectangular through-slots (``VENT_SLOT_LENGTH`` x
``VENT_SLOT_HEIGHT``) with 1 mm solid margins (``VENT_MARGIN``) perforate
all four side walls of each container below the rim and both lids' top plates
- never the bottom plate or the rim.  Cutting boxes extend slightly past the
faces they pierce (``VENT_OVERCUT``, ``LID_SLOT_OVERCUT``) so the booleans
stay clean.

The interior cavity is formed by offsetting each of the four outer faces
inward by ``WALL_THICKNESS`` perpendicular to that face (a true polygon
offset), so the slanted side walls - like the end walls - are exactly
``WALL_THICKNESS`` thick measured normal to the face.  The same perpendicular
offset (by ``RIM_INSET``) defines the rim step on the top of every wall.

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
# The rim is the lip the lids grip.  The full-thickness wall below it is
# ``BODY_HEIGHT - RIM_HEIGHT`` tall and carries the vent slots.
RIM_HEIGHT = 12.0
RIM_INSET = 2.0
# The gap between the two independent containers.  Its centre is
# ``DIVIDER_RATIO`` of LENGTH from the short end.
GAP = 5.0
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
    """Corner vertices of an isosceles trapezoid centred on the origin.

    X spans ``+/- length/2`` along the length; Y spans ``+/- short_end/2``
    at the short (left) end and ``+/- long_end/2`` at the long (right) end.
    ``inset`` offsets each of the four faces inward by that amount
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


def _container_wall_length(left_x: float, right_x: float) -> float:
    """Length of one slanted side wall within [left_x, right_x], in mm."""
    dx = right_x - left_x
    dy = _outer_half_width(right_x) - _outer_half_width(left_x)
    return math.sqrt(dx ** 2 + dy ** 2)


def _slot_centers(span: float, slot_size: float, margin: float) -> tuple[list[float], float]:
    """Return equally spaced slot centres and the gap between them within ``span``.

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


def _container_vent_slot_boxes(left_x: float, right_x: float) -> list[Part]:
    """Positioned through-slot boxes for all four walls of a container
    spanning [left_x, right_x].

    The boxes are returned as a list of un-cut shapes so ``make_body`` can
    subtract them in a single fused boolean operation.  Slots perforate only
    the full-thickness wall below the rim, and never the bottom plate or the
    rim itself.  Each box extends slightly beyond the wall faces
    (``VENT_OVERCUT``) to avoid coplanar boolean issues.
    """
    boxes: list[Part] = []
    overcut = VENT_OVERCUT
    z_centers, _ = _slot_centers(
        BODY_HEIGHT - RIM_HEIGHT, VENT_SLOT_HEIGHT, VENT_MARGIN
    )
    if not z_centers:
        return boxes

    left_half = _outer_half_width(left_x)
    right_half = _outer_half_width(right_x)

    # Left end wall.
    y_centers, _ = _slot_centers(2 * left_half, VENT_SLOT_LENGTH, VENT_MARGIN)
    for y_rel in y_centers:
        y = y_rel - left_half
        for z in z_centers:
            boxes.append(
                Box(
                    WALL_THICKNESS + overcut,
                    VENT_SLOT_LENGTH,
                    VENT_SLOT_HEIGHT,
                    align=(Align.CENTER, Align.CENTER, Align.CENTER),
                ).moved(Location((left_x + WALL_THICKNESS / 2, y, z)))
            )

    # Right end wall.
    y_centers, _ = _slot_centers(2 * right_half, VENT_SLOT_LENGTH, VENT_MARGIN)
    for y_rel in y_centers:
        y = y_rel - right_half
        for z in z_centers:
            boxes.append(
                Box(
                    WALL_THICKNESS + overcut,
                    VENT_SLOT_LENGTH,
                    VENT_SLOT_HEIGHT,
                    align=(Align.CENTER, Align.CENTER, Align.CENTER),
                ).moved(Location((right_x - WALL_THICKNESS / 2, y, z)))
            )

    # Slanted side walls (both Y signs).
    angle = _wall_angle()
    wall_len = _container_wall_length(left_x, right_x)
    s_centers, _ = _slot_centers(wall_len, VENT_SLOT_LENGTH, VENT_MARGIN)
    for y_sign in (1, -1):
        angle_deg = (
            math.degrees(angle) if y_sign > 0 else math.degrees(-angle)
        )
        for s in s_centers:
            x = left_x + s * math.cos(angle)
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
    """X centres of the SILICA (small) and ALUMINA (large) label inlays.

    Each label is centred between the inner face of its end wall and the
    inner face of the gap-facing wall, on the interior floor.
    """
    gap_center_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    gap_half = GAP / 2
    small_left = -LENGTH / 2 + WALL_THICKNESS
    small_right = gap_center_x - gap_half - WALL_THICKNESS
    large_left = gap_center_x + gap_half + WALL_THICKNESS
    large_right = LENGTH / 2 - WALL_THICKNESS
    return (small_left + small_right) / 2, (large_left + large_right) / 2


def make_body() -> Part:
    """Return the desiccant container body as a build123d Part.

    Construction:
    1. extrude the full outer trapezoid footprint to ``BOTTOM_THICKNESS`` to
       form the shared base plate,
    2. build the small container: extrude its outer trapezoid footprint from
       the base top, hollow out its interior, cut its full-perimeter rim ring,
    3. build the large container: same operations with its own footprint,
    4. cut ``LABEL_DEPTH``-deep recesses for the SILICA and ALUMINA label
       inlays into each container's interior floor (see ``make_labels``),
    5. cut the vent slots (5 x 1 mm, 1 mm margins) through all four side walls
       of each container below the rim, in a single fused boolean operation;
       the bottom plate and the rim carry no vents.
    """
    gap_center_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    gap_half = GAP / 2

    # Small container outer footprint.
    small_left_x = -LENGTH / 2
    small_right_x = gap_center_x - gap_half
    small_outer_length = small_right_x - small_left_x
    small_center_x = (small_left_x + small_right_x) / 2
    small_left_width = SHORT_END
    small_right_width = 2 * _outer_half_width(small_right_x)

    # Large container outer footprint.
    large_left_x = gap_center_x + gap_half
    large_right_x = LENGTH / 2
    large_outer_length = large_right_x - large_left_x
    large_center_x = (large_left_x + large_right_x) / 2
    large_left_width = 2 * _outer_half_width(large_left_x)
    large_right_width = LONG_END

    with BuildPart() as body:
        # 1. Shared base plate: full trapezoid, BOTTOM_THICKNESS tall.
        with BuildSketch(Plane.XY):
            Polygon(_trapezoid_vertices(LENGTH, SHORT_END, LONG_END))
        extrude(amount=BOTTOM_THICKNESS)

        # 2a. Small container: extrude outer footprint above the base.
        small_outer = _trapezoid_vertices(
            small_outer_length, small_left_width, small_right_width
        )
        small_outer = [v + Vector(small_center_x, 0) for v in small_outer]
        with BuildSketch(Plane.XY.offset(BOTTOM_THICKNESS)):
            Polygon(small_outer)
        extrude(amount=BODY_HEIGHT - BOTTOM_THICKNESS)

        # 2b. Small container: hollow out interior (WALL_THICKNESS walls).
        small_inner = _trapezoid_vertices(
            small_outer_length, small_left_width, small_right_width,
            WALL_THICKNESS,
        )
        small_inner = [v + Vector(small_center_x, 0) for v in small_inner]
        with BuildSketch(Plane.XY.offset(BOTTOM_THICKNESS)):
            Polygon(small_inner)
        extrude(amount=BODY_HEIGHT - BOTTOM_THICKNESS, mode=Mode.SUBTRACT)

        # 3a. Large container: extrude outer footprint above the base.
        large_outer = _trapezoid_vertices(
            large_outer_length, large_left_width, large_right_width
        )
        large_outer = [v + Vector(large_center_x, 0) for v in large_outer]
        with BuildSketch(Plane.XY.offset(BOTTOM_THICKNESS)):
            Polygon(large_outer)
        extrude(amount=BODY_HEIGHT - BOTTOM_THICKNESS)

        # 3b. Large container: hollow out interior.
        large_inner = _trapezoid_vertices(
            large_outer_length, large_left_width, large_right_width,
            WALL_THICKNESS,
        )
        large_inner = [v + Vector(large_center_x, 0) for v in large_inner]
        with BuildSketch(Plane.XY.offset(BOTTOM_THICKNESS)):
            Polygon(large_inner)
        extrude(amount=BODY_HEIGHT - BOTTOM_THICKNESS, mode=Mode.SUBTRACT)

        # 4a. Small container perimeter rim ring: cut away the top RIM_HEIGHT
        #     outer RIM_INSET ring, leaving a 2 mm rim flush with the interior.
        small_rim_outer = _trapezoid_vertices(
            small_outer_length, small_left_width, small_right_width
        )
        small_rim_outer = [v + Vector(small_center_x, 0) for v in small_rim_outer]
        small_rim_inner = _trapezoid_vertices(
            small_outer_length, small_left_width, small_right_width, RIM_INSET
        )
        small_rim_inner = [v + Vector(small_center_x, 0) for v in small_rim_inner]
        with BuildSketch(Plane.XY.offset(BODY_HEIGHT - RIM_HEIGHT)):
            Polygon(small_rim_outer)
            Polygon(small_rim_inner, mode=Mode.SUBTRACT)
        extrude(amount=RIM_HEIGHT, mode=Mode.SUBTRACT)

        # 4b. Large container perimeter rim ring.
        large_rim_outer = _trapezoid_vertices(
            large_outer_length, large_left_width, large_right_width
        )
        large_rim_outer = [v + Vector(large_center_x, 0) for v in large_rim_outer]
        large_rim_inner = _trapezoid_vertices(
            large_outer_length, large_left_width, large_right_width, RIM_INSET
        )
        large_rim_inner = [v + Vector(large_center_x, 0) for v in large_rim_inner]
        with BuildSketch(Plane.XY.offset(BODY_HEIGHT - RIM_HEIGHT)):
            Polygon(large_rim_outer)
            Polygon(large_rim_inner, mode=Mode.SUBTRACT)
        extrude(amount=RIM_HEIGHT, mode=Mode.SUBTRACT)

        # 5. Label-inlay recesses: cut LABEL_DEPTH-deep pockets for the
        #    separate SILICA and ALUMINA inlay part into the interior floor.
        small_center_label_x, large_center_label_x = _label_centers()
        with BuildSketch(Plane.XY.offset(BOTTOM_THICKNESS)):
            with Locations((small_center_label_x, 0)):
                Text(SILICA_LABEL, font_size=LABEL_FONT_SIZE)
            with Locations((large_center_label_x, 0)):
                Text(ALUMINA_LABEL, font_size=LABEL_FONT_SIZE)
        extrude(amount=-LABEL_DEPTH, mode=Mode.SUBTRACT)

    # 6. Vent slots on all four side walls of each container (never on the
    #    bottom plate or the rim), fused into a single boolean cut.
    return Part(
        [
            body.part.cut(
                *_container_vent_slot_boxes(small_left_x, small_right_x),
                *_container_vent_slot_boxes(large_left_x, large_right_x),
            )
        ]
    )


def _make_lid(left_x: float, right_x: float) -> Part:
    """Return a lid covering the trapezoidal footprint between two X stations.

    The lid is a 2 mm top plate plus a 12 mm skirt.  The skirt wall is
    inset from the outer footprint by ``RIM_INSET - OOZE_CLEARANCE`` so it
    clears the container's 2 mm rim by ``OOZE_CLEARANCE`` radially while the
    skirt's outer face stays flush with the container's outer face.

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

        # Hollow out the underside to leave a 12 mm skirt around the rim.
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
    """Return the lid for the small (silica) container."""
    gap_center_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    right_x = gap_center_x - GAP / 2
    return _make_lid(-LENGTH / 2, right_x)


def make_lid_large() -> Part:
    """Return the lid for the large (alumina) container."""
    gap_center_x = -LENGTH / 2 + LENGTH * DIVIDER_RATIO
    left_x = gap_center_x + GAP / 2
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