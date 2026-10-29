# Personal AI Memory Layer - Design

## Overview

Build a personal AI memory system using Cognee to store, index, and retrieve notes from Obsidian vault and local documents.

## Architecture

```
Obsidian Vault ─┬─→ Cognee API (localhost:8000) ──→ Knowledge Graph
Local Files ────┘              │
                              ▼
                    NVIDIA API (NVIDIA NIM)
```

## Configuration

| Component | Value |
|-----------|-------|
| LLM Provider | NVIDIA API (nvidia/nim) |
| LLM Model | nvidia/llama-3.1-nemotron-70b-instruct |
| Vault Path | `C:\Users\X\WPSDrive\257510155\WPS云盘\我的文档\moophier` |
| Vector DB | SQLite (local, embedded) |
| Graph DB | SQLite (local, embedded) |
| API Server | localhost:8000 |

## Features

### Core
1. **Note Ingestion** — Sync Obsidian markdown files to knowledge graph
2. **File Parsing** — Support md, txt, pdf, docx
3. **Search** — Semantic search via CLI and API
4. **Context Injection** — API for other tools to retrieve relevant memories

### API Endpoints
- `POST /remember` — Store new memory
- `GET /recall?q=<query>` — Search memories
- `DELETE /forget` — Remove memory

### CLI Commands
```bash
cognee-cli remember "note content"
cognee-cli recall "search query"
cognee-cli -ui  # Open local UI
```

## Implementation Steps

1. Install cognee with dependencies
2. Configure NVIDIA API key
3. Set up vault path
4. Test ingestion of sample notes
5. Verify search functionality

## Files

- `cognee_memory.py` — Main integration script
- `.env` — API keys and configuration