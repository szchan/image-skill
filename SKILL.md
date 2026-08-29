---
name: image-gen-skill
description: Generate images using Modelscope API Inference. Use when user wants to create, generate, or edit images via Modelscope's hosted models (Z-Image-Turbo, Qwen-Image, FLUX, etc.). Trigger phrases: "generate image", "create image", "image generation", "Modelscope image", "AI image", "画图", "生成图片".
---

# Image Gen Skill — Modelscope API Inference

A skill for generating images via Modelscope's API Inference service.

## Setup

The skill expects a project at `scripts/` with:

- `config.yaml` — API key, model list, generation defaults
- `modelscope_client.py` — Python client library
- `main.py` — CLI entry point
- `venv/` — Python virtual environment with dependencies

## Quick Start

```bash
cd scripts
source venv/bin/activate
python main.py generate "中文提示词/English prompt"
```

## Commands

| Command | Description |
|---------|-------------|
| `python main.py generate "prompt"` | Generate image with default model |
| `python main.py generate "prompt" --model <model-id>` | Generate with specific model |
| `python main.py list-models` | List available models |
| `python main.py set-model <model-id>` | Set default model (persists to config.yaml) |
| `python main.py current-model` | Show current default model |

## Available Models (from config.yaml)

- `Tongyi-MAI/Z-Image-Turbo` — Fast, low cost, LoRA support
- `Qwen/Qwen-Image` — High quality, editing support, LoRA support
- `Qwen/Qwen-Image-Edit` — Image editing, LoRA support
- `black-forest-labs/FLUX.1-dev` — High quality open model
- `black-forest-labs/FLUX.1-schnell` — Fast FLUX variant

## Python API

```python
from modelscope_client import ModelscopeClient

client = ModelscopeClient(config_path="config.yaml")

# Generate and save to ./outputs/
paths = client.generate_and_save(
    prompt="A golden cat",
    model="Tongyi-MAI/Z-Image-Turbo",  # optional, uses default
    width=1024,
    height=1024,
    steps=20,
    cfg_scale=7.0,
)

# Just get URLs
urls = client.generate(prompt="A beautiful landscape")

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

- Python 3.10+
- `requests`, `pyyaml`, `pillow` (in requirements.txt)

## Trigger Keywords

Use this skill when user says:
- "generate image", "create image", "image generation"
- "Modelscope image", "AI image", "画图", "生成图片"
- "Z-Image", "Qwen-Image", "FLUX"
- "Modelscope API", "image-gen-skill"