---
name: image-skill
description: Generate/Edit images using Modelscope API Inference. Use when user wants to generate, or edit images via Modelscope's hosted models (Z-Image-Turbo, Qwen-Image, FLUX, etc.). Trigger phrases: "generate image", "create image", "image generation", "edit image", "Modelscope image", "AI image", "画图", "生成图片".
---

# Image Skill — Modelscope API Inference

A skill for generating and editing images via Modelscope's API Inference service.

## Setup

The skill expects a project at `scripts/` with:

- `config.yaml` — API key, model list, generation defaults
- `src/image_skill/modelscope_client.py` — Python client library
- `src/image_skill/main.py` — CLI entry point
- `pyproject.toml` — `uv`-managed package definition, exposes the `image-gen` CLI script

### Installing as a local tool (recommended for Agent use)

```bash
cd scripts
uv tool install --editable .
```

This installs `image-gen` as a globally available command (`~/.local/bin/image-gen`), backed by an editable install — source edits under `scripts/src/` take effect immediately without reinstalling. Once installed, `image-gen` can be invoked from any directory; it automatically falls back to `scripts/config.yaml` for its API key when no `config.yaml` exists in the current directory.

### Running without installing

```bash
cd scripts
uv run image-gen generate "中文提示词/English prompt"
# or
uv run python -m image_skill.main generate "..."
```

## Commands

| Command | Description |
|---------|-------------|
| `image-gen generate "prompt"` | Generate image with default model |
| `image-gen generate "prompt" --model <model-id>` | Generate with specific model |
| `image-gen edit <image> "prompt"` | Edit an existing image (path or URL) with a prompt |
| `image-gen edit <image> "prompt" --model <model-id>` | Edit with a specific edit-capable model |
| `image-gen list-models` | List available models |
| `image-gen set-model <model-id>` | Set default model (persists to config.yaml) |
| `image-gen current-model` | Show current default model |

Every generation/edit command accepts: `--negative-prompt`, `--steps`, `--cfg-scale`, `--width`, `--height`, `--seed`, `-o/--output` (output directory), `-p/--prefix` (filename prefix).

`edit` defaults to `Qwen/Qwen-Image-Edit` when `--model` is omitted, since not all models support editing.

## Available Models (from config.yaml)

- `Tongyi-MAI/Z-Image-Turbo` — Fast, low cost, LoRA support (generate only)
- `Qwen/Qwen-Image` — High quality, editing support, LoRA support
- `Qwen/Qwen-Image-Edit` — Image editing, LoRA support
- `black-forest-labs/FLUX.1-dev` — High quality open model
- `black-forest-labs/FLUX.1-schnell` — Fast FLUX variant

## Python API

```python
from image_skill.modelscope_client import ModelscopeClient

client = ModelscopeClient(config_path="config.yaml")

# Generate and save to ./outputs/
paths = client.generate_and_save(
    prompt="A golden cat",
    model="Tongyi-MAI/Z-Image-Turbo",  # optional, uses default
    negative_prompt="blurry, low quality",
    width=1024,
    height=1024,
    steps=20,
    cfg_scale=7.0,
)

# Edit an existing image (local path or URL) and save to ./outputs/
paths = client.edit_and_save(
    image="./cat.jpg",
    prompt="Add a blue hat",
    model="Qwen/Qwen-Image-Edit",  # optional, uses default
    negative_prompt="deformed",
    width=1024,
    height=1024,
)

# Just get URLs, without downloading
urls = client.generate(prompt="A beautiful landscape")
urls = client.edit(image="https://example.com/cat.jpg", prompt="Make it night time")

# Switch model programmatically
client.set_model("Qwen/Qwen-Image")
```

## LoRA Support

```python
# Single LoRA
client.generate(prompt="...", loras="username/lora-repo-id")

# Multiple LoRAs (weights must sum to 1.0)
client.generate(prompt="...", loras={"lora1": 0.6, "lora2": 0.4})
```

## Configuration

Edit `config.yaml` to customize:

```yaml
modelscope:
  api_key: "ms-your-key"  # Your Modelscope token
  base_url: "https://api-inference.modelscope.cn/"
  default_model: "Tongyi-MAI/Z-Image-Turbo"
  async_mode: true

generation:
  output_dir: "./outputs"
  poll_interval: 5
  timeout: 300
  default_width: 1024
  default_height: 1024
```

## Adding New Models

Add to `models` list in `config.yaml`:

```yaml
models:
  - id: "org/model-id"
    name: "Display Name"
    description: "Description"
    supports_lora: true
```

## Requirements

- Python 3.13+
- `requests`, `pyyaml`, `pillow` (managed via `uv` / `pyproject.toml`)

## Trigger Keywords

Use this skill when user says:
- "generate image", "create image", "image generation"
- "edit image", "image editing"
- "Modelscope image", "AI image", "画图", "生成图片", "编辑图片"
- "Z-Image", "Qwen-Image", "FLUX"
- "Modelscope API", "image-skill"
