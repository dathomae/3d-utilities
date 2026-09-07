# Project Brief

## Overview

`3d-utilities` is a collection of small, single-purpose, parametric 3D-modeling utilities for 3D printing and milling. Each utility is one self-contained object — a container, a jig, a fixture, or something similar — defined in Python with build123d, exported as STEP geometry, and manufactured from that STEP file with a slicer (additive: 3D printing) or a CAM tool (subtractive: milling).

The repository provides the shared scaffolding for all of these utilities: a Python package for the modeling code, a workflow that exports STEP into `manufacture/`, a plan-and-story workflow under `memory-bank/`, and reusable modeling knowledge under `resources/modeling/`. Individual utilities add one module under `src/scaffold/` and, when they warrant it, their own design document under `memory-bank/design/`.

## Project Goals

1. Provide a single home and shared tooling for many small modeling utilities rather than a separate repository per object.
2. Keep every utility parametric and code-first: dimensions are Python parameters, so a change is a re-run, not a redraw.
3. Export every utility to STEP so it can be manufactured by either method — sliced and 3D printed, or machined on a mill.
4. Capture reusable, cross-utility knowledge (fastener dimensions, jig conventions, modeling techniques) so later utilities do not re-derive it.

## Key Design Considerations

- **Manufacturing methods**: utilities target 3D printing (FDM), milling (subtractive), or both, so designs account for print tolerances and overhangs as well as tool clearances and workholding.
- **Units and fasteners**: dimensions are in millimeters; machine screws use the standardized sizes documented in `resources/modeling/screws.md`, and mill-bed jigs follow the M5 mounting convention in `resources/modeling/vertical_mill_jigs.md`.
- **Self-containment**: each utility is a small module that builds exactly one object, so utilities stay independent and easy to reuse or remove.
- **STEP as the interchange**: the source of truth is the Python module; the generated STEP file is a gitignored artifact under `manufacture/`.
