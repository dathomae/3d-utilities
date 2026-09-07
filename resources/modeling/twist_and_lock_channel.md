# Twist and Lock Channel Creation

This document details the specific steps and logic used to create a twist-and-lock channel on the surface of a cylinder using `build123d`.

## The Challenge
Creating a twist-and-lock channel on a cylinder involves a complex 3D path with sharp corners. A typical channel consists of:
1. An initial straight section (longitudinal).
2. An inclined segment (e.g., a 45-degree helix) to guide the mating nub.
3. A circumferential section (right angle to the straight section) where the nub rests.

Sweeping a rectangular profile along this entire path often results in an invalid, self-intersecting solid due to the sharp corners and the twisting of the Frenet frame. When subtracted from the main cylinder, this invalid solid fails silently, leaving only an outline instead of a cut channel.

## The Solution: Simulating a Ball-End Mill
To create a robust, valid, and smooth channel, we simulate the action of a ball-end mill cutting into the cylinder surface.

### 1. Define the Path Segments
Break the channel down into its individual geometric segments:
- **Straight Section**: A `Line` along the Z-axis on the cylinder's surface.
- **Inclined Segment**: A `Helix` with a pitch equal to the cylinder's circumference (`2 * pi * radius`) for a 45-degree angle. The height of the helix determines the longitudinal travel.
- **Circumferential Section**: A `ThreePointArc` along the cylinder's circumference at the resting Z-height.

### 2. Sweep a Circular Profile
Instead of a rectangular profile, use a `Circle` with a radius equal to half the desired channel width.
- For each segment, create a `Plane` normal to the segment's starting tangent.
- Draw the `Circle` on this plane.
- `sweep` the circle along the segment with `is_frenet=True`.

### 3. Smooth the Transitions with Spheres
To connect the swept segments and create perfectly smooth, rounded corners (just like a ball-end mill would leave):
- Place a `Sphere` with the same radius as the circular profile at every joint (vertex) where two segments meet.
- Place a `Sphere` at the start and end points of the entire channel to create rounded end caps.

### 4. Combine and Subtract
- Combine all the swept segments and spheres into a single `BuildPart` (the "tool").
- Subtract this tool from the main cylinder body using `mode=Mode.SUBTRACT`.

## Example Code Snippet
```python
# Define segments
l1 = Line((radius, 0, z_start), (radius, 0, z_mid1))
h1 = Helix(pitch=2*math.pi*radius, radius=radius, height=dz).moved(Location((0, 0, z_mid1)))
a1 = ThreePointArc(start_pt, mid_pt, end_pt)

with BuildPart() as groove_tool:
    # Sweep segment 1
    plane1 = Plane(origin=l1.start_point(), z_dir=l1.tangent_at(0))
    with BuildSketch(plane1): Circle(radius=groove_radius)
    sweep(path=l1, is_frenet=True)
    
    # Sweep segment 2
    plane2 = Plane(origin=h1.start_point(), z_dir=h1.tangent_at(0))
    with BuildSketch(plane2): Circle(radius=groove_radius)
    sweep(path=h1, is_frenet=True)
    
    # Sweep segment 3
    plane3 = Plane(origin=a1.start_point(), z_dir=a1.tangent_at(0))
    with BuildSketch(plane3): Circle(radius=groove_radius)
    sweep(path=a1, is_frenet=True)
    
    # Add spheres at joints and ends
    with Locations(l1.start_point(), h1.start_point(), a1.start_point(), a1.end_point()):
        Sphere(radius=groove_radius)

# Subtract from main body
add(groove_tool.part, mode=Mode.SUBTRACT)
```
