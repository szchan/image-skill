# Image Gen Skill - Modelscope API Inference

A Python CLI tool for generating and editing images using Modelscope's API Inference service.

## Features

- Config-based API key management (no hardcoded secrets)
- Support for multiple models with easy switching
- Text-to-image generation and prompt-driven image editing
- Async task polling with configurable intervals
- Automatic image download and saving
- Installable as a global `uv tool`, or run in-place with `uv run`

## Installation

```bash
cd scripts
uv sync                        # install deps into scripts/.venv
# or, to get a global `image-gen` command:
uv tool install --editable .
```

The `--editable` install means edits to `scripts/src/` take effect immediately, without reinstalling.

## Configuration

Copy `config.yaml.example` to `config.yaml` and add your API key:

```bash
cd scripts
cp config.yaml.example config.yaml
# Edit config.yaml with your API key
```

`config.yaml` is gitignored. When `image-gen` is installed as a tool and run from another directory, it automatically falls back to `scripts/config.yaml` if no `config.yaml` exists in the current directory.

### Config Structure

```yaml
modelscope:
  api_key: "your-api-key"
  base_url: "https://api-inference.modelscope.cn/"
  default_model: "Tongyi-MAI/Z-Image-Turbo"
  async_mode: true

models:
  - id: "Tongyi-MAI/Z-Image-Turbo"
    name: "Z-Image-Turbo"
    description: "Fast generation, low cost"
    supports_lora: true
  # ... more models

generation:
  default_prompt: "A golden cat"
  output_dir: "./outputs"
  poll_interval: 5
  timeout: 300
```

## Usage

### Generate an image

```bash
# Use default model from config
image-gen generate "A beautiful sunset over mountains"

# Use specific model
image-gen generate "A golden cat" --model Qwen/Qwen-Image

# With custom parameters
image-gen generate "A cyberpunk city" \
  --width 1024 --height 1024 \
  --steps 30 --cfg-scale 7.5 \
  --output ./my_images --prefix cyberpunk
```

### Edit an existing image

```bash
# Local file path
image-gen edit ./cat.jpg "Add a blue hat"

# Remote URL, with a specific model and negative prompt
image-gen edit https://example.com/cat.jpg "Make it night time" \
  --model Qwen/Qwen-Image-Edit --negative-prompt "blurry"
```

### List available models

```bash
image-gen list-models
```

### Switch default model

```bash
image-gen set-model Qwen/Qwen-Image
```

### Show current default model

```bash
image-gen current-model
```

Not using the installed tool? Prefix any command with `uv run`, e.g. `uv run image-gen generate "..."`.

## Python API

```python
from image_skill.modelscope_client import ModelscopeClient

client = ModelscopeClient(config_path="config.yaml")

# Generate and save
paths = client.generate_and_save(
    prompt="A golden cat",
    model="Tongyi-MAI/Z-Image-Turbo",
    width=1024,
    height=1024,
)

# Edit an existing image (local path or URL) and save
paths = client.edit_and_save(
    image="./cat.jpg",
    prompt="Add a blue hat",
    model="Qwen/Qwen-Image-Edit",
)

# Or just get URLs
urls = client.generate(prompt="A beautiful landscape")
urls = client.edit(image="./cat.jpg", prompt="Add a blue hat")

# Switch model
client.set_model("Qwen/Qwen-Image")
```

## Supported Models (from config)

- **Tongyi-MAI/Z-Image-Turbo** - Fast, low cost, LoRA support (generate only)
- **Qwen/Qwen-Image** - High quality, editing support, LoRA support
- **Qwen/Qwen-Image-Edit** - Image editing, LoRA support

Add more models to `config.yaml` as needed.

## LoRA Usage

```python
# Single LoRA
client.generate(prompt="...", loras="username/lora-repo-id")

# Multiple LoRAs (weights must sum to 1.0)
client.generate(prompt="...", loras={"lora1": 0.6, "lora2": 0.4})
```

## License

MIT
