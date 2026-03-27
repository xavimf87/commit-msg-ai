# commit-msg-ai

Generate commit messages from your staged changes using an LLM. Supports [Ollama](https://ollama.com) for local models and any OpenAI-compatible API (vLLM, LiteLLM, text-generation-inference, etc.).

## Getting started

### 1. Install and set up Ollama

commit-msg-ai requires [Ollama](https://ollama.com) to run language models locally. Install it first:

**macOS:**

```bash
brew install ollama
```

**Linux:**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:** Download the installer from [ollama.com/download](https://ollama.com/download).

Once installed, start the Ollama server:

```bash
ollama serve
```

> On macOS, Ollama runs automatically in the background after installation. You can skip this step if you see the Ollama icon in your menu bar.

### 2. Choose a model

You need at least one model downloaded. See what's available on your machine:

```bash
ollama list
```

If the list is empty, pull a model. Some good options for commit message generation:

```bash
# Lightweight and fast (~2GB)
ollama pull llama3.2

# Good for code understanding (~4.7GB)
ollama pull qwen2.5-coder

# Small and capable (~2.3GB)
ollama pull mistral
```

You can browse all available models at [ollama.com/library](https://ollama.com/library).

### 3. Install commit-msg-ai

```bash
pip install commit-msg-ai
```

### 4. Configure your model

By default commit-msg-ai uses `llama3.2`. If you pulled a different model, set it as default:

```bash
commit-msg-ai config model qwen2.5-coder
```

Verify your config:

```bash
commit-msg-ai config
```

### 5. Use it

```bash
git add .
commit-msg-ai
```

```
Staged files:
M  src/auth.py
A  src/middleware.py

Generating commit message with qwen2.5-coder...

──────────────────────────────────────────────────
feat: add JWT authentication middleware
──────────────────────────────────────────────────

Commit with this message? [Y/n] y
[main 3a1b2c3] feat: add JWT authentication middleware
 2 files changed, 45 insertions(+), 3 deletions(-)
```

That's it.

## Configuration

commit-msg-ai stores config in `~/.config/commit-msg-ai/config.json`.

```bash
# Set default model
commit-msg-ai config model mistral

# Set Ollama server URL (useful for remote setups)
commit-msg-ai config url http://192.168.1.50:11434

# Set provider (ollama or openai)
commit-msg-ai config provider ollama

# View all config
commit-msg-ai config

# View a single value
commit-msg-ai config model
```

Override any config for a single run with flags:

```bash
commit-msg-ai --model codellama
commit-msg-ai --url http://other-server:11434
commit-msg-ai --provider openai
```

## Providers

### Ollama (default)

Uses Ollama's `/api/chat` endpoint. This is the default provider — no extra configuration needed beyond installing Ollama.

### OpenAI-compatible API

Uses the `/v1/chat/completions` endpoint, compatible with any server that implements the OpenAI API format: vLLM, LiteLLM, text-generation-inference, Qwen, etc.

```bash
commit-msg-ai config provider openai
commit-msg-ai config url https://your-server.example.com
commit-msg-ai config model your-model-name
```

Or use flags for a single run:

```bash
commit-msg-ai --provider openai --url https://your-server.example.com --model your-model-name
```

## Commit message format

commit-msg-ai generates messages with only three prefixes:

- `feat:` new features
- `fix:` bug fixes
- `bc:` breaking changes

## Requirements

- Python 3.9+
- One of:
  - [Ollama](https://ollama.com) running locally or on a reachable server
  - Any OpenAI-compatible API server
