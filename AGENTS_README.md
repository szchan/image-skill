# Agent Installation Guide

This document is for an AI agent (e.g. Claude Code) installing and wiring up **image-skill** into an environment — not for a human user (see [README.md](README.md) / [README_zh.md](README_zh.md) for that) and not for the agent that will *use* the skill day-to-day once installed (see [SKILL.md](SKILL.md) for that). Follow the steps below in order; each has an explicit way to confirm it succeeded before moving on.

## What this is

A `uv`-managed Python CLI (`image-gen`) that generates and edits images through Modelscope's API Inference service, packaged as a Claude Code skill (`SKILL.md` at repo root). Installing it means two independent things: (1) making the `image-gen` command runnable, and (2) making the skill discoverable so an agent auto-invokes it on trigger phrases like "generate image" / "生成图片".

## Prerequisites

- `uv` installed and on PATH (`uv --version` should succeed; if not, this is a human/environment blocker — stop and report it rather than trying to install `uv` yourself unless you have been explicitly told to).
- Python 3.13+ available for `uv` to provision (`uv python list` — `uv` will fetch it automatically if missing).
- A Modelscope account and API key (`ms-...` token) from https://modelscope.cn/. **You cannot obtain this yourself** — it requires a human to sign in, bind an Alibaba Cloud account, complete real-name verification, and copy a token from their account settings. If step 1 below has no key available, walk the user through [Getting the user a free ModelScope API key](#getting-the-user-a-free-modelscope-api-key); do not fabricate a placeholder and continue.

## Step 1 — Configure the API key

```bash
mkdir -p ~/.image-skill
cp -n scripts/config.yaml.example ~/.image-skill/config.yaml   # -n: don't clobber an existing config.yaml
```

Edit `~/.image-skill/config.yaml` and set `modelscope.api_key` to the real key. This file lives outside the repo (never committed); `scripts/config.yaml` inside the repo is gitignored too and only used as a dev fallback when running an editable install in-place.

If the user doesn't have a key yet, see the dedicated section [Getting the user a free ModelScope API key](#getting-the-user-a-free-modelscope-api-key) below before continuing.

**Done when**: `~/.image-skill/config.yaml` exists and `modelscope.api_key` is not the placeholder `Your-ModelScope-API-Key`.

## Step 2 — Install the CLI

```bash
cd scripts
uv tool install --editable .
```

`--editable` is deliberate, not incidental: it symlinks the installed command back to `scripts/src/`, so any future edit to the source takes effect immediately with no reinstall step. Don't substitute a non-editable `uv tool install .` here.

**Done when**: `image-gen current-model` runs successfully from a directory *other than* `scripts/` (this exercises the `~/.image-skill/config.yaml` fallback path, not just a lucky cwd) and prints a model id.

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

**Done when**: the output lists the models from `~/.image-skill/config.yaml` (`Tongyi-MAI/Z-Image-Turbo`, `Qwen/Qwen-Image`, `Qwen/Qwen-Image-Edit` as of this writing) with no error. This confirms the CLI is installed, the config is readable, and the API key is at least well-formed. It does not by itself confirm the API key is *valid* — that only gets exercised by an actual `generate`/`edit` call, which costs quota, so don't run one just to test installation unless the user asks for that level of verification.

## Getting the user a free ModelScope API key

If Step 1 has no key available, don't stall silently and don't invent a placeholder — actively walk the user through it. You cannot do any of this yourself (it requires the user's own login, phone/Alipay verification, and real-name check), but you can shorten the round-trip a lot by telling them exactly what to click, in order, and by verifying the result once they're done. The full human-readable version of these steps lives in [`GetFreeToken_ModelScope.md`](GetFreeToken_ModelScope.md) — point the user there directly, or relay the steps inline:

1. **Register/log in** at https://modelscope.cn (GitHub, Alipay, or phone login).
2. **Bind an Alibaba Cloud account and complete real-name verification.** This is the step people skip, and skipping it is the single most common cause of `401 please bind your alibaba cloud account before use` once the key is otherwise configured correctly. Tell the user: avatar menu (top-right) → "绑定阿里云账号" (Bind Alibaba Cloud account) → follow the linked flow to log in/register an Alibaba Cloud account → authorize ModelScope → complete real-name verification (Alipay-linked check or facial recognition) on Alibaba Cloud's side.
3. **Create the token** at https://modelscope.cn/my/myaccesstoken → "新建令牌" (Create new token) → copy the `ms-...` value.
4. **Hand the key back to you**, then you write it into `~/.image-skill/config.yaml` yourself (per Step 1 above) — don't ask the user to edit YAML by hand if you can do it for them.

The free tier is roughly 2000 API calls/day, resetting at 00:00 UTC+8 — mention this if the user asks about limits, but don't block installation on checking it.

After the user reports the key is created, resume at Step 1: write it into `~/.image-skill/config.yaml` and continue with Step 2 onward. If a `generate`/`edit` call still comes back `401 please bind your alibaba cloud account before use` after the key is in place, that means step 2 above wasn't actually completed — send the user back to it rather than treating it as a bad key.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `image-gen: command not found` | `~/.local/bin` (uv tool's bin dir) not on PATH, or Step 2 wasn't run | `uv tool install --editable .` from `scripts/`, then check `uv tool dir --bin` is on PATH |
| `Config file not found: config.yaml` | Step 1 skipped, or running from a directory with no local `config.yaml`, no `~/.image-skill/config.yaml`, and no `scripts/config.yaml` reachable relative to the installed package | Redo Step 1; confirm with `image-gen -c ~/.image-skill/config.yaml current-model` |
| `401 please bind your alibaba cloud account before use` | Key is present but the account never completed step 2 of [Getting the user a free ModelScope API key](#getting-the-user-a-free-modelscope-api-key) (Alibaba Cloud binding + real-name verification) | Send the user back to that step — this is not a bad-key problem |
| `401`/`403` with any other message | Invalid or expired API key | Ask the user for a fresh key; redo Step 1 |
| Skill doesn't auto-trigger on phrases like "generate image" | Step 3 not done, done at the wrong scope, or a stale non-symlink copy exists | Verify with the Step 3 completion check; remove a stale copy and re-symlink |
| Edits to `SKILL.md`/code don't seem to take effect | An old non-editable install, or a copied (not symlinked) skill directory | Re-run Step 2 with `--editable` and Step 3 with `ln -s` (not `cp -r`) |

## Repo map (for orientation, not required reading)

```
SKILL.md                 # the skill itself — what a triggered agent reads
GetFreeToken_ModelScope.md # human-facing walkthrough for registering + getting an API key
references/              # progressive-disclosure detail SKILL.md points into
  setup.md                 # this doc's sibling for a human running things by hand
  prompt-guide.md           # model-specific prompt-writing rules
  python-api.md              # calling ModelscopeClient directly, LoRA usage
scripts/
  pyproject.toml          # uv package definition; [project.scripts] defines `image-gen`
  config.yaml.example     # template — copy to ~/.image-skill/config.yaml
  src/image_skill/
    main.py                 # CLI entry point (argparse subcommands)
    modelscope_client.py    # HTTP client: generate/edit + async task polling + config path resolution
```

`~/.image-skill/config.yaml` — the installed config, outside the repo entirely; not shown above since it isn't part of this checkout.
