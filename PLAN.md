# snAIke Implementation Plan

## Architecture Decisions

- **Grid-only logic**: `snake.py` and `food.py` work entirely in grid cells (integer tuples), never pixels. Pixels are the renderer's concern only.
- **pygame isolation**: All pygame calls live in a `Renderer` class inside `game.py`. Pure logic never imports pygame — this makes the whole domain layer unit-testable without a display.
- **Direction as enum**: Makes 180° reversal checks clean.
- **`next_head()` helper**: `GameState.tick()` peeks at the next head position before stepping, so it can decide `grow=True/False` without any rollback logic.

---

## Phase 1 — Direction enum and Vec2 (`snake.py`)

`Direction(Enum)` with `.delta` (grid offset) and `.opposite`. `Vec2 = tuple[int, int]` type alias.

**Tests**: each direction's delta, opposite pairs.

---

## Phase 2 — Snake model (`snake.py`)

`Snake` class: `segments`, `step(grow)`, `set_direction` (rejects reversal), `next_head()`, `is_alive()`, `occupies()`.

**Tests**: movement, growth/shrink, wall collision, self-collision, reversal rejection.

---

## Phase 3 — Food model (`food.py`)

`FoodKind(Enum)` (frog/bird/mouse with point values), `Food` dataclass, `spawn_food(occupied, grid_width, grid_height, rng)`.

**Tests**: correct points, placement in free cells only, returns `None` on full grid. Uses injected `rng` for determinism.

---

## Phase 4 — Game state machine (`game.py`, no rendering)

`GameState` with `tick(rng)` and `handle_input(direction)`. Tick: peek `next_head`, determine `grow`, step, update food/score, check alive.

**Tests**: eat increases score and spawns new food, no-eat leaves food unchanged, wall death, self-collision death.

---

## Phase 5 — Renderer (`game.py`, pygame, not unit tested)

`Renderer` class: draws grid, snake (head distinct), food (colored pygame primitives — no images/emojis for cross-platform reliability), score bar. `SDL_VIDEODRIVER=dummy` smoke test for CI.

---

## Phase 6 — Input and game loop (`game.py` + `main.py`)

`KEY_MAP` (WASD + arrows → Direction), `run_game()` loop at 10 FPS. Wire `main.py` to call `run_game()`.

---

## Phase 7 — Game over screen

Overlay "GAME OVER" + score + "R to restart / ESC to quit". `R` key calls `GameState.new()`.

---

## Phase 8 — Hunger timer tuning

Add `HUNGER_TICKS = 30` so the snake only loses a segment every N ticks without eating. Minimum length of 1. Snake dies only from wall/self-collision, not starvation.

---

## Dependency Order

```
Phase 1: Direction + Vec2
Phase 2: Snake          (needs Direction)
Phase 3: Food           (needs Vec2 only — parallel with Phase 2)
Phase 4: GameState      (needs Snake + Food)
Phase 5: Renderer       (needs GameState + pygame)
Phase 6: Game loop      (needs Renderer + GameState)
Phase 7: Game over      (extends 5 + 6)
Phase 8: Hunger tuning  (extends 4)
```
