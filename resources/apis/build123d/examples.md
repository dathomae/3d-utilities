# build123d Examples

This document provides practical examples demonstrating common patterns and use cases in build123d.

## Basic Shapes

### Simple Box (Algebra Mode)

```python
from build123d import *

# Create a rectangular box
length, width, thickness = 80.0, 60.0, 10.0
box = Box(length, width, thickness)
```

### Simple Box (Builder Mode)

```python
from build123d import *

with BuildPart() as box:
    length, width, thickness = 80.0, 60.0, 10.0
    Box(length, width, thickness)
```

## Creating Holes

### Plate with Center Hole

```python
from build123d import *

# Algebra mode
plate = Box(4, 4, 1)
cylinder = Cylinder(1, 1) @ Pos(0, 0, 0.5)
plate_with_hole = plate - cylinder

# Builder mode
with BuildPart() as plate:
    Box(4, 4, 1)
    with Locations((0, 0, 0.5)):
        Cylinder(1, 1, mode=Mode.SUBTRACT)
```

### Multiple Holes in a Pattern

```python
from build123d import *

with BuildPart() as plate:
    # Base plate
    Box(5, 5, 1)
    
    # Create 4 holes in corners
    with Locations((2, 2), (-2, 2), (2, -2), (-2, -2)):
        Cylinder(0.3, 1, mode=Mode.SUBTRACT)
```

## Extruded Profiles

### Extruded Circle (Cylinder)

```python
from build123d import *

# Builder mode
with BuildPart() as cylinder:
    with BuildSketch() as sketch:
        Circle(1)
    extrude(amount=3)

# Algebra mode
sketch = Circle(1)
cylinder = extrude(sketch, 3)
```

### Complex Extruded Profile

```python
from build123d import *

with BuildPart() as part:
    with BuildSketch() as profile:
        # Outer rectangle
        Rectangle(4, 3)
        # Subtract inner rectangle (hollow section)
        Rectangle(2, 1.5, mode=Mode.SUBTRACT)
    extrude(amount=2)
```

## Combining Shapes

### Boolean Union

```python
from build123d import *

with BuildPart() as combined:
    # Base shape
    Box(3, 3, 1)
    # Add cylinder on top
    with Locations((0, 0, 0.5)):
        Cylinder(1, 2, mode=Mode.ADD)
```

### Boolean Difference

```python
from build123d import *

with BuildPart() as bracket:
    Box(4, 2, 3)
    # Cut out material
    with Locations((0, 0, 0)):
        Box(2, 2.1, 2, mode=Mode.SUBTRACT)
```

### Intersection

```python
from build123d import *

with BuildPart() as intersection:
    Box(3, 3, 3)
    with Locations((1.5, 1.5, 1.5)):
        Cylinder(1.5, 3, mode=Mode.INTERSECT)
```

## Using Algebra Mode

### Complex Shape with Operators

```python
from build123d import *

# Create a disk with cutouts
a, b, c, d = 2, 1, 0.5, 0.3
sketch = Circle(a) - Pos(b, 0.0) * Rectangle(c, c) - Pos(0.0, b) * Circle(d)
disk = extrude(sketch, 0.5)
```

### Positioning with @ Operator

```python
from build123d import *

# Create two boxes at different positions
box1 = Box(1, 1, 1) @ Pos(0, 0, 0)
box2 = Box(1, 1, 1) @ Pos(2, 0, 0)

# Combine them
combined = box1 + box2
```

## Patterns and Arrays

### Circular Pattern (PolarLocations)

```python
from build123d import *

with BuildPart() as part:
    # Base cylinder
    Cylinder(3, 1)
    
    # 6 bolt holes in a circle
    with PolarLocations(radius=2, count=6):
        Cylinder(0.3, 1, mode=Mode.SUBTRACT)
```

### Grid Pattern (GridLocations)

```python
from build123d import *

with BuildPart() as part:
    Box(5, 5, 1)
    
    # 3x3 grid of holes
    with GridLocations(x_spacing=1.5, y_spacing=1.5, x_count=3, y_count=3):
        Cylinder(0.2, 1, mode=Mode.SUBTRACT)
```

### Linear Pattern (Locations)

```python
from build123d import *

with BuildPart() as part:
    Box(6, 2, 1)
    
    # Row of holes
    with Locations((-2, 0), (0, 0), (2, 0)):
        Cylinder(0.3, 1, mode=Mode.SUBTRACT)
```

## Fillets and Chamfers

### Adding Fillets (Rounded Edges)

