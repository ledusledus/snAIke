# snAIke

snAIke is an AI generated snake game in Python. It works as a usual snake game and can be run from the command line. It supports running on both MacOS and Windows machines.

## How it works

You start as a small snake, travel around the world and eat frogs, birds, and mice. As you eat, you grow longer. If you don't eat for a while, you shrink. Hit a wall or yourself and it's game over.

| Food  | Points |
|-------|--------|
| Frog  | 1      |
| Bird  | 2      |
| Mouse | 3      |

## Controls

| Key          | Action |
|--------------|--------|
| W / ↑        | Up     |
| S / ↓        | Down   |
| A / ←        | Left   |
| D / →        | Right  |
| R            | Restart (after game over) |
| ESC          | Quit   |

## Requirements

- Python 3.11 or newer

## Setup

```bash
# 1. Create a virtual environment
python3 -m venv .venv

# 2. Install the game and its dependencies
.venv/bin/pip install -e .
```

On Windows, replace `.venv/bin/` with `.venv\Scripts\`.

## Run

```bash
.venv/bin/snaike
```

On Windows:

```bash
.venv\Scripts\snaike
```
