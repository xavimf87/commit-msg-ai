import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import httpx

SYSTEM_PROMPT = """\
You are a commit message generator. Given a git diff and file list, write a clear and concise commit message.

Allowed prefixes (use ONLY these, never add a scope in parentheses):
- feat: for new features or functionality
- fix: for bug fixes
- bc: for breaking changes

Rules:
- Write a SINGLE line: prefix and short summary, max 72 characters. Example: "feat: add user authentication"
- NEVER use scopes like feat(app): or fix(core): — just "feat:", "fix:", or "bc:" directly.
- NEVER write multi-line messages. Output exactly ONE line, no body, no bullets.
- Always consider the FULL file list to understand the scope, especially if the diff is truncated.
- The summary must capture the overall intent, not list individual changes.
- Write in English.
- Focus on WHY the change was made, not just WHAT changed.
- Do NOT wrap the message in quotes or markdown.
- Do NOT include any text other than the commit message itself.\
"""

DEFAULT_MODEL = "llama3.2"
DEFAULT_URL = "http://localhost:11434"
CONFIG_PATH = Path.home() / ".config" / "commit-msg-ai" / "config.json"


def load_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_config(config: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, indent=2) + "\n")


def get_staged_diff() -> str:
    result = subprocess.run(
        ["git", "diff", "--staged"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Error running git diff: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return result.stdout


def get_branch_issue() -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    branch = result.stdout.strip()
    match = re.search(r"/([A-Z][A-Z0-9]+-\d+)", branch)
    return match.group(1) if match else None


def get_staged_files() -> str:
    result = subprocess.run(
        ["git", "diff", "--staged", "--name-status"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def generate_message(diff: str, files: str, model: str, url: str) -> str:
    max_diff_chars = 12000
    truncated = len(diff) > max_diff_chars

    parts = [f"Files changed:\n{files}\n"]
    if truncated:
        parts.append(f"Diff (truncated, showing first {max_diff_chars} chars):\n{diff[:max_diff_chars]}")
        parts.append("\n\nThe diff was truncated. Use the file list above to understand the full scope of changes.")
    else:
        parts.append(f"Diff:\n{diff}")

    user_prompt = "Generate a commit message for these changes:\n\n" + "\n".join(parts)

    try:
        response = httpx.post(
            f"{url}/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                "stream": False,
            },
            timeout=60.0,
        )
        response.raise_for_status()
    except httpx.ConnectError:
        print(
            "Error: Cannot connect to Ollama. Is it running?\n"
            f"Expected at: {url}",
            file=sys.stderr,
        )
        sys.exit(1)
    except httpx.HTTPStatusError as e:
        print(f"Error from Ollama: {e.response.text}", file=sys.stderr)
        sys.exit(1)

    return response.json()["message"]["content"].strip()


def confirm(prompt: str) -> bool:
    answer = input(f"{prompt} [Y/n] ").strip().lower()
    return answer in ("", "y", "yes")


def do_commit(message: str) -> None:
    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Commit failed: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(result.stdout)


def cmd_config(args):
    config = load_config()

    if args.key is None:
        if not config:
            print("No config set. Use: commit-msg-ai config model <value>")
        else:
            for k, v in config.items():
                print(f"{k} = {v}")
        return

    if args.value is None:
        value = config.get(args.key)
        if value is None:
            print(f"{args.key} is not set")
        else:
            print(f"{args.key} = {value}")
        return

    config[args.key] = args.value
    save_config(config)
    print(f"{args.key} = {args.value}")


def cmd_run(args):
    config = load_config()
    model = args.model or config.get("model", DEFAULT_MODEL)
    url = args.url or config.get("url", DEFAULT_URL)

    diff = get_staged_diff()
    if not diff.strip():
        print("No staged changes found. Stage your changes with `git add` first.")
        sys.exit(1)

    files = get_staged_files()
    print(f"Staged files:\n{files}\n")
    print(f"Generating commit message with {model}...\n")

    message = generate_message(diff, files, model, url)

    issue = get_branch_issue()
    if issue:
        message = re.sub(r"^(feat|fix|bc):\s*", rf"\1: [{issue}] ", message)

    print("─" * 50)
    print(message)
    print("─" * 50)
    print()

    if confirm("Commit with this message?"):
        do_commit(message)
    else:
        print("Aborted.")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a commit message from staged changes using a local LLM.",
    )
    sub = parser.add_subparsers(dest="command")

    # config subcommand
    cfg = sub.add_parser("config", help="Get or set config values (model, url)")
    cfg.add_argument("key", nargs="?", help="Config key (model, url)")
    cfg.add_argument("value", nargs="?", help="Value to set")

    # Default run flags (also work without subcommand)
    parser.add_argument("--model", default=None, help="Ollama model to use")
    parser.add_argument("--url", default=None, help="Ollama server URL")

    args = parser.parse_args()

    if args.command == "config":
        cmd_config(args)
    else:
        cmd_run(args)


if __name__ == "__main__":
    main()
