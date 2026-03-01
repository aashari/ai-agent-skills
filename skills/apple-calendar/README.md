# Apple Calendar Skills

11 skills for querying Apple Calendar data locally on macOS. Works entirely offline — queries the local SQLite database that Apple Calendar syncs to disk. Supports all account types: iCloud, Google, Exchange, and local calendars.

## Prerequisites

- macOS with Apple Calendar configured and syncing at least one account
- `sqlite3` and `python3` (both included with macOS — no install needed)
- **Full Disk Access** granted to your terminal app (required on macOS 10.14+)

### Granting Full Disk Access

System Settings → Privacy & Security → Full Disk Access → enable your terminal app (Terminal, iTerm2, or whichever you use).

Without this, SQLite queries against `~/Library/Group Containers/` will fail silently.

---

## Installation

### Claude Code

Copy or symlink the skill directories into Claude Code's personal skills folder:

```bash
for d in skills/apple-calendar/calendar-*; do
  ln -sf "$(pwd)/$d" ~/.claude/skills/$(basename $d)
done
```

Restart Claude Code. Skills are loaded automatically — no further configuration needed.

**Verify** by typing `/calendar-` in Claude Code — you should see all 11 skills in autocomplete.

### OpenClaw

Skills load from the **managed skills directory** (`~/.openclaw/skills/`), which is visible to all agents. Symlink for easy updates:

```bash
REPO="/path/to/ai-agent-skills"

mkdir -p ~/.openclaw/skills
for d in "$REPO/skills/apple-calendar"/calendar-*; do
  ln -sf "$d" ~/.openclaw/skills/$(basename $d)
done
```

Then create a real `calendar-core` directory in `~/.openclaw/skills/` (not a symlink) to provide agent-specific access configuration. If the agent runs directly on the Mac, it can query SQLite locally. If the agent runs on a remote server, wrap the queries in an SSH call. See `calendar-core/SKILL.md` for the schema reference to include in your override.

OpenClaw picks up managed skills automatically — no restart needed.

### Any Other Platform

Skills follow the standard `SKILL.md` convention: a directory named after the skill, containing a `SKILL.md` with YAML frontmatter and natural language instructions. Install by copying to your platform's skills directory.

---

## Skills Reference

| Skill | Description |
|---|---|
| `calendar-core` | Background technical reference — schema, epoch, query patterns (auto-loaded, not a slash command) |
| `calendar-today` | Today's full schedule |
| `calendar-upcoming` | Events for the next N days, grouped by day |
| `calendar-search` | Search events by title, location, or description |
| `calendar-accounts` | List all synced calendars and accounts |
| `calendar-event` | Full details for a specific event (attendees, video link, description) |
| `calendar-attendees` | Find meetings with a person, or list attendees of an event |
| `calendar-conflicts` | Detect overlapping or double-booked events |
| `calendar-recurring` | List all standing meetings and recurring series |
| `calendar-free` | Find available time slots in a day |
| `calendar-stats` | Meeting volume stats — hours in meetings, busiest days, top calendars |

---

## How It Works

Apple Calendar syncs all accounts to a local SQLite database at:

```
~/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb
```

These skills query that database directly — no API calls, no network access, no Apple Calendar API tokens needed.

The database is safe to query while Calendar.app is open.

### Key Design Decisions

**OccurrenceCache over CalendarItem.start_date:** Direct `start_date` queries miss future instances of recurring events. All date-range queries use `OccurrenceCache` as the entry point.

**Exclude `Store.type = 5`:** The "Found in Mail" store contains auto-created duplicate events sourced from email invites. Always filtered out.

**CoreData epoch:** All timestamps are offset from January 1, 2001 (not 1970). In SQLite: `datetime(field + 978307200, 'unixepoch', 'localtime')`.

**No AppleScript:** AppleScript requires a GUI session and times out over SSH. SQLite access is faster, more reliable, and works headlessly.

---

## Troubleshooting

**"no such file or directory" on Calendar.sqlitedb**
Apple Calendar hasn't synced yet. Open Calendar.app and let it sync, then try again.

**Empty results for future events**
Ensure queries go through `OccurrenceCache` — direct `CalendarItem.start_date` queries miss recurring event instances.

**Skills not appearing**
Ensure skill directories are named correctly (e.g., `calendar-today`, not `apple-calendar-today`). The directory name becomes the slash command.

**Remote agent can't access the database**
If your agent runs on a remote server, you need an SSH wrapper in `calendar-core`. See the OpenClaw installation section above.
