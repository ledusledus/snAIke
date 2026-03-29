import random
from dataclasses import dataclass

import pygame

from snaike.food import Food, FoodKind, spawn_food
from snaike.snake import Direction, Snake, Vec2

GRID_WIDTH = 30
GRID_HEIGHT = 20
INITIAL_LENGTH = 3
HUNGER_TICKS = 30


@dataclass
class GameState:
    snake: Snake
    food: Food | None
    score: int
    ticks: int
    ticks_since_eat: int
    is_over: bool

    @classmethod
    def new(cls, rng: random.Random | None = None) -> "GameState":
        start: Vec2 = (GRID_WIDTH // 2, GRID_HEIGHT // 2)
        snake = Snake(start=start, length=INITIAL_LENGTH, direction=Direction.RIGHT)
        occupied = set(snake.segments)
        food = spawn_food(occupied, GRID_WIDTH, GRID_HEIGHT, rng)
        return cls(snake=snake, food=food, score=0, ticks=0, ticks_since_eat=0, is_over=False)

    def handle_input(self, direction: Direction) -> None:
        self.snake.set_direction(direction)

    def tick(self, rng: random.Random | None = None) -> None:
        if self.is_over:
            return

        next_head = self.snake.next_head()
        eat = self.food is not None and next_head == self.food.pos

        self.snake.step(grow=eat)
        self.ticks += 1

        if eat:
            self.score += self.food.points  # type: ignore[union-attr]
            self.ticks_since_eat = 0
            occupied = set(self.snake.segments)
            self.food = spawn_food(occupied, GRID_WIDTH, GRID_HEIGHT, rng)
        else:
            self.ticks_since_eat += 1
            if self.ticks_since_eat >= HUNGER_TICKS and len(self.snake.segments) > 1:
                self.snake.segments.pop()
                self.ticks_since_eat = 0

        if not self.snake.is_alive(GRID_WIDTH, GRID_HEIGHT):
            self.is_over = True


_SCORE_BAR_HEIGHT = 28
_CELL = 24

_COLOR_BG = (15, 20, 15)
_COLOR_HEAD = (80, 220, 80)
_COLOR_BODY = (40, 150, 40)
_COLOR_SCORE = (220, 220, 220)
_COLOR_GAME_OVER = (220, 60, 60)

_FOOD_COLORS: dict[FoodKind, tuple[int, int, int]] = {
    FoodKind.FROG: (0, 200, 80),
    FoodKind.BIRD: (100, 160, 255),
    FoodKind.MOUSE: (200, 180, 160),
}


class Renderer:
    FPS = 10

    def __init__(self, grid_width: int, grid_height: int) -> None:
        self._gw = grid_width
        self._gh = grid_height
        width = grid_width * _CELL
        height = grid_height * _CELL + _SCORE_BAR_HEIGHT
        self._screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("snAIke")
        self._font = pygame.font.SysFont("monospace", 18)
        self._clock = pygame.time.Clock()

    def draw(self, state: GameState) -> None:
        self._screen.fill(_COLOR_BG)
        self._draw_score(state)
        self._draw_food(state)
        self._draw_snake(state)
        if state.is_over:
            self._draw_game_over(state)
        pygame.display.flip()
        self._clock.tick(self.FPS)

    def _cell_rect(self, x: int, y: int) -> pygame.Rect:
        return pygame.Rect(x * _CELL, _SCORE_BAR_HEIGHT + y * _CELL, _CELL, _CELL)

    def _draw_score(self, state: GameState) -> None:
        text = self._font.render(f"Score: {state.score}", True, _COLOR_SCORE)
        self._screen.blit(text, (8, 5))

    def _draw_snake(self, state: GameState) -> None:
        for i, (x, y) in enumerate(state.snake.segments):
            color = _COLOR_HEAD if i == 0 else _COLOR_BODY
            pygame.draw.rect(self._screen, color, self._cell_rect(x, y))

    def _draw_food(self, state: GameState) -> None:
        if state.food is None:
            return
        x, y = state.food.pos
        color = _FOOD_COLORS[state.food.kind]
        rect = self._cell_rect(x, y)
        cx, cy = rect.centerx, rect.centery
        r = _CELL // 2 - 2

        if state.food.kind == FoodKind.FROG:
            pygame.draw.circle(self._screen, color, (cx, cy), r)
        elif state.food.kind == FoodKind.BIRD:
            points = [(cx, cy - r), (cx + r, cy + r), (cx - r, cy + r)]
            pygame.draw.polygon(self._screen, color, points)
        else:  # MOUSE
            pygame.draw.circle(self._screen, color, (cx, cy), r)
            ear_r = r // 2
            pygame.draw.circle(self._screen, color, (cx - r + 2, cy - r + 2), ear_r)
            pygame.draw.circle(self._screen, color, (cx + r - 2, cy - r + 2), ear_r)

    def _draw_game_over(self, state: GameState) -> None:
        overlay = pygame.Surface(self._screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self._screen.blit(overlay, (0, 0))
        lines = [
            self._font.render("GAME OVER", True, _COLOR_GAME_OVER),
            self._font.render(f"Score: {state.score}", True, _COLOR_SCORE),
            self._font.render("R to restart  |  ESC to quit", True, _COLOR_SCORE),
        ]
        cx = self._screen.get_width() // 2
        cy = self._screen.get_height() // 2 - (len(lines) * 24) // 2
        for i, surf in enumerate(lines):
            self._screen.blit(surf, (cx - surf.get_width() // 2, cy + i * 28))

    def close(self) -> None:
        pygame.quit()


KEY_MAP: dict[int, Direction] = {
    pygame.K_UP: Direction.UP,
    pygame.K_DOWN: Direction.DOWN,
    pygame.K_LEFT: Direction.LEFT,
    pygame.K_RIGHT: Direction.RIGHT,
    pygame.K_w: Direction.UP,
    pygame.K_s: Direction.DOWN,
    pygame.K_a: Direction.LEFT,
    pygame.K_d: Direction.RIGHT,
}


def run_game() -> None:
    pygame.init()
    state = GameState.new()
    renderer = Renderer(GRID_WIDTH, GRID_HEIGHT)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                renderer.close()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    renderer.close()
                    return
                if event.key == pygame.K_r and state.is_over:
                    state = GameState.new()
                elif event.key in KEY_MAP:
                    state.handle_input(KEY_MAP[event.key])

        state.tick()
        renderer.draw(state)
