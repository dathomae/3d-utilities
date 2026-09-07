# Base Repository Setup Plan

## Objective

1. **Remove** all content specific to the eight-sided menora die project (the project this repository was copied from), including its stories, finished stories, plans, design docs, requirements, brief, context history, the candle-arrangement resource, and the leftover `alder-paradox` git worktree.
2. **Replace** the memory-bank documentation with project-agnostic skeletons that a new manufacturing repository can fill in, keeping the reusable resources and data that apply across many kinds of builds.
3. **Establish a correct Python project structure** for build123d-based modeling (`pyproject.toml` + `src/` layout + `tests/`), plus a `setup.sh` environment script and a `GETTINGSTARTED.md` explaining how to derive a new repository from this template.
4. **Generalize** the leftover tooling (PDD scripts, rule files) so it is no longer tied to the Chronocone / menora projects and will work in derived repositories.

This plan is intended to be turned into one or more stories via the `scripts/add-new-story.pdd.script.md` script; the Story-Writer Guidance section at the end supplies the parameters and task decomposition that script's executor needs.

## Background

The current working tree was copied from an eight-sided menora die project. It still contains:

- `memory-bank/` — menora-specific `brief.md`, `requirements.md`, `context.md`, `arrangement_approach.md`, `design/candle-arrangement-*.md` + `design/design.md`, `stories/Story004` + `Story005`, `finished-stories/Story001..003`, and 7 menora-specific plan files.
- `memory-bank/concepts.md` and `memory-bank/terms.md` — contain rows from two prior projects (a bee-house project and the menora project), neither of which belongs in a template.
- `memory-bank/lessons-learned.md` — mostly generic and worth keeping, but one row is menora-specific.
- `resources/chanukah-halacha/` — menora-specific (already deleted in the working tree; uncommitted).
- `memory-bank/plans/*.md` — the 7 menora plan files (already deleted in the working tree; uncommitted).
- `.kilo/worktrees/alder-paradox` — a nested git repository (a different project's worktree), tracked as a gitlink, plus a top-level `worktrees` symlink pointing at `.kilo/worktrees`.
- PDD scripts and rule files carry stale references to a third project ("Chronocone", Go/Gradle/`chronocone_planning_language`, `src/main/go/`, `chronocone/resources/...`, a mock-mode frontend path) that do not apply here.
- The local rule `organization.md` still documents the menora `design/` documents by name.

Missing from the current tree (to be created): `README.md`, `GETTINGSTARTED.md`, `setup.sh`, `.gitignore`, a `src/` package, a `tests/` directory, and a `manufacture/` output directory. There is no Python packaging manifest (`pyproject.toml`); only a 90-line fully-pinned `requirements.txt` (a `pip freeze`-style dump, with `build123d==0.10.0` buried in it).

## Proposed target structure

```
.
├── .gitignore                     (new) — ignore .venv/, __pycache__/, manufacture/*.step, .kilo/worktrees/
├── .kilocode/                     (kept) — rule files, cleaned of menora/Chronocone references
├── .kilo/agent/                   (kept) — the story-implementor sub-agent definitions
├── .kilo/setup-script.sh          (new) — worktree env bootstrap, consumed by story-implementor
├── LICENSE                        (replaced) — MIT license text (GPL-3.0 removed)
├── README.md                      (new) — minimal overview + pointer to GETTINGSTARTED
├── GETTINGSTARTED.md              (new) — how to derive a new repo and get modeling
├── setup.sh                       (new) — create .venv, install the package + deps
├── pyproject.toml                 (new) — PEP 621 project metadata + build123d/pytest deps
├── kilo.jsonc                     (kept as-is)
├── src/
│   └── scaffold/                  (new placeholder package; renamed per-project)
│       ├── __init__.py
│       └── example.py             (trivial build123d box builder + CLI → .step)
├── tests/
│   └── test_example.py            (new; trivial test, test-first)
├── manufacture/                   (new; .gitkeep — .step outputs are gitignored)
├── memory-bank/
│   ├── brief.md                   (skeleton stub)
│   ├── requirements.md            (skeleton stub)
│   ├── context.md                 (skeleton: Active Tasks / Recently Completed empty)
│   ├── concepts.md                (empty table with header only)
│   ├── terms.md                   (empty table with header only)
│   ├── lessons-learned.md         (generic lessons kept; menora-specific row generalized)
│   ├── bugs.md                    (kept, already empty)
│   ├── design/
│   │   └── design.md              (generic skeleton, menora docs removed)
│   ├── plans/
│   │   └── base-repository-setup_plan.md  (this plan)
│   └── stories/
│       ├── toc.md                 (empty skeleton, Active + Finished sections)
│       └── finished-stories/
│           └── toc.md             (empty skeleton)
├── resources/                     (kept; chanukah-halacha/ removed; toc.md updated)
│   ├── apis/build123d/            (kept — reusable API/install/concepts/examples docs)
│   ├── modeling/                  (kept — general modeling knowledge)
│   ├── code_review/               (kept)
│   ├── writing_resources/         (kept)
│   └── templates/                 (kept — stories + PDD templates)
└── scripts/                       (kept — PDD scripts, cleaned of Chronocone/Go refs)
```

## Impacted files

### Delete (project-specific)

| File/Dir | Reason |
|----------|--------|
| `memory-bank/arrangement_approach.md` | Menora candle-arrangement worked example |
| `memory-bank/design/candle-arrangement-arc.md` | Menora-specific |
| `memory-bank/design/candle-arrangement-circular.md` | Menora-specific |
| `memory-bank/design/design.md` | Menora die design (replaced by skeleton) |
| `memory-bank/stories/Story004_parabolic-arch-layout.md` | Menora-specific |
| `memory-bank/stories/Story005_stock-generation-utility.md` | Menora-specific |
| `memory-bank/stories/walkthrough/` | Menora-specific walkthrough |
| `memory-bank/finished-stories/Story001..003` | Menora-specific |
| `memory-bank/plans/*.md` (7 files) | Menora-specific (already deleted in working tree) |
| `resources/chanukah-halacha/` | Menora-specific (already deleted in working tree) |
| `.kilo/worktrees/alder-paradox` gitlink + `worktrees` symlink | A different project's worktree; not part of a template |
| `requirements.txt` | Superseded by `pyproject.toml` (per decision) |

### Replace with project-agnostic skeleton

| File | New content |
|------|-------------|
| `LICENSE` | Replace GPL-3.0 text with MIT license text |
| `memory-bank/brief.md` | Header + "fill in project overview/goals/design considerations" placeholders |
| `memory-bank/requirements.md` | Header + empty FR/NFR/Constraints sections with placeholder text |
| `memory-bank/context.md` | Standard header + empty "Active Tasks" and "Recently Completed" sections |
| `memory-bank/concepts.md` | Standard header + empty table (header row only) |
| `memory-bank/terms.md` | Standard header + empty table (header row only) |
| `memory-bank/lessons-learned.md` | Keep generic rows (venv, ocp_vscode, resources, worktree discipline); generalize the menora assembly row into a generic "verify all-pairs part intersection" lesson |
| `memory-bank/design/design.md` | Generic skeleton (project design + parts list placeholders) |
| `memory-bank/stories/toc.md` | Empty Active/Finished sections |
| `memory-bank/finished-stories/toc.md` | Empty Finished section |

### Create

`pyproject.toml`, `src/scaffold/__init__.py`, `src/scaffold/example.py`, `tests/test_example.py`, `setup.sh`, `.kilo/setup-script.sh`, `GETTINGSTARTED.md`, `README.md`, `.gitignore`, `manufacture/.gitkeep`.

### Keep and update

| File/Dir | Update |
|----------|--------|
| `resources/toc.md` | Remove the `chanukah-halacha/` row |
| `.kilocode/rules/organization.md` | Replace the menora `design/` description with a generic one |
| `.kilocode/rules/system-rules.md` | Remove "Chronocone" and non-existent `specifications/patterns/toc.md` references |
| `scripts/add-new-story.pdd.script.md` | Remove `chronocone/...` links and CPL/Go path conventions; replace Go commands with Python equivalents |
| `scripts/story-implementor.pdd.script.md` | Replace CPL/Go/Gradle defaults with Python (`source_root`=repo root, `test_command`=`python -m pytest`, `go test`/`go build` → `python -m pytest`/`python -m build`) |
| `.kilocode/rules/rules-mock/mock.md` | Remove `chronoconev0_frontend` references |
| `kilo.jsonc` | Keep as-is |

## Design decisions

- **Python packaging**: adopt a modern `src/`-layout package with a `pyproject.toml` (PEP 621) and an editable install (`pip install -e .`) via a plain `venv`+pip. `requirements.txt` is deleted; `build123d` and `pytest` are declared as dependencies in `pyproject.toml` only. This removes the `sys.path` bootstrap hacks the menora project used, and is the "correct" structure the template should model.
- **Smoke-test example**: the placeholder `src/scaffold/` package contains one trivial build123d function (`make_box`) with a small CLI that exports a `.step`, and a matching unit test. This gives `setup.sh` → `pytest` → generate an immediate end-to-end verification and demonstrates the intended workflow to anyone deriving a new repo. The package is renamed per-project (documented in `GETTINGSTARTED.md`).
- **Two setup scripts**: `setup.sh` (developer entry point, creates `.venv`, upgrades pip, installs editable package) and `.kilo/setup-script.sh` (thin wrapper the story-implementor PDD script already expects for worktree environment setup). Keeping both avoids a later surprise when story execution warns about a missing `.kilo/setup-script.sh`.
- **`.step` outputs are not committed**: `manufacture/*.step` is gitignored and `manufacture/.gitkeep` keeps the directory. `.step` files are generated artifacts; derived repos can choose to un-ignore them if they want to publish models.
- **License**: replace GPL-3.0 with **MIT** (Apache-2.0 is the acceptable alternative if preferred). The `license` field in `pyproject.toml` must match.
- **Tooling generalization is in-scope but separable**: the stale Chronocone/Go references in the PDD scripts would otherwise break story creation in derived repositories, so they are included here but marked as their own story so the core cleanup is not blocked by it. Go-specific instructions are replaced with their Python equivalents, not merely deleted.

## Constraints

- **Do not modify `.kilo/agent/*.md`** (the story-implementor sub-agent definitions) unless a path reference in them is demonstrably stale; they are reusable as-is.
- **Preserve reusable resources** under `resources/apis/build123d/`, `resources/modeling/`, `resources/code_review/`, `resources/writing_resources/`, and `resources/templates/` — only remove the menora-specific `chanukah-halacha/`.
- **Memory-bank skeletons must match the structure documented in `.kilocode/rules/organization.md`** (brief, requirements, context, concepts, terms, lessons-learned, bugs, design/, stories/ + finished-stories/, plans/).
- **Follow the Logical TDD Lifecycle** for the only coding task: write `tests/test_example.py` before `src/scaffold/example.py`.
- **No new third-party dependency** beyond `build123d` and `pytest`.
- **Story numbering resets to Story001** after the menora stories are cleared.
- **README stays minimal**: it must not contain onboarding detail that a derived repo would lose if it replaces the README; all "get back up to speed" content lives in `GETTINGSTARTED.md`.

## Steps

### Step 1: Remove project-specific content and the nested worktree

**Goal**: the repository no longer contains any menora-specific files or the `alder-paradox` worktree.

**Completion criteria**: `grep -rniE "menorah|candle|octahedron|manora|chanukah|halacha|hanukkah"` (excluding `.git`, `node_modules`, `.kilo/worktrees`) returns zero hits in tracked files; `git ls-files` shows no menora story/plan/design files and no `alder-paradox` gitlink.

- (a) Delete the menora `memory-bank/` files listed under "Delete" (stories, finished-stories, walkthrough, arrangement_approach, design docs, plans).
- (b) Delete `resources/chanukah-halacha/` (confirm the uncommitted working-tree deletions for plans and chanukah-halacha are captured).
- (c) Remove the `.kilo/worktrees/alder-paradox` gitlink and the `worktrees` symlink; record `.kilo/worktrees/` in `.gitignore`.
- (d) Update `resources/toc.md` to remove the `chanukah-halacha/` row.

### Step 2: Replace memory-bank docs with project-agnostic skeletons

**Goal**: every memory-bank doc is either a generic skeleton or contains only reusable content.

**Completion criteria**: each replaced file is a valid, self-describing skeleton (header + placeholder); `concepts.md`/`terms.md` contain only header rows; `lessons-learned.md` retains only generic lessons; no menora terms/concepts remain.

- (a) Write skeleton `brief.md`, `requirements.md`, `context.md`, `concepts.md`, `terms.md`, and `design/design.md`.
- (b) Prune `lessons-learned.md` to generic lessons; generalize the "assembled-die holder↔holder collision" lesson into a generic "verify all-pairs part intersection in assemblies" lesson.
- (c) Leave `bugs.md` as-is (already empty).

### Step 3: Reset the stories directories (terminal step)

**Goal**: `memory-bank/stories/` and `memory-bank/stories/finished-stories/` are in a clean, empty, template-ready state with no leftover menora stories or this arc's own meta-stories.

**Completion criteria**: `stories/` and `finished-stories/` contain only fresh `toc.md` skeletons; `plans/` contains only this plan; story numbering is free to restart at Story001.

**Execution order**: this step is split out as the **terminal story** of the arc and must run **last**, after every other setup story is complete and moved to `finished-stories/`. Running it earlier would delete the arc's own in-progress stories (the stories created from this plan). See the Story-Writer Guidance below for its position in the story sequence.

- (a) Rewrite `memory-bank/stories/toc.md` with empty "Active Stories" and "Finished Stories" sections.
- (b) Rewrite `memory-bank/finished-stories/toc.md` with an empty "Finished Stories" table.
- (c) Remove all remaining story files, including the menora stories and the arc's own completed meta-stories (once the reset story's work is recorded, the reset story itself is removed too).
- (d) Confirm `plans/` still contains only this plan.

