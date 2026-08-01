---
name: add-design-spec-and-implementation-plan
description: Workflow command scaffold for add-design-spec-and-implementation-plan in morning-edition.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /add-design-spec-and-implementation-plan

Use this workflow when working on **add-design-spec-and-implementation-plan** in `morning-edition`.

## Goal

Adds a new feature or system design specification, often followed by an implementation plan document.

## Common Files

- `docs/superpowers/specs/*.md`
- `docs/superpowers/plans/*.md`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Create a design spec markdown file in docs/superpowers/specs/
- Optionally, create a corresponding implementation plan markdown file in docs/superpowers/plans/

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.