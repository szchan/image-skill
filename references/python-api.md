# Python API & LoRA

Reference for calling `ModelscopeClient` directly instead of the `image-gen` CLI (e.g. to build LoRA requests, which the CLI has no flags for), or for using return-URLs-without-downloading calls.

## Basic usage

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

## Submit without waiting

Mirrors the CLI's `--no-wait` / `status`: submit a job, get a `task_id` back immediately, and check or block on it later — without holding the process open or resorting to OS-level backgrounding.

```python
task_id = client.submit_generate(prompt="A beautiful landscape")
# ... do other work ...

status = client.get_task_status(task_id)   # one non-blocking check
if status["task_status"] == "SUCCEED":
    paths = client.save_urls(status["output_images"])

# or just block until it's done, whenever that's convenient:
urls = client.wait_for_task(task_id)
paths = client.save_urls(urls)
```

`submit_edit(image, prompt, ...)` is the edit-side equivalent of `submit_generate`. Both require `modelscope.async_mode: true` (the default) since there's no `task_id` to check in sync mode.

## LoRA support

Only reachable via the Python API — `generate()` and `edit()` both accept `loras`:

```python
# Single LoRA
client.generate(prompt="...", loras="username/lora-repo-id")

# Multiple LoRAs (weights must sum to 1.0)
client.generate(prompt="...", loras={"lora1": 0.6, "lora2": 0.4})
```

Only models with `supports_lora: true` in `config.yaml` accept this parameter.
