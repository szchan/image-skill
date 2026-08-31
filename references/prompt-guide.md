# Prompt Guide

Full rationale and examples behind the checklist in `SKILL.md`. Each model family here needs a genuinely different prompt shape — generation prompts describe a scene, edit prompts describe an operation — so read the section for the command you're about to run.

## Generation: Qwen/Qwen-Image

Prompt structure, in order: **[main subject] → [visual style/medium] → [environment & background] → [lighting/mood] → [extra detail] → ["exact text if any"]**. Keep it to 1–3 plain-language sentences — state subject, style, and mood simply rather than piling on adjectives.

**Text rendering**: put the literal text in double quotes. This is the single highest-leverage rule for this model — quoting exact wording raises rendering accuracy from roughly 65% to 96% in community benchmarks. For a poster/typography-heavy image with multiple text blocks, describe each block on its own line with its position, size, and contrast literally ("small caption bottom-right", not "a caption somewhere"), since the model follows spatial description more reliably than vague layout language.

Example:
> A futuristic sports car, photorealistic style, parked under neon city lights, reflections on wet streets, cinematic lighting, "Night Racer" in metallic chrome text on the hood

**Parameters**: `--cfg-scale 4.5 --steps 40` is a reliable general-purpose setting; push `--steps` to 50 when the image is dense with text. `--negative-prompt` is supported and works normally here (unlike Z-Image-Turbo below).

Source: [Segmind Qwen-Image prompt & parameter guide](https://blog.segmind.com/qwen-image-prompt-parameter-guide/), [WaveSpeed text-rendering guide](https://wavespeed.ai/blog/posts/qwen-image-2512-text-rendering/).

## Generation: Tongyi-MAI/Z-Image-Turbo

This model behaves differently enough from Qwen-Image that reusing the same short-prompt style under-performs:

- **Write long, detailed prompts** — treat it like a creative brief (subject, medium, setting, lighting, mood, fine detail), not a short caption. It was tuned to reward detail rather than punished for verbosity.
- **`--negative-prompt` does not work on this model** — its architecture runs at zero classifier-free guidance, so negation has no effect even though the CLI will still send it. Never rely on it here: fold every constraint directly into the main prompt as a positive statement ("sharp focus, clean lines" instead of "not blurry, no artifacts").
- Effective attention is capped around ~512 tokens' worth of prompt — quality starts drifting before you hit any hard limit, so don't pad past what's actually descriptive.
- Works in both Chinese and English; if a Chinese prompt underperforms, try an English rewrite of the same brief.

Source: [Tongyi-MAI/Z-Image-Turbo prompting discussion](https://huggingface.co/Tongyi-MAI/Z-Image-Turbo/discussions/8).

## Editing: Qwen/Qwen-Image-Edit

The defining rule: **write an instruction describing the change, never a description of the end state.** This model is given the source image plus your prompt and performs an edit operation — a prompt that reads like a fresh image caption confuses it about what's supposed to change versus stay.

- Bad (a description): `"A woman with short brown hair in a blue blouse, studio portrait"`
- Good (an instruction): `"Change her hair to short brown and change her blouse to blue"`

**Disambiguating multiple similar objects**: point at the one you mean by position or attribute — `"the second person from the left"`, `"the cup on the right side of the table"` — rather than a bare noun that could match several things in frame.

**Editing text inside the image**: put the exact replacement text in quotes. Original font, size, and style carry over automatically unless you say otherwise — only mention font feel (`"bold sans-serif"`, `"brush-script"`) or placement (`"centered at the top"`) when you actually want it to change. Works bilingually (Chinese/English) in the same image.

**Scope of a single edit call**: the model handles a tightly related bundle of changes in one instruction fine (e.g. "change her hair to brown and add sunglasses"), but a long chain of loosely related edits in one prompt loses precision. For a multi-stage transformation, prefer running `image-gen edit` twice — feed the first result back in as the `image` argument for the second call — over stacking every change into one instruction.

Supports both low-level appearance edits (add/remove/recolor an object, swap clothing) and high-level semantic edits (style transfer, pose change, background swap) — phrase either as an instruction, per the rule above.

**Parameters**: `--steps 30` to `--steps 40` with `--cfg-scale 3` is a reasonable native-quality setting — edit-model guidance tends to favor a slightly lower CFG than generation.

Source: [Qwen Image Edit Plus prompting guide](https://deapi.ai/blog/qwen-image-edit-plus-prompting-guide-how-to-write-edit-instructions-that-actually-work), [Qwen-Image-Edit paper](https://arxiv.org/pdf/2508.02324).
