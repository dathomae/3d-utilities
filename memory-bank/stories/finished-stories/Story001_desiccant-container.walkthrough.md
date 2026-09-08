# Story001 Walkthrough & Post-Mortem

Execution record for `Story001_desiccant-container.md` (feature branch `story001`, checkpoint mode `none`).

## Outcome

All six tasks completed, reviewed, and merged. Final suite: **60 passed** (35 desiccant-container tests + 13 scaffold tests + 8 CLI/export tests + ... totals include the mill-bed/mounting-sheet tests). The CLI `python -m desiccant_container.container` writes `desiccant_body.step`, `desiccant_lid_small.step`, and `desiccant_lid_large.step` into `manufacture/`.

Delivered artifacts:

- `src/desiccant_container/__init__.py` — package marker re-exporting builders, dimension constants, `PARTS`, `main`, `make_assembly`, `show_part` (via a PEP 562 lazy `__getattr__` + `__dir__`).
- `src/desiccant_container/container.py` — `make_body`, `make_lid_small`, `make_lid_large`, vent slots, `SILICA`/`ALUMINA` embossing, `PARTS`, and the STEP-export CLI.
- `src/desiccant_container/README.md` — utility documentation.
- `tests/test_desiccant_container.py` — body, lid, vent, and embossing tests.
- `tests/test_desiccant_container_cli.py` — CLI/export tests.
- Updated repo-root `README.md`, `memory-bank/{brief,requirements,concepts}.md`, `memory-bank/design/design.md` for the per-utility directory convention.

## Task-by-task

| Task | Agent | Result |
|------|-------|--------|
| 1 — per-utility directory convention | technical-writer | Done (re-dispatched once after dot-path permission bug) |
| 2 — body geometry | code → big-code | Done (code hit step limit; big-code completed) |
| 3 — lid geometry | code | Done |
| 4a — vent slots | code → big-code | Done (code left broken uncommitted work; big-code fixed in place) |
| 4b — floor embossing | code | Done |
| 5 — STEP CLI + PARTS | code | Done |
| 6 — utility README | technical-writer | Done |

## Post-mortem (lessons)

1. **Coding agents repeatedly hit step limits before writing files**, especially when they began with exploratory `python -c` probing of build123d. Two effective mitigations emerged: (a) directive prompts that say "write tests and implementation directly, run pytest once, iterate only on failures"; (b) resuming the same sub-agent session via `task_id`, which grants a fresh budget while preserving its already-loaded analysis.
2. **Sub-agents repeatedly ran git/pytest from the wrong directory** (the main repo instead of the worktree), producing false "green" reports and failed commits. This recurred across code-for, big-code, and small-code agents despite explicit worktree instructions. Worth encoding as a standing instruction and re-verifying the branch before any merge.
3. **The dot-prefixed path permissions bug** aborted a technical-writer dispatch (`.kilo/worktrees/...`). Emphasizing the `worktrees/` symlink form and warning against dot-prefixed paths resolved it.
4. **A "minor" robustness fix can become a rabbit hole.** The coplanar-boolean epsilon change (Task 4b review issue 2) broke the single-closed-shell invariant and consumed multiple agent round-trips; the reviewer had already marked the original "acceptable because tests pass". Reverting and accepting that verdict was the right call. Optional "consider" recommendations should be weighed against risk before delegating.
5. **`small-code` overstepped its boundary** by editing the story file and `toc.md` (story-implementor files). The edits happened to be correct, but sub-agent prompts should explicitly forbid touching the story file / `toc.md`.
6. **Committing verified-but-uncommitted sub-agent work as a coordination checkpoint** (lessons-learned #17) was used successfully on Tasks 4a and 5 when agents hit their step limit after applying a trivial, verifiable change.
