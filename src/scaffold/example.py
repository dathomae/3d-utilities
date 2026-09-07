"""Example build123d box builder with a small STEP-export CLI.

This module is intentionally minimal and dependency-light (only build123d is
imported for geometry) because the scaffold package is meant to be replaced
wholesale by a derived repository.
"""

import argparse
from pathlib import Path

from build123d import Box, Compound, Part, export_step


def make_box() -> Part:
    """Return a 10 mm cube centered at the origin as a build123d Part."""
    return Box(10, 10, 10)


#: The parts this scaffold builds, keyed by the name a `--show` call uses.
PARTS: dict[str, Part] = {"box": make_box()}


def make_assembly() -> Compound:
    """Return the entire assembly of parts as a single build123d Compound."""
    return Compound(list(PARTS.values()))


def show_part(name: str) -> None:
    """Show a part by name, or the full assembly, in the ocp_vscode viewer."""
    from ocp_vscode import show

    if name == "assembly":
        show(make_assembly())
    elif name in PARTS:
        show(PARTS[name])
    else:
        known = ", ".join(sorted(PARTS)) + ", or assembly"
        raise SystemExit(f"unknown part {name!r}; choose from: {known}")


def main(argv: list[str] | None = None) -> None:
    """Export the example box to a STEP file and optionally show it."""
    parser = argparse.ArgumentParser(
        description="Export the scaffold example box to a STEP file."
    )
    parser.add_argument(
        "-o",
        "--outdir",
        default="manufacture",
        help="Output directory for the STEP file (default: manufacture)",
    )
    parser.add_argument(
        "--show",
        nargs="?",
        const="box",
        metavar="PART",
        help="Show a part (or 'assembly') in ocp_vscode after export; "
        "with no value, shows the primary part (default: box)",
    )
    args = parser.parse_args(argv)

    if args.show and args.show != "assembly" and args.show not in PARTS:
        known = ", ".join(sorted(PARTS)) + ", or assembly"
        parser.error(f"unknown part {args.show!r}; choose from: {known}")

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    outpath = outdir / "scaffold_box.step"
    export_step(make_box(), str(outpath))
    print(f"wrote {outpath}")

    if args.show:
        show_part(args.show)


if __name__ == "__main__":
    main()
