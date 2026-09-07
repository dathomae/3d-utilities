# Mounting Brackets

This document captures lessons learned and best practices for designing mounting brackets, specifically gravity-locking angled brackets (similar to a French cleat).

## Gravity-Locking Angled Brackets

A gravity-locking bracket consists of a flat plate attached to a wall and an extension that juts upwards and outwards at an angle (typically 45 degrees). The mounted object (carrier) has a matching slot. When the carrier is placed onto the bracket, gravity pulls it down, and the angled interface forces it back against the wall, creating a secure, flush mount.

### Key Design Considerations

1. **Flush Mounting**: To ensure the carrier sits flush against the wall, the carrier's back plate must have a recess that completely swallows the flat part of the mounting bracket.
2. **Slide-Down Clearance**: The slot in the carrier must be extended downwards by a "drop distance" to allow the carrier to be positioned above the bracket and slid down into place.
3. **Constant Thickness**: When the bracket bends from the flat plate to the angled extension, the perpendicular thickness of the extension should match the thickness of the flat plate for structural integrity.
4. **Interference Avoidance**: The angled extension must not be so long that it protrudes into functional areas of the carrier (e.g., internal cavities or holes).

### What Did Not Work Well

#### Incorrect Bend Geometry
Simply drawing a line from the inner corner `(0,0)` to the tip of the extension results in an extension that is thinner than the flat plate.

```python
# BAD: This creates an extension with incorrect perpendicular thickness
t = 12.7
L = 25.0
a = math.radians(45)

with BuildSketch(Plane.YZ) as bad_profile:
    Polygon([
        (-50, 0),
        (-50, t),
        (0, t),
        (L * math.cos(a), t + L * math.sin(a)), # Tip front
        (L * math.cos(a) - t * math.sin(a), t + L * math.sin(a) + t * math.cos(a)), # Tip back
        (0, 0) # BAD: Connecting directly to the origin makes the extension too thin
    ])
```

#### Unconstrained Extension Length
Allowing the extension to grow arbitrarily long based on a length parameter `L` can cause it to punch through the back plate of the carrier and interfere with internal components.

### What Worked Well

#### Exact Mathematical Profile
To maintain a constant perpendicular thickness `t` across the bend, the back face of the extension must intersect the wall at a specific point below the origin.

```python
# GOOD: Exact geometry for constant thickness
t = 12.7  # Thickness of the bracket
a = math.radians(45) # Angle of the extension
flat_height = 50.0

# The back face of the extension intersects the wall at this Y coordinate
y6 = t * (math.sqrt(2) - 1) 

# Calculate tip coordinates for a given length L
L = 25.0
y4 = L * math.cos(a)
z4 = t + L * math.sin(a)
y5 = y4 + t * math.sin(a)
z5 = z4 - t * math.cos(a)

with BuildSketch(Plane.YZ) as good_profile:
    Polygon([
        (-flat_height, 0),
        (-flat_height, t),
        (0, t),
        (y4, z4),
        (y5, z5),
        (y6, 0) # Correct inner corner intersection
    ])
```

#### Truncating to Prevent Interference
Instead of using an arbitrary length `L`, calculate the intersection of the extension faces with the maximum allowable depth (`z_max`) defined by the carrier's back plate thickness.

```python
# GOOD: Truncating the extension to fit within the carrier's back plate
t = 12.7
flat_height = 50.0
z_max = 20.0  # Maximum depth before interfering with internal components

y6 = t * (math.sqrt(2) - 1)

# Front face intersects z_max (Z = t + Y)
y4 = z_max - t
z4 = z_max

# Back face intersects z_max (Z = Y - y6)
y5 = z_max + y6
z5 = z_max

with BuildSketch(Plane.YZ) as truncated_profile:
    Polygon([
        (-flat_height, 0),
        (-flat_height, t),
        (0, t),
        (y4, z4),
        (y5, z5),
        (y6, 0)
    ])
```

#### Creating the Carrier Slot with Clearance and Tolerance
The slot in the carrier is created by taking the exact bracket profile, extending the bottom edge downwards by `drop_distance`, and applying a tolerance offset.

```python
# GOOD: Creating the slot with drop clearance and tolerance
drop_distance = 20.0

with BuildSketch(Plane.YZ) as slot_sketch:
    Polygon([
        (-flat_height - drop_distance, 0), # Extended downwards
        (-flat_height - drop_distance, t), # Extended downwards
        (0, t),
        (y4, z4),
        (y5, z5),
        (y6, 0)
    ])
    # Apply a 0.5mm tolerance offset to all faces of the slot
    offset(amount=0.5)

# Extrude the slot, adding tolerance to the width as well
slot_width = bracket_width + 1.0 
extrude(slot_sketch.sketch, amount=slot_width/2, both=True, mode=Mode.SUBTRACT)
```

#### Filleting for Strength
Sharp interior angles (like the 135-degree bend) can be points of mechanical weakness. Adding a fillet to the inner corner of the bend spreads the stress and strengthens the bracket.

```python
# GOOD: Adding a fillet to the inner corner
with BuildSketch(Plane.YZ) as profile:
    Polygon([
        (-flat_height, 0),
        (-flat_height, t),
        (0, t), # This is the inner corner of the bend
        (y4, z4),
        (y5, z5),
        (y6, 0)
    ])
    # Find the vertex at the inner corner and fillet it
    v_inner = profile.vertices().sort_by_distance((0, t))[0]
    fillet(v_inner, radius=3.0)
```
When creating the corresponding slot in the carrier, apply the same fillet to the slot sketch *before* applying the tolerance offset. This ensures the slot perfectly matches the filleted bracket.
