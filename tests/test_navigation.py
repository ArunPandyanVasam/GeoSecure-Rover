import pytest
from navigation.navigation import Navigation
from rover.rover import Rover
from environment.environment import Environment
from mission.mission import Mission


def test_navigation_moves_east_toward_destination():
    navigation = Navigation()
    assert navigation.choose_direction((0, 0), (5, 0)) == "EAST"


def test_navigation_moves_west_toward_destination():
    navigation = Navigation()
    assert navigation.choose_direction((5, 0), (0, 0)) == "WEST"


def test_navigation_moves_north_toward_destination():
    navigation = Navigation()
    assert navigation.choose_direction((0, 0), (0, 5)) == "NORTH"


def test_navigation_moves_south_toward_destination():
    navigation = Navigation()
    assert navigation.choose_direction((0, 5), (0, 0)) == "SOUTH"


def test_navigation_returns_none_when_destination_reached():
    navigation = Navigation()
    assert navigation.choose_direction((5, 5), (5, 5)) is None


def test_navigation_rejects_invalid_position():
    navigation = Navigation()
    with pytest.raises(ValueError):
        navigation.choose_direction(None, (5, 5))


def test_navigation_rejects_invalid_destination():
    navigation = Navigation()
    with pytest.raises(ValueError):
        navigation.choose_direction((0, 0), None)


def test_navigation_and_rover_reach_destination():
    environment = Environment(10, 10)
    navigation = Navigation()
    mission = Mission((0, 0), (5, 5))
    rover = Rover(0, 0, "WEST", 1)
    while not mission.is_destination_reached((rover.x, rover.y)):
        direction = navigation.choose_direction(
            (rover.x, rover.y),
            mission.destination
        )
        rover.change_direction(direction)
        moved = rover.move(environment)
        if not moved:
            break
    assert (rover.x, rover.y) == mission.destination