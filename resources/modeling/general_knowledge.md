# General 3D Modeling Knowledge with build123d

This document captures general knowledge and practical lessons learned while using the `build123d` package for 3D modeling.

## 1. Hexagonal Grids
While `HexLocations` is available, it centers the grid based on the count of items, which can sometimes make it difficult to align the grid exactly with the origin `(0,0)`. For precise control over the grid center and boundaries (e.g., fitting tubes within a cylinder), generating the grid manually using nested loops and `math.sqrt(3)/2` for row spacing is often more predictable and robust.

## 2. Working with 1D Edges (e.g., Helix)
- `Helix` is an edge object, not a context manager. By default, it starts at `(radius, 0, 0)`.
- To position a `Helix` or other 1D edges within a `BuildLine` context, you must move the object explicitly using `.moved(Location(...))` and then add it to the context using the `add()` function.
- Example: `h1 = Helix(...).moved(Location((0, 0, z)))` followed by `add(h1)` inside `with BuildLine():`.

## 3. Sweeping Profiles along Complex Paths
- **Self-Intersecting Solids**: Sweeping a non-circular profile (like a `Rectangle`) along a 3D path with sharp corners or tight curves can result in an invalid, self-intersecting solid. Even using `transition=Transition.ROUND` might not resolve this if the profile is too large relative to the path's curvature.
- **Silent Failures**: If a swept solid is invalid, boolean operations like `Mode.SUBTRACT` will fail silently, leaving only an outline or surface instead of actually cutting into the target body.
- **The Ball-End Mill Approach**: To create a robust, valid, and smooth groove or channel along a complex path with sharp corners:
  1. Use a circular profile (simulating a ball-end mill).
  2. Sweep the circular profile along each segment of the path individually.
  3. Place a `Sphere` of the same radius at each joint (vertex) where the segments meet.
  4. This guarantees a valid, continuous solid with perfectly smooth, rounded transitions, avoiding the twisting and self-intersection issues of sweeping a single profile along the entire path.

## 4. Frenet Frame (`is_frenet=True`)
When sweeping along 3D curves (like a helix), using `is_frenet=True` keeps the profile normal to the path. However, the Frenet frame can twist abruptly at inflection points or straight lines, causing non-circular profiles to twist unpredictably. Using a circular profile avoids these twisting issues entirely because circles are rotationally invariant.

## 5. Invalid Solids and Silent Failures
- **Features Sticking Out**: If you add a feature (like a `Sphere` or `Box`) to a solid body, and that feature protrudes past the outer boundary of the main body in a way that creates a zero-thickness intersection or non-manifold geometry (e.g., a sphere whose radius is larger than the wall thickness it's embedded in), the resulting part may become an "invalid solid" in OpenCASCADE.
- **Silent Drops in Assemblies**: When `build123d` attempts to export an assembly (`Compound`) containing an invalid solid to a `.step` file, the invalid part will often be silently dropped from the assembly. The export will succeed, but the resulting file will be missing the invalid component.
- **Corrupt Files**: Exporting an invalid solid directly to a `.step` file can result in a corrupt file that cannot be read by other CAD programs.
- **Debugging**: If a part is missing from an assembly or a `.step` file is unreadable, check the validity of the individual parts using `part.is_valid`. If a part is invalid, check for features that might be protruding through walls or creating non-manifold geometry.

## 6. Nested Contexts and Redundant `add()` Calls
When using nested `BuildPart` (or `BuildSketch`, `BuildLine`) contexts, `build123d` automatically adds the result of the inner context to the outer context upon exiting the `with` block. 

**Do NOT explicitly call `add()` on the inner context's `.part` or `.sketch` if it was created inside the outer context.** Doing so can cause silent boolean operation failures, which may result in the outer part being completely replaced by the inner part (e.g., your main body disappears and only the small added features remain).

**What DOES NOT work (Redundant Add):**
```python
with BuildPart() as main_body:
    Box(10, 10, 10)
    
    # Inner context automatically adds its result to main_body
    with BuildPart() as nubs:
        with Locations((5, 0, 0)):
            Sphere(2)
            
    # BAD: This redundant add() will cause a boolean failure!
    # The main_body might disappear, leaving only the nubs.
    add(nubs.part) 
```

**What DOES work (Automatic Add):**
```python
with BuildPart() as main_body:
    Box(10, 10, 10)
    
    # Inner context automatically adds its result to main_body
    with BuildPart() as nubs:
        with Locations((5, 0, 0)):
            Sphere(2)
            
    # GOOD: No explicit add() is needed. The nubs are already part of main_body.
```

## 7. BuildSketch and Active Locations
When using `BuildSketch()` inside a `BuildPart` context, it does **not** automatically inherit the active locations from the parent `BuildPart` to position the sketch plane. If you call `BuildSketch()` without arguments, it will always create a sketch on the default `Plane.XY` at the origin `(0, 0, 0)`.

If you want to create sketches at multiple active locations (e.g., to extrude a profile at several different points), you must explicitly pass those locations as workplanes to `BuildSketch`.

**What DOES NOT work (Sketch created at origin):**
```python
with BuildPart() as p:
    with Locations(Location((10, 0, 0)), Location((-10, 0, 0))):
        # This sketch will be created at (0, 0, 0), ignoring the active locations!
        with BuildSketch():
            Circle(5)
        # This will extrude a single cylinder at the origin.
        extrude(amount=10)
```

**What DOES work (Passing locations explicitly):**
```python
locs = [Location((10, 0, 0)), Location((-10, 0, 0))]
with BuildPart() as p:
    # Pass the locations directly to BuildSketch as workplanes
    with BuildSketch(*locs):
        Circle(5)
    # This will correctly extrude two cylinders at the specified locations.
    extrude(amount=10)
```
