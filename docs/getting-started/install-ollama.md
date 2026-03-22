---
layout: default
title: Install Ollama
parent: Getting Started
nav_order: 1
---

# Install Ollama

commit-msg-ai requires [Ollama](https://ollama.com) to run language models locally on your machine. Ollama handles downloading, running, and managing LLMs.

## macOS

```bash
brew install ollama
```

## Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Windows

Download the installer from [ollama.com/download](https://ollama.com/download).

## Start the server

After installing, start Ollama:

```bash
ollama serve
```

{: .note }
On macOS, Ollama runs automatically in the background after installation. If you see the Ollama icon in your menu bar, you can skip this step.

## Verify installation

```bash
ollama --version
```

You should see something like `ollama version 0.6.x`. If you do, you're ready to pull a model.

---

Next: [Choose a model]({{ site.baseurl }}/getting-started/choose-model/)