### Step 4: Establish the Python project structure

**Goal**: a standard `src/`-layout package with `pyproject.toml`, a runnable example, a passing test, and a `manufacture/` output directory.

**Completion criteria**: `pip install -e .` succeeds; `python -m pytest` passes; `python -m scaffold.example` (or the documented CLI) writes a `.step` into `manufacture/`.

- (a) Write `tests/test_example.py` first (asserts `make_box()` returns a build123d `Part`/`Solid` with the expected bounding box).
- (b) Write `src/scaffold/__init__.py` and `src/scaffold/example.py` (a `make_box()` function and a minimal `argparse` CLI exporting to `manufacture/`).
- (c) Write `pyproject.toml` (`[project]` metadata, `build123d` + `pytest` dependencies, `license` field, `[tool.pytest]` config).
- (d) Create `manufacture/.gitkeep`; write `.gitignore` (`.venv/`, `__pycache__/`, `*.pyc`, `manufacture/*.step`, `.kilo/worktrees/`, `*.egg-info/`, `dist/`, `build/`).
- (e) Delete `requirements.txt`.
- (f) Replace `LICENSE` with MIT license text.

### Step 5: Write setup scripts

**Goal**: a new clone can be made runnable with a single command, and the story-implementor worktree flow has its expected bootstrap.

