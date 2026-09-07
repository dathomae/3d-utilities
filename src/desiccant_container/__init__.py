"""Desiccant container utility: parametric two-compartment tray geometry.

Exports the body builder (`make_body`) and the two lid builders
(`make_lid_small`, `make_lid_large`) together with the module-level dimension
parameters.
"""

from desiccant_container.container import (
    BODY_HEIGHT,
    BOTTOM_THICKNESS,
    DIVIDER_RATIO,
    DIVIDER_THICKNESS,
    LENGTH,
    LID_HEIGHT,
    LID_TOP_THICKNESS,
    LONG_END,
    OOZE_CLEARANCE,
    RIM_HEIGHT,
    RIM_INSET,
    SHORT_END,
    WALL_THICKNESS,
    make_body,
    make_lid_large,
    make_lid_small,
)

__all__ = [
    "BODY_HEIGHT",
    "BOTTOM_THICKNESS",
    "DIVIDER_RATIO",
    "DIVIDER_THICKNESS",
    "LENGTH",
    "LID_HEIGHT",
    "LID_TOP_THICKNESS",
    "LONG_END",
    "OOZE_CLEARANCE",
    "RIM_HEIGHT",
    "RIM_INSET",
    "SHORT_END",
    "WALL_THICKNESS",
    "make_body",
    "make_lid_large",
    "make_lid_small",
]
