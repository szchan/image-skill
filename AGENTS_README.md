# Agent Installation Guide

This document is for an AI agent (e.g. Claude Code) installing and wiring up **image-skill** into an environment — not for a human user (see [README.md](README.md) / [README_zh.md](README_zh.md) for that) and not for the agent that will *use* the skill day-to-day once installed (see [SKILL.md](SKILL.md) for that). Follow the steps below in order; each has an explicit way to confirm it succeeded before moving on.

## What this is

A `uv`-managed Python CLI (`image-gen`) that generates and edits images through Modelscope's API Inference service, packaged as a Claude Code skill (`SKILL.md` at repo root). Installing it means two independent things: (1) making the `image-gen` command runnable, and (2) making the skill discoverable so an agent auto-invokes it on trigger phrases like "generate image" / "生成图片".

## Prerequisites

- `uv` installed and on PATH (`uv --version` should succeed; if not, this is a human/environment blocker — stop and report it rather than trying to install `uv` yourself unless you have been explicitly told to).
- Python 3.13+ available for `uv` to provision (`uv python list` — `uv` will fetch it automatically if missing).
- A Modelscope account and API key (`ms-...` token) from https://modelscope.cn/. **You cannot obtain this yourself** — it requires a human to sign in and copy a token from their account settings. If step 1 below has no key available, stop and ask the user for one; do not fabricate a placeholder and continue.

## Step 1 — Configure the API key

```bash
cd scripts
cp -n config.yaml.example config.yaml   # -n: don't clobber an existing config.yaml
```

Edit `scripts/config.yaml` and set `modelscope.api_key` to the real key. `config.yaml` is gitignored — never commit it.

**Done when**: `scripts/config.yaml` exists and `modelscope.api_key` is not the placeholder `Your-ModelScope-API-Key`.

## Step 2 — Install the CLI

```bash
cd scripts
uv tool install --editable .
```

`--editable` is deliberate, not incidental: it symlinks the installed command back to `scripts/src/`, so any future edit to the source takes effect immediately with no reinstall step. Don't substitute a non-editable `uv tool install .` here.

**Done when**: `image-gen current-model` runs successfully from a directory *other than* `scripts/` (this exercises the config fallback path, not just a lucky cwd) and prints a model id.

## Step 3 — Register the skill for auto-invocation

The skill's identity is the `SKILL.md` at this repo's root — nothing needs building or copying for the skill content itself, only a discovery path needs to exist. Pick one, matching the scope you were asked for:

**User scope** (available in every project for this user):
```bash
ln -s "$(pwd)" ~/.claude/skills/image-skill
```
Run this from the repo root. Use a symlink, not a copy — a copy silently drifts out of date the next time this repo's `SKILL.md` or `references/` change.

**Project scope** (available only inside one specific project):
```bash
ln -s /absolute/path/to/image-skill /path/to/that-project/.claude/skills/image-skill
```

If a skill already exists at the target path, check whether it's a symlink to this same repo (`readlink`) before overwriting — don't clobber an unrelated skill someone else installed under the same name.

**Done when**: `readlink -f ~/.claude/skills/image-skill` (or the project-scope path) prints this repo's absolute path.

## Step 4 — Verify end-to-end

```bash
image-gen list-models
```

**Done when**: the output lists the models from `scripts/config.yaml` (`Tongyi-MAI/Z-Image-Turbo`, `Qwen/Qwen-Image`, `Qwen/Qwen-Image-Edit` as of this writing) with no error. This confirms the CLI is installed, the config is readable, and the API key is at least well-formed. It does not by itself confirm the API key is *valid* — that only gets exercised by an actual `generate`/`edit` call, which costs quota, so don't run one just to test installation unless the user asks for that level of verification.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `image-gen: command not found` | `~/.local/bin` (uv tool's bin dir) not on PATH, or Step 2 wasn't run | `uv tool install --editable .` from `scripts/`, then check `uv tool dir --bin` is on PATH |
| `Config file not found: config.yaml` | Step 1 skipped, or running from a directory with neither a local `config.yaml` nor a `scripts/config.yaml` reachable relative to the installed package | Redo Step 1; confirm with `image-gen -c /full/path/to/scripts/config.yaml current-model` |
| `401`/`403` from the API | Invalid or expired API key | Ask the user for a fresh key; redo Step 1 |
| Skill doesn't auto-trigger on phrases like "generate image" | Step 3 not done, done at the wrong scope, or a stale non-symlink copy exists | Verify with the Step 3 completion check; remove a stale copy and re-symlink |
| Edits to `SKILL.md`/code don't seem to take effect | An old non-editable install, or a copied (not symlinked) skill directory | Re-run Step 2 with `--editable` and Step 3 with `ln -s` (not `cp -r`) |

## Repo map (for orientation, not required reading)

```
SKILL.md                 # the skill itself — what a triggered agent reads
references/              # progressive-disclosure detail SKILL.md points into
  setup.md                 # this doc's sibling for a human running things by hand
  prompt-guide.md           # model-specific prompt-writing rules
  python-api.md              # calling ModelscopeClient directly, LoRA usage
scripts/
  pyproject.toml          # uv package definition; [project.scripts] defines `image-gen`
  config.yaml.example     # template — copy to config.yaml, gitignored
  src/image_skill/
    main.py                 # CLI entry point (argparse subcommands)
    modelscope_client.py    # HTTP client: generate/edit + async task polling
```
