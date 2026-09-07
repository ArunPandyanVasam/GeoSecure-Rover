import pytest
from rover.rover import Rover
from environment.environment import Environment


def test_rover_moves_east():
    rover = Rover(0, 0, "EAST", 1)
    environment = Environment(10, 10)
    moved = rover.move(environment)
    assert moved is True
    assert rover.status == "MOVING"
    assert rover.x == 1
    assert rover.y == 0


def test_rover_moves_west():
    rover = Rover(1, 0, "WEST", 1)
    environment = Environment(10, 10)
    moved = rover.move(environment)
    assert moved is True
    assert rover.x == 0
    assert rover.y == 0


def test_rover_moves_north():
    rover = Rover(0, 0, "NORTH", 1)
    environment = Environment(10, 10)
    moved = rover.move(environment)
    assert moved is True
    assert rover.y == 1
    assert rover.x == 0


def test_rover_moves_south():
    rover = Rover(0, 1, "SOUTH", 1)
    environment = Environment(10, 10)
    moved = rover.move(environment)
    assert moved is True
    assert rover.y == 0
    assert rover.x == 0


def test_rover_cannot_move_outside_environment():
    rover = Rover(0, 0, "WEST", 1)
    environment = Environment(10, 10)
    moved = rover.move(environment)
    assert moved is False
    assert rover.x == 0
    assert rover.y == 0
    assert rover.status == "STOPPED"


def test_rover_changes_direction():
    rover = Rover(0, 0, "EAST", 1)
    rover.change_direction("NORTH")
    assert rover.direction == "NORTH"


def test_rover_moves_based_on_speed():
    rover = Rover(0, 0, "EAST", 2)
    environment = Environment(10, 10)
    moved = rover.move(environment)
    assert moved is True
    assert rover.x == 2
    assert rover.y == 0


def test_rover_moves_north_based_on_speed():
    rover = Rover(0, 0, "NORTH", 2)
    environment = Environment(10, 10)
    moved = rover.move(environment)
    assert moved is True
    assert rover.y == 2
    assert rover.x == 0


def test_rover_cannot_move_outside_with_speed():
    rover = Rover(8, 0, "EAST", 2)
    environment = Environment(10, 10)
    moved = rover.move(environment)
    assert moved is False
    assert rover.x == 8
    assert rover.y == 0
    assert rover.status == "STOPPED"


def test_rover_initial_status():
    rover = Rover(0, 0, "EAST", 1)
    assert rover.status == "STOPPED"


def test_rover_initial_position():
    rover = Rover(3, 4, "EAST", 1)
    assert rover.x == 3
    assert rover.y == 4


def test_rover_initial_direction():
    rover = Rover(0, 0, "NORTH", 1)
    assert rover.direction == "NORTH"

def test_rover_initial_speed():
    rover = Rover(0, 0, "EAST", 5)
    assert rover.speed == 5


def test_rover_status_after_successful_move():
    rover = Rover(0, 0, "EAST", 1)
    environment = Environment(10, 10)
    rover.move(environment)
    assert rover.status == "MOVING"


def test_rover_status_after_failed_move():
    rover = Rover(0, 0, "WEST", 1)
    environment = Environment(10, 10)
    rover.move(environment)
    assert rover.status == "STOPPED"


def test_rover_position_after_failed_move():
    rover = Rover(0, 0, "WEST", 1)
    environment = Environment(10, 10)
    rover.move(environment)
    assert rover.x == 0
    assert rover.y == 0


def test_rover_moves_after_changing_direction():
    rover = Rover(0, 0, "EAST", 1)
    environment = Environment(10, 10)
    rover.change_direction("NORTH")
    rover.move(environment)
    assert rover.x == 0
    assert rover.y == 1


def test_rover_moves_west_after_changing_direction():
    rover = Rover(2, 0, "EAST", 1)
    environment = Environment(10, 10)
    rover.change_direction("WEST")
    rover.move(environment)
    assert rover.x == 1
    assert rover.y == 0


def test_rover_moves_south_after_changing_direction():
    rover = Rover(0, 2, "EAST", 1)
    environment = Environment(10, 10)
    rover.change_direction("SOUTH")
    rover.move(environment)
    assert rover.x == 0
    assert rover.y == 1


def test_rover_moves_east_after_changing_direction():
    rover = Rover(0, 0, "NORTH", 1)
    environment = Environment(10, 10)
    rover.change_direction("EAST")
    rover.move(environment)
    assert rover.x == 1
    assert rover.y == 0


def test_rover_moves_with_speed_after_changing_direction():
    rover = Rover(0, 0, "EAST", 2)
    environment = Environment(10, 10)
    rover.change_direction("NORTH")
    rover.move(environment)
    assert rover.x == 0
    assert rover.y == 2


