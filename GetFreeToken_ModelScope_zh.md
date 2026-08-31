# 获取免费的 ModelScope API Key

[English](GetFreeToken_ModelScope.md) | 中文

本指南带你完成：注册 ModelScope（魔搭）账号、解锁每日免费 API 额度、创建 API Key，并把它填到 `image-skill` 的配置文件里。这是给人类手动操作看的；如果你是 AI Agent，请改看 [AGENTS_README.md](AGENTS_README.md#getting-the-user-a-free-modelscope-api-key) 里的"For AI agents"小节——下面这些步骤你没法替人类完成，只能引导人类去做。

### 1. 注册 / 登录

1. 打开 **https://modelscope.cn**，点击右上角 **登录**。
2. 用 GitHub、支付宝或手机号登录，任选一种。

### 2. 绑定阿里云账号 + 完成实名认证（免费额度的必要条件）

这一步很容易漏掉，也是 API 调用报 `401 please bind your alibaba cloud account before use` 最常见的原因。**只有同时完成阿里云账号绑定和实名认证，才能拿到每日免费额度。**

1. 点击右上角头像 → **绑定阿里云账号**。
2. 按提示点击"关联阿里云账号领取免费资源"之类的链接。
3. 登录已有阿里云账号，或免费注册一个新账号。
4. 在阿里云弹出的授权页面中，同意授权 ModelScope 访问。
5. 通过阿里云完成个人实名认证——可以用支付宝授权认证，也可以用人脸识别，都是在阿里云侧完成的。

**完成标志**：ModelScope 头像下拉菜单不再提示"绑定账号"，阿里云那边显示账号已实名认证。

### 3. 创建 API Key（访问令牌）

1. 打开 **https://modelscope.cn/my/myaccesstoken**（或：头像菜单 → 访问令牌）。
2. 点击 **新建令牌**，填写描述后确认创建。
3. 复制生成的令牌，格式类似 `ms-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`，这就是要填的 `api_key`。

令牌不会过期，除非你主动吊销，所以这一步通常只需要做一次。

### 4. 查看免费额度（可选）

头像菜单 → **API 使用情况**。免费额度大约是**每天 2000 次调用**，每天 00:00（UTC+8）重置，不会累积到第二天。这个额度是给开发、测试、原型验证用的，不适合生产环境的高并发流量；部分模型在总额度之外可能还有单独更低的每日上限。

### 5. 把 Key 填到 `image-skill` 会读取的位置

`image-skill` 按以下顺序查找 `config.yaml`：

1. 当前目录下的 `./config.yaml`（如果你在项目本地目录里直接运行）
2. **`~/.image-skill/config.yaml`** —— `image-gen` 安装为全局工具后的标准位置
3. 本仓库 `scripts/` 目录里自带的 `config.yaml`（仅在可编辑安装、开发场景下兜底）

正常安装的情况下，把配置文件放在标准位置：

```bash
mkdir -p ~/.image-skill
cp scripts/config.yaml.example ~/.image-skill/config.yaml
```

然后编辑 `~/.image-skill/config.yaml`，把占位符换成真实的值：

```yaml
modelscope:
  api_key: "ms-your-real-token-here"
```

验证是否生效：

```bash
image-gen current-model
```

如果能正常打印出模型 ID 而没有报错，说明 Key 放对了地方。完整的配置结构见 [`references/setup.md`](references/setup.md)，完整的安装流程见 [`AGENTS_README.md`](AGENTS_README.md)。

### 常见问题

| 现象 | 原因 | 解决办法 |
|---|---|---|
| `401 please bind your alibaba cloud account before use` | 第 2 步（绑定阿里云 + 实名认证）没做完 | 重新走一遍第 2 步——这是最常见的卡点 |
| 其他信息的 `401`/`403` | API Key 无效、被吊销，或填错了 | 回到第 3 步核对令牌，必要时重新生成 |
| `429` | 每日免费额度（约 2000 次）用完了 | 等 00:00（UTC+8）每日重置，或按第 4 步查看用量 |
| `Config file not found: config.yaml` | cwd、`~/.image-skill/`、仓库兜底位置都没有 `config.yaml` | 重新走一遍第 5 步 |
