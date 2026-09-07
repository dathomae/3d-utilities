# Debugging Build123D Models

When working with Build123D, it's common to encounter issues where parts don't align correctly, holes don't appear, or boolean operations fail silently. This document captures techniques that work well for diagnosing and fixing these problems.

## 1. The "Silent Failure" of Part Operations

**Problem:** You call a part operation like `CounterSinkHole` or `Cylinder(mode=Mode.SUBTRACT)`, but the resulting part doesn't have the expected holes or cuts.

**Why it happens:** Part operations apply to the active `BuildPart` context. If the operation's geometry (e.g., the hole) doesn't intersect the part's geometry, the operation will succeed silently without modifying the part. This usually happens because the part or the hole is not located where you think it is.

**Debugging Technique:**
1. **Check the Bounding Box:** Print the bounding box of the part *before* the operation to verify its location in global space.
   ```python
   print(my_part.part.bounding_box())
   ```
2. **Isolate the Operation:** Create a minimal test script with a simple `Box` and apply the operation to see if it works in isolation.
3. **Verify Local vs. Global Coordinates:** Remember that `Locations` contexts stack. If you extrude a sketch, the resulting solid is in global space. If you then apply a hole, ensure the hole's location is correct relative to the solid's global position.

## 2. The "Shifted Sketch" Problem

**Problem:** You define a 2D profile using `Polygon` or other sketch objects, but when you extrude it, the resulting 3D part is shifted from the coordinates you specified.

**Why it happens:** Many 2D objects in Build123D, such as `Polygon`, have an `align` parameter that defaults to `(Align.CENTER, Align.CENTER)`. This automatically centers the sketch around the origin `(0, 0)`, shifting all your carefully calculated coordinates.

**Debugging Technique:**
1. **Print the Sketch Bounding Box:** Before extruding, print the bounding box of the sketch to see if it matches your expected coordinates.
   ```python
   print(my_profile.sketch.bounding_box())
   ```
2. **Disable Alignment:** If you want the sketch to remain exactly at the coordinates you specified, explicitly set `align=None`.
   ```python
   # What works well:
   with BuildSketch(Plane.YZ) as profile:
       Polygon([
           (0, 0),
           (10, 0),
           (10, 10),
           (0, 10)
       ], align=None) # Keeps coordinates exactly as specified
   ```

## 3. Composing Locations

**Problem:** You want to apply an operation at multiple locations, but it only applies to one, or it applies in the wrong place.

**Why it happens:** `Locations` contexts compose, but you must be careful about how you nest them.

**Debugging Technique:**
1. **Test Location Composition:** Write a small script to verify how locations are combining.
   ```python
   # What works well:
   hole_locs = [Location((10, 0, 0)), Location((-10, 0, 0))]
   with Locations(*hole_locs):
       # This adds (0, 0, 5) to EACH of the hole_locs
       with Locations((0, 0, 5)):
           CounterSinkHole(radius=1, counter_sink_radius=2)
   ```
2. **Count Faces:** A quick way to verify if multiple holes were created is to count the faces of the resulting part. A simple box has 6 faces. Each countersink hole adds 2 faces (cylinder + cone). If you expect 2 holes, you should have 6 + 2*2 = 10 faces.
   ```python
   print(len(my_part.part.faces()))
   ```

## 4. Visualizing Intermediate Steps

**Problem:** A complex assembly is failing, and it's hard to tell which part is causing the issue.

**Debugging Technique:**
1. **Export Intermediate Parts:** Export individual parts or intermediate stages of the assembly to `.step` files and view them in a CAD viewer.
   ```python
   export_step(intermediate_part, "manufacture/debug_part.step")
   ```
2. **Use ocp_vscode:** If available, use the `show()` function from `ocp_vscode` to visualize the model directly in your editor. Pay attention to warnings in the console, such as `CameraKeepWarning`, which might indicate you need to reset your camera view to see the updated model.
