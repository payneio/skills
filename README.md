# Skills

Paul's agent skills — one directory per skill, each with a `SKILL.md` (frontmatter
`name` + `description`, then the instructions) and any reference files it loads on
demand. Skills follow the open [Agent Skills](https://agentskills.io) format, so
the same directory works in Claude Code, OpenCode, Codex and the rest.

| Skill | What it's for |
|---|---|
| `pitch-deck` | Turn a product idea into a pitch document and an HTML slide deck |
| `walk-a-scenario` | Judge whether a surface actually works, by walking one scenario |
| `model-the-domain` | Decide what a concept *is* before modelling it |
| `change-the-model` | Questions to answer before changing a schema |

Skills that live in other people's repos (Anthropic's skill-creator, Microsoft's
Azure skills) are listed in [EXTERNAL-SKILLS.md](EXTERNAL-SKILLS.md) rather than
copied here.

## Installing

Use [`npx skills`](https://github.com/vercel-labs/skills). It installs from a git
repo or a local path, into each agent's skills directory.

```bash
# From GitHub (any machine)
npx skills add payneio/skills -g -s pitch-deck -s walk-a-scenario

# From this checkout (the machine where skills are written)
npx skills add /data/repos/skills -g -s pitch-deck -s walk-a-scenario

npx skills add payneio/skills --list   # what's available, without installing
npx skills list -g                      # what's installed
npx skills update -g                    # pull newer versions
npx skills remove -g -s pitch-deck
```

- **`-g` (global)** installs for your user, in every project. Without it, skills go
  into the current project (`.claude/skills`, `.agents/skills`, …) — right for
  skills that only make sense in one repo.
- **`-s`** picks skills by name. Install globally only what's useful everywhere:
  each global skill's description is in every session of every agent.
- **`-a`** picks agents (`-a claude-code -a opencode`, or `'*'`). Without it, the
  tool detects installed agents and asks. Global locations it uses include
  `~/.claude/skills` (Claude Code) and `~/.config/opencode/skills` (OpenCode).
- **Installs are copies.** The agents' directories link to the tool's own copy,
  not to this checkout, so after editing a skill here, re-run the `add` command
  (or `update`) to pick up the change.
- **Amplifier** isn't one of the tool's agents. Its skills bundle loads from the
  standard skill locations; if a skill doesn't show up there, link it into
  `~/.amplifier/skills/`.
- **Telemetry:** the tool reports each install, including its source, unless
  `DO_NOT_TRACK=1` (or `DISABLE_TELEMETRY=1`) is set. On this machine it is set
  globally, in `~/.zsh.d/telemetry.sh` (interactive shells) and
  `~/.config/environment.d/50-telemetry.conf` (the session and user services).

## Writing a skill

```bash
npx skills init my-skill        # creates my-skill/SKILL.md
```

Or use Anthropic's skill-creator (see [EXTERNAL-SKILLS.md](EXTERNAL-SKILLS.md)),
which also tests a skill's triggering and output.
