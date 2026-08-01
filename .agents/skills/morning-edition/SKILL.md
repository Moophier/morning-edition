```markdown
# morning-edition Development Patterns

> Auto-generated skill from repository analysis

## Overview

This skill provides a comprehensive guide to the development patterns, coding conventions, and collaborative workflows used in the `morning-edition` Python codebase. It covers file organization, commit standards, code style, and repeatable processes for adding features, fixing bugs, and maintaining both backend and frontend components. Whether you're onboarding or seeking to contribute more effectively, this document will help you align with established project practices.

## Coding Conventions

**File Naming**
- Use `camelCase` for Python files and modules.
  - Example: `userProfile.py`, `dataFetcher.py`

**Import Style**
- Use aliases for imports to clarify usage and avoid conflicts.
  - Example:
    ```python
    import numpy as np
    import pandas as pd
    ```

**Export Style**
- Use default exports (typical in JavaScript/TypeScript, but in Python, this means exposing main classes/functions at the module level).
  - Example:
    ```python
    # In userProfile.py
    class UserProfile:
        ...
    ```

**Commit Messages**
- Follow [Conventional Commits](https://www.conventionalcommits.org/) with these prefixes:
  - `feat`: New feature
  - `fix`: Bug fix
  - `docs`: Documentation change
  - `chore`: Maintenance
  - `test`: Tests
- Example:  
  ```
  feat: add user authentication middleware
  ```

## Workflows

### Add Design Spec and Implementation Plan
**Trigger:** When proposing or planning a new feature or system  
**Command:** `/new-design-spec`

1. Create a design spec markdown file in `docs/superpowers/specs/`.
2. Optionally, create a corresponding implementation plan in `docs/superpowers/plans/`.

_Example:_
```bash
touch docs/superpowers/specs/myFeatureSpec.md
touch docs/superpowers/plans/myFeaturePlan.md
```

---

### Feature Implementation with Tests
**Trigger:** When adding a new backend feature or integration  
**Command:** `/add-feature-with-tests`

1. Add or update the implementation Python file (e.g., `myFeature.py`).
2. Add or update the corresponding test file in `tests/` (e.g., `tests/myFeature.test.py`).

_Example:_
```python
# myFeature.py
def new_feature():
    pass

# tests/myFeature.test.py
import myFeature

def test_new_feature():
    assert myFeature.new_feature() is None
```

---

### Scaffold Project or Module
**Trigger:** When starting a new project or major module  
**Command:** `/scaffold-project`

1. Add config and requirements files (`config.py`, `requirements.txt`).
2. Add initial code files (e.g., `models.py`, `main.py`).
3. Add initial README or documentation.

_Example:_
```bash
touch backend/config.py
touch backend/requirements.txt
touch backend/models.py
touch frontend/package.json
touch frontend/README.md
```

---

### Add Frontend Page or Component
**Trigger:** When adding new UI functionality or views  
**Command:** `/add-frontend-component`

1. Create a new page/component file under `frontend/app/` or `frontend/components/`.
2. Update `frontend/components/index.ts` if needed to export the new component.

_Example:_
```tsx
// frontend/components/MyComponent.tsx
export default function MyComponent() { ... }

// frontend/components/index.ts
export { default as MyComponent } from './MyComponent'
```

---

### Fix or Enhance Existing Feature
**Trigger:** When fixing a bug or improving an existing feature  
**Command:** `/fix-feature`

1. Update the relevant implementation file(s) (e.g., `feature.py`).
2. Update or add test file(s) as needed (e.g., `tests/feature.test.py`).

_Example:_
```python
# feature.py
def improved_feature():
    # bug fix or enhancement
    pass

# tests/feature.test.py
def test_improved_feature():
    assert improved_feature() == expected_value
```

## Testing Patterns

- **Framework:** Not explicitly detected; likely uses standard Python testing tools (e.g., `unittest`, `pytest`).
- **File Pattern:** Test files are named with `.test.ts` (for TypeScript) and `.py` (for Python), typically located in `tests/` directories.
- **Practice:** Each new feature or fix should be accompanied by corresponding test cases.

_Example:_
```python
# tests/userProfile.test.py
import userProfile

def test_user_creation():
    user = userProfile.UserProfile("Alice")
    assert user.name == "Alice"
```

## Commands

| Command                   | Purpose                                                  |
|---------------------------|----------------------------------------------------------|
| /new-design-spec          | Start a new design specification and (optionally) plan   |
| /add-feature-with-tests   | Add a backend feature/class with corresponding tests     |
| /scaffold-project         | Scaffold a new project or major module                   |
| /add-frontend-component   | Add a new frontend page or UI component                  |
| /fix-feature              | Fix or enhance an existing feature (with tests)          |
```
