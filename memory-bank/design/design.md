# Design

## Project Design

`3d-utilities` is a collection, not a single artifact, so its "design" is the repository structure and shared conventions rather than one assembly of parts.

- Modeling code lives in per-utility directories under `src/`: each new utility is its own `src/<utility_name>/` directory, containing the utility's parametric modeling code and its `README.md`, and exports its geometry as STEP into `manufacture/`. The existing `src/scaffold/` package is grandfathered as the pre-convention home of the older modeling code.
- `resources/modeling/` holds reusable, cross-utility knowledge (screws, mill jigs, brackets, snap fits, and general techniques); `resources/apis/build123d/` holds the build123d API and usage notes.
- `memory-bank/` holds the living project records (brief, requirements, context, concepts, terms, lessons learned, bugs) plus plans and stories.
- A utility may also carry its own design document in a subdirectory under `memory-bank/design/`, following the same skeleton as this file.

The workflow is code-first and parametric: model in Python, export STEP, then manufacture with a slicer (3D printing) or CAM (milling). The source of truth is the Python module; STEP files under `manufacture/` are generated, gitignored artifacts.

## Parts List

There is no single parts list for the collection. Each utility defines its own parts in its source and, where a design document exists, lists them there with material, dimensions, and manufacturing method.

The utilities that predate the per-utility directory convention remain in the grandfathered `src/scaffold/` package:

| Utility | Module | Purpose | Manufacturing method |
|---------|--------|---------|----------------------|
| Mounting-hole pattern | `src/scaffold/mill_bed.py` | Encodes the vertical mill bed's M5 mounting-hole grid (7 × 5, lower-left absent) for reuse by jigs. | — (reference data) |
| Mounting test sheet | `src/scaffold/mounting_sheet.py` | A 1 mm sheet with an M5 clearance hole at each bed location, printed to verify the pattern. | 3D printing |
| Example box | `src/scaffold/example.py` | A 10 mm cube demonstrating the module-and-export workflow. | 3D printing / milling |

The desiccant container is the first utility to follow the per-utility directory convention, living in `src/desiccant_container/`. It defines three parts, built by `make_body`, `make_lid_small`, and `make_lid_large`, and exported as `desiccant_body.step`, `desiccant_lid_small.step`, and `desiccant_lid_large.step`; the parts are specified in the [desiccant container plan](../plans/desiccant-container_plan.md).
