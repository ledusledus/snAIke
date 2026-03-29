import random

from snaike.food import FoodKind
from snaike.game import GRID_HEIGHT, GRID_WIDTH, HUNGER_TICKS, GameState
from snaike.snake import Direction, Snake


def make_state(rng_seed: int = 0) -> GameState:
    return GameState.new(rng=random.Random(rng_seed))


def test_initial_state():
    state = make_state()
    assert state.score == 0
    assert state.ticks == 0
    assert not state.is_over
    assert state.food is not None
    assert state.snake.is_alive(GRID_WIDTH, GRID_HEIGHT)


def test_tick_advances_ticks():
    state = make_state()
    state.tick()
    assert state.ticks == 1


def test_tick_no_eat_keeps_score():
    state = make_state()
    # Point food somewhere the snake won't reach on first tick
    from snaike.food import Food

    state.food = Food(pos=(0, 0), kind=FoodKind.FROG)
    state.tick()
    assert state.score == 0


def test_tick_eat_increases_score():
    state = make_state()
    from snaike.food import Food

    # Place food directly in front of the snake's head
    next_head = state.snake.next_head()
    state.food = Food(pos=next_head, kind=FoodKind.MOUSE)
    state.tick()
    assert state.score == 3


def test_tick_eat_grows_snake():
    state = make_state()
    from snaike.food import Food

    initial_length = len(state.snake.segments)
    next_head = state.snake.next_head()
    state.food = Food(pos=next_head, kind=FoodKind.FROG)
    state.tick()
    assert len(state.snake.segments) == initial_length + 1


def test_tick_eat_spawns_new_food():
    state = make_state()
    from snaike.food import Food

    next_head = state.snake.next_head()
    old_food = Food(pos=next_head, kind=FoodKind.FROG)
    state.food = old_food
    state.tick(rng=random.Random(1))
    assert state.food is not None
    assert state.food.pos != next_head


def test_tick_eat_resets_hunger():
    state = make_state()
    from snaike.food import Food

    state.ticks_since_eat = 10
    next_head = state.snake.next_head()
    state.food = Food(pos=next_head, kind=FoodKind.FROG)
    state.tick()
    assert state.ticks_since_eat == 0


def test_hunger_shrinks_snake(monkeypatch):
    import snaike.game as game_module

    monkeypatch.setattr(game_module, "HUNGER_TICKS", 5)
    state = make_state()
    from snaike.food import Food

    state.food = Food(pos=(0, 0), kind=FoodKind.FROG)
    state.snake = Snake(start=(10, 10), length=5, direction=Direction.RIGHT)
    initial_length = len(state.snake.segments)
    for _ in range(5):
        state.tick()
    assert len(state.snake.segments) == initial_length - 1


def test_hunger_does_not_shrink_below_one():
    state = make_state()
    from snaike.food import Food

    state.food = Food(pos=(0, 0), kind=FoodKind.FROG)
    state.snake = Snake(start=(15, 10), length=1, direction=Direction.RIGHT)
    for _ in range(HUNGER_TICKS * 3):
        if state.is_over:
            break
        state.tick()
    assert len(state.snake.segments) >= 1


def test_wall_collision_ends_game():
    state = make_state()
    state.snake = Snake(start=(GRID_WIDTH - 1, 10), length=1, direction=Direction.RIGHT)
    state.tick()
    assert state.is_over


def test_self_collision_ends_game():
    state = make_state()
    # Build a snake that will collide with itself
    state.snake = Snake(start=(5, 5), length=4, direction=Direction.RIGHT)
    state.snake.set_direction(Direction.DOWN)
    state.snake.step(grow=True)
    state.snake.set_direction(Direction.LEFT)
    state.snake.step(grow=True)
    state.snake.set_direction(Direction.UP)
    state.tick()
    assert state.is_over


def test_tick_does_nothing_when_over():
    state = make_state()
    state.is_over = True
    state.tick()
    assert state.ticks == 0


def test_handle_input_delegates_direction():
    state = make_state()
    state.handle_input(Direction.UP)
    state.tick()
    x, y = state.snake.head
    # After turning up from initial position, y should decrease
    assert y < GRID_HEIGHT // 2