def test_rover_failed_move_with_speed():
    rover = Rover(8, 0, "EAST", 2)
    environment = Environment(10, 10)
    rover.move(environment)
    assert rover.x == 8
    assert rover.y == 0


def test_rover_failed_move_keeps_status_stopped():
    rover = Rover(8, 0, "EAST", 2)
    environment = Environment(10, 10)
    rover.move(environment)
    assert rover.status == "STOPPED"


def test_rover_status_after_changing_direction():
    rover = Rover(0, 0, "EAST", 1)
    rover.change_direction("NORTH")
    assert rover.status == "STOPPED"


def test_rover_changes_direction_after_movement():
    rover = Rover(0, 0, "EAST", 1)
    environment = Environment(10, 10)
    rover.move(environment)
    rover.change_direction("NORTH")
    assert rover.direction == "NORTH"


def test_rover_moves_again_after_changing_direction():
    rover = Rover(0, 0, "EAST", 1)
    environment = Environment(10, 10)
    rover.move(environment)
    rover.change_direction("NORTH")
    rover.move(environment)
    assert rover.x == 1
    assert rover.y == 1


def test_rover_multiple_moves_with_speed():
    rover = Rover(0, 0, "EAST", 2)
    environment = Environment(10, 10)
    rover.move(environment)
    rover.move(environment)
    assert rover.x == 4
    assert rover.y == 0


def test_rover_multiple_moves_after_changing_direction():
    rover = Rover(0, 0, "EAST", 2)
    environment = Environment(10, 10)
    rover.change_direction("NORTH")
    rover.move(environment)
    rover.move(environment)
    assert rover.x == 0
    assert rover.y == 4


def test_rover_follows_multi_direction_route():
    rover = Rover(0, 0, "EAST", 2)
    environment = Environment(10, 10)
    rover.move(environment)
    rover.move(environment)
    rover.change_direction("NORTH")
    rover.move(environment)
    assert rover.x == 4
    assert rover.y == 2


def test_rover_stops_when_multi_step_route_is_blocked():
    rover = Rover(6, 0, "EAST", 2)
    environment = Environment(10, 10)
    first_move = rover.move(environment)
    second_move = rover.move(environment)
    assert first_move is True
    assert second_move is False
    assert rover.x == 8
    assert rover.y == 0
    assert rover.status == "STOPPED"


def test_rover_successful_move_returns_true():
    rover = Rover(0, 0, "EAST", 1)
    environment = Environment(10, 10)
    result = rover.move(environment)
    assert result is True


def test_rover_failed_move_returns_false():
    rover = Rover(0, 0, "WEST", 1)
    environment = Environment(10, 10)
    result = rover.move(environment)
    assert result is False


def test_rover_does_not_change_position_with_zero_speed():
    rover = Rover(3, 3, "EAST", 0)
    environment = Environment(10, 10)
    result = rover.move(environment)
    assert result is True
    assert rover.x == 3
    assert rover.y == 3


def test_rover_zero_speed_status():
    rover = Rover(3, 3, "EAST", 0)
    environment = Environment(10, 10)
    rover.move(environment)
    assert rover.status == "MOVING"


def test_rover_can_move_to_boundary_with_speed():
    rover = Rover(7, 0, "EAST", 2)
    environment = Environment(10, 10)
    result = rover.move(environment)
    assert result is True
    assert rover.x == 9
    assert rover.y == 0


def test_rover_can_move_to_minimum_boundary_with_speed():
    rover = Rover(2, 0, "WEST", 2)
    environment = Environment(10, 10)
    result = rover.move(environment)
    assert result is True
    assert rover.x == 0
    assert rover.y == 0


def test_rover_can_move_to_maximum_y_boundary_with_speed():
    rover = Rover(0, 7, "NORTH", 2)
    environment = Environment(10, 10)
    result = rover.move(environment)
    assert result is True
    assert rover.x == 0
    assert rover.y == 9


def test_rover_can_move_to_minimum_y_boundary_with_speed():
    rover = Rover(0, 2, "SOUTH", 2)
    environment = Environment(10, 10)
    result = rover.move(environment)
    assert result is True
    assert rover.x == 0
    assert rover.y == 0


def test_rover_cannot_move_beyond_maximum_y_boundary():
    rover = Rover(0, 8, "NORTH", 2)
    environment = Environment(10, 10)
    result = rover.move(environment)
    assert result is False
    assert rover.x == 0
    assert rover.y == 8
    assert rover.status == "STOPPED"


