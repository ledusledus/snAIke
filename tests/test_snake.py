from snaike.snake import Direction


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
