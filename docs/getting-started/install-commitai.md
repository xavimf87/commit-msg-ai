---
layout: default
title: Install commit-msg-ai
parent: Getting Started
nav_order: 3
---

# Install commit-msg-ai

## With pip

```bash
pip install commit-msg-ai
```

## Verify installation

```bash
commit-msg-ai --help
```

You should see:

```
usage: commit-msg-ai [-h] [--model MODEL] [--url URL] {config} ...

Generate a commit message from staged changes using a local LLM.
```

## Requirements

- Python 3.9 or higher
- Ollama running locally (or on a reachable server)
- At least one model pulled

---

Next: [Configuration]({{ site.baseurl }}/getting-started/configuration/)
