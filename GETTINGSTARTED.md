# Getting Started

This repository is a template for code-first, parametric 3D-modeling projects built on build123d, the Python CAD library. A template exists so you can derive a new repository from it (section 1) and rename the placeholder package (section 4). Sections 2 and 3 then show the workflow the template supports: describe models in Python, export them as STEP files, and manufacture them with a slicer or a CAM tool.

The template is self-verifying. It ships a `src/scaffold/` package that builds a 10 mm cube, a pytest test suite for that package, a setup script that creates the Python environment, and this guide. Section 5 describes the plan-and-story workflow used to run this repository, and section 6 covers viewing models while you design.

## What the template provides

| Path | Purpose |
|------|---------|
| `pyproject.toml` | PEP 621 packaging manifest. Declares the `scaffold` package (installed from `src/`) and its three dependencies: build123d, pytest, and ocp_vscode. |
| `src/scaffold/` | The placeholder package. `example.py` builds a 10 mm box and exports it as a STEP file through a small command-line interface. |
| `tests/test_example.py` | pytest tests for the example, written first and used to prove the install works. |
| `setup.sh` | Creates the Python environment and installs the package. |
| `manufacture/` | Output directory for generated STEP files. Tracked via `.gitkeep`; the `.step` files themselves are gitignored. |
| `GETTINGSTARTED.md`, `README.md` | This guide and a minimal repository overview. |
| `memory-bank/`, `resources/`, `scripts/`, `.kilocode/`, `.kilo/` | Planning records, reusable knowledge, agent scripts, and agent rules (sections 5 and 6 point into them). |

## 1. Create a new repository from this template

This repository is meant to be consumed as a GitHub template: you create a fresh repository whose files are copied from this one, then you make that copy your own.

1. Open this repository on GitHub.
2. Click **Use this template**, which appears near the top-right of the repository page, next to the fork button.
3. On the form, choose the owner, give the new repository a name, and pick its visibility (public or private). A template copy starts from a single initial commit with no history, so leave the branch options at their defaults.
4. Click **Create repository from template**. GitHub creates a new, independent repository. Changes you make there never flow back into this template, and later changes to this template are not applied to your copy automatically.
5. Clone the new repository and move into it:

   ```bash
   git clone git@github.com:<your-account>/<your-repo>.git
   cd <your-repo>
   ```

If the **Use this template** button is absent, the owner has not enabled template mode. A normal fork still copies the files, but a fork retains the connection to this repository and its full history, so prefer the template flow when it is available.

Once you have a derived repository, update the copyright line in `LICENSE` if the existing holder is not you, and rename the placeholder package before you write real geometry (section 4). The remaining sections apply unchanged to both the template and any repository derived from it.

## 2. Set up the environment and run the example

All Python dependencies live in `pyproject.toml`, and the list is deliberately short: build123d, pytest, and ocp_vscode. `setup.sh` does the environment bootstrap in one step. From the repository root, run:

```bash
./setup.sh
```

The script creates a virtual environment at `.venv`, upgrades pip inside it, and runs `pip install -e .`, which installs the `scaffold` package and resolves all declared dependencies from the manifest. pytest is a regular dependency rather than an optional extra, so this single editable install also provides the test runner; ocp_vscode is a regular dependency too, so the viewer (section 6) is ready to use as soon as setup finishes. The script prints the next steps when it finishes.

These instructions assume a Unix shell (the scripts are bash). On Windows, run the commands from Git Bash or WSL.

Python commands below must use the virtual environment's interpreter. Either activate the environment first,

```bash
source .venv/bin/activate
```

or call the interpreter directly, prefixing each command with `.venv/bin/`. The two forms are equivalent; the rest of this section writes the short form with the environment active.

### Run the tests

```bash
python -m pytest
```

pytest reads `[tool.pytest.ini_options]` from `pyproject.toml`, which points `testpaths` at `tests/` and adds `src/` to the import path. The three tests in `tests/test_example.py` import `make_box` from `scaffold.example`, then assert that the function returns a build123d `Part` whose bounding box is the expected 10 mm cube centered at the origin.

### Run the example

```bash
python -m scaffold.example
```

The example calls `make_box()` and exports the result to `manufacture/scaffold_box.step`, the module's default output directory and filename. An `-o/--outdir` option redirects the output elsewhere, and a `--show` option opens the exported part in the ocp_vscode viewer (section 6). Run the command from the repository root so the default relative path resolves to the tracked `manufacture/` directory. STEP files are generated artifacts and are gitignored (`manufacture/*.step` in `.gitignore`), so `scaffold_box.step` appears on disk but never in git; `manufacture/` itself stays in version control through `manufacture/.gitkeep`.

This is the smoke test for the whole template: after `./setup.sh`, a passing `python -m pytest` and a written `manufacture/scaffold_box.step` prove the environment, the package, and the export path all work.

## 3. The modeling methodology: build123d → STEP → slicer or CAM

Models in this workflow are written as Python code, exported as STEP geometry, and manufactured from that STEP file. The pipeline has three stages.

**Model in Python with build123d.** You assemble the geometry from primitives such as `Box` and `Cylinder`, from extruded or revolved sketches, and from boolean operations, all expressed in ordinary Python. Because the model is code, its dimensions are ordinary parameters: variables, function arguments, or configuration you can compute. Change a number and re-run the script to rebuild the model. This is what makes the approach parametric, and it is why the source of truth for a part is the `.py` file, not a point-and-click CAD session. Start with the build123d notes under `resources/apis/build123d/`, which cover core concepts, the API reference, and worked examples.

