# Screw Dimensions and Modeling Reference

This document provides dimensional and general information on screws, specifically tailored for 3D modeling purposes (e.g., determining clearance holes, pilot holes, countersink and counterbore sizes, and head dimensions). Wood screws are covered in sections 1–7 and metric machine screws in section 8.

## 1. Screw Size Chart (Gauge to Diameter)

Wood screws are typically sized by a "Gauge" number. The gauge determines the shank diameter (the unthreaded portion under the head) and the major thread diameter.

| Gauge Size | Shank Diameter (inches) | Shank Diameter (mm) | Root Diameter (inches) | Threads Per Inch (TPI) |
|------------|-------------------------|---------------------|------------------------|------------------------|
| #2         | 0.086"                  | 2.18 mm             | 0.062"                 | 56                     |
| #3         | 0.099"                  | 2.51 mm             | 0.073"                 | 48                     |
| #4         | 0.112"                  | 2.84 mm             | 0.084"                 | 42                     |
| #5         | 0.125"                  | 3.18 mm             | 0.095"                 | 38                     |
| #6         | 0.138"                  | 3.51 mm             | 0.106"                 | 32                     |
| #7         | 0.151"                  | 3.84 mm             | 0.120"                 | 30                     |
| #8         | 0.164"                  | 4.17 mm             | 0.131"                 | 32                     |
| #9         | 0.177"                  | 4.50 mm             | 0.145"                 | 30                     |
| #10        | 0.190"                  | 4.83 mm             | 0.158"                 | 24                     |
| #12        | 0.216"                  | 5.49 mm             | 0.182"                 | 24                     |
| #14        | 0.242"                  | 6.15 mm             | 0.207"                 | 20                     |
| 1/4"       | 0.250"                  | 6.35 mm             | 0.211"                 | 20                     |
| 5/16"      | 0.3125"                 | 7.94 mm             | 0.265"                 | 18                     |

*Note: 1 inch = 25.4 mm.*

## 2. Hole Sizes for 3D Modeling

When modeling parts that will accept wood screws, you typically need to model two types of holes:
1. **Clearance Hole:** A hole in the top piece of material that allows the screw threads to pass through without biting. This should be slightly larger than the shank diameter.
2. **Pilot Hole:** A hole in the bottom piece of material that the screw threads bite into. The size depends on whether the material is soft or hard.

