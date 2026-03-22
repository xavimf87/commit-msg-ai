---
layout: default
title: Configuration
parent: Getting Started
nav_order: 4
---

# Configuration

commit-msg-ai stores its configuration in `~/.config/commit-msg-ai/config.json`.

## Set your default model

By default, commit-msg-ai uses `llama3.2`. To change it:

```bash
commit-msg-ai config model qwen2.5-coder
```

## Set a custom Ollama URL

If Ollama runs on another machine or port:

```bash
commit-msg-ai config url http://192.168.1.50:11434
```

## View your configuration

```bash
# See all settings
commit-msg-ai config

# See a single value
commit-msg-ai config model
```

## Override per run

Flags override your saved config for a single execution:

```bash
# Use a different model just this once
commit-msg-ai --model mistral

# Use a different server
commit-msg-ai --url http://other-server:11434
```

## Config file

The config is a simple JSON file:

```json
{
  "model": "qwen2.5-coder",
  "url": "http://localhost:11434"
}
```

You can also edit it directly at `~/.config/commit-msg-ai/config.json`.

---

Next: [Usage]({{ site.baseurl }}/getting-started/usage/)
