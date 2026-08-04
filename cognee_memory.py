import os
import asyncio
from dotenv import load_dotenv
from typing import List, Optional

load_dotenv()

os.environ["ENABLE_BACKEND_ACCESS_CONTROL"] = "false"

import cognee


class CogneeMemory:
    def __init__(self, api_url: str = "http://localhost:8000"):
        self.api_url = api_url
        self._client = None

    def _get_client(self):
        if self._client is None:
            import cognee

            self._client = cognee
        return self._client

    def remember(self, content: str, session_id: Optional[str] = None) -> bool:
        client = self._get_client()
        asyncio.run(client.remember(content, session_id=session_id))
        return True

    def recall(self, query: str, session_id: Optional[str] = None) -> List:
        client = self._get_client()
        results = asyncio.run(client.recall(query, session_id=session_id))
        return results

    def forget(
        self, session_id: Optional[str] = None, dataset: Optional[str] = None
    ) -> bool:
        client = self._get_client()
        asyncio.run(client.forget(session_id=session_id, dataset=dataset))
        return True


def remember(content: str, session_id: Optional[str] = None) -> bool:
    return CogneeMemory().remember(content, session_id)


def recall(query: str, session_id: Optional[str] = None) -> List:
    return CogneeMemory().recall(query, session_id)


def forget(session_id: Optional[str] = None, dataset: Optional[str] = None) -> bool:
    return CogneeMemory().forget(session_id, dataset)
