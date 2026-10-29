# Ivy's Obsidian Life System — Merge Design

## Overview

Merge Ivy's Obsidian Life System (PARA + Periodic Notes) into the existing Obsidian Vault at `C:\Users\X\Documents\Obsidian Vault\`, preserving existing Jarvis/A股 workflows while adding the Ivy framework.

## Target Structure

```
C:\Users\X\Documents\Obsidian Vault\
├── .obsidian/                    # Plugin configs (updated with Ivy plugins)
│   ├── snippets/                 # CSS/JS snippets for dashboards
│   └── templates/                # Deprecated by Templater
├── 00PeriodicNotes/              # TIME dimension
│   ├── Daily/                    # Daily notes (migrated from 03-DAILY)
│   ├── Weekly/
│   ├── Monthly/
│   ├── Yearly/
│   ├── ImportantDates.md         # Key dates tracked on Home dashboard
│   └── 2026.md                   # Yearly schedule dashboard
├── 01Projects/                   # Active projects with deadlines
│   └── A股投资研究/              # ← existing Jarvis project
├── 02Areas/                      # Ongoing responsibilities
│   ├── 01Reading/                # Reading workflow + dashboard
│   ├── 投资研究/                 # Investment research area
│   └── 个人成长/                 # Personal growth
├── 03Resources/                  # Knowledge base
│   ├── 00Obsidian/               # Obsidian configuration docs
│   │   └── Assets/               # Screenshots for docs
│   ├── 知识库/                   # ← migrated from 01-KNOWLEDGE
│   ├── Inbox/                    # ← migrated from 00-INBOX
│   ├── 投资研究/                 # ← migrated from 05-RESOURCES
│   └── Jarvis/                   # ← migrated from 04-JARVIS-OUTPUTS
├── 04Archives/                   # Completed/abandoned projects
│   └── ← migrated from 06-ARCHIVE
├── 04-JARVIS-OUTPUTS/            # Jarvis write-only zone (preserved)
├── 🏠 Home.md                    # Dashboard homepage
└── README.md                     # System overview
```

## Plugins Required (12)

| Plugin | Purpose |
|--------|---------|
| Calendar | Calendar view + daily note navigation |
| Columns | Multi-column layout in dashboards |
| Dataview | Dynamic queries for dashboards, reading lists, stats |
| Editing Toolbar | Visual Markdown toolbar |
| Excalidraw | In-obsidian drawing/diagrams |
| Homepage | Default to Home.md on open |
| Kanban | Project management boards |
| Minimal Theme Settings | Theme customization |
| Style Settings | Per-plugin visual config |
| Tasks | Enhanced task management |
| Tasks Calendar Wrapper | Show tasks on calendar |
| Templater | Auto-template for daily/reading/monthly/yearly |

## Template Design

### TP01_Diary (maps to 00PeriodicNotes/Daily/)
- Date header
- Tasks section
- Habits tracker section
- Daily log / freeform notes

### TP02_Reading (maps to 02Areas/01Reading/)
- Book metadata (title, author, cover, status, rating)
- Progress tracking
- Notes/高光 section

### TP03_Monthly (maps to 00PeriodicNotes/Monthly/)
- Monthly goals
- Review against yearly goals
- Habit stats

### TP04_Yearly (maps to 00PeriodicNotes/Yearly/)
- Yearly theme/goals
- Mermaid timeline
- Quarterly review references

## Dashboard Design (Home)

Used by homepage plugin as vault entry point. Contains:
1. Statistics bar (Dataview: project count, reading count, knowledge count)
2. Important Dates (from ImportantDates.md, auto-hides expired)
3. Quick Navigation (links to all sections)
4. Recent Activity (Dataview query on recent modifications)
5. Tasks overview

## Schedule Dashboard (2026.md)

- Mermaid Gantt chart for yearly goals (editable inline)
- Habit Tracker (JS+CSS reading Daily Notes)
- Monthly task columns (Tasks + Columns plugins)
- Calendar heatmap for monthly todos

## Implementation Steps

1. Backup existing vault
2. Create new folder structure
3. Migrate existing content to new folders
4. Install and configure 12 community plugins
5. Create CSS/JS snippets for dashboards
6. Create Templater templates
7. Build Home.md dashboard
8. Build 2026.md schedule dashboard
9. Build Reading workflow
10. Update obsidian-vault skill path
11. Verify all dashboards render correctly