| Gauge Size | Clearance Hole | Clearance Hole (mm) | Pilot Hole (Softwood) | Pilot Hole (Softwood mm) | Pilot Hole (Hardwood) | Pilot Hole (Hardwood mm) |
|------------|----------------|---------------------|-----------------------|--------------------------|-----------------------|--------------------------|
| #2         | 3/32" (0.094") | 2.38 mm             | 1/16" (0.063")        | 1.59 mm                  | 5/64" (0.078")        | 1.98 mm                  |
| #3         | 7/64" (0.109") | 2.78 mm             | 1/16" (0.063")        | 1.59 mm                  | 5/64" (0.078")        | 1.98 mm                  |
| #4         | 1/8" (0.125")  | 3.18 mm             | 5/64" (0.078")        | 1.98 mm                  | 3/32" (0.094")        | 2.38 mm                  |
| #5         | 9/64" (0.141") | 3.57 mm             | 5/64" (0.078")        | 1.98 mm                  | 3/32" (0.094")        | 2.38 mm                  |
| #6         | 5/32" (0.156") | 3.97 mm             | 3/32" (0.094")        | 2.38 mm                  | 7/64" (0.109")        | 2.78 mm                  |
| #7         | 5/32" (0.156") | 3.97 mm             | 3/32" (0.094")        | 2.38 mm                  | 7/64" (0.109")        | 2.78 mm                  |
| #8         | 11/64" (0.172")| 4.37 mm             | 7/64" (0.109")        | 2.78 mm                  | 1/8" (0.125")         | 3.18 mm                  |
| #9         | 3/16" (0.188") | 4.76 mm             | 7/64" (0.109")        | 2.78 mm                  | 1/8" (0.125")         | 3.18 mm                  |
| #10        | 3/16" (0.188") | 4.76 mm             | 1/8" (0.125")         | 3.18 mm                  | 9/64" (0.141")        | 3.57 mm                  |
| #12        | 7/32" (0.219") | 5.56 mm             | 9/64" (0.141")        | 3.57 mm                  | 5/32" (0.156")        | 3.97 mm                  |
| #14        | 1/4" (0.250")  | 6.35 mm             | 5/32" (0.156")        | 3.97 mm                  | 3/16" (0.188")        | 4.76 mm                  |
| 1/4"       | 17/64" (0.266")| 6.75 mm             | 11/64" (0.172")       | 4.37 mm                  | 3/16" (0.188")        | 4.76 mm                  |
| 5/16"      | 21/64" (0.328")| 8.33 mm             | 7/32" (0.219")        | 5.56 mm                  | 15/64" (0.234")       | 5.95 mm                  |

*Note: For 3D printing (e.g., FDM), you may need to slightly oversize pilot holes (by 0.1mm - 0.2mm) depending on your printer's tolerances to prevent splitting the plastic.*

## 3. Head Dimensions (Flat Head / Countersunk)

When modeling countersinks for flat head wood screws, use the following maximum head diameters and heights. The standard countersink angle for US wood screws is **82 degrees**.

| Gauge Size | Max Head Diameter (inches) | Max Head Diameter (mm) | Max Head Height (inches) | Max Head Height (mm) |
|------------|----------------------------|------------------------|--------------------------|----------------------|
| #2         | 0.172"                     | 4.37 mm                | 0.051"                   | 1.30 mm              |
| #3         | 0.199"                     | 5.05 mm                | 0.059"                   | 1.50 mm              |
| #4         | 0.225"                     | 5.72 mm                | 0.067"                   | 1.70 mm              |
| #5         | 0.252"                     | 6.40 mm                | 0.075"                   | 1.91 mm              |
| #6         | 0.279"                     | 7.09 mm                | 0.083"                   | 2.11 mm              |
| #7         | 0.305"                     | 7.75 mm                | 0.091"                   | 2.31 mm              |
| #8         | 0.332"                     | 8.43 mm                | 0.100"                   | 2.54 mm              |
| #9         | 0.358"                     | 9.09 mm                | 0.108"                   | 2.74 mm              |
| #10        | 0.385"                     | 9.78 mm                | 0.116"                   | 2.95 mm              |
| #12        | 0.438"                     | 11.13 mm               | 0.132"                   | 3.35 mm              |
| #14        | 0.507"                     | 12.88 mm               | 0.153"                   | 3.89 mm              |

*Modeling Tip: When creating a countersink in CAD, use the Max Head Diameter as the top diameter of the chamfer, and set the angle to 82 degrees.*

## 4. Head Dimensions (Round Head)

For round head screws, the head sits flat against the surface. You may need to model a counterbore if you want the head recessed.

| Gauge Size | Max Head Diameter (inches) | Max Head Diameter (mm) | Max Head Height (inches) | Max Head Height (mm) |
|------------|----------------------------|------------------------|--------------------------|----------------------|
| #2         | 0.162"                     | 4.11 mm                | 0.069"                   | 1.75 mm              |
| #4         | 0.211"                     | 5.36 mm                | 0.086"                   | 2.18 mm              |
| #5         | 0.236"                     | 5.99 mm                | 0.095"                   | 2.41 mm              |
| #6         | 0.260"                     | 6.60 mm                | 0.103"                   | 2.62 mm              |
| #7         | 0.285"                     | 7.24 mm                | 0.111"                   | 2.82 mm              |
| #8         | 0.309"                     | 7.85 mm                | 0.120"                   | 3.05 mm              |
| #9         | 0.334"                     | 8.48 mm                | 0.128"                   | 3.25 mm              |
| #10        | 0.359"                     | 9.12 mm                | 0.137"                   | 3.48 mm              |
| #12        | 0.408"                     | 10.36 mm               | 0.153"                   | 3.89 mm              |
| #14        | 0.457"                     | 11.61 mm               | 0.170"                   | 4.32 mm              |

## 5. Common Head Styles

When designing parts, consider the head style of the screw to determine the appropriate hole feature (countersink, counterbore, or simple clearance hole):

*   **Flat Head (Countersunk):** Conical underside, flat top. Sits flush when countersunk. Standard angle is 82°.
*   **Round Head:** Dome-shaped top with a flat bearing surface underneath. Sits above the material.
*   **Oval Head:** Countersunk underside (82°) with a rounded top. Partially visible above the surface.
*   **Pan Head:** Rounded top with a flat bearing surface. Low profile design, good load distribution.
*   **Bugle Head:** Curved taper, flat top. Self-countersinking design (common on deck and drywall screws).
*   **Truss Head:** Extra-wide, low dome. Very large bearing surface, prevents pull-through in soft or thin materials.
*   **Hex Head:** Hexagonal head for wrench driving. Used on lag screws for high torque.
*   **Washer Head:** Built-in washer under the head for extra bearing surface (common on pocket hole screws).

## 6. Common Drive Types

*   **Phillips:** Most common, cross-shaped slot. Can cam-out under high torque.
*   **Square (Robertson):** Excellent torque transfer, bit stays in screw. Common on deck/construction screws.
*   **Star (Torx):** Superior torque transfer, no cam-out. Increasingly popular.
*   **Slotted:** Traditional single slot. Classic appearance but hard to drive.
*   **Hex Socket:** High torque capacity, requires hex key.

## 7. General Modeling Guidelines

1.  **Thread Modeling:** For most 3D modeling purposes (especially for 3D printing or general assembly visualization), it is unnecessary and computationally expensive to model the actual helical threads of a wood screw. Model the screw as a cylinder with the major thread diameter, or simply model the appropriate pilot/clearance holes in the mating parts.
2.  **Clearance vs. Pilot:** Always use a clearance hole in the part being attached (the top part) and a pilot hole in the part receiving the threads (the bottom part). This ensures the screw pulls the two parts tightly together.
3.  **Countersink Depth:** When modeling a countersink, ensure the depth is sufficient for the screw head to sit flush or slightly below the surface. Use the "Max Head Height" from the tables above as a minimum depth reference.
4.  **Material Considerations:** If designing for 3D printing, treat the plastic similar to a hardwood when selecting pilot hole sizes, or slightly larger, to prevent the layers from splitting when the screw is driven in.

---
*Sources:*
*   *AFT Fasteners: Wood Screws Dimensions & Mechanical Specs*
*   *Albany County Fasteners: Fasteners 101 - Wood Screws Information*
*   *Maxave Group: Wood Screw Size Chart*
*   *The Fastener Depot: Wood Screws Guide*

## 8. Metric Machine Screw Dimensions

Machine screws are specified by a metric thread size (e.g., M5). ISO metric coarse thread dimensions for M5, from the Accu metric thread chart, are:

| Property | Value |
|----------|-------|
| Major diameter | 5.0 mm |
| Minor diameter | 4.134 mm |
| Thread pitch | 0.80 mm |
| Pitch diameter | 4.480 mm |
| Tapping drill diameter | 4.20 mm |
| Clearance hole diameter | 5.8 mm |

*Note: clearance hole diameters for M5 commonly range 5.5–6.0 mm; Accu's chart lists 5.8 mm. Tapping drill and clearance values vary with material and fit — test on scrap first.*

### Standardized jig mounting screw

The jigs in this repository use a single standardized mounting screw:

| Property | Value |
|----------|-------|
| Thread | M5 (coarse, 0.80 mm pitch) |
| Length | 30 mm |
| Thread coverage | Full thread |
| Head style | Flat head (countersunk / conical), hex socket |
| Head diameter | 10 mm |
| Countersink angle | 90° (included) |
| Head height (cone depth) | ~2.5 mm |
| Minimum jig base thickness | 4 mm |

The head is a 90° conical (countersunk) flat head. With a 10 mm head diameter over a 5 mm thread, the head cone is (10 − 5) / 2 = 2.5 mm tall, so a base 4 mm thick buries the head below the working face with roughly 1.5 mm of material to spare.

Model the hole with build123d's `CounterSinkHole` (see section 9): the through-hole radius is the clearance radius (5.8 / 2 = 2.9 mm), and the countersink radius is the head radius (10 / 2 = 5 mm) at 90°:

```python
from build123d import *

# M5 flat-head (countersunk) mounting screw hole
clearance_radius = 5.8 / 2  # 2.9 mm through-hole for the M5 shank/thread
head_radius = 10 / 2        # 5.0 mm countersink for the 10 mm head

with BuildPart() as base:
    Box(50, 50, 4)  # jig base, 4 mm thick
    with Locations((0, 0, 2)):  # top face
        CounterSinkHole(
            radius=clearance_radius,
            counter_sink_radius=head_radius,
            counter_sink_angle=90,
        )
```

## 9. Modeling Screws in Build123D

When modeling screw holes in Build123D, the `CounterSinkHole` and `CounterBoreHole` part operations are highly recommended over manually combining `Cylinder` and `Cone` objects.

### What Works Well

Using `CounterSinkHole` automatically handles the through-hole and the countersink in a single operation. It cuts in the `-Z` direction of the current location context.

```python
from build123d import *

# Example: Creating a countersink hole for a #7 flathead wood screw
clearance_radius = 3.97 / 2  # 1.985 mm
head_radius = 7.75 / 2       # 3.875 mm

with BuildPart() as part:
    Box(100, 100, 12.7)
    
    # Place the hole on the top face (Z = 12.7 / 2 = 6.35)
    with Locations((0, 0, 6.35)):
        # CounterSinkHole cuts in the -Z direction by default.
        # If depth is not specified, it cuts all the way through the part.
        CounterSinkHole(
            radius=clearance_radius, 
            counter_sink_radius=head_radius, 
            counter_sink_angle=82
        )
```

### What Doesn't Work Well

Manually combining `Cylinder` and `Cone` can lead to alignment issues and requires manual calculation of the cone's height based on the countersink angle.

```python
# AVOID THIS APPROACH
with BuildPart() as part:
    Box(100, 100, 12.7)
    
    with Locations((0, 0, 6.35)):
        # Manually cutting the clearance hole
        Cylinder(radius=clearance_radius, height=15, mode=Mode.SUBTRACT)
        
    # Manually calculating and placing the cone is error-prone
    # Cone is centered at Z=0 by default, making placement tricky
    with Locations((0, 0, 6.35 - head_height / 2)):
        Cone(bottom_radius=clearance_radius, top_radius=head_radius, height=head_height, mode=Mode.SUBTRACT)
```
