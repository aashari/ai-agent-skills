# Contributing

## Adding a New Skill Set

Create a new directory under `skills/<domain>/` with:
- `README.md` — setup guide (prerequisites, installation, skills reference)
- `<skill-name>/SKILL.md` for each skill
- `_<domain>-shared/` for any shared utilities (parsers, helpers)

Follow the existing `apple-mail` or `apple-calendar` structure as a reference.

## Skill Frontmatter

Every `SKILL.md` must include:

```yaml
---
name: skill-name
description: >-
  One-sentence description of what the skill does and when to invoke it.
user-invocable: true          # false for background reference skills
allowed-tools: Bash           # Claude Code field
metadata:
  openclaw:
    requires:
      bins: [tool1, tool2]    # CLI tools required at runtime
---
```

- `name` must match the directory name
- `description` should state the trigger condition clearly ("Use when user asks about...")
- Background/reference skills (auto-loaded, no slash command) use `user-invocable: false`
- Declare all CLI dependencies in `metadata.openclaw.requires.bins`

> **YAML gotcha — always use block scalar for descriptions:** OpenClaw's YAML parser rejects plain (unquoted) scalar values containing `: ` (colon-space). A description like `"Search emails. Arguments: optional filter"` will cause the skill to silently fail to load in OpenClaw. Use `>-` block scalar format for all descriptions:
>
> ```yaml
> description: >-
>   Search emails. Arguments: optional filter, date range.
> ```
>
> Block scalar is safe for all platforms — Claude Code accepts it too. Use it by default for every skill, not only when `: ` appears.

## SQL Standards (for mail-* skills)

- Always filter `deleted = 0` and exclude Spam/Trash/Junk/Draft mailboxes
- Use `automated_conversation` and `unsubscribe_type` columns for noise filtering — never address-regex patterns
- Use `datetime(date_received, 'unixepoch', 'localtime')` for date display
- See `skills/apple-mail/mail-core/SKILL.md` for the full schema reference

## SQL Standards (for calendar-* skills)

- Always query through `OccurrenceCache` for date-range lookups — `CalendarItem.start_date` misses recurring event instances
- Always exclude `Store.type = 5` ("Found in Mail" store — auto-created duplicates from email invites)
- CoreData epoch: add `978307200` to all timestamps before Unix conversion — `datetime(field + 978307200, 'unixepoch', 'localtime')`
- See `skills/apple-calendar/calendar-core/SKILL.md` for the full schema reference

## Pull Requests

- One skill set per PR
- Include a `README.md` with setup instructions for Claude Code, OpenClaw, and any other platform
- Test on at least one supported platform before submitting