**Export to STEP.** STEP (ISO 10303, files ending in `.step` or `.stp`) records exact boundary-representation geometry, so a downstream tool imports the model at full precision, not as a mesh approximation. build123d writes STEP files with `export_step`:

```python
from build123d import Box, export_step

box = Box(10, 10, 10)
export_step(box, "manufacture/my_part.step")
```

The example CLI performs exactly this export for the scaffold box. Write STEP files into `manufacture/`, the repository's output directory for generated models.

**Manufacture from the STEP file.** A slicer (for 3D printing) or a CAM package (for subtractive machining) imports the STEP file and computes the tool paths or print layers from that geometry. The units in this template's models are millimeters, which matches how the example's 10 mm box is specified.

Keeping models parametric and exporting to a neutral format means you regenerate rather than redraw: when the design changes, you edit the parameters and re-run, then re-import the fresh STEP file. The template exercises this loop end to end: the tests pin down `make_box()`'s geometry, the CLI writes `manufacture/scaffold_box.step`, and a slicer or CAM tool can open that file.

## 4. Rename the scaffold package for your project

`scaffold` is a placeholder package name, and the example it contains is meant to be replaced by your real geometry. Rename the package before you build on it. Pick a valid Python package name: lowercase letters, digits, and underscores, with no hyphens.

1. Rename the package directory with `git mv`, so version control records the move:

   ```bash
   git mv src/scaffold src/<your_package>
   ```

2. Update `pyproject.toml`. In the `[project]` table, change `name = "scaffold"` to your package's distribution name and revise the `description`. The `[tool.setuptools.packages.find]` table already points at `src/` (`where = ["src"]`), so the renamed directory is picked up without further edits. If you later add more than one package under `src/` and want discovery limited to your package, add `include = ["<your_package>*"]` to that table.
3. Update the imports that reference the old path. At minimum, change the import in `tests/test_example.py`:

   ```python
   from scaffold.example import make_box
   ```

   to import from your package instead.
4. Sweep the source and tests for any remaining `scaffold` references, in docstrings, help text, and comments, and update the ones that name the package:

   ```bash
   grep -rn "scaffold" src tests
   ```

   The sweep stays out of the documentation: this guide and `README.md` mention the placeholder name on purpose, and the editable install leaves `*.egg-info` metadata (gitignored) behind that is regenerated on the next install. The example module's default output filename (`scaffold_box.step`) is independent of the package name; keep it or change it as you like.
5. Reinstall and re-test so the manifest and the layout agree:

   ```bash
   ./setup.sh
   python -m pytest
   ```

Renaming the package in step 1 changes the module path on its own: the command in section 2 becomes `python -m <your_package>.example`, and the import in section 6 becomes `from <your_package>.example import make_box`. If you also rename `example.py` itself, or replace it with your own module, update those references again to match the new module path.

## 5. The plan-and-story workflow in memory-bank

This repository plans and tracks its work in `memory-bank/`, and the layout is documented in `.kilocode/rules/organization.md`. Two kinds of artifacts describe work before anyone writes anything.

A **plan file** lives in `memory-bank/plans/` and carries a name of the form `<objective>_plan.md`. It states one objective and gives a step-by-step plan to reach it. Plans are executed across several tasks, with the result reviewed at the end of each step.

A **story** lives in `memory-bank/stories/` as one markdown file per chunk of work, named `StoryNNN_<short-purpose>.md`. Stories break a large plan into smaller, executable pieces; each story contains its own tasks, dependencies, acceptance criteria, and execution order. The table of contents in `memory-bank/stories/toc.md` lists every story with its state (Not Started, In Progress, or Done). When a story's tasks are all complete, the story file moves to `memory-bank/finished-stories/` and its `toc.md` entry moves to the finished list. The story file format is defined in `resources/templates/stories.md`.

Execution follows the repository's prompt-driven-development scripts in `scripts/`. The story-implementor runs a story by following `scripts/story-implementor.pdd.script.md`, delegating each task to a specialized agent (a code agent, a technical writer, and so on) and routing results back to the story's branch. New stories are generated with `scripts/add-new-story.pdd.script.md`. The other `memory-bank/` documents hold the project's living state: `brief.md`, `requirements.md`, `context.md`, `concepts.md`, `terms.md`, `lessons-learned.md`, and `bugs.md`, plus design notes under `memory-bank/design/`.

The template itself, including this guide, was produced through that workflow. You may keep using it in a derived repository, or ignore it and model directly. The workflow documents and scripts remain useful either way.

## 6. View models with ocp_vscode

build123d does not include a windowed viewer. The viewing convention for this repository is ocp_vscode, a viewer that pairs a VS Code extension with a small Python server that serves the parts you show from code. ocp_vscode is a declared dependency, so `setup.sh` installs it alongside build123d and pytest.

To view a part:

1. Install the **OCP CAD Viewer** extension in VS Code and follow its setup instructions for this project.
2. Start the viewer's server in the background. It listens on port 3939, so if that port is already in use, a server is already running and you can skip this step:

   ```bash
   python -m ocp_vscode &
   ```

3. Show a part from your modeling code with a `show` call:

   ```python
   from ocp_vscode import show
   from scaffold.example import make_box

   show(make_box())
   ```

The scaffold example shows its part through a `--show` option on the command line, so you can view the box without editing code:

```bash
python -m scaffold.example --show          # show the box
python -m scaffold.example --show box      # show the box by name
python -m scaffold.example --show assembly # show the whole assembly
```

The `--show` option takes a part name, or `assembly` to show the entire assembly of parts. The part appears in the viewer in VS Code. Consult the build123d materials under `resources/apis/build123d/` for modeling specifics, and `resources/modeling/` for general modeling knowledge and debugging techniques.
