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

## Writing the prompt

Apply before every `generate`/`edit` call — generation and editing need genuinely different prompt shapes, and getting this wrong is the main cause of bad output:

- **Generate** with Qwen-Image: order the prompt subject → style/medium → setting → lighting/mood → detail, 1–3 sentences. Any text that must render in the image goes in `"double quotes"` — this alone is the biggest lever on text accuracy.
- **Generate** with Z-Image-Turbo: write a long, detailed creative brief instead — this model rewards detail. It has no negative-prompt support at all; `--negative-prompt` is silently ignored, so fold every constraint into the main prompt as a positive statement ("sharp focus" not "not blurry").
- **Edit** with Qwen-Image-Edit: write an instruction describing the *change*, never a description of the end state. Bad: `"A woman with short brown hair in a blue blouse"`. Good: `"Change her hair to short brown and her blouse to blue"`. When multiple similar objects are in frame, disambiguate by position/attribute (`"the second person from the left"`). For in-image text edits, quote the exact replacement text — font/size/style carry over unless you say otherwise.
- For a multi-stage edit, run `edit` twice — feed the first result back in as the next `image` argument — rather than stacking unrelated changes into one instruction.

Full rationale, more examples, and per-model parameter recommendations (`--cfg-scale`/`--steps`) — `references/prompt-guide.md`.

## Available Models (from config.yaml)

- `Tongyi-MAI/Z-Image-Turbo` — Fast, low cost, LoRA support (generate only)
- `Qwen/Qwen-Image` — High quality, editing support, LoRA support
- `Qwen/Qwen-Image-Edit` — Image editing, LoRA support

## Further reference

- Full prompt-writing rationale, examples, and sources — `references/prompt-guide.md`.
- Installing `image-gen` as a `uv tool`, first-time `config.yaml` setup, adding new models, and how `output_dir` resolves — `references/setup.md`.
- Calling `ModelscopeClient` directly from Python and passing `loras` (not exposed via the CLI) — `references/python-api.md`.
