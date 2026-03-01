# Apple Calendar Skills

Reusable skills for querying Apple Calendar data via direct SQLite access on mac-mini.

## Requirements

- SSH access to `mac-mini.ashari.cloud`
- macOS with Apple Calendar syncing accounts (iCloud, Google, Exchange)
- `sqlite3` and `python3` available on mac-mini (both included with macOS)

## Database

All data lives at:
```
/Users/andi/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb
```

Direct SQLite reads work against the live database. **CoreData epoch** — all timestamps are offset from January 1, 2001, not 1970. Add `978307200` to convert to Unix epoch.

## Skills

| Skill | Description |
|-------|-------------|
| `calendar-core` | Background reference — schema, epoch, query patterns (auto-loaded, not invocable) |
| `calendar-today` | Today's full schedule |
| `calendar-upcoming` | Events for the next N days, grouped by day |
| `calendar-search` | Search events by title, location, or description |
| `calendar-accounts` | List all synced calendars and accounts |
| `calendar-event` | Full details for a specific event (attendees, video link, description) |
| `calendar-attendees` | Find meetings with a person, or list attendees of an event |
| `calendar-conflicts` | Detect overlapping/double-booked events |
| `calendar-recurring` | List all standing meetings and recurring series |
| `calendar-free` | Find available time slots in a day |
| `calendar-stats` | Meeting volume stats — hours, busiest days, top calendars |

## Key Design Decisions

**OccurrenceCache over CalendarItem.start_date:** Direct start_date queries miss future instances of recurring events. Always use `OccurrenceCache` as the entry point for date-range queries.

**Exclude `Store.type = 5`:** The "Found in Mail" store contains auto-created duplicate events sourced from email invites. Always filter it out.

**CoreData epoch:** `datetime(field + 978307200, 'unixepoch', 'localtime')` in SQLite.

**No AppleScript:** AppleScript requires a GUI session and times out over SSH. SQLite access is faster, more reliable, and supports all read operations.
