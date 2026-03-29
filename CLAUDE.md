# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

snAIke is a Python-based snake game playable from the command line on macOS and Windows. The player controls a snake that eats frogs, birds, and mice to grow longer; not eating causes the snake to shrink. Controls: WASD and arrow keys.

## Setup

Requires Python 3.11+ (Homebrew Python 3.13 is available at `/opt/homebrew/bin/python3.13`).

```bash
/opt/homebrew/bin/python3.13 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Running the Game

```bash
python main.py  # adjust once entry point is established
```

## Architecture Notes

- **Early-stage repo**: Only README and .gitignore exist. No source code has been committed yet.
- The `.gitignore` is pre-configured for Python tooling (pytest, coverage, mypy, ruff, poetry, pipenv, pdm, etc.), so those tools can be adopted without gitignore changes.
- Game framework not yet chosen — likely Pygame or curses-based for terminal rendering.

## Commands

```bash
.venv/bin/pip install -e ".[dev]"   # install with dev dependencies
.venv/bin/snaike                    # run the game
.venv/bin/pytest                    # run tests
.venv/bin/ruff format .             # format code
.venv/bin/ruff check .              # lint
```

## Development Rules

- **Formatting**: Run `ruff format .` before every commit. Also run `ruff check .` and fix any reported issues.
- **Tests**: All tests must pass before committing. Run with `pytest`. Never commit code that breaks existing tests.
- **Writing tests**: Write unit tests for new logic. Tests should be focused and fast. Prefer testing behavior over implementation details.
- **Commits**: Make small, focused commits — one logical change per commit. Do not bundle unrelated changes together.
- **Devlog**: After completing any task, append an entry to `devlog.md` with the date, the user's request (verbatim or a close paraphrase), and a short summary of what was done.
