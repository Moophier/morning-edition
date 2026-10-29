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
    assert sync.vault_path == Path(temp_vault)


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
