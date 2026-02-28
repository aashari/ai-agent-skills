# Contributing

## Adding a New Skill Set

Create a new directory under `skills/<domain>/` with:
- `README.md` — setup guide (prerequisites, installation, skills reference)
- `<skill-name>/SKILL.md` for each skill
- `_<domain>-shared/` for any shared utilities (parsers, helpers)

Follow the existing `apple-mail` structure as a reference.

## Skill Frontmatter

Every `SKILL.md` must include:

```yaml
---
name: skill-name
description: One-sentence description of what the skill does and when to invoke it.
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

## SQL Standards (for mail-* skills)

- Always filter `deleted = 0` and exclude Spam/Trash/Junk/Draft mailboxes
- Use `automated_conversation` and `unsubscribe_type` columns for noise filtering — never address-regex patterns
- Use `datetime(date_received, 'unixepoch', 'localtime')` for date display
- See `skills/apple-mail/mail-core/SKILL.md` for the full schema reference

## Pull Requests

- One skill set per PR
- Include a `README.md` with setup instructions
- Test on at least one supported platform before submitting
