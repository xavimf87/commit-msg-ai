import argparse
import subprocess
import sys

import httpx

SYSTEM_PROMPT = """\
You are a commit message generator. Given a git diff, write a clear and concise \
commit message following the Conventional Commits format (e.g. feat:, fix:, refactor:, docs:, chore:).

Rules:
- First line: type and short summary, max 72 characters.
- If needed, add a blank line followed by a longer explanation.
- Write in English.
- Focus on WHY the change was made, not just WHAT changed.
- Do NOT wrap the message in quotes or markdown.
- Do NOT include any text other than the commit message itself.\
"""

DEFAULT_MODEL = "llama3.2"
DEFAULT_URL = "http://localhost:11434"


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


def get_staged_files() -> str:
    result = subprocess.run(
        ["git", "diff", "--staged", "--name-status"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def generate_message(diff: str, model: str, url: str) -> str:
    user_prompt = f"Generate a commit message for this diff:\n\n{diff}"

    # Truncate very large diffs to avoid overwhelming the model
    max_chars = 12000
    if len(user_prompt) > max_chars:
        user_prompt = user_prompt[:max_chars] + "\n\n... (diff truncated)"

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


def main():
    parser = argparse.ArgumentParser(
        description="Generate a commit message from staged changes using a local LLM.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Ollama model to use (default: {DEFAULT_MODEL})",
    )
    parser.add_argument(
        "--url",
        default=DEFAULT_URL,
        help=f"Ollama server URL (default: {DEFAULT_URL})",
    )
    args = parser.parse_args()

    diff = get_staged_diff()
    if not diff.strip():
        print("No staged changes found. Stage your changes with `git add` first.")
        sys.exit(1)

    files = get_staged_files()
    print(f"Staged files:\n{files}\n")
    print(f"Generating commit message with {args.model}...\n")

    message = generate_message(diff, args.model, args.url)

    print("─" * 50)
    print(message)
    print("─" * 50)
    print()

    if confirm("Commit with this message?"):
        do_commit(message)
    else:
        print("Aborted.")


if __name__ == "__main__":
    main()
