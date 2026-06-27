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
