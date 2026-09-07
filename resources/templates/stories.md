# Story Template

Stories break large plans into manageable chunks. Each story is a single markdown file stored in `memory-bank/stories/`.

## File Naming Convention

Story files use the format `StoryNNN_<short-purpose>.md`, where `NNN` is a unique three-digit number (e.g., `Story001_workspace-setup.md`). If a story is
part of an epic story, the file name should reference the epic story number as well, for example `StoryNNN_epicEEE_<short_purpose>.md`

## Table of Contents

Each story appears in `memory-bank/stories/toc.md` with its current status and a brief goal statement.

Valid statuses are:

- **Not Started**: Work has not begun
- **In Progress**: Work is actively being done
- **Completed**: All tasks are finished

Most stories involve writing code, though some cover documentation or planning tasks.

## Header Section

### 1. Goal

Explain the functionality being implemented in this story. Provide enough context so a reader can understand what the story accomplishes without reading the entire plan.

If the story is part of an epic, include a link to the epic story file in the goal statement.

### 2. References

List links to relevant documents. These links are relative to the `memory-bank` directory:

- [requirements](specifications/requirements/requirements.md)
- [architecture](specifications/architecture/architecture.md)
- [design](specifications/design/design.md)

### 3. Dependencies

List any stories that must complete before work on this story can begin:

- [StoryNNN\_<short-purpose>.md](memory-bank/stories/StoryNNN_<short-purpose>.md) - <status>

If this story has no dependencies, write "None" and briefly explain why (e.g., "This is the foundational story for the project").

### 4. Dependent Stories

List any stories that are blocked by this story:

- [StoryNNN\_<short-purpose>.md](memory-bank/stories/StoryNNN_<short-purpose>.md) - <status>

If no stories depend on this one, write "None".

## Body Section

### 1. Tasks

List the tasks that need to be completed to implement the story. Use simple numbering without grouping into stages or phases. Include sufficient detail so it is clear exactly what needs to be done.

Use this format:

```markdown
1. <task description> - <status>
   a. <sub-task description> - <status>
   b. <sub-task description> - <status>
```

Valid statuses: Not Started, In Progress, Completed.

### 2. Test-First Development

This project follows the Logical TDD Lifecycle. For coding tasks, write tests before implementing the code. Include the test-and-implement cycle within each task in the correct order. Do not break tests out as separate tasks. See `memory-bank/concepts.md` for more information on the Logical TDD Lifecycle.

### 3. Constraints

Explicitly call out any constraints to consider when implementing the story, such as:

- Algorithmic constraints (e.g., the solution must run in O(n) time)
- Memory constraints
- Required packages or libraries
- Standards or procedures to follow

### 4. Intent

For each task, explicitly state the overall goal. This ensures the purpose remains clear even if implementation details change.

### 5. Acceptance Criteria

Explicitly define what must be true to consider the task successfully completed. These criteria should be verifiable and specific.

### 6. Requesting Clarification

If at any point during story construction there is confusion or ambiguity about the goal or how to accomplish it, stop and ask the user for clarification.

## Footer Section (Optional)

Include any additional information relevant to the story:

1. **Open Questions**: Questions that need answers before work can begin
2. **Known Issues**: Issues identified that need addressing
3. **Additional Context**: Any other relevant information

## Example Story

Below is a minimal example showing all sections properly filled out:

```markdown
# Story001: Basic Workspace Setup

## Goal

Set up the project workspace with properly configured backend and frontend environments.

## References

- [Architecture](../architecture/v0_architecture.md)
- [Brief](../brief.md)

## Dependencies

None - This is the foundational story for the project.

## Dependent Stories

- [Story002_backend-structure.md](Story002_backend-structure.md) - Not Started

## Tasks

1. Create workspace configuration - Not Started
   a. Create workspace file defining project roots - Not Started
   b. Configure workspace-specific settings - Not Started

2. Set up backend environment - Not Started
   a. Create Python virtual environment - Not Started
   b. Create requirements.txt with dependencies - Not Started
   c. Verify environment configuration - Not Started

## Notes

- The backend uses Python 3.11+ with FastAPI
- This story focuses on basic setup; detailed structure is in Story002
```
