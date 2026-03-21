---
layout: default
title: Configuration
parent: Getting Started
nav_order: 4
---

# Configuration

commitai stores its configuration in `~/.config/commitai/config.json`.

## Set your default model

By default, commitai uses `llama3.2`. To change it:

```bash
commitai config model qwen2.5-coder
```

## Set a custom Ollama URL

If Ollama runs on another machine or port:

```bash
commitai config url http://192.168.1.50:11434
```

## View your configuration

```bash
# See all settings
commitai config

# See a single value
commitai config model
```

## Override per run

Flags override your saved config for a single execution:

```bash
# Use a different model just this once
commitai --model mistral

# Use a different server
commitai --url http://other-server:11434
```

## Config file

The config is a simple JSON file:

```json
{
  "model": "qwen2.5-coder",
  "url": "http://localhost:11434"
}
```

You can also edit it directly at `~/.config/commitai/config.json`.

---

Next: [Usage]({{ site.baseurl }}/getting-started/usage/)
