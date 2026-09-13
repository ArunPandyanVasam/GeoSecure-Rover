import pytest

from navigation.navigation import Navigation
from rover.rover import Rover
from environment.environment import Environment
from mission.mission import Mission


def test_navigation_moves_east_toward_destination():
    navigation = Navigation()
    environment = Environment(10, 10)

    assert navigation.choose_direction(
        (0, 0),
        (5, 0),
        environment
    ) == "EAST"


def test_navigation_moves_west_toward_destination():
    navigation = Navigation()
    environment = Environment(10, 10)

    assert navigation.choose_direction(
        (5, 0),
        (0, 0),
        environment
    ) == "WEST"


def test_navigation_moves_north_toward_destination():
    navigation = Navigation()
    environment = Environment(10, 10)

    assert navigation.choose_direction(
        (0, 0),
        (0, 5),
        environment
    ) == "NORTH"


def test_navigation_moves_south_toward_destination():
    navigation = Navigation()
    environment = Environment(10, 10)

    assert navigation.choose_direction(
        (0, 5),
        (0, 0),
        environment
    ) == "SOUTH"


def test_navigation_returns_none_when_destination_reached():
    navigation = Navigation()
    environment = Environment(10, 10)

    assert navigation.choose_direction(
        (5, 5),
        (5, 5),
        environment
    ) is None


def test_navigation_rejects_invalid_position():
    navigation = Navigation()
    environment = Environment(10, 10)

    with pytest.raises(ValueError):
        navigation.choose_direction(
            None,
            (5, 5),
            environment
        )


def test_navigation_rejects_invalid_destination():
    navigation = Navigation()
    environment = Environment(10, 10)

    with pytest.raises(ValueError):
        navigation.choose_direction(
            (0, 0),
            None,
            environment
        )


def test_navigation_and_rover_reach_destination():
    environment = Environment(10, 10)
    navigation = Navigation()
    mission = Mission((0, 0), (5, 5))
    rover = Rover(0, 0, "WEST", 1)

    while not mission.is_destination_reached((rover.x, rover.y)):
        direction = navigation.choose_direction(
            (rover.x, rover.y),
            mission.destination,
            environment
        )

        rover.change_direction(direction)

        moved = rover.move(environment)

        if not moved:
            break

    assert (rover.x, rover.y) == mission.destination


