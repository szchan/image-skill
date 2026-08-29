# Image Gen Skill - Modelscope API Inference

A Python CLI tool for generating images using Modelscope's API Inference service.

## Features

- Config-based API key management (no hardcoded secrets)
- Support for multiple models with easy switching
- Async task polling with configurable intervals
- Automatic image download and saving
- CLI interface for generation and model management

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

1. Copy `.env.example` to `.env` and add your API key:
   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

2. Or edit `config.yaml` directly to set your API key and preferred models.

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
python main.py generate "A beautiful sunset over mountains"

# Use specific model
python main.py generate "A golden cat" --model Qwen/Qwen-Image

# With custom parameters
python main.py generate "A cyberpunk city" \
  --width 1024 --height 1024 \
  --steps 30 --cfg-scale 7.5 \
  --output ./my_images --prefix cyberpunk
```

### List available models

```bash
python main.py list-models
```

### Switch default model

```bash
python main.py set-model Qwen/Qwen-Image
```

### Show current default model

```bash
python main.py current-model
```

## Python API

```python
from modelscope_client import ModelscopeClient

client = ModelscopeClient(config_path="config.yaml")

# Generate and save
paths = client.generate_and_save(
    prompt="A golden cat",
    model="Tongyi-MAI/Z-Image-Turbo",
    width=1024,
    height=1024,
)

# Or just get URLs
urls = client.generate(prompt="A beautiful landscape")

# Switch model
client.set_model("Qwen/Qwen-Image")
```

## Supported Models (from config)

- **Tongyi-MAI/Z-Image-Turbo** - Fast, low cost, LoRA support
- **Qwen/Qwen-Image** - High quality, editing support, LoRA support
- **Qwen/Qwen-Image-Edit** - Image editing, LoRA support
- **black-forest-labs/FLUX.1-dev** - High quality open model
- **black-forest-labs/FLUX.1-schnell** - Fast FLUX variant

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