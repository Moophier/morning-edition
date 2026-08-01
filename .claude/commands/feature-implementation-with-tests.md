---
name: feature-implementation-with-tests
description: Workflow command scaffold for feature-implementation-with-tests in morning-edition.
allowed_tools: ["Bash", "Read", "Write", "Grep", "Glob"]
---

# /feature-implementation-with-tests

Use this workflow when working on **feature-implementation-with-tests** in `morning-edition`.

## Goal

Implements a new backend feature/class and adds corresponding tests.

## Common Files

- `*.py`
- `tests/*.py`

## Suggested Sequence

1. Understand the current state and failure mode before editing.
2. Make the smallest coherent change that satisfies the workflow goal.
3. Run the most relevant verification for touched files.
4. Summarize what changed and what still needs review.

## Typical Commit Signals

- Add or update implementation file (e.g., *.py)
- Add or update corresponding test file in tests/

## Notes

- Treat this as a scaffold, not a hard-coded script.
- Update the command if the workflow evolves materially.