import random
from dataclasses import dataclass
from enum import Enum

from snaike.snake import Vec2


class FoodKind(Enum):
    FROG = "frog"
    BIRD = "bird"
    MOUSE = "mouse"


_POINTS: dict[FoodKind, int] = {
    FoodKind.FROG: 1,
    FoodKind.BIRD: 2,
    FoodKind.MOUSE: 3,
}


@dataclass(frozen=True)
class Food:
    pos: Vec2
    kind: FoodKind

    @property
    def points(self) -> int:
        return _POINTS[self.kind]


def spawn_food(
    occupied: set[Vec2],
    grid_width: int,
    grid_height: int,
    rng: random.Random | None = None,
) -> Food | None:
    free = [(x, y) for x in range(grid_width) for y in range(grid_height) if (x, y) not in occupied]
    if not free:
        return None
    r = rng or random.Random()
    pos = r.choice(free)
    kind = r.choice(list(FoodKind))
    return Food(pos=pos, kind=kind)
