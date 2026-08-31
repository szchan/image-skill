# Setup & Configuration

Reference for installing and configuring the `image-gen` CLI. Not needed for a routine generate/edit call — only when `image-gen` isn't on PATH yet, when `config.yaml` is missing, or when adding/changing models.

## Installing as a local tool (recommended for Agent use)

```bash
cd scripts
uv tool install --editable .
```

This installs `image-gen` as a globally available command (`~/.local/bin/image-gen`), backed by an editable install — source edits under `scripts/src/` take effect immediately without reinstalling. Once installed, `image-gen` can be invoked from any directory; its config resolves in this order: `./config.yaml` in the current directory, then `~/.image-skill/config.yaml`, then `scripts/config.yaml` shipped in this repo (a dev fallback that only resolves for an editable install).

## Running without installing

```bash
cd scripts
uv run image-gen generate "中文提示词/English prompt"
# or
uv run python -m image_skill.main generate "..."
```

## First-time configuration

Don't have an API key yet? See [`GetFreeToken_ModelScope.md`](../GetFreeToken_ModelScope.md) at the repo root for the full registration/free-quota/API-key walkthrough.

Copy `config.yaml.example` to `~/.image-skill/config.yaml` and add a Modelscope API key:

```bash
mkdir -p ~/.image-skill
cp scripts/config.yaml.example ~/.image-skill/config.yaml
# Edit ~/.image-skill/config.yaml with your API key
```

`config.yaml` is gitignored / kept outside the repo — it holds the real API key. `config.yaml.example` is the checked-in template. A `config.yaml` in the current directory (if you're running in-place inside a checkout) still takes priority over `~/.image-skill/config.yaml`.

### Config structure

```yaml
modelscope:
  api_key: "ms-your-key"
  base_url: "https://api-inference.modelscope.cn/"
  default_model: "Tongyi-MAI/Z-Image-Turbo"
  async_mode: true

models:
  - id: "org/model-id"
    name: "Display Name"
    description: "Description"
    supports_lora: true

generation:
  output_dir: "./outputs"   # relative to the cwd the command is run from, not to config.yaml
  poll_interval: 5
  timeout: 300
  default_width: 1024
  default_height: 1024
```

## Adding new models

Append to the `models` list in `config.yaml` (see structure above), then reference the new `id` with `--model` or `image-gen set-model <model-id>`.

## Output directory behavior

`generation.output_dir` (default `./outputs`) is resolved relative to the process's current working directory at the time `image-gen` is run — not relative to `config.yaml` or the installed package location. So the same command run from two different directories writes to two different `outputs/` folders, unless overridden per-call with `-o/--output`.
