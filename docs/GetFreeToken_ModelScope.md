# Getting a Free ModelScope API Key

English | [中文](GetFreeToken_ModelScope_zh.md)

This guide walks you through registering a ModelScope (魔搭) account, unlocking the free daily API quota, creating an API key, and filling it into `image-skill`'s config. It's written for a human doing this by hand; if you're an AI agent, see the "For AI agents" section in [references/AGENTS_README.md](../references/AGENTS_README.md#getting-the-user-a-free-modelscope-api-key) instead — you cannot complete the steps below yourself, only guide a human through them.

### 1. Register / log in

1. Go to **https://modelscope.cn** and click **登录 (Login)** in the top-right corner.
2. Sign in with GitHub, Alipay, or a phone number — whichever you have.

### 2. Bind an Alibaba Cloud account + complete real-name verification (required for the free quota)

This step is easy to miss and is the #1 cause of API calls failing with `401 please bind your alibaba cloud account before use`. The free quota is granted only after both an Alibaba Cloud account binding **and** real-name verification are complete.

1. Click your avatar (top-right) → **绑定阿里云账号 (Bind Alibaba Cloud account)**.
2. Follow the link to link your Alibaba Cloud account for free resources.
3. Log in to an existing Alibaba Cloud account, or register a new one — it's free.
4. Authorize ModelScope's access when Alibaba Cloud prompts you.
5. Complete real-name verification through Alibaba Cloud (个人实名认证) — either an Alipay-linked check or facial recognition, both handled on Alibaba Cloud's side.

**Done when**: your ModelScope avatar menu no longer shows a "bind account" prompt, and Alibaba Cloud shows your account as real-name verified.

### 3. Create an API key (access token)

1. Go to **https://modelscope.cn/my/myaccesstoken** (or: avatar menu → 访问令牌 / Access Tokens).
2. Click **新建令牌 (Create new token)**, give it a description, and confirm.
3. Copy the token — it looks like `ms-xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`. This is your `api_key`.

Tokens don't expire unless you revoke them, so you only need to do this once.

### 4. Check your free quota (optional)

Avatar menu → **API 使用情况 (API usage)**. The free tier is roughly **2000 API calls per day**, resetting at 00:00 (UTC+8). This is meant for development/testing/prototyping, not production traffic — some individual models may carry a lower per-model daily cap on top of the overall limit.

### 5. Put the key where `image-skill` reads it

`image-skill` looks for `config.yaml` in this order:

1. `./config.yaml` in the current directory (if you're running from a project-local checkout)
2. **`~/.image-skill/config.yaml`** — the standard location once `image-gen` is installed as a global tool
3. `config.yaml` shipped inside this repo's `scripts/` folder (dev fallback for an editable install)

For a normal install, create the file at the standard location:

```bash
mkdir -p ~/.image-skill
cp scripts/config.yaml.example ~/.image-skill/config.yaml
```

Then edit `~/.image-skill/config.yaml` and replace the placeholder:

```yaml
modelscope:
  api_key: "ms-your-real-token-here"
```

Verify it worked:

```bash
image-gen current-model
```

If that prints a model id with no error, the key is in the right place. See [`references/AGENTS_README.md`](references/AGENTS_README.md) for the full config structure and the full install walkthrough.

### Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `401 please bind your alibaba cloud account before use` | Step 2 (Alibaba Cloud binding + real-name verification) wasn't completed | Redo step 2 — this is the most common blocker |
| `401`/`403` with a different message | Invalid, revoked, or mistyped API key | Recheck the token at step 3, regenerate if needed |
| `429` | Daily free quota (~2000 calls) exhausted | Wait for the daily reset at 00:00 UTC+8, or check usage per step 4 |
| `Config file not found: config.yaml` | No `config.yaml` in cwd, `~/.image-skill/`, or the repo fallback | Redo step 5 |
