# build123d Core Concepts

## Overview

build123d is built on top of OpenCASCADE (OCCT) and provides two primary APIs:

1. **Builder Mode** - Uses context managers for intuitive, step-by-step construction
2. **Algebra Mode** - Uses Python operators for concise, expression-based modeling

## Topology Hierarchy

build123d organizes geometric elements in a hierarchical structure based on topological dimension:

### Topological Elements

| Element | Dimension | Description |
|---------|-----------|-------------|
| **Vertex** | 0D | A precise point in 3D space; endpoints or intersections of edges |
| **Edge** | 1D | A curve with shape and position; defines boundaries of faces |
| **Wire** | 1D | A connected sequence of edges forming an open or closed loop |
| **Face** | 2D | A bounded surface; provides surfaces for constructing solids |
| **Shell** | 2D | A collection of faces defining a closed, connected volume |
| **Solid** | 3D | A bounded volume with well-defined interior and exterior |
| **Compound** | Any | A container grouping multiple geometric shapes of any type |

### Shape Base Class

All topological elements inherit from the `Shape` base class, which provides:

- Common transformation methods
- Topology inspection (`show_topology()`)
- Bounding box calculations
- Center point queries

```python
from build123d import *

# Display topology of a unit cube
box = Solid.make_box(1, 1, 1)
print(box.show_topology(limit_class="Face"))
```

## Location and Positioning

### Location Class

A `Location` represents the combination of translation and rotation applied to an object:

```python
from build123d import *

# Create a box and get its location
box = Box(1, 1, 1)
box_location = box.location

# Access position and orientation
print(box_location.position)    # Vector(0, 0, 0)
print(box_location.orientation) # Vector(0, 0, 0) - rotations

# Set position and orientation
box_location.position = (1, 2, 3)
box_location.orientation = (30, 40, 50)  # degrees

# Relative changes
box_location.position += (3, 2, 1)
```

### Position Helper

The `Pos` class provides a convenient way to specify positions:

```python
from build123d import *

# Position an object at specific coordinates
box = Box(1, 1, 1) @ Pos(5, 0, 0)

# Equivalent in builder mode
with BuildPart() as box:
    with Locations((5, 0, 0)):
        Box(1, 1, 1)
```

## Builder Mode vs Algebra Mode

### Builder Mode

Builder mode uses context managers for step-by-step construction:

```python
from build123d import *

with BuildPart() as part:
    with BuildSketch() as sketch:
        Circle(1)
    extrude(amount=2)
```

Key features:
- Uses `with` statements for context
- Objects are automatically added to the current builder
- `Locations` context positions objects
- Operations like `extrude()` transform the current sketch

### Algebra Mode

Algebra mode uses Python operators for concise expressions:

```python
from build123d import *

# Create a disk by subtracting rectangles from a circle
sketch = Circle(1) - Pos(0.5, 0) * Rectangle(0.5, 1)
disk = extrude(sketch, 0.5)
```

Key features:
- Uses `+`, `-`, `*` operators for union, subtraction, and positioning
- No context managers required
- Functions like `extrude()` operate on shapes directly

## Alignment

Objects can be aligned relative to themselves using the `Align` enum:

```python
from build123d import *

# Align a circle to minimum X and Y (top-right corner)
circle = Circle(1, align=(Align.MIN, Align.MIN))

# Use a single alignment value for all axes
circle = Circle(1, align=Align.CENTER)
```

Alignment values:
- `Align.MIN` - Align to minimum (left/bottom)
- `Align.CENTER` - Center the object
- `Align.MAX` - Align to maximum (right/top)

## Modes for Boolean Operations

When combining objects in builder mode, the `mode` parameter controls how they interact:

| Mode | Description |
|------|-------------|
| `Mode.ADD` | Add object to the object under construction (default) |
| `Mode.SUBTRACT` | Cut this object from the object under construction |
| `Mode.INTERSECT` | Intersect this object with the object under construction |
| `Mode.REPLACE` | Replace the object under construction with this object |
| `Mode.PRIVATE` | Do not interact with the object under construction |

```python
from build123d import *

with BuildPart() as part:
    Box(4, 4, 1)  # Base plate
    with Locations((0, 0, 1)):
        Cylinder(1, 2, mode=Mode.ADD)  # Add cylinder
    with Locations((2, 0, 0)):
        Cylinder(0.5, 1, mode=Mode.SUBTRACT)  # Cut hole
```

## Workplanes and Planes

Workplanes define the 2D drawing surface for sketches:

```python
from build123d import *

with BuildPart() as part:
    # Create base on XY plane
    Box(5, 5, 1)
    
    # Create a workplane on the top face
    with Workplanes(part.faces().sort_by(Axis.Z)[-1]):
        with BuildSketch() as sketch:
            Circle(1)
        extrude(amount=2)
```

Common planes:
- `Plane.XY` - XY plane (Z=0)
- `Plane.YZ` - YZ plane (X=0)
- `Plane.ZX` - ZX plane (Y=0)

## Selectors and Filtering

Selectors help identify and filter topological elements:

```python
from build123d import *

box = Box(1, 2, 3)

# Select faces
box.faces()           # All faces
box.faces().sort_by(Axis.Z)[-1]  # Top face (highest Z)

# Select edges
box.edges()           # All edges
box.edges().filter_by(Axis.Z)    # Edges parallel to Z axis

# Select vertices
box.vertices()        # All vertices
```

Common selectors:
- `faces()`, `edges()`, `vertices()`, `wires()`, `solids()`
- `filter_by(axis)` - Filter by orientation
- `sort_by(axis)` - Sort by position along axis
- `group_by()` - Group by geometric property
