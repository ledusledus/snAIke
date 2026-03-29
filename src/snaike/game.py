import random
from dataclasses import dataclass

from snaike.food import Food, spawn_food
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
