---
layout: default
title: Choose a Model
parent: Getting Started
nav_order: 2
---

# Choose a Model

commitai works with any model available in Ollama. You need at least one downloaded.

## List your models

See what's already on your machine:

```bash
ollama list
```

If the list is empty, you'll need to pull one.

## Recommended models

| Model | Size | Best for |
|:------|:-----|:---------|
| `llama3.2` | ~2 GB | General purpose, fast, good default |
| `qwen2.5-coder` | ~4.7 GB | Code understanding, best quality |
| `mistral` | ~2.3 GB | Fast and capable |
| `codellama` | ~3.8 GB | Code-focused |

## Pull a model

```bash
# Lightweight and fast (recommended to start)
ollama pull llama3.2

# Better code understanding
ollama pull qwen2.5-coder
```

{: .tip }
Start with `llama3.2` if you're unsure. It's small, fast, and produces good commit messages. You can always switch later.

## Browse all models

The full catalog is at [ollama.com/library](https://ollama.com/library). Any model that works with Ollama works with commitai.

## Test your model

Make sure it's working:

```bash
ollama run llama3.2 "Say hello"
```

If you get a response, you're ready to install commitai.

---

Next: [Install commitai]({{ site.baseurl }}/getting-started/install-commitai/)
