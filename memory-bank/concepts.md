# Concepts

General or abstract ideas used across the project. Add one row per concept and link the closely related concepts and terms.

| Concept | Description | Related Concepts/Terms |
|---------|-------------|------------------------|
| Utility project | A small, single-purpose object (a container, jig, fixture, or similar) defined in its own directory under `src/` and manufactured as one part. | Parametric modeling, STEP export |
| Parametric modeling | Defining geometry in code so dimensions are parameters (variables or function arguments) that can be changed and re-run, rather than drawn by hand. | build123d, Utility project |
| STEP export | Writing the model as a STEP (ISO 10303) boundary-representation file, the neutral interchange used by slicers and CAM tools. | Manufacturing method, Parametric modeling |
| Manufacturing method | The process that turns STEP geometry into a physical object: additive (3D printing via a slicer) or subtractive (milling via CAM). | STEP export |
| Jig / fixture | A device that locates, holds, or guides a workpiece or tool, for example a mill-bed mounting jig. | Utility project, M5 |
| Container | An enclosure or holder for storing or organizing objects. | Utility project |
