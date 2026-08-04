# Personal AI Memory Layer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a personal AI memory layer using Cognee to store, index, and retrieve notes from Obsidian vault and local documents.

**Architecture:** Cognee API server with NVIDIA NIM as LLM, storing memories in local SQLite (graph + vector). Obsidian vault path monitored for automatic sync.

**Tech Stack:** Python 3.10+, cognee, NVIDIA API, SQLite, Obsidian markdown

---

## File Structure

```
C:\Users\X\
├── cognee_memory.py          # Main integration script
├── .env                      # API keys and configuration
├── memory_sync.py            # Vault sync utility
└── tests/
    └── test_memory.py        # Unit tests
```

---

## Task 1: Install Cognee

**Files:**
- Create: `.env`
- Modify: `requirements.txt` (create if not exists)

- [ ] **Step 1: Create requirements.txt with dependencies**

```text
cognee>=1.0.0
python-dotenv>=1.0.0
```

- [ ] **Step 2: Install with pip**

Run: `uv pip install cognee python-dotenv`
Expected: Successfully installed cognee-X.X.X

- [ ] **Step 3: Create .env file**

```env
# NVIDIA API Configuration
NVIDIA_API_KEY="your-nvidia-api-key-here"

# Cognee Configuration
DB_PROVIDER=sqlite
VECTOR_DB_PROVIDER=sqlite
GRAPH_DATABASE_PROVIDER=sqlite
CACHE_BACKEND=sqlite

# Vault Path
OBSIDIAN_VAULT_PATH="C:\\Users\\X\\WPSDrive\\257510155\\WPS云盘\\我的文档\\moophier"
```

- [ ] **Step 4: Commit**

```bash
git add requirements.txt .env
git commit -m "chore: add cognee dependencies and env template"
```

---

## Task 2: Create Main Integration Script

**Files:**
- Create: `cognee_memory.py`
- Test: `tests/test_memory.py`

- [ ] **Step 1: Write the failing test**

```python
import pytest
from cognee_memory import CogneeMemory

@pytest.fixture
def memory():
    return CogneeMemory()

def test_initialization(memory):
    assert memory is not None
    assert memory.api_url == "http://localhost:8000"

def test_remember_single_note(memory):
    result = memory.remember("Test note content", session_id="test_session")
    assert result is True

def test_recall_notes(memory):
    memory.remember("Python is a programming language", session_id="test_session")
    results = memory.recall("Python", session_id="test_session")
    assert len(results) > 0
    assert "Python" in results[0].text

def test_forget_session(memory):
    memory.remember("Temporary note", session_id="forget_test")
    result = memory.forget(session_id="forget_test")
    assert result is True
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_memory.py -v`
Expected: FAIL - ModuleNotFoundError: No module named 'cognee_memory'

- [ ] **Step 3: Write minimal implementation**

```python
import os
import asyncio
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()


class CogneeMemory:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self._client = None

    async def _get_client(self):
        if self._client is None:
            import cognee
            self._client = cognee
        return self._client

    async def remember(self, content: str, session_id: Optional[str] = None) -> bool:
        client = await self._get_client()
        await client.remember(content, session_id=session_id)
        return True

    async def recall(self, query: str, session_id: Optional[str] = None) -> List:
        client = await self._get_client()
        results = await client.recall(query, session_id=session_id)
        return results

    async def forget(self, session_id: Optional[str] = None, dataset: Optional[str] = None) -> bool:
        client = await self._get_client()
        await client.forget(session_id=session_id, dataset=dataset)
        return True


def remember(content: str, session_id: Optional[str] = None) -> bool:
    return asyncio.run(CogneeMemory().remember(content, session_id))


def recall(query: str, session_id: Optional[str] = None) -> List:
    return asyncio.run(CogneeMemory().recall(query, session_id))


def forget(session_id: Optional[str] = None, dataset: Optional[str] = None) -> bool:
    return asyncio.run(CogneeMemory().forget(session_id, dataset))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_memory.py -v`
Expected: PASS (with cognee running)

- [ ] **Step 5: Commit**

```bash
git add cognee_memory.py tests/test_memory.py
git commit -m "feat: add CogneeMemory integration class"
```

---

## Task 3: Create Vault Sync Utility

**Files:**
- Create: `memory_sync.py`
- Test: `tests/test_sync.py`

- [ ] **Step 1: Write the failing test**

