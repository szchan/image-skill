# 🎨 Image Gen Skill - Modelscope API Inference

English | [中文](README_zh.md)

A skill for generating and editing images using Modelscope's API Inference service.

## ⚡ Quick Install

Send this to your AI Agent:

```bash
Install this skill: https://raw.githubusercontent.com/szchan/image-skill/main/AGENTS_README.md
```

## 🖼️ Examples

Both images below were produced by this tool — nothing hand-picked from elsewhere.

| `generate` | `edit` |
|---|---|
| ![A fox painting at an easel](assets/demo_generate.jpg) | ![A robot handing the fox a paintbrush](assets/demo_edit.jpg) |
| `image-gen generate "A fluffy orange fox sitting at a wooden easel in a cozy sunlit art studio, painting a vibrant abstract canvas with a brush in its paw, warm golden afternoon light through a window, whimsical children's book illustration style, soft textures, rich warm color palette"` | `image-gen edit demo_generate.jpg "Add a small friendly robot standing on the desk next to the fox, handing it a paintbrush, keep the fox and studio the same"` |

## ✨ Features

- 🔑 Config-based API key management (no hardcoded secrets)
- 🔀 Support for multiple models with easy switching
- 🖌️ Text-to-image generation and prompt-driven image editing
- ⏳ Async task polling with configurable intervals
- 💾 Automatic image download and saving
- 🧰 Installable as a global `uv tool`, or run in-place with `uv run`

## 📦 Installation

```bash
cd scripts
uv sync                        # install deps into scripts/.venv
# or, to get a global `image-gen` command:
uv tool install --editable .
```

The `--editable` install means edits to `scripts/src/` take effect immediately, without reinstalling.

## ⚙️ Configuration

Copy `config.yaml.example` to `config.yaml` and add your API key:

```bash
cd scripts
cp config.yaml.example config.yaml
# Edit config.yaml with your API key
```

`config.yaml` is gitignored. When `image-gen` is installed as a tool and run from another directory, it automatically falls back to `scripts/config.yaml` if no `config.yaml` exists in the current directory.

### 🗂️ Config Structure

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

## 🚀 Usage

### 🎨 Generate an image

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

### ✏️ Edit an existing image

```bash
# Local file path
image-gen edit ./cat.jpg "Add a blue hat"

# Remote URL, with a specific model and negative prompt
image-gen edit https://example.com/cat.jpg "Make it night time" \
  --model Qwen/Qwen-Image-Edit --negative-prompt "blurry"
```

### ⏱️ Run without waiting

`generate`/`edit` normally block until Modelscope's job finishes (20s–2min, sometimes longer for edits). Add `--no-wait` to get a task id back immediately instead, then check on it whenever you like:

```bash
image-gen generate "A beautiful sunset over mountains" --no-wait
# → Task submitted: 7ebfeaa1-...

image-gen status 7ebfeaa1-...              # one check; downloads the image if it's done
image-gen status 7ebfeaa1-... --wait       # or block until it's done, then download
```

This only ever reports done when the task actually is — no more nested background jobs reporting "completed" early.

### 📋 List available models

```bash
image-gen list-models
```

### 🔀 Switch default model

```bash
image-gen set-model Qwen/Qwen-Image
```

### ℹ️ Show current default model

```bash
image-gen current-model
```

Not using the installed tool? Prefix any command with `uv run`, e.g. `uv run image-gen generate "..."`.

## 🐍 Python API

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

## 🧩 Supported Models (from config)

- **Tongyi-MAI/Z-Image-Turbo** - Fast, low cost, LoRA support (generate only)
- **Qwen/Qwen-Image** - High quality, editing support, LoRA support
- **Qwen/Qwen-Image-Edit** - Image editing, LoRA support

Add more models to `config.yaml` as needed.

## 🎛️ LoRA Usage

```python
# Single LoRA
client.generate(prompt="...", loras="username/lora-repo-id")

# Multiple LoRAs (weights must sum to 1.0)
client.generate(prompt="...", loras={"lora1": 0.6, "lora2": 0.4})
```

## 📄 License

MIT
