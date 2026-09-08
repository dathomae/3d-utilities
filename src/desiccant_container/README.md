# Desiccant container

The desiccant container is a two-compartment tray that holds filament desiccant at the bottom of a clear cereal storage box. It is printed in clear PLA, so the color-change indicator in the silica gel is visible through the container and the box.

## Purpose

The tray keeps desiccant at the bottom of a clear cereal storage box so the filament stored in the box stays dry. A solid internal dividing wall splits the tray into two compartments, each with its own lid:

- The **large compartment** occupies about two thirds of the length at the 75 mm end and holds **activated alumina**.
- The **small compartment** occupies about one third of the length at the 65 mm end and holds **color-changing silica gel**.

The two desiccants recharge at very different temperatures, so they must stay physically separate during filling and removal. Because each compartment has its own independent lid, either desiccant can be refilled or recharged without opening the other.

## Dimensions

Top view is an isosceles trapezoid, symmetric about its long centerline. All dimensions are in millimeters, and the geometry is parametric: every value below is a module-level constant in `container.py`.

| Parameter | Symbol | Value (mm) |
|-----------|--------|------------|
| Length between the two end walls | `LENGTH` | 185.0 |
| Short end width (silica compartment) | `SHORT_END` | 65.0 |
| Long end width (alumina compartment) | `LONG_END` | 75.0 |
| Assembled height | — | 15.0 |
| Body total height | `BODY_HEIGHT` | 13.0 |
| Bottom plate thickness | `BOTTOM_THICKNESS` | 2.0 |
| Outer wall thickness | `WALL_THICKNESS` | 4.0 |
| Internal dividing-wall thickness | `DIVIDER_THICKNESS` | 8.0 |
| Lid total height | `LID_HEIGHT` | 4.0 |
| Lid top-plate thickness | `LID_TOP_THICKNESS` | 2.0 |
| Rim height (vertical engagement) | `RIM_HEIGHT` | 2.0 |
| Rim inset from the wall's outer face | `RIM_INSET` | 2.0 |
| Lid-to-rim radial clearance (ooze allowance) | `OOZE_CLEARANCE` | 0.2 |
| Divider position, as a fraction of length from the short end | `DIVIDER_RATIO` | 1/3 |

The assembled container is 15 mm tall: a 13 mm body plus a 4 mm lid whose 2 mm skirt overlaps the body's 2 mm rim. The taper is intentional and matches the cereal container's floor; at roughly 1.5° per side it presents no meaningful overhang.

Each lid is a 2 mm top plate plus a 2 mm skirt. The skirt drops over the rim with its outer face flush with the body's outer face and a 0.2 mm radial clearance, so the lids mate without binding. The divider's 4 mm rim ridge separates the two lids along the top, keeping each compartment independently openable.

Ventilation comes from rectangular through-slots, 5 mm long by 1 mm tall, spaced with a 1 mm solid margin. They cut through both lids' top plates and the four outer side walls. The bottom plate and the internal dividing wall carry no vents.

The interior floor of each compartment is embossed with its desiccant's name, `SILICA` in the small compartment and `ALUMINA` in the large compartment, raised about 0.5 mm, so the compartments are identifiable when opened for refill.

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

- `desiccant_body.step`
- `desiccant_lid_small.step`
- `desiccant_lid_large.step`

The `-o/--outdir` option redirects the STEP files to another directory, and `--show` opens a part in the ocp_vscode viewer after export. Run the command from the repository root so the default relative path resolves to the tracked `manufacture/` directory. STEP files are generated artifacts and are gitignored.

## Print

Print the parts in clear PLA so the silica gel's color-change indicator stays visible through the container. The gentle taper of the walls presents no meaningful overhang.

## View

The `--show` option opens a part in the ocp_vscode viewer after export:

```bash
python -m desiccant_container.container --show            # the body (default)
python -m desiccant_container.container --show lid_small
python -m desiccant_container.container --show lid_large
python -m desiccant_container.container --show assembly   # all three parts
```

The viewer requires the OCP CAD Viewer VS Code extension and a running ocp_vscode server, which listens on port 3939. If the server is not already running, start it with `python -m ocp_vscode &` before showing a part.
