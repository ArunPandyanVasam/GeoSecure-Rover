from mission.mission import Mission
from environment.environment import Environment


def test_mission_destination_reached():
    mission = Mission((0, 0), (5, 5))
    assert mission.is_destination_reached((5, 5)) is True


def test_mission_destination_not_reached():
    mission = Mission((0, 0), (5, 5))
    assert mission.is_destination_reached((4, 5)) is False


def test_mission_stores_start_position():
    mission = Mission((0, 0), (5, 5))
    assert mission.start_position == (0, 0)


def test_mission_stores_destination():
    mission = Mission((0, 0), (5, 5))
    assert mission.destination == (5, 5)


def test_mission_is_valid():
    environment = Environment(10, 10)
    mission = Mission((0, 0), (5, 5))
    assert mission.is_valid(environment) is True


def test_mission_is_invalid():
    environment = Environment(10, 10)
    mission = Mission((0, 0), (10, 10))
    assert mission.is_valid(environment) is False