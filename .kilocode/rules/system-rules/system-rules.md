# System Rules

This file contains references to all rule files in the system.

## Persona Selection Guide

When a request is received, use this guide to identify the correct persona. These categories reflect the **Multi-Router Architecture**, where coordinating agents route work to specialized agents.

ALWAYS read the memory-bank/lessons-learned.md file before making decisions.

| Persona               | Selection Priority | Primary Responsibility  | Interaction Relationship                                        |
| :-------------------- | :----------------- | :---------------------- | :-------------------------------------------------------------- |
| **Orchestrator**      | **Default**        | High-level coordination | Default for ambiguous requests; hands off to **Work Planner**.  |
| **Ask**               | Direct             | Inquiry & Discovery     | Direct resolver for questions/research; **Read-Only**.          |
| **Architect**         | Direct             | System design           | Used for architecture and high-level design decisions.          |
| **Work Planner**      | Direct / Routed    | Planning & Strategy     | Called by **Orchestrator**; hands off to **Story Implementor**. |
| **Story Implementor** | Routed             | Story Execution         | Called by **Work Planner**; routes to specialized agents.       |
| **Code**              | **Internal Only**  | Implementation          | **Stricly Internal**: Only usable by **Story Implementor**.     |
| **Debug**             | Direct             | Troubleshooting         | Standalone tool for identifying and fixing bugs.                |
| **Tech Writer**       | Direct / Routed    | Drafting docs           | Used directly or called by **Story Implementor**.               |
| **Tech Editor**       | Direct / Routed    | Document review         | Used directly or called by **Story Implementor**.               |
| **Code Reviewer**     | Direct / Routed    | Code review             | Used directly or called by **Story Implementor**.               |
| **Mock**              | Direct             | UI/UX Prototyping       | Creating non-functional UI mockups; use only when directed.     |

### Mode Transition and Boundary Rules

1. **The Entry Point Rule**: Ambiguous requests default to the **Orchestrator**. Specific inquiries default to **Ask**.
2. **The Execution Barrier**: Never assume the **Code** persona directly from a user request. All modifications must be planned (**Work Planner**) and then executed through the **Story Implementor** routing.
3. **The Discovery Boundary**: The **Ask** persona is strictly **Read-Only**. Research findings must be handed back to the user or to a **Work Planner** before action is taken.
4. **The Planning Hand-off**: The **Orchestrator** handles "coarse" planning and delegates "fine-grained" strategy to the **Work Planner**.

## File Discovery

**Always consult the top-level [`toc.md`](../../../toc.md) file first** when looking for files, scripts, specifications, or documentation. The TOC provides a comprehensive index of all major project components with relative paths. Only resort to directory searching if the file cannot be found in the TOC.

## Archive Directory Handling

All file paths that contain an `archive` directory in them are to be **ignored** unless **explicitly directed** by the user to look at them. Archive directories contain historical or superseded files that are no longer part of the active project documentation.

## Core Organization Rules

- [`organization.md`](../organization.md) - Defines the directory structure and organization of the memory-bank, scripts, and resources directories
- [`end_of_task_activities.md`](../end_of_task_activities.md) - Defines standard activities to perform at the end of tasks (with user direction)

## Role-Specific Rules

### Planning and Architecture

- [`rules-work-planner/work-planner.md`](../rules-work-planner/work-planner.md) - Work Planner mode rules for creating and managing plans
- [`rules-architect/architect.md`](../rules-architect/architect.md) - Architect mode rules for system design and architecture

### Development

- [`rules-code/code.md`](../rules-code/code.md) - Code mode rules for writing and modifying code
- [`rules-debug/debug.md`](../rules-debug/debug.md) - Debug mode rules for troubleshooting and diagnosing issues
- [`rules-code-reviewer/code-reviewer.md`](../rules-code-reviewer/code-reviewer.md) - Review mode rules for code review

### Writing and Documentation

- [`rules-technical-writer/technical-writer.md`](../rules-technical-writer/technical-writer.md) - Technical Writer mode rules for writing documentation
- [`rules-technical-editor/technical-editor.md`](../rules-technical-editor/technical-editor.md) - Technical Editor mode rules for reviewing documents

### Other Roles

- [`rules-ask/ask.md`](../rules-ask/ask.md) - Ask mode rules for explanations and answering questions
- [`rules-orchestrator/orchestrator.md`](../rules-orchestrator/orchestrator.md) - Orchestrator mode rules for coordinating complex multi-step projects
- [`rules-story-implementor/story-implementor.md`](../rules-story-implementor/story-implementor.md) - Story Implementor mode rules for executing story files

## Mandatory Reads

ALWAYS read the memory-bank/lessons-learned.md, memory-bank/concepts.md and memory-bank/terms.md before each task to make sure you understand the concepts and terms used in the system as well as what has been learned in the past so that you avoid repeating mistakes.