**Completion criteria**: running `./setup.sh` from a clean checkout creates `.venv`, installs the package, and `python -m pytest` passes; `.kilo/setup-script.sh` exists and reuses the same steps.

- (a) Write `setup.sh` (create `.venv`, upgrade pip, `pip install -e .`, print next steps and the model-viewer hint).
- (b) Write `.kilo/setup-script.sh` as a thin wrapper around the same install (per the story-implementor PDD script's expectation).

### Step 6: Write GETTINGSTARTED.md and README.md

**Goal**: a newcomer can derive a new repository from this template and start modeling.

**Completion criteria**: `GETTINGSTARTED.md` documents: (1) how to create a new repo from a GitHub template, (2) running `setup.sh`, (3) the build123d → `.step` → slicer/CAM methodology, (4) renaming the `scaffold` package, (5) the memory-bank plan/story workflow, and (6) how to view models (`ocp_vscode`). `README.md` is minimal (title, one-line description, pointer to `GETTINGSTARTED.md`) and contains no onboarding detail that would be lost if a derived repo replaces it.

- (a) Write `GETTINGSTARTED.md`.
- (b) Write `README.md` (minimal, as described).

### Step 7: Generalize the leftover tooling and rule files

**Goal**: the PDD scripts and rule files no longer reference Chronocone/Go or menora specifics and will run correctly in a derived Python repository.

**Completion criteria**: `grep -rn "chronocone\|chronocone_planning_language\|gradlew\|src/main/go\|go test\|go build\|chanukah\|candle-arrangement"` (excluding `node_modules`, `.git`, `.kilo/worktrees`) returns zero hits; `scripts/story-implementor.pdd.script.md` defaults `source_root` to the repo root and `test_command` to `python -m pytest`.

- (a) Update `.kilocode/rules/organization.md` to describe a generic `design/` directory.
- (b) Generalize `scripts/add-new-story.pdd.script.md` (drop `chronocone/...` links; replace CPL/Go path conventions and `go test`/`go build` with `python -m pytest`/`python -m build` equivalents).
- (c) Generalize `scripts/story-implementor.pdd.script.md` (drop CPL/Go/Gradle defaults; set `source_root` to the repo root, `build_command`/`test_command` to Python equivalents; update `source_root` examples from `src/chronocone_planning_language` to `.`).
- (d) Update `.kilocode/rules/system-rules.md` (drop "Chronocone" and the missing `specifications/patterns/toc.md` reference).
- (e) Clean `.kilocode/rules/rules-mock/mock.md` (remove `chronoconev0_frontend` references). Leave `kilo.jsonc` as-is.

### Step 8: End-to-end verification

**Goal**: the template works as a fresh clone would.

**Completion criteria**: from a clean state, `./setup.sh` succeeds, `python -m pytest` is green, the example CLI emits a `.step`, and `git status` shows only intended changes.

- (a) Run `./setup.sh`.
- (b) Run `python -m pytest`.
- (c) Run the example CLI and confirm a `.step` appears in `manufacture/`.
- (d) Review `git status`/`git ls-files` for any stray menora/Chronocone/Go content.

## Story-Writer Guidance

Suggested decomposition for the `add-new-story` executor (each becomes one story; all tasks `Not Started`). Stories execute in the order listed; `stories-reset` is the terminal story and must be created **last** so it does not wipe out the other stories added for this arc:

1. **Story `base-repo-cleanup`** — Steps 1–2 (remove project-specific content, replace memory-bank docs). Mostly writing/deletion tasks; route to `technical-writer-for-story-implementor`. Pure docs, no TDD.
2. **Story `python-structure-and-setup`** — Steps 4–6 (pyproject + package + test, setup scripts, GETTINGSTARTED/README, LICENSE, requirements.txt removal). The single coding task (package + test) follows test-first; docs route to `technical-writer-for-story-implementor`.
3. **Story `tooling-generalization`** — Step 7 (PDD scripts + rule files). Writing tasks; verify by grep and by a dry run of story creation.
4. **Story `template-verification`** (optional) — Step 8, or fold Step 8 into each story's completion criteria.
5. **Story `stories-reset`** (TERMINAL — last) — Step 3 only. Depends on stories 1–4 being complete and moved to `finished-stories/`. Resets `stories/` and `finished-stories/` to empty skeletons, removing the menora stories and the arc's own meta-stories. Route to `technical-writer-for-story-implementor`; pure docs/deletion, no TDD.

## Resolved Decisions

1. **Dependency manifest**: `pyproject.toml` only; delete `requirements.txt`. Installer: plain `venv` + pip.
2. **Placeholder package / smoke test**: keep `src/scaffold/` with the box example, its test, and the `.step` CLI.
3. **License**: replace GPL-3.0 with **MIT** (default; Apache-2.0 acceptable if preferred).
4. **README.md**: create a minimal one; keep all onboarding detail in `GETTINGSTARTED.md`.
5. **`.step` outputs**: gitignored by default (`manufacture/.gitkeep` keeps the directory).
6. **Tooling generalization**: in scope. Remove all Chronocone **and** Go references (replace Go with Python equivalents); clean `rules-mock/mock.md`; leave `kilo.jsonc` as-is.
7. **Lessons-learned**: keep the generic lessons; generalize the menora assembly-collision lesson.
8. **Two setup scripts**: `setup.sh` + `.kilo/setup-script.sh` (implemented).
9. **Story numbering**: resets to Story001 (implemented).
10. **Stories reset is a terminal story**: Step 3 is split out into its own story (`stories-reset`) that runs last in the arc, so it does not delete the new stories created from this plan.

## Completion criteria (overall)

- No menora/Chronocone/Go-specific content remains in tracked files (verified by grep and `git ls-files`).
- `memory-bank/` docs are project-agnostic skeletons; stories/plans/finished-stories are empty skeletons.
- A fresh `./setup.sh` succeeds and `python -m pytest` passes.
- The example generates a `.step` in `manufacture/`.
- `GETTINGSTARTED.md` accurately describes deriving a new repository from this template.
