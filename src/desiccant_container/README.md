# Desiccant container

The desiccant container is a two-compartment tray that holds filament desiccant at the bottom of a clear cereal storage box. It is printed in clear PLA, so the color-change indicator in the silica gel is visible through the container and the box.

## Purpose

The tray keeps desiccant at the bottom of a clear cereal storage box so the filament stored in the box stays dry. Two independent trapezoidal containers rise from a monolithic base plate, separated by a 5 mm gap, each with its own lid:

- The **large compartment** occupies about two thirds of the length at the 75 mm end and holds **activated alumina**.
- The **small compartment** occupies about one third of the length at the 65 mm end and holds **color-changing silica gel**.

The two desiccants recharge at very different temperatures, so they must stay physically separate during filling and removal. Because each compartment has its own independent lid, either desiccant can be refilled or recharged without opening the other.

## Dimensions

Top view is an isosceles trapezoid, symmetric about its long centerline. All dimensions are in millimeters, and the geometry is parametric: every named value below is a module-level constant in `container.py` (assembled height is derived).

| Parameter | Symbol | Value (mm) |
|-----------|--------|------------|
| Length between the two end walls | `LENGTH` | 185.0 |
| Short end width (silica compartment) | `SHORT_END` | 65.0 |
| Long end width (alumina compartment) | `LONG_END` | 75.0 |
| Assembled height | — | 25.0 |
| Body total height | `BODY_HEIGHT` | 23.0 |
| Bottom plate thickness | `BOTTOM_THICKNESS` | 2.0 |
| Outer wall thickness | `WALL_THICKNESS` | 4.0 |
| Gap between the two containers | `GAP` | 5.0 |
| Lid total height | `LID_HEIGHT` | 14.0 |
| Lid top-plate thickness | `LID_TOP_THICKNESS` | 2.0 |
| Rim height (vertical engagement) | `RIM_HEIGHT` | 12.0 |
| Rim inset from the wall's outer face | `RIM_INSET` | 2.0 |
| Lid-to-rim radial clearance (ooze allowance) | `OOZE_CLEARANCE` | 0.2 |
| Gap centre position, as a fraction of length from the short end | `DIVIDER_RATIO` | 1/3 |

The assembled container is 25 mm tall: a 23 mm body plus a 14 mm lid whose 12 mm skirt overlaps the body's 12 mm rim. The taper is intentional and matches the cereal container's floor; at roughly 1.5° per side it presents no meaningful overhang.

The body consists of a monolithic 2 mm thick base plate spanning the full 185 × (65/75) mm footprint, with two independent trapezoidal containers rising from it. Each container has 4 mm walls on all four sides and a full-perimeter 12 mm tall rim stepped 2 mm inward from the outer face of every wall. The containers are separated by a 5 mm air gap centred at `DIVIDER_RATIO` (1/3) of the length from the short end.

Each lid is a 2 mm top plate plus a 12 mm skirt. The skirt drops over its container's rim with its outer face flush with the container's outer face and a 0.2 mm radial clearance, so the lids mate without binding. The tall rim gives the skirt a long gripping surface so the lids stay in place. The two lids sit adjacent with a 5 mm gap between them, keeping each compartment independently openable.

Ventilation comes from rectangular through-slots, 5 mm long by 1 mm tall, spaced with a 1 mm solid margin. They cut through both lids' top plates (as a grid covering each lid top) and all four side walls of each container below the rim. The bottom plate and the rim carry no vents.

The interior floor of each compartment carries its desiccant's name — `SILICA` in the small compartment and `ALUMINA` in the large compartment — as a flush, 0.8 mm-deep inlay. The lettering is a separate part, printed in a contrasting filament and pressed into matching recesses cut into the floor, so the compartments are identifiable when opened for refill.

## Desiccant fill

- Activated alumina goes in the **large** compartment, at the 75 mm end.
- Color-changing silica gel goes in the **small** compartment, at the 65 mm end.

The two compartments stay physically separate during filling and removal, and each has its own lid, so one desiccant can be refilled or recharged without disturbing the other.

## Recharge temperatures

The two desiccants recharge at very different temperatures, which is why they are kept in separate compartments:

- Activated alumina: roughly 200 to 250 °C.
- Color-changing silica gel: roughly 120 °C.

Always remove the desiccant from the container and dry it separately. The PLA container is never oven-dried; it must not be heated.

## Build and export

From the repository root, run:

```bash
python -m desiccant_container.container
```

The command builds the three parts and writes a STEP file for each into `manufacture/` by default:

- `desiccant_body.step` (the body plus its `SILICA`/`ALUMINA` label inlays as separate solids, for multi-material printing)
- `desiccant_lid_small.step`
- `desiccant_lid_large.step`

The `-o/--outdir` option redirects the STEP files to another directory, and `--show` opens a part in the ocp_vscode viewer after export. Run it from the repository root so the default relative path resolves to the tracked `manufacture/` directory. STEP files are generated artifacts and are gitignored.

## Print

Print the parts in clear PLA so the silica gel's color-change indicator stays visible through the container. The gentle taper of the walls presents no meaningful overhang.

## View

The `--show` option opens a part in the ocp_vscode viewer after export:

```bash
python -m desiccant_container.container --show            # the body (default)
python -m desiccant_container.container --show lid_small
python -m desiccant_container.container --show lid_large
python -m desiccant_container.container --show assembly   # all parts
```

The viewer requires the OCP CAD Viewer VS Code extension and a running ocp_vscode server, which listens on port 3939. If the server is not already running, start it with `python -m ocp_vscode &` before showing a part.