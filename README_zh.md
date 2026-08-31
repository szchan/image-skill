# Image Gen Skill - Modelscope API Inference

[English](README.md) | 中文

使用 Modelscope API Inference 服务生成和编辑图片的 Python 命令行工具。

## 特性

- 基于配置文件管理 API Key（不硬编码密钥）
- 支持多个模型，可随时切换
- 支持文生图与提示词驱动的图片编辑
- 异步任务轮询，轮询间隔可配置
- 自动下载并保存生成的图片
- 可安装为全局 `uv tool`，也可用 `uv run` 原地运行

## 安装

```bash
cd scripts
uv sync                        # 将依赖安装到 scripts/.venv
# 或者，安装为全局 `image-gen` 命令：
uv tool install --editable .
```

`--editable` 安装意味着修改 `scripts/src/` 下的代码会立即生效，无需重新安装。

## 配置

复制 `config.yaml.example` 为 `config.yaml` 并填入你的 API Key：

```bash
cd scripts
cp config.yaml.example config.yaml
# 编辑 config.yaml，填入你的 API Key
```

`config.yaml` 已被 gitignore。当 `image-gen` 作为全局工具安装后，从其他目录运行时，如果当前目录下没有 `config.yaml`，会自动回退使用 `scripts/config.yaml`。

### 配置文件结构

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
  # ... 更多模型

generation:
  default_prompt: "A golden cat"
  output_dir: "./outputs"
  poll_interval: 5
  timeout: 300
```

## 使用方法

### 生成图片

```bash
# 使用配置文件中的默认模型
image-gen generate "A beautiful sunset over mountains"

# 使用指定模型
image-gen generate "A golden cat" --model Qwen/Qwen-Image

# 使用自定义参数
image-gen generate "A cyberpunk city" \
  --width 1024 --height 1024 \
  --steps 30 --cfg-scale 7.5 \
  --output ./my_images --prefix cyberpunk
```

### 编辑已有图片

```bash
# 本地文件路径
image-gen edit ./cat.jpg "Add a blue hat"

# 远程 URL，指定模型和反向提示词
image-gen edit https://example.com/cat.jpg "Make it night time" \
  --model Qwen/Qwen-Image-Edit --negative-prompt "blurry"
```

### 列出可用模型

```bash
image-gen list-models
```

### 切换默认模型

```bash
image-gen set-model Qwen/Qwen-Image
```

### 查看当前默认模型

```bash
image-gen current-model
```

没有安装为全局工具？在任意命令前加上 `uv run` 即可，例如 `uv run image-gen generate "..."`。

## Python API

```python
from image_skill.modelscope_client import ModelscopeClient

client = ModelscopeClient(config_path="config.yaml")

# 生成并保存
paths = client.generate_and_save(
    prompt="A golden cat",
    model="Tongyi-MAI/Z-Image-Turbo",
    width=1024,
    height=1024,
)

# 编辑已有图片（本地路径或 URL）并保存
paths = client.edit_and_save(
    image="./cat.jpg",
    prompt="Add a blue hat",
    model="Qwen/Qwen-Image-Edit",
)

# 或者只获取图片 URL
urls = client.generate(prompt="A beautiful landscape")
urls = client.edit(image="./cat.jpg", prompt="Add a blue hat")

# 切换模型
client.set_model("Qwen/Qwen-Image")
```

## 支持的模型（来自配置文件）

- **Tongyi-MAI/Z-Image-Turbo** - 速度快、成本低，支持 LoRA（仅支持生成）
- **Qwen/Qwen-Image** - 高质量，支持编辑，支持 LoRA
- **Qwen/Qwen-Image-Edit** - 图片编辑，支持 LoRA

如有需要，可在 `config.yaml` 中添加更多模型。

## LoRA 用法

```python
# 单个 LoRA
client.generate(prompt="...", loras="username/lora-repo-id")

# 多个 LoRA（权重之和必须为 1.0）
client.generate(prompt="...", loras={"lora1": 0.6, "lora2": 0.4})
```

## 许可证

MIT
