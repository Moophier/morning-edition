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
