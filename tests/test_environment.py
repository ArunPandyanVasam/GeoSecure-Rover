import pytest
from environment.environment import Environment
from rover.rover import Rover


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


def test_environment_rejects_invalid_width():
    with pytest.raises(ValueError):
        Environment(0, 10)


def test_environment_rejects_invalid_height():
    with pytest.raises(ValueError):
        Environment(10, 0)


def test_environment_rejects_negative_width():
    with pytest.raises(ValueError):
        Environment(-5, 10)


def test_environment_rejects_negative_height():
    with pytest.raises(ValueError):
        Environment(10, -5)


def test_environment_adds_obstacle():
    environment = Environment(10, 10)
    environment.add_obstacle(3, 4)
    assert (3, 4) in environment.obstacles


def test_environment_detects_added_obstacle():
    environment = Environment(10, 10)
    environment.add_obstacle(3, 4)
    assert environment.has_obstacle(3, 4) is True


def test_environment_returns_false_for_free_position():
    environment = Environment(10, 10)
    environment.add_obstacle(3, 4)
    assert environment.has_obstacle(3, 5) is False

def test_environment_allows_obstacle_at_boundary():
    environment = Environment(10, 10)
    environment.add_obstacle(9, 9)
    assert environment.has_obstacle(9, 9) is True


def test_environment_rejects_obstacle_just_outside_boundary():
    environment = Environment(10, 10)
    with pytest.raises(ValueError):
        environment.add_obstacle(10, 9)


def test_environment_does_not_store_duplicate_obstacles():
    environment = Environment(10, 10)
    environment.add_obstacle(3, 4)
    environment.add_obstacle(3, 4)
    assert len(environment.obstacles) == 1


def test_environment_stores_multiple_obstacles():
    environment = Environment(10, 10)
    environment.add_obstacle(2, 3)
    environment.add_obstacle(5, 5)
    environment.add_obstacle(8, 1)
    assert len(environment.obstacles) == 3
    assert environment.has_obstacle(2, 3) is True
    assert environment.has_obstacle(5, 5) is True
    assert environment.has_obstacle(8, 1) is True


def test_environment_displays_free_grid():
    environment = Environment(3, 2)
    expected_grid = [
        [".", ".", "."],
        [".", ".", "."]
    ]
    assert environment.display_grid() == expected_grid


def test_environment_displays_obstacles_in_grid():
    environment = Environment(3, 3)
    environment.add_obstacle(1, 1)
    expected_grid = [
        [".", ".", "."],
        [".", "#", "."],
        [".", ".", "."]
    ]
    assert environment.display_grid() == expected_grid


def test_environment_displays_grid_from_highest_y_to_lowest_y():
    environment = Environment(3, 3)
    environment.add_obstacle(1, 2)
    environment.add_obstacle(1, 0)
    expected_grid = [
        [".", "#", "."],
        [".", ".", "."],
        [".", "#", "."]
    ]
    assert environment.display_grid() == expected_grid


def test_environment_displays_rover():
    environment = Environment(3, 3)
    rover = Rover(1, 1, "EAST", 1)
    expected_grid = [
        [".", ".", "."],
        [".", "R", "."],
        [".", ".", "."]
    ]
    assert environment.display_grid(rover) == expected_grid


def test_environment_displays_rover_and_obstacles():
    environment = Environment(4, 4)
    environment.add_obstacle(0, 0)
    environment.add_obstacle(3, 3)
    rover = Rover(1, 2, "EAST", 1)
    expected_grid = [
        [".", ".", ".", "#"],
        [".", "R", ".", "."],
        [".", ".", ".", "."],
        ["#", ".", ".", "."]
    ]
    assert environment.display_grid(rover) == expected_grid


def test_environment_displays_rover_after_movement():
    environment = Environment(4, 4)
    rover = Rover(1, 1, "EAST", 1)
    rover.move(environment)
    expected_grid = [
        [".", ".", ".", "."],
        [".", ".", ".", "."],
        [".", ".", "R", "."],
        [".", ".", ".", "."]
    ]
    assert environment.display_grid(rover) == expected_grid



def test_environment_displays_rover_when_movement_is_blocked():
    environment = Environment(4, 4)
    environment.add_obstacle(2, 1)
    rover = Rover(1, 1, "EAST", 1)
    moved = rover.move(environment)
    expected_grid = [
        [".", ".", ".", "."],
        [".", ".", ".", "."],
        [".", "R", "#", "."],
        [".", ".", ".", "."]
    ]
    assert moved is False
    assert environment.display_grid(rover) == expected_grid


def test_environment_does_not_display_obstacle_under_rover():
    environment = Environment(3, 3)
    environment.add_obstacle(1, 1)
    rover = Rover(1, 1, "EAST", 1)
    expected_grid = [
        [".", ".", "."],
        [".", "R", "."],
        [".", ".", "."]
    ]
    assert environment.display_grid(rover) == expected_grid


def test_environment_displays_grid_without_rover():
    environment = Environment(3, 3)
    environment.add_obstacle(1, 1)
    expected_grid = [
        [".", ".", "."],
        [".", "#", "."],
        [".", ".", "."]
    ]
    assert environment.display_grid() == expected_grid


def test_position_is_free_when_inside_environment_and_no_obstacle():
    environment = Environment(5, 5)
    assert environment.is_position_free(2, 2) is True


def test_position_is_not_free_when_obstacle_exists():
    environment = Environment(5, 5)
    environment.add_obstacle(2, 2)
    assert environment.is_position_free(2, 2) is False


def test_position_is_not_free_when_outside_environment():
    environment = Environment(5, 5)
    assert environment.is_position_free(-1, 2) is False


def test_position_is_not_free_when_beyond_environment_boundary():
    environment = Environment(5, 5)
    assert environment.is_position_free(5, 2) is False


def test_position_is_not_free_below_environment_boundary():
    environment = Environment(5, 5)
    assert environment.is_position_free(2, -1) is False


def test_position_is_not_free_above_environment_boundary():
    environment = Environment(5, 5)
    assert environment.is_position_free(2, 5) is False


def test_position_is_free_on_environment_boundary():
    environment = Environment(5, 5)
    assert environment.is_position_free(0, 0) is True


def test_position_is_free_at_interior_position():
    environment = Environment(5, 5)
    assert environment.is_position_free(3, 4) is True


def test_position_is_not_free_when_one_of_multiple_obstacles_occupies_position():
    environment = Environment(5, 5)
    environment.add_obstacle(1, 1)
    environment.add_obstacle(2, 2)
    environment.add_obstacle(3, 3)
    assert environment.is_position_free(2, 2) is False