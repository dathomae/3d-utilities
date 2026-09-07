# build123d API Reference

## 1D Objects (Curves and Lines)

1D objects are used in `BuildLine` contexts and are not affected by `Locations` in builder mode.

### Basic Curves

| Class | Description | Key Parameters |
|-------|-------------|----------------|
| `Line` | Line defined by end points | `start`, `end` |
| `Polyline` | Connected line segments | List of points |
| `Spline` | Curve defined by points | Control points |

### Arcs

| Class | Description | Key Parameters |
|-------|-------------|----------------|
| `CenterArc` | Arc by center, radius, angles | `center`, `radius`, `start_angle`, `end_angle` |
| `RadiusArc` | Arc by two points and radius | `start`, `end`, `radius` |
| `SagittaArc` | Arc by two points and sagitta | `start`, `end`, `sagitta` |
| `ThreePointArc` | Arc by three points | Three points on arc |
| `TangentArc` | Arc tangent to a line | `start`, `tangent`, `radius` |

### Special Curves

| Class | Description | Key Parameters |
|-------|-------------|----------------|
| `Bezier` | Curve by control points | Control points and weights |
| `Helix` | Spiral curve | `pitch`, `radius`, `height` |
| `Airfoil` | NACA airfoil profile | `airfoil_code` (e.g., '2412') |
| `BlendCurve` | Blends two curves | Two curves to blend |

## 2D Objects (Sketches)

2D objects are used in `BuildSketch` contexts and can be extruded into 3D parts.

### Basic Shapes

| Class | Description | Key Parameters |
|-------|-------------|----------------|
| `Circle` | Circular shape | `radius` |
| `Rectangle` | Rectangular shape | `width`, `height` |
| `Polygon` | Regular polygon | `radius`, `side_count` |
| `Slot` | Slot shape | `width`, `height` |

### Rounded Shapes

| Class | Description | Key Parameters |
|-------|-------------|----------------|
| `RoundedRectangle` | Rectangle with rounded corners | `width`, `height`, `radius` |
| `FilletPolyline` | Polyline with filleted corners | Points and fillet radius |

### Special 2D Objects

| Class | Description | Key Parameters |
|-------|-------------|----------------|
| `Text` | 2D text outline | `text`, `font_size`, `font` |
| `SlotArc` | Arc-shaped slot | Arc parameters |

## 3D Objects (Parts)

3D objects create solid geometry directly.

### Primitives

| Class | Description | Key Parameters |
|-------|-------------|----------------|
| `Box` | Rectangular prism | `length`, `width`, `height` |
| `Cylinder` | Cylindrical shape | `radius`, `height` |
| `Sphere` | Spherical shape | `radius` |
| `Cone` | Conical shape | `bottom_radius`, `top_radius`, `height` |
| `Torus` | Toroidal shape | `major_radius`, `minor_radius` |
| `Wedge` | Wedge/prism shape | `length`, `width`, `height` |

### Constructive Objects

| Class | Description | Key Parameters |
|-------|-------------|----------------|
| `Extrude` | Extruded 2D shape | Sketch and amount |
| `Revolve` | Revolved 2D shape | Sketch and axis |
| `Loft` | Lofted between sections | List of sections |
| `Sweep` | Swept along path | Section and path |

## Operations

### Transformations

| Function | Description | Parameters |
|----------|-------------|------------|
| `extrude()` | Extrude 2D to 3D | `amount`, `direction` |
| `revolve()` | Revolve around axis | `axis`, `angle` |
| `loft()` | Loft between profiles | `sections` |
| `sweep()` | Sweep along path | `section`, `path` |
| `add()` | Add to builder | Object to add |
| `subtract()` | Subtract from builder | Object to subtract |

### Modifications

| Function | Description | Parameters |
|----------|-------------|------------|
| `fillet()` | Round edges | `radius`, `edges` |
| `chamfer()` | Bevel edges | `length`, `edges` |
| `draft()` | Add taper | `angle`, `faces` |
| `scale()` | Scale object | `factor`, `axis` |
| `split()` | Divide by plane | `plane`, `object` |
| `section()` | 2D slice | `plane` |

### Utility Operations

| Function | Description | Parameters |
|----------|-------------|------------|
| `mirror()` | Mirror geometry | `plane`, `object` |
| `project()` | Project to plane | `objects`, `plane` |
| `bounding_box()` | Get bounding box | `object` |
| `make_hull()` | Create convex hull | `edges` |
| `make_face()` | Create face from edges | `edges` |

## Geometric Classes

### Location and Positioning

#### `Location`
Represents translation and rotation.

```python
Location()                          # Identity location
Location(position=(x, y, z))        # Translation only
Location(rotation=(rx, ry, rz))     # Rotation only
Location(position, rotation)        # Both
```

Properties:
- `position: Vector` - Translation component
- `orientation: Vector` - Rotation component (degrees)
- `inverse: Location` - Inverse transformation

