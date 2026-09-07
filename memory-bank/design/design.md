# Design

## Project Design

`3d-utilities` is a collection, not a single artifact, so its "design" is the repository structure and shared conventions rather than one assembly of parts.

- Modeling code lives in the Python package under `src/scaffold/`, one module per utility. Each module defines the object's geometry as build123d code and exports it as STEP into `manufacture/`.
- `resources/modeling/` holds reusable, cross-utility knowledge (screws, mill jigs, brackets, snap fits, and general techniques); `resources/apis/build123d/` holds the build123d API and usage notes.
- `memory-bank/` holds the living project records (brief, requirements, context, concepts, terms, lessons learned, bugs) plus plans and stories.
- Each utility that needs more than a module may add its own design document in a subdirectory under `memory-bank/design/`, following the same skeleton as this file.

The workflow is code-first and parametric: model in Python, export STEP, then manufacture with a slicer (3D printing) or CAM (milling). The source of truth is the Python module; STEP files under `manufacture/` are generated, gitignored artifacts.

## Parts List

There is no single parts list for the collection. Each utility defines its own parts in its module and, where a design document exists, lists them there with material, dimensions, and manufacturing method.

Initial utilities:

| Utility | Module | Purpose | Manufacturing method |
|---------|--------|---------|----------------------|
| Mounting-hole pattern | `src/scaffold/mill_bed.py` | Encodes the vertical mill bed's M5 mounting-hole grid (7 × 5, lower-left absent) for reuse by jigs. | — (reference data) |
| Mounting test sheet | `src/scaffold/mounting_sheet.py` | A 1 mm sheet with an M5 clearance hole at each bed location, printed to verify the pattern. | 3D printing |
| Example box | `src/scaffold/example.py` | A 10 mm cube demonstrating the module-and-export workflow. | 3D printing / milling |
