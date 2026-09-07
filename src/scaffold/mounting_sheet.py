"""Test sheet for verifying the vertical mill bed mounting-hole pattern.

Builds a thin sheet with a clearance (shank) hole at each bed mounting
location, so it can be 3D printed and laid against the mill bed to confirm the
hole measurements. The sheet is too thin (1 mm) to recess the screw heads, so
each hole is a plain through-hole sized for the M5 shank and threads.

See `resources/modeling/vertical_mill_jigs.md` for the pattern and
`resources/modeling/screws.md` for the M5 dimensions.
"""

import argparse
from pathlib import Path

from build123d import Box, BuildPart, Hole, Locations, Part, export_step

from scaffold.mill_bed import mounting_hole_locations

SHEET_LENGTH = 310.0
SHEET_HEIGHT = 225.0
SHEET_THICKNESS = 1.0

#: Clearance (shank) hole radius for an M5 screw (5.8 mm diameter).
SHANK_RADIUS = 5.8 / 2


def make_mounting_sheet() -> Part:
    """Return a 340 × 225 × 1 mm sheet with an M5 clearance hole at each bed
    mounting location.

    The sheet is centered at the origin. Hole positions are the bed's mounting
    locations translated from the lower-left bed origin to the sheet center.
    """
    with BuildPart() as sheet:
        Box(SHEET_LENGTH, SHEET_HEIGHT, SHEET_THICKNESS)
        hole_positions = [
            (x - SHEET_LENGTH / 2, y - SHEET_HEIGHT / 2, SHEET_THICKNESS / 2)
            for x, y in mounting_hole_locations()
        ]
        with Locations(hole_positions):
            Hole(radius=SHANK_RADIUS)
    return sheet.part


def main(argv: list[str] | None = None) -> None:
    """Export the mounting test sheet to a STEP file."""
    parser = argparse.ArgumentParser(
        description="Export the mounting test sheet to a STEP file."
    )
    parser.add_argument(
        "-o",
        "--outdir",
        default="manufacture",
        help="Output directory for the STEP file (default: manufacture)",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Show the sheet in ocp_vscode after export",
    )
    args = parser.parse_args(argv)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / "mounting_sheet.step"
    export_step(make_mounting_sheet(), str(outpath))
    print(f"wrote {outpath}")

    if args.show:
        from ocp_vscode import show

        show(make_mounting_sheet())


if __name__ == "__main__":
    main()
