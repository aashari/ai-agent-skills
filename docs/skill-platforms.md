# Skill Platform Comparison

How the `SKILL.md` convention is implemented across different AI agent platforms.

## Claude Code

**Platform:** Anthropic's Claude Code CLI
**Install location:** `~/.claude/skills/<skill-name>/SKILL.md` (personal) or `.claude/skills/` (project)
**Invocation:** `/skill-name` slash command, or auto-invoked when Claude judges it relevant
**Marketplace:** None — private/personal only

### Frontmatter Fields

```yaml
---
name: my-skill
description: What this skill does and when Claude should use it
user-invocable: false        # Hide from / menu (background knowledge only)
disable-model-invocation: true  # Prevent Claude from auto-invoking (manual only)
allowed-tools: Read, Grep, Bash # Tools pre-approved without permission prompt
context: fork               # Run in isolated subagent context
agent: Explore              # Subagent type when context: fork
argument-hint: [issue-number]   # Hint shown in / autocomplete
model: sonnet               # Model override
---
```

**Key capability:** `user-invocable: false` makes a skill background knowledge — Claude loads it automatically when relevant but it doesn't appear as a slash command. Useful for reference material and technical context.

---

## OpenClaw

**Platform:** Open-source local AI agent (gateway + messaging interface)
**Install location:** Via `claw install <skill>` from ClawHub, or manual directory drop
**Invocation:** Via chat message to the agent, or auto-invoked based on relevance
**Marketplace:** [ClawHub](https://github.com/openclaw/clawhub) — 3,200+ community skills

### Frontmatter Fields

```yaml
---
name: my-skill
description: What this skill does
version: 1.0.0
metadata:
  openclaw:
    requires:
      env: [API_KEY_NAME]       # Required environment variables
      bins: [curl, jq]          # Required CLI binaries (ALL must exist)
      anyBins: [python3, python] # Required CLI binaries (ANY must exist)
      config: [~/.config/tool]  # Required config file paths
    primaryEnv: API_KEY_NAME    # Main credential env var
    emoji: "📧"                 # Display icon
    homepage: https://github.com/...
---
```

**Key capability:** Dependency declarations (`requires.env`, `requires.bins`) let the registry validate skill prerequisites before install. Skills are community-published and installable with one command.

---

## Key Differences

| | Claude Code | OpenClaw |
|---|---|---|
| **Focus** | Developer workflow in terminal/IDE | Personal agent via messaging apps |
| **Invocation control** | Fine-grained (`user-invocable`, `disable-model-invocation`) | Basic (on/off relevance) |
| **Dependencies** | Not declared (assumed from environment) | Declared in frontmatter |
| **Marketplace** | None | ClawHub (2,800+ skills) |
| **Self-install** | Manual | AI can install skills autonomously |
| **Background knowledge** | `user-invocable: false` | Not directly equivalent |
| **Subagent execution** | `context: fork` | Not supported |

## Compatibility

Skills in this repo use Claude Code frontmatter format. To use with OpenClaw, add `metadata.openclaw` to the frontmatter with relevant `requires` declarations. The instruction body (everything after frontmatter) is platform-agnostic.
