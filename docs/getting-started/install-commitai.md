---
layout: default
title: Install commitai
parent: Getting Started
nav_order: 3
---

# Install commitai

## With pipx (recommended)

[pipx](https://pipx.pypa.io/) installs Python CLI tools in isolated environments:

```bash
pipx install git+https://github.com/xavimf87/commitai.git
```

{: .tip }
If you don't have pipx: `brew install pipx` (macOS) or `pip install pipx` (any platform).

## With pip

```bash
pip install git+https://github.com/xavimf87/commitai.git
```

## Verify installation

```bash
commitai --help
```

You should see:

```
usage: commitai [-h] [--model MODEL] [--url URL] {config} ...

Generate a commit message from staged changes using a local LLM.
```

## Requirements

- Python 3.9 or higher
- Ollama running locally (or on a reachable server)
- At least one model pulled

---

Next: [Configuration]({{ site.baseurl }}/getting-started/configuration/)