```python
from build123d import *

with BuildPart() as part:
    Box(4, 3, 2)
    
    # Fillet all edges
    fillet(part.edges(), radius=0.3)
```

### Adding Chamfers (Beveled Edges)

```python
from build123d import *

with BuildPart() as part:
    Box(4, 3, 2)
    
    # Chamfer top edges
    top_edges = part.faces().sort_by(Axis.Z)[-1].edges()
    chamfer(top_edges, length=0.3)
```

## Revolved Shapes

### Revolve a Profile

```python
from build123d import *

with BuildPart() as bowl:
    with BuildSketch(Plane.YZ) as profile:
        # Create profile (cross-section)
        with BuildLine() as outline:
            Line((0, 0), (2, 0))
            Line((2, 0), (2.5, 1))
            Line((2.5, 1), (0, 1.5))
        make_face()
    
    # Revolve around Z axis
    revolve(axis=Axis.Z, angle=360)
```

## Lofted Shapes

### Loft Between Profiles

```python
from build123d import *

with BuildPart() as shape:
    # Bottom profile
    with BuildSketch(Plane.XY) as bottom:
        Circle(1)
    
    # Middle profile
    with BuildSketch(Plane.XY.offset(2)) as middle:
        Rectangle(2, 2)
    
    # Top profile
    with BuildSketch(Plane.XY.offset(4)) as top:
        Circle(0.5)
    
    # Loft through all profiles
    loft()
```

## Swept Shapes

### Sweep Along a Path

```python
from build123d import *

with BuildPart() as pipe:
    # Create the path
    with BuildLine() as path:
        Line((0, 0, 0), (5, 0, 0))
        CenterArc((5, 2, 0), 2, -90, 90)
        Line((5, 4, 0), (10, 4, 0))
    
    # Create cross-section and sweep
    with BuildSketch(path.line) as section:
        Circle(0.5)
    sweep()
```

## Working with Faces

### Extrude from Face

```python
from build123d import *

with BuildPart() as part:
    # Base shape
    Box(4, 4, 1)
    
    # Create workplane on top face
    top_face = part.faces().sort_by(Axis.Z)[-1]
    with Workplanes(top_face):
        with BuildSketch():
            Circle(1)
        extrude(amount=2)
```

### Mirror Geometry

```python
from build123d import *

with BuildPart() as part:
    # Create half
    with BuildSketch():
        Rectangle(2, 1)
        Rectangle(1, 2, align=(Align.MIN, Align.MAX))
    extrude(amount=1)
    
    # Mirror to create symmetric part
    mirror(about=Plane.YZ)
```

## Text and Labels

### 3D Text

```python
from build123d import *

with BuildPart() as label:
    # Base plate
    Box(10, 3, 0.5)
    
    # Raised text
    with Workplanes(Plane.XY.offset(0.5)):
        with BuildSketch():
            Text("HELLO", font_size=2)
        extrude(amount=0.3)
```

## Import and Export

### Export to STL

```python
from build123d import *

# Create your model
part = Box(10, 10, 5)

# Export for 3D printing
export_stl(part, "output.stl")
```

### Export to STEP

```python
from build123d import *

part = Box(10, 10, 5)
export_step(part, "output.step")
```

### Import STEP File

```python
from build123d import *

# Import existing CAD file
part = import_step("existing.step")
```

## Complete Example: Mechanical Part

### Bracket with Multiple Features

```python
from build123d import *

with BuildPart() as bracket:
    # Main body
    Box(6, 4, 1)
    
    # Add mounting flange
    with Locations((-3, 0, 0.5)):
        Box(1, 4, 2, align=(Align.MAX, Align.CENTER, Align.MIN))
    
    # Holes in flange
    with Workplanes(Plane.YZ.offset(-3)):
        with PolarLocations(radius=1.5, count=4):
            Cylinder(0.25, 1, mode=Mode.SUBTRACT)
    
    # Center hole
    with Locations((0, 0, 0)):
        Cylinder(1, 1, mode=Mode.SUBTRACT)
    
    # Fillets on edges
    fillet(bracket.edges(), radius=0.2)

# Export result
export_stl(bracket.part, "bracket.stl")
```

## Tips and Best Practices

1. **Choose Your Mode**: Use builder mode for complex multi-step parts, algebra mode for simple expressions
2. **Naming**: Use descriptive variable names for intermediate shapes
3. **Debugging**: Use `show_topology()` to inspect your geometry
4. **Performance**: Reuse sketches when possible to avoid recalculation
5. **Organization**: Group related features in separate `with` blocks
