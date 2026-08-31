---
name: image-skill
description: Generate/Edit images using Modelscope API Inference. Use when user wants to generate, or edit images via Modelscope's hosted models (Z-Image-Turbo, Qwen-Image, FLUX, etc.). Trigger phrases: "generate image", "create image", "image generation", "edit image", "Modelscope image", "AI image", "画图", "生成图片".
---

# Image Skill — Modelscope API Inference

Generate and edit images via Modelscope's API Inference, through the `image-gen` CLI.

If `image-gen` is not found on PATH, or `config.yaml` is missing/needs an API key, stop and read `references/setup.md` first.

## Commands

| Command | Description |
|---------|-------------|
| `image-gen generate "prompt"` | Generate image with default model |
| `image-gen generate "prompt" --model <model-id>` | Generate with specific model |
| `image-gen edit <image> "prompt"` | Edit an existing image (local path or URL) with a prompt |
| `image-gen edit <image> "prompt" --model <model-id>` | Edit with a specific edit-capable model |
| `image-gen list-models` | List available models |
| `image-gen set-model <model-id>` | Set default model (persists to config.yaml) |
| `image-gen current-model` | Show current default model |

Every generate/edit command accepts: `--negative-prompt`, `--steps`, `--cfg-scale`, `--width`, `--height`, `--seed`, `-o/--output` (output directory, defaults to `./outputs` relative to wherever the command runs), `-p/--prefix` (filename prefix).

`edit` defaults to `Qwen/Qwen-Image-Edit` when `--model` is omitted, since not all models support editing.

## Available Models (from config.yaml)

- `Tongyi-MAI/Z-Image-Turbo` — Fast, low cost, LoRA support (generate only)
- `Qwen/Qwen-Image` — High quality, editing support, LoRA support
- `Qwen/Qwen-Image-Edit` — Image editing, LoRA support

## Further reference

- Installing `image-gen` as a `uv tool`, first-time `config.yaml` setup, adding new models, and how `output_dir` resolves — `references/setup.md`.
- Calling `ModelscopeClient` directly from Python and passing `loras` (not exposed via the CLI) — `references/python-api.md`.
