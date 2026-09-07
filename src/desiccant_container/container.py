"""Parametric geometry for the desiccant container body.

The body is a trapezoidal tray: an isosceles trapezoid in plan view,
symmetric about its long centerline, centered on the origin (X along length,
Y across width, Z up).  It holds two compartments of desiccant:

* the small (silica) compartment at the 65 mm short end, and
* the large (alumina) compartment at the 75 mm long end.

It consists of a 2 mm bottom plate, 4 mm outer walls, a solid 8 mm internal
dividing wall (no vents) that keeps the two desiccants apart, and a 2 mm rim
stepped 2 mm inward on the top of every wall (outer perimeter and divider).
All dimensions are module-level parameters in millimetres.

The interior cavity is formed by offsetting each of the four outer faces
inward by ``WALL_THICKNESS`` perpendicular to that face (a true polygon
offset), so the slanted side walls - like the end walls - are exactly
``WALL_THICKNESS`` thick measured normal to the face.  The same
perpendicular offset (by ``RIM_INSET``) defines the rim step on the top of
every wall.
"""

import math

from build123d import (
    Align,
    Box,
    BuildPart,
    BuildSketch,
    Locations,
    Mode,
    Part,
    Plane,
    Polygon,
    Rectangle,
    Vector,
    extrude,
)

# --- Body dimensions (mm) ---
LENGTH = 185.0
SHORT_END = 65.0
LONG_END = 75.0
BODY_HEIGHT = 13.0
BOTTOM_THICKNESS = 2.0
WALL_THICKNESS = 4.0
DIVIDER_THICKNESS = 8.0
RIM_HEIGHT = 2.0
RIM_INSET = 2.0
DIVIDER_RATIO = 1 / 3


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
       leaving the 4 mm centered divider rim ridge.
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

    return body.part
