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

**Request:** Create a plan on how to work on this.
Created `PLAN.md` with 8 phased implementation plan covering Direction/Vec2, Snake model, Food model, GameState, Renderer, game loop, game over screen, and hunger tuning.

**Request:** Let's go (start implementing).
Implemented Phases 1–6:
- Phase 1: `Direction` enum + `Vec2` type alias in `snake.py`
- Phase 2: `Snake` class with movement, growth, collision detection
- Phase 3: `FoodKind`, `Food` dataclass, `spawn_food()` in `food.py`
- Phase 4: `GameState` with `tick()` and `handle_input()` in `game.py`
- Phase 5: `Renderer` class with pygame drawing (snake, food shapes, score bar, game over overlay)
- Phase 6: `KEY_MAP`, `run_game()` loop, wired `main.py` entry point
Game is now fully playable via `.venv/bin/snaike`. 40 tests passing.
