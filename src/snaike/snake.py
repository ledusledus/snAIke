from enum import Enum

Vec2 = tuple[int, int]


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"

    @property
    def opposite(self) -> "Direction":
        return _OPPOSITES[self]

    @property
    def delta(self) -> Vec2:
        return _DELTAS[self]


_OPPOSITES: dict[Direction, Direction] = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}

_DELTAS: dict[Direction, Vec2] = {
    Direction.UP: (0, -1),
    Direction.DOWN: (0, 1),
    Direction.LEFT: (-1, 0),
    Direction.RIGHT: (1, 0),
}


class Snake:
    def __init__(self, start: Vec2, length: int, direction: Direction) -> None:
        dx, dy = direction.delta
        # segments[0] is head; build body extending opposite to movement direction
        self.segments: list[Vec2] = [(start[0] - dx * i, start[1] - dy * i) for i in range(length)]
        self.direction = direction
        self._pending: Direction = direction

    @property
    def head(self) -> Vec2:
        return self.segments[0]

    def set_direction(self, new_dir: Direction) -> None:
        if new_dir != self._pending.opposite:
            self._pending = new_dir

    def next_head(self) -> Vec2:
        dx, dy = self._pending.delta
        return (self.head[0] + dx, self.head[1] + dy)

    def step(self, grow: bool = False) -> None:
        self.direction = self._pending
        self.segments.insert(0, self.next_head())
        if not grow:
            self.segments.pop()

    def occupies(self, pos: Vec2) -> bool:
        return pos in self.segments

    def is_alive(self, grid_width: int, grid_height: int) -> bool:
        x, y = self.head
        if not (0 <= x < grid_width and 0 <= y < grid_height):
            return False
        return self.head not in self.segments[1:]
