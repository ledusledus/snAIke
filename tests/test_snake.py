from snaike.snake import Direction, Snake


def test_direction_deltas():
    assert Direction.UP.delta == (0, -1)
    assert Direction.DOWN.delta == (0, 1)
    assert Direction.LEFT.delta == (-1, 0)
    assert Direction.RIGHT.delta == (1, 0)


def test_direction_deltas_are_unit_vectors():
    for d in Direction:
        dx, dy = d.delta
        assert abs(dx) + abs(dy) == 1


def test_direction_opposites():
    assert Direction.UP.opposite == Direction.DOWN
    assert Direction.DOWN.opposite == Direction.UP
    assert Direction.LEFT.opposite == Direction.RIGHT
    assert Direction.RIGHT.opposite == Direction.LEFT


def test_opposite_is_symmetric():
    for d in Direction:
        assert d.opposite.opposite == d


# --- Snake tests ---


def make_snake(length: int = 3, direction: Direction = Direction.RIGHT) -> Snake:
    return Snake(start=(10, 10), length=length, direction=direction)


def test_snake_initial_segments():
    snake = make_snake(length=3, direction=Direction.RIGHT)
    assert len(snake.segments) == 3
    assert snake.head == (10, 10)
    # body extends opposite to movement direction
    assert snake.segments == [(10, 10), (9, 10), (8, 10)]


def test_snake_step_moves_head():
    snake = make_snake(direction=Direction.RIGHT)
    snake.step()
    assert snake.head == (11, 10)


def test_snake_step_no_grow_keeps_length():
    snake = make_snake(length=3)
    snake.step(grow=False)
    assert len(snake.segments) == 3


def test_snake_step_grow_increases_length():
    snake = make_snake(length=3)
    snake.step(grow=True)
    assert len(snake.segments) == 4


def test_snake_set_direction_valid_turn():
    snake = make_snake(direction=Direction.RIGHT)
    snake.set_direction(Direction.UP)
    snake.step()
    assert snake.head == (10, 9)


def test_snake_set_direction_rejects_reversal():
    snake = make_snake(direction=Direction.RIGHT)
    snake.set_direction(Direction.LEFT)  # 180° reversal — should be ignored
    snake.step()
    assert snake.head == (11, 10)  # still moved right


def test_snake_is_alive_within_grid():
    snake = make_snake()
    assert snake.is_alive(grid_width=30, grid_height=20)


def test_snake_is_alive_hits_left_wall():
    snake = Snake(start=(0, 10), length=1, direction=Direction.LEFT)
    snake.step()
    assert not snake.is_alive(grid_width=30, grid_height=20)


def test_snake_is_alive_hits_top_wall():
    snake = Snake(start=(10, 0), length=1, direction=Direction.UP)
    snake.step()
    assert not snake.is_alive(grid_width=30, grid_height=20)


def test_snake_is_alive_hits_right_wall():
    snake = Snake(start=(29, 10), length=1, direction=Direction.RIGHT)
    snake.step()
    assert not snake.is_alive(grid_width=30, grid_height=20)


def test_snake_is_alive_hits_bottom_wall():
    snake = Snake(start=(10, 19), length=1, direction=Direction.DOWN)
    snake.step()
    assert not snake.is_alive(grid_width=30, grid_height=20)


def test_snake_self_collision():
    # Build a snake that will collide with itself
    snake = Snake(start=(5, 5), length=4, direction=Direction.RIGHT)
    # Turn it into a U shape: right, down, left — head will meet body
    snake.set_direction(Direction.DOWN)
    snake.step(grow=True)
    snake.set_direction(Direction.LEFT)
    snake.step(grow=True)
    snake.set_direction(Direction.UP)
    snake.step(grow=True)
    # head is now back at (5, 5) which is in the body
    assert not snake.is_alive(grid_width=30, grid_height=20)


def test_snake_occupies():
    snake = Snake(start=(5, 5), length=3, direction=Direction.RIGHT)
    assert snake.occupies((5, 5))
    assert snake.occupies((4, 5))
    assert snake.occupies((3, 5))
    assert not snake.occupies((6, 5))