def test_navigation_can_choose_alternative_when_east_is_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 1)

    current_position = (1, 1)
    destination = (4, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "NORTH"


def test_navigation_calculates_next_position_for_east():
    navigation = Navigation()

    next_position = navigation.calculate_next_position(
        (1, 1),
        "EAST"
    )

    assert next_position == (2, 1)


def test_navigation_calculates_next_position_for_west():
    navigation = Navigation()

    next_position = navigation.calculate_next_position(
        (1, 1),
        "WEST"
    )

    assert next_position == (0, 1)


def test_navigation_calculates_next_position_for_north():
    navigation = Navigation()

    next_position = navigation.calculate_next_position(
        (1, 1),
        "NORTH"
    )

    assert next_position == (1, 2)


def test_navigation_calculates_next_position_for_south():
    navigation = Navigation()

    next_position = navigation.calculate_next_position(
        (1, 1),
        "SOUTH"
    )

    assert next_position == (1, 0)


def test_navigation_rejects_invalid_direction_when_calculating_next_position():
    navigation = Navigation()

    with pytest.raises(ValueError, match="Invalid direction"):
        navigation.calculate_next_position(
            (1, 1),
            "INVALID"
        )


def test_navigation_chooses_north_only_when_north_is_free():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 1)

    current_position = (1, 1)
    destination = (4, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    next_position = navigation.calculate_next_position(
        current_position,
        direction
    )

    assert direction == "NORTH"
    assert environment.is_position_free(*next_position) is True


def test_navigation_does_not_choose_blocked_north_as_alternative():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 1)  # EAST
    environment.add_obstacle(1, 2)  # NORTH

    current_position = (1, 1)
    destination = (4, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction != "NORTH"


def test_navigation_can_choose_south_when_east_and_north_are_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 1)  # EAST
    environment.add_obstacle(1, 2)  # NORTH

    current_position = (1, 1)
    destination = (4, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "SOUTH"


def test_navigation_can_choose_west_when_west_is_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(1, 1)  # WEST

    current_position = (2, 1)
    destination = (0, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "NORTH"


def test_navigation_can_choose_south_when_west_is_blocked_and_north_is_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(1, 1)  # WEST
    environment.add_obstacle(2, 2)  # NORTH

    current_position = (2, 1)
    destination = (0, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "SOUTH"


def test_navigation_chooses_east_when_west_north_and_south_are_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(1, 1)  # WEST
    environment.add_obstacle(2, 2)  # NORTH
    environment.add_obstacle(2, 0)  # SOUTH

    current_position = (2, 1)
    destination = (0, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "EAST"


def test_navigation_can_choose_south_when_east_is_blocked_and_north_is_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 1)  # EAST
    environment.add_obstacle(1, 2)  # NORTH

    current_position = (1, 1)
    destination = (4, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "SOUTH"


def test_navigation_prefers_east_when_east_is_free():
    environment = Environment(5, 5)
    navigation = Navigation()

    current_position = (1, 1)
    destination = (4, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "EAST"


def test_navigation_prefers_west_when_west_is_free():
    environment = Environment(5, 5)
    navigation = Navigation()

    current_position = (3, 1)
    destination = (0, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "WEST"


def test_navigation_chooses_north_when_destination_is_north():
    environment = Environment(5, 5)
    navigation = Navigation()

    current_position = (2, 1)
    destination = (2, 4)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "NORTH"


def test_navigation_chooses_south_when_destination_is_south():
    environment = Environment(5, 5)
    navigation = Navigation()

    current_position = (2, 4)
    destination = (2, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "SOUTH"


def test_navigation_chooses_east_when_south_is_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 0)

    current_position = (2, 1)
    destination = (2, 0)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "EAST"


def test_navigation_prefers_south_when_south_is_free():
    environment = Environment(5, 5)
    navigation = Navigation()

    current_position = (2, 3)
    destination = (2, 0)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "SOUTH"


def test_navigation_chooses_east_when_north_is_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 2)

    current_position = (2, 1)
    destination = (2, 4)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "EAST"

def test_navigation_north_choice_leads_to_free_position():
    environment = Environment(5, 5)
    navigation = Navigation()

    current_position = (2, 1)
    destination = (2, 4)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    next_position = navigation.calculate_next_position(
        current_position,
        direction
    )

    assert direction == "NORTH"
    assert environment.is_position_free(*next_position) is True


def test_navigation_south_alternative_leads_to_free_position():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 1)  # EAST
    environment.add_obstacle(1, 2)  # NORTH

    current_position = (1, 1)
    destination = (4, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    next_position = navigation.calculate_next_position(
        current_position,
        direction
    )

    assert direction == "SOUTH"
    assert environment.is_position_free(*next_position) is True


def test_navigation_north_alternative_leads_to_free_position():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(1, 1)  # WEST

    current_position = (2, 1)
    destination = (0, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    next_position = navigation.calculate_next_position(
        current_position,
        direction
    )

    assert direction == "NORTH"
    assert environment.is_position_free(*next_position) is True


def test_navigation_chooses_west_when_east_north_and_south_are_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 1)  # EAST
    environment.add_obstacle(1, 2)  # NORTH
    environment.add_obstacle(1, 0)  # SOUTH

    current_position = (1, 1)
    destination = (4, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "WEST"


def test_navigation_can_choose_west_when_east_north_and_south_are_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 1)  # EAST
    environment.add_obstacle(1, 2)  # NORTH
    environment.add_obstacle(1, 0)  # SOUTH

    current_position = (1, 1)
    destination = (4, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "WEST"


def test_navigation_can_choose_east_when_west_north_and_south_are_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(1, 1)  # WEST
    environment.add_obstacle(2, 2)  # NORTH
    environment.add_obstacle(2, 0)  # SOUTH

    current_position = (2, 1)
    destination = (0, 1)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "EAST"


def test_navigation_creates_east_first_direction_priority():
    navigation = Navigation()

    priority = navigation.get_direction_priority(
        (1, 1),
        (4, 1)
    )

    assert priority == [
        "EAST",
        "NORTH",
        "SOUTH",
        "WEST"
    ]


def test_navigation_creates_west_first_direction_priority():
    navigation = Navigation()

    priority = navigation.get_direction_priority(
        (4, 1),
        (1, 1)
    )

    assert priority == [
        "WEST",
        "NORTH",
        "SOUTH",
        "EAST"
    ]


def test_navigation_creates_north_first_direction_priority():
    navigation = Navigation()

    priority = navigation.get_direction_priority(
        (1, 1),
        (1, 4)
    )

    assert priority == [
        "NORTH",
        "EAST",
        "WEST",
        "SOUTH"
    ]


def test_navigation_creates_south_first_direction_priority():
    navigation = Navigation()

    priority = navigation.get_direction_priority(
        (1, 4),
        (1, 1)
    )

    assert priority == [
        "SOUTH",
        "EAST",
        "WEST",
        "NORTH"
    ]


def test_navigation_uses_direction_priority_when_east_is_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 1)

    direction = navigation.choose_direction(
        (1, 1),
        (4, 1),
        environment
    )

    assert direction == "NORTH"


def test_navigation_uses_west_when_east_north_and_south_are_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 1)  # EAST
    environment.add_obstacle(1, 2)  # NORTH
    environment.add_obstacle(1, 0)  # SOUTH

    direction = navigation.choose_direction(
        (1, 1),
        (4, 1),
        environment
    )

    assert direction == "WEST"


def test_navigation_uses_east_when_west_north_and_south_are_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(1, 1)  # WEST
    environment.add_obstacle(2, 2)  # NORTH
    environment.add_obstacle(2, 0)  # SOUTH

    direction = navigation.choose_direction(
        (2, 1),
        (0, 1),
        environment
    )

    assert direction == "EAST"


def test_navigation_returns_none_when_all_directions_are_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 1)  # EAST
    environment.add_obstacle(0, 1)  # WEST
    environment.add_obstacle(1, 2)  # NORTH
    environment.add_obstacle(1, 0)  # SOUTH

    direction = navigation.choose_direction(
        (1, 1),
        (4, 1),
        environment
    )

    assert direction is None


def test_navigation_does_not_choose_direction_outside_environment():
    environment = Environment(5, 5)
    navigation = Navigation()

    direction = navigation.choose_direction(
        (0, 1),
        (-2, 1),
        environment
    )

    assert direction != "WEST"


def test_navigation_chooses_valid_fallback_at_boundary():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(1, 1)  # EAST

    direction = navigation.choose_direction(
        (0, 1),
        (4, 1),
        environment
    )

    assert direction == "NORTH"


def test_navigation_chooses_alternative_when_direct_path_is_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 2)

    current_position = (1, 2)
    destination = (4, 2)

    direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    assert direction == "NORTH"


def test_rover_moves_in_alternative_direction_when_direct_path_is_blocked():
    environment = Environment(5, 5)
    navigation = Navigation()
    rover = Rover(1, 2, "EAST", 1)

    environment.add_obstacle(2, 2)

    direction = navigation.choose_direction(
        (rover.x, rover.y),
        (4, 2),
        environment
    )

    rover.change_direction(direction)

    moved = rover.move(environment)

    assert moved is True
    assert (rover.x, rover.y) == (1, 3)


def test_navigation_reassesses_after_alternative_movement():
    environment = Environment(5, 5)
    navigation = Navigation()
    rover = Rover(1, 2, "EAST", 1)

    environment.add_obstacle(2, 2)
    environment.add_obstacle(2, 3)

    # First decision: EAST is blocked, so choose NORTH.
    direction = navigation.choose_direction(
        (rover.x, rover.y),
        (4, 2),
        environment
    )

    rover.change_direction(direction)
    moved = rover.move(environment)

    assert moved is True
    assert (rover.x, rover.y) == (1, 3)

    # Second decision: EAST is still blocked, so Navigation must reassess.
    direction = navigation.choose_direction(
        (rover.x, rover.y),
        (4, 2),
        environment
    )

    assert direction != "EAST"


def test_navigation_multiple_avoidance_decisions_choose_free_positions():
    environment = Environment(5, 5)
    navigation = Navigation()

    environment.add_obstacle(2, 2)
    environment.add_obstacle(2, 3)
    environment.add_obstacle(2, 1)

    current_position = (1, 2)
    destination = (4, 2)

    first_direction = navigation.choose_direction(
        current_position,
        destination,
        environment
    )

    first_position = navigation.calculate_next_position(
        current_position,
        first_direction
    )

    assert environment.is_position_free(*first_position)

    second_direction = navigation.choose_direction(
        first_position,
        destination,
        environment
    )

    second_position = navigation.calculate_next_position(
        first_position,
        second_direction
    )

    assert environment.is_position_free(*second_position)