import pytest

pygame = pytest.importorskip("pygame")


@pytest.fixture(autouse=True)
def headless(monkeypatch):
    monkeypatch.setenv("SDL_VIDEODRIVER", "dummy")
    monkeypatch.setenv("SDL_AUDIODRIVER", "dummy")


def test_renderer_importable():
    from snaike.game import Renderer  # noqa: F401


def test_renderer_init_and_close():
    import pygame as pg

    pg.init()
    from snaike.game import Renderer

    r = Renderer(grid_width=30, grid_height=20)
    r.close()


def test_renderer_draw_does_not_crash():
    import pygame as pg

    pg.init()
    from snaike.game import GameState, Renderer

    state = GameState.new()
    r = Renderer(grid_width=30, grid_height=20)
    r.draw(state)
    r.close()


def test_renderer_draw_game_over_does_not_crash():
    import pygame as pg

    pg.init()
    from snaike.game import GameState, Renderer

    state = GameState.new()
    state.is_over = True
    r = Renderer(grid_width=30, grid_height=20)
    r.draw(state)
    r.close()
