# devlog

## 2026-03-29

**Request:** `/init` — analyze codebase and create CLAUDE.md
Created `CLAUDE.md` with project overview, setup instructions, and architecture notes.

**Request:** Add AI instructions: good unittests, run ruff formatter, make sure tests pass, make small commits.
Added a Development Rules section to `CLAUDE.md` with the four guidelines.

**Request:** Create project structure with pyproject.toml.
Set up `src/snaike/` package with stubs for `main.py`, `game.py`, `snake.py`, `food.py`; added `tests/`; configured `pyproject.toml` with hatchling, pygame, pytest, and ruff.

**Request:** Add to AI rules that commands and summary of what was done should be inserted in devlog.md.
Added devlog rule to `CLAUDE.md` and created this file.
