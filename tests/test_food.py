import random

from snaike.food import Food, FoodKind, spawn_food


def test_food_points():
    assert Food(pos=(0, 0), kind=FoodKind.FROG).points == 1
    assert Food(pos=(0, 0), kind=FoodKind.BIRD).points == 2
    assert Food(pos=(0, 0), kind=FoodKind.MOUSE).points == 3


def test_food_is_immutable():
    food = Food(pos=(1, 2), kind=FoodKind.FROG)
    try:
        food.pos = (3, 4)  # type: ignore[misc]
        assert False, "should have raised"
    except Exception:
        pass


def test_spawn_food_within_grid():
    rng = random.Random(42)
    food = spawn_food(occupied=set(), grid_width=10, grid_height=10, rng=rng)
    assert food is not None
    x, y = food.pos
    assert 0 <= x < 10
    assert 0 <= y < 10


def test_spawn_food_not_in_occupied():
    occupied = {(x, y) for x in range(10) for y in range(10) if not (x == 5 and y == 5)}
    rng = random.Random(0)
    food = spawn_food(occupied=occupied, grid_width=10, grid_height=10, rng=rng)
    assert food is not None
    assert food.pos == (5, 5)


def test_spawn_food_returns_none_when_full():
    occupied = {(x, y) for x in range(5) for y in range(5)}
    food = spawn_food(occupied=occupied, grid_width=5, grid_height=5)
    assert food is None


def test_spawn_food_produces_all_kinds():
    rng = random.Random(0)
    kinds = {
        spawn_food(occupied=set(), grid_width=20, grid_height=20, rng=rng).kind  # type: ignore[union-attr]
        for _ in range(100)
    }
    assert kinds == set(FoodKind)