```python
import pytest
import tempfile
import os
from pathlib import Path
from memory_sync import VaultSync

@pytest.fixture
def temp_vault():
    with tempfile.TemporaryDirectory() as tmpdir:
        vault_path = Path(tmpdir) / "vault"
        vault_path.mkdir()
        (vault_path / "test_note.md").write_text("# Test\nThis is a test note.")
        yield str(vault_path)

def test_initialization(temp_vault):
    sync = VaultSync(vault_path=temp_vault)
    assert sync.vault_path == temp_vault

def test_find_markdown_files(temp_vault):
    sync = VaultSync(vault_path=temp_vault)
    files = sync.find_markdown_files()
    assert len(files) == 1
    assert files[0].name == "test_note.md"

def test_read_note_content(temp_vault):
    sync = VaultSync(vault_path=temp_vault)
    files = sync.find_markdown_files()
    content = sync.read_note_content(files[0])
    assert "test note" in content.lower()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_sync.py -v`
Expected: FAIL - ModuleNotFoundError: No module named 'memory_sync'

- [ ] **Step 3: Write minimal implementation**

```python
from pathlib import Path
from typing import List, Optional
import asyncio

from cognee_memory import remember, recall


class VaultSync:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)

    def find_markdown_files(self) -> List[Path]:
        return list(self.vault_path.rglob("*.md"))

    def read_note_content(self, file_path: Path) -> str:
        return file_path.read_text(encoding="utf-8")

    def sync_note(self, file_path: Path, session_id: Optional[str] = None) -> bool:
        content = self.read_note_content(file_path)
        return remember(content, session_id=session_id)

    def sync_all_notes(self, session_id: Optional[str] = None) -> int:
        files = self.find_markdown_files()
        count = 0
        for f in files:
            try:
                self.sync_note(f, session_id)
                count += 1
            except Exception:
                pass
        return count
```

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_sync.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add memory_sync.py tests/test_sync.py
git commit -m "feat: add VaultSync for Obsidian note synchronization"
```

---

## Task 4: Verify End-to-End

**Files:**
- Verify: Full integration

- [ ] **Step 1: Start Cognee API server**

Run: `cognee-cli -ui &` or `docker compose up` (if using docker)
Expected: API server running on localhost:8000

- [ ] **Step 2: Test manual remember**

Run: `python -c "from cognee_memory import remember; print(remember('Test memory'))"`
Expected: `True`

- [ ] **Step 3: Test manual recall**

Run: `python -c "from cognee_memory import recall; print(recall('Test'))"`
Expected: List of results containing "Test memory"

- [ ] **Step 4: Test vault sync (use small sample)**

Create 2-3 test notes in vault, then run:
```python
from memory_sync import VaultSync
sync = VaultSync("C:\\Users\\X\\WPSDrive\\257510155\\WPS云盘\\我的文档\\moophier")
count = sync.sync_all_notes()
print(f"Synced {count} notes")
```
Expected: Count of successfully synced notes

- [ ] **Step 5: Test search**

Run: `python -c "from cognee_memory import recall; results = recall('your search term'); print(results)"`
Expected: Relevant results from vault

- [ ] **Step 6: Commit**

```bash
git add -A
git commit -m "feat: complete personal AI memory layer setup"
```

---

## Configuration Reference

### Environment Variables (.env)

```env
# NVIDIA API - Get from https://ngc.nvidia.com/setup/api-key
NVIDIA_API_KEY="nvapi-..."

# Cognee LLM Configuration
LLM_PROVIDER=nvidia
LLM_MODEL=nvidia/llama-3.1-nemotron-70b-instruct
LLM_API_KEY=${NVIDIA_API_KEY}

# Cognee Database (SQLite for local)
DB_PROVIDER=sqlite
VECTOR_DB_PROVIDER=sqlite
GRAPH_DATABASE_PROVIDER=sqlite
CACHE_BACKEND=sqlite

# Vault Path
OBSIDIAN_VAULT_PATH="C:\\Users\\X\\WPSDrive\\257510155\\WPS云盘\\我的文档\\moophier"
```

### CLI Usage

```bash
# Store a memory
cognee-cli remember "User prefers detailed explanations."

# Recall memories
cognee-cli recall "What does the user prefer?"

# Open UI
cognee-cli -ui
```

### API Usage

```python
from cognee_memory import remember, recall, forget

# Store
remember("Important context", session_id="chat_1")

# Retrieve
results = recall("What context exists?", session_id="chat_1")

# Delete
forget(session_id="chat_1")
```

---

## Spec Coverage Checklist

- [x] Install cognee with dependencies
- [x] Configure NVIDIA API key
- [x] Set up vault path
- [x] Test ingestion of sample notes
- [x] Verify search functionality
- [x] CLI + API hybrid mode
- [x] Obsidian vault sync