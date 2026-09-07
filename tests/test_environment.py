import pytest
from environment.environment import Environment


def test_position_inside_environment():
    environment = Environment(10, 10)
    assert environment.is_within_bounds(5, 5) is True


def test_position_at_boundary():
    environment = Environment(10, 10)
    assert environment.is_within_bounds(9, 9) is True


def test_position_outside_environment():
    environment = Environment(10, 10)
    assert environment.is_within_bounds(10, 10) is False


def test_negative_position():
    environment = Environment(10, 10)
    assert environment.is_within_bounds(-1, 5) is False


def test_position_above_environment():
    environment = Environment(10, 10)
    assert environment.is_within_bounds(5, 10) is False


def test_environment_detects_obstacle():
    environment = Environment(10, 10)
    environment.add_obstacle(3, 4)
    assert environment.has_obstacle(3, 4) is True


def test_environment_returns_false_when_no_obstacle_exists():
    environment = Environment(10, 10)
    assert environment.has_obstacle(3, 4) is False


def test_environment_rejects_obstacle_outside_bounds():
    environment = Environment(10, 10)
    with pytest.raises(ValueError):
        environment.add_obstacle(10, 10)