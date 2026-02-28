# AI Agent Skills

A collection of reusable skills for AI agent platforms. Each skill set is self-contained, documented, and compatible with any agent platform that supports the `SKILL.md` convention.

## Available Skill Sets

| Skill Set | Skills | Description |
|---|---|---|
| [apple-mail](skills/apple-mail/) | 22 skills | Read and query synced Apple Mail data locally on macOS |

## What Are Skills?

Skills are markdown files (`SKILL.md`) that give an AI agent reusable instructions for a specific domain. The agent loads relevant skills automatically or on-demand, extending its capability without needing custom code.

This format is supported by:
- **Claude Code** — Anthropic's CLI (`~/.claude/skills/`)
- **OpenClaw** — Open-source local AI agent (via ClawHub or manual install)
- Any agent platform following the `SKILL.md` convention

See [docs/skill-platforms.md](docs/skill-platforms.md) for a comparison of how each platform handles skills.

## Repository Structure

```
skills/
└── apple-mail/         # Apple Mail skill set (22 skills)
    ├── README.md       # Setup guide for all platforms
    ├── _mail-shared/   # Shared utilities (parser.py)
    ├── mail-core/      # Background technical reference (auto-loaded)
    ├── mail-digest/    # Email digest for any time period
    ├── mail-triage/    # Intelligent inbox triage
    └── ...             # 19 more skills

docs/
└── skill-platforms.md  # Claude Code vs OpenClaw skill format comparison
```

## Contributing

Skills in this repo are maintained by [Ashari Tech](https://ashari.tech). Contributions welcome — open a PR with a new skill set under `skills/<domain>/`.
