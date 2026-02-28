# Apple Mail Skills

22 skills for reading and querying Apple Mail data locally on macOS. Works entirely offline — no mail is sent to any server. Queries the local SQLite database that Apple Mail syncs to disk.

## Prerequisites

- macOS with Apple Mail configured and synced (at least one account)
- Python 3 (included with macOS — no install needed)
- **Full Disk Access** granted to your terminal app (required on macOS 10.14+)

### Granting Full Disk Access

System Settings → Privacy & Security → Full Disk Access → enable your terminal app (Terminal, iTerm2, or whichever you use).

Without this, SQLite queries against `~/Library/Mail/` will fail silently.

---

## Installation

### Claude Code

Copy the skill directories into Claude Code's personal skills folder:

```bash
cp -r skills/apple-mail/mail-* ~/.claude/skills/
cp -r skills/apple-mail/_shared ~/.claude/skills/
```

Or symlink if you want to stay in sync with this repo:

```bash
for d in skills/apple-mail/mail-* skills/apple-mail/_shared; do
  ln -sf "$(pwd)/$d" ~/.claude/skills/$(basename $d)
done
```

Restart Claude Code. Skills are loaded automatically — no further configuration needed.

**Verify** by typing `/mail-` in Claude Code — you should see all 22 skills in autocomplete.

### OpenClaw

Drop the skill directories into OpenClaw's skills folder (check your OpenClaw config for the exact path, typically `~/.openclaw/skills/` or `~/.config/openclaw/skills/`):

```bash
cp -r skills/apple-mail/mail-* ~/.openclaw/skills/
cp -r skills/apple-mail/_shared ~/.openclaw/skills/
```

Reload OpenClaw skills. The skills use standard `SKILL.md` format — no additional frontmatter is required for basic usage. If OpenClaw requires dependency declarations, add `metadata.openclaw.requires.bins: [python3, sqlite3]` to each skill's frontmatter.

### Any Other Platform

Skills follow the standard `SKILL.md` convention: a directory named after the skill, containing a `SKILL.md` with YAML frontmatter and natural language instructions. Install by copying to your platform's skills directory.

The `_shared/parser.py` utility must be accessible from the skill execution context. Either place it in a shared location your platform recognizes, or copy `parser.py` inline into skills that use it.

---

## Skills Reference

### Core (auto-loaded)

| Skill | Description |
|---|---|
| `mail-core` | Background technical reference — auto-loaded when any mail skill executes. Not a slash command. |

### Inbox & Triage

| Skill | Description |
|---|---|
| `mail-digest` | Email digest for any time period — today, yesterday, last N hours/days, while-I-was-away |
| `mail-triage` | Intelligent inbox triage — surface most important emails by urgency |
| `mail-action-items` | Extract action items, tasks, and to-dos from recent emails |
| `mail-needs-reply` | Find emails waiting for a reply from real people |
| `mail-work` | Work emails only (Exchange/EWS accounts and corporate domains) |

### Search & Discovery

| Skill | Description |
|---|---|
| `mail-search` | Search across all accounts by keyword, subject, sender |
| `mail-from` | All emails from a specific person, address, or domain |
| `mail-read` | Read the full content of a specific email by ROWID or subject |
| `mail-thread` | Read and summarize a complete email thread |
| `mail-attachments` | Find emails with attachments by filename, extension, or sender |

### Finance & Subscriptions

| Skill | Description |
|---|---|
| `mail-expenses` | Extract financial transactions, receipts, and payments |
| `mail-banking` | Bank notifications, transaction alerts, account activity |
| `mail-subscriptions` | Active subscriptions and recurring charges |
| `mail-newsletter` | Newsletters and mailing lists — volume per sender |

### People & Accounts

| Skill | Description |
|---|---|
| `mail-accounts` | List all synced accounts with counts and folder structure |
| `mail-contacts` | Extract contacts and communication directory from email history |
| `mail-top-senders` | Who emails you most — frequency and relationship analysis |

### Domain-Specific

| Skill | Description |
|---|---|
| `mail-meetings` | Meeting invites, calendar events, agendas |
| `mail-security` | Login alerts, 2FA changes, password resets, suspicious activity |
| `mail-travel` | Flight bookings, hotel reservations, travel itineraries |
| `mail-stats` | Email volume statistics, trends, read rates |

---

## How It Works

Apple Mail syncs all accounts to a local SQLite database at `~/Library/Mail/V10/MailData/Envelope Index`. These skills query that database directly — no API calls, no network access, no credentials needed beyond Full Disk Access.

Email bodies are read from `.emlx` files in `~/Library/Mail/V10/`. The `_shared/parser.py` utility handles emlx parsing (skip the byte-count header, parse RFC 2822, strip HTML).

The database is safe to query while Mail.app is open (WAL journal mode).

### Noise Filtering

Skills use Apple Mail's built-in classification columns rather than fragile address-regex patterns:

- `automated_conversation = 2` — bulk automated (newsletters, CI/CD, monitoring)
- `unsubscribe_type > 0` — has unsubscribe headers (mailing lists, marketing)

Each skill applies the appropriate filter for its use case. See `mail-core/SKILL.md` for the full schema reference.

---

## Troubleshooting

**"no such file or directory" on the Envelope Index**
Apple Mail hasn't synced yet, or the path differs. Check `~/Library/Mail/` for the correct version directory (`V10`, `V9`, etc.).

**Empty results**
Verify Full Disk Access is granted. Test with: `sqlite3 "$HOME/Library/Mail/V10/MailData/Envelope Index" "SELECT COUNT(*) FROM messages;"` — if this returns a number, access is working.

**emlx files not found**
The `find` command in `mail-core` handles variable path depths. If messages exist in the DB but emlx files aren't found, Mail may not have downloaded the bodies yet (common with IMAP). Open Mail.app and let it sync.

**Skills not appearing**
Ensure skill directories are named correctly (e.g., `mail-digest`, not `apple-mail-digest`). The directory name becomes the slash command.
