# commitai

Generate commit messages from your staged changes using a local LLM via [Ollama](https://ollama.com). No API keys, no cloud — everything runs on your machine.

## Getting started

### 1. Install and set up Ollama

commitai requires [Ollama](https://ollama.com) to run language models locally. Install it first:

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

### 3. Install commitai

**With pipx (recommended):**

```bash
pipx install git+https://github.com/YOUR_USER/commitai.git
```

**With pip:**

```bash
pip install git+https://github.com/YOUR_USER/commitai.git
```

### 4. Configure your model

By default commitai uses `llama3.2`. If you pulled a different model, set it as default:

```bash
commitai config model qwen2.5-coder
```

Verify your config:

```bash
commitai config
```

### 5. Use it

```bash
git add .
commitai
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

commitai stores config in `~/.config/commitai/config.json`.

```bash
# Set default model
commitai config model mistral

# Set Ollama server URL (useful for remote setups)
commitai config url http://192.168.1.50:11434

# View all config
commitai config

# View a single value
commitai config model
```

Override any config for a single run with flags:

```bash
commitai --model codellama
commitai --url http://other-server:11434
```

## Commit message format

commitai generates messages with only three prefixes:

- `feat:` new features
- `fix:` bug fixes
- `bc:` breaking changes

## Requirements

- Python 3.9+
- [Ollama](https://ollama.com) running locally (or on a reachable server)
- At least one model pulled (`ollama pull llama3.2`)
