# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

snAIke is a Python-based snake game playable from the command line on macOS and Windows. The player controls a snake that eats frogs, birds, and mice to grow longer; not eating causes the snake to shrink. Controls: WASD and arrow keys.

## Setup

This project has no dependency management files yet. When adding dependencies, use `pyproject.toml` (preferred) or `requirements.txt`. Install dependencies with:

```bash
pip install -r requirements.txt
# or
pip install -e .
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
pip install -e ".[dev]"   # install with dev dependencies
snaike                    # run the game
pytest                    # run tests
ruff format .             # format code
ruff check .              # lint
```

## Development Rules

- **Formatting**: Run `ruff format .` before every commit. Also run `ruff check .` and fix any reported issues.
- **Tests**: All tests must pass before committing. Run with `pytest`. Never commit code that breaks existing tests.
- **Writing tests**: Write unit tests for new logic. Tests should be focused and fast. Prefer testing behavior over implementation details.
- **Commits**: Make small, focused commits — one logical change per commit. Do not bundle unrelated changes together.
