# Setup & Configuration

Reference for installing and configuring the `image-gen` CLI. Not needed for a routine generate/edit call — only when `image-gen` isn't on PATH yet, when `config.yaml` is missing, or when adding/changing models.

## Installing as a local tool (recommended for Agent use)

```bash
cd scripts
uv tool install --editable .
```

This installs `image-gen` as a globally available command (`~/.local/bin/image-gen`), backed by an editable install — source edits under `scripts/src/` take effect immediately without reinstalling. Once installed, `image-gen` can be invoked from any directory; it automatically falls back to `scripts/config.yaml` for its API key when no `config.yaml` exists in the current directory.

## Running without installing

```bash
cd scripts
uv run image-gen generate "中文提示词/English prompt"
# or
uv run python -m image_skill.main generate "..."
```

## First-time configuration

Copy `config.yaml.example` to `config.yaml` and add a Modelscope API key:

```bash
cd scripts
cp config.yaml.example config.yaml
# Edit config.yaml with your API key
```

`config.yaml` is gitignored — it holds the real API key. `config.yaml.example` is the checked-in template.

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