Methods:
- `__mul__(other: Location) -> Location` - Combine locations
- `__pow__(other: Location) -> Location` - Relative location

#### `Pos` (Position Helper)
Convenient shorthand for positioning.

```python
Pos(x, y)           # Position on XY plane
Pos(x, y, z)        # 3D position
```

### Vectors and Axes

#### `Vector`
3D vector with x, y, z components.

```python
Vector(1, 2, 3)
Vector((1, 2, 3))   # From tuple
```

Properties:
- `x`, `y`, `z` - Components
- `length` - Magnitude
- `normalized` - Unit vector

#### `Axis`
Defines an axis with origin and direction.

```python
Axis(origin=(0, 0, 0), direction=(0, 0, 1))  # Z-axis
Axis.X, Axis.Y, Axis.Z                       # Predefined axes
```

Properties:
- `position: Vector` - Origin point
- `direction: Vector` - Direction vector

Methods:
- `angle_between(other: Axis) -> float` - Angle between axes
- `is_coaxial(other) -> bool` - Check if parallel

### Planes

#### `Plane`
Defines a 2D workplane in 3D space.

```python
Plane.XY    # XY plane
Plane.YZ    # YZ plane
Plane.ZX    # ZX plane
Plane(origin, normal)  # Custom plane
```

Predefined planes:
- `Plane.XY`, `Plane.YZ`, `Plane.ZX`
- `Plane.NX`, `Plane.NY`, `Plane.NZ` (negative normals)

Methods:
- `from_face(face: Face) -> Plane` - Create from face
- `shift(distance) -> Plane` - Offset plane
- `rotated((rx, ry, rz)) -> Plane` - Rotate plane

## Builder Classes

### `BuildPart`
Context for building 3D parts.

```python
with BuildPart() as part:
    # Create 3D geometry
    Box(1, 2, 3)
    Cylinder(1, 2)
```

Properties:
- `part: Solid` - Resulting solid object
- `faces`, `edges`, `vertices` - Topological elements

### `BuildSketch`
Context for building 2D sketches.

```python
with BuildSketch() as sketch:
    # Create 2D geometry
    Circle(1)
    Rectangle(2, 3)
```

Properties:
- `sketch: Sketch` - Resulting sketch object

### `BuildLine`
Context for building 1D lines/curves.

```python
with BuildLine() as line:
    # Create 1D geometry
    Line((0, 0), (1, 1))
    Arc((1, 1), (2, 0), radius=1)
```

## Context Managers

### `Locations`
Positions objects within a builder context.

```python
with BuildPart() as part:
    with Locations((1, 0, 0), (2, 0, 0)):
        Box(1, 1, 1)  # Creates boxes at both positions
```

### `Workplanes`
Sets the active workplane for sketching.

```python
with BuildPart() as part:
    with Workplanes(Plane.XY.offset(5)):
        with BuildSketch():
            Circle(1)
```

### `PolarLocations`
Positions objects in a circular pattern.

```python
with PolarLocations(radius=5, count=6):
    Cylinder(1, 2)  # 6 cylinders in a circle
```

### `GridLocations`
Positions objects in a grid pattern.

```python
with GridLocations(x_spacing=2, y_spacing=2, x_count=3, y_count=3):
    Cylinder(0.5, 1)  # 3x3 grid of cylinders
```

## Enums

### `Mode`
Boolean operation modes.

- `Mode.ADD` - Union operation
- `Mode.SUBTRACT` - Difference operation
- `Mode.INTERSECT` - Intersection operation
- `Mode.REPLACE` - Replace operation
- `Mode.PRIVATE` - No interaction

### `Align`
Alignment options.

- `Align.MIN` - Minimum edge/corner
- `Align.CENTER` - Centered
- `Align.MAX` - Maximum edge/corner

### `FontStyle`
Text font styles.

- `FontStyle.REGULAR`
- `FontStyle.BOLD`
- `FontStyle.ITALIC`
- `FontStyle.BOLDITALIC`

## Selectors and Filters

### ShapeList Methods

Shape collections provide filtering and sorting:

```python
box = Box(1, 2, 3)

# Filtering
box.faces().filter_by(Axis.Z)      # Faces parallel to Z
box.edges().filter_by(GeomType.CIRCLE)  # Circular edges

# Sorting
box.faces().sort_by(Axis.Z)[-1]    # Top face
box.faces().sort_by(SortBy.AREA)[0]  # Smallest face

# Grouping
box.faces().group_by(Axis.Z)       # Group by Z position
```

### Common Selectors

- `faces()`, `edges()`, `vertices()`, `wires()`, `shells()`, `solids()`
- `filter_by(axis)` - By orientation
- `filter_by(geom_type)` - By geometry type
- `sort_by(criteria)` - Sort by property
- `group_by(criteria)` - Group by property