def test_rover_cannot_move_beyond_minimum_y_boundary():
    rover = Rover(0, 1, "SOUTH", 2)
    environment = Environment(10, 10)
    result = rover.move(environment)
    assert result is False
    assert rover.x == 0
    assert rover.y == 1
    assert rover.status == "STOPPED"


def test_rover_changes_direction_multiple_times():
    rover = Rover(0, 0, "EAST", 1)
    environment = Environment(10, 10)
    rover.move(environment)
    rover.change_direction("NORTH")
    rover.move(environment)
    rover.change_direction("EAST")
    rover.move(environment)
    assert rover.x == 2
    assert rover.y == 1


def test_rover_changes_direction_multiple_times_with_speed():
    rover = Rover(0, 0, "EAST", 2)
    environment = Environment(10, 10)
    rover.move(environment)
    rover.change_direction("NORTH")
    rover.move(environment)
    rover.change_direction("WEST")
    rover.move(environment)
    assert rover.x == 0
    assert rover.y == 2


def test_change_direction_does_not_change_position():
    rover = Rover(4, 5, "EAST", 1)
    rover.change_direction("NORTH")
    assert rover.x == 4
    assert rover.y == 5


def test_change_direction_does_not_change_speed():
    rover = Rover(0, 0, "EAST", 5)
    rover.change_direction("NORTH")
    assert rover.speed == 5


def test_rover_can_change_direction_after_failed_move():
    rover = Rover(0, 0, "WEST", 1)
    environment = Environment(10, 10)
    rover.move(environment)
    rover.change_direction("EAST")
    assert rover.direction == "EAST"


def test_rover_moves_after_recovering_from_failed_move():
    rover = Rover(0, 0, "WEST", 1)
    environment = Environment(10, 10)
    rover.move(environment)
    rover.change_direction("EAST")
    result = rover.move(environment)
    assert result is True
    assert rover.x == 1
    assert rover.y == 0
    assert rover.status == "MOVING"


def test_rover_moves_after_failed_move_with_speed():
    rover = Rover(0, 0, "WEST", 2)
    environment = Environment(10, 10)
    rover.move(environment)
    rover.change_direction("EAST")
    result = rover.move(environment)
    assert result is True
    assert rover.x == 2
    assert rover.y == 0
    assert rover.status == "MOVING"


def test_rover_moves_after_failed_south_move():
    rover = Rover(0, 0, "SOUTH", 1)
    environment = Environment(10, 10)
    rover.move(environment)
    rover.change_direction("NORTH")
    result = rover.move(environment)
    assert result is True
    assert rover.x == 0
    assert rover.y == 1
    assert rover.status == "MOVING"


def test_rover_rejects_invalid_direction():
    with pytest.raises(ValueError):
        Rover(0, 0, "INVALID", 1)


def test_rover_rejects_negative_speed():
    with pytest.raises(ValueError):
        Rover(0, 0, "EAST", -1)


def test_rover_rejects_invalid_direction_change():
    rover = Rover(0, 0, "EAST", 1)

    with pytest.raises(ValueError):
        rover.change_direction("INVALID")


def test_rover_cannot_move_into_obstacle():
    environment = Environment(10, 10)
    environment.add_obstacle(3, 4)
    rover = Rover(2, 4, "EAST", 1)
    moved = rover.move(environment)
    assert moved is False
    assert (rover.x, rover.y) == (2, 4)


def test_rover_can_move_when_no_obstacle():
    environment = Environment(10, 10)
    environment.add_obstacle(5, 5)
    rover = Rover(2, 4, "EAST", 1)
    moved = rover.move(environment)
    assert moved is True
    assert (rover.x, rover.y) == (3, 4)


def test_rover_cannot_move_north_into_obstacle():
    environment = Environment(10, 10)
    environment.add_obstacle(3, 4)
    rover = Rover(3, 3, "NORTH", 1)
    moved = rover.move(environment)
    assert moved is False
    assert (rover.x, rover.y) == (3, 3)


def test_rover_cannot_move_west_into_obstacle():
    environment = Environment(10, 10)
    environment.add_obstacle(3, 4)
    rover = Rover(4, 4, "WEST", 1)
    moved = rover.move(environment)
    assert moved is False
    assert (rover.x, rover.y) == (4, 4)


def test_rover_cannot_move_south_into_obstacle():
    environment = Environment(10, 10)
    environment.add_obstacle(3, 4)
    rover = Rover(3, 5, "SOUTH", 1)
    moved = rover.move(environment)
    assert moved is False
    assert (rover.x, rover.y) == (3, 5)


def test_rover_status_is_stopped_when_blocked_by_obstacle():
    environment = Environment(10, 10)
    environment.add_obstacle(3, 4)
    rover = Rover(2, 4, "EAST", 1)
    rover.move(environment)
    assert rover.status == "STOPPED"