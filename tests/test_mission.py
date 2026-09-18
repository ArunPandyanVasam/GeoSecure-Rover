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


def test_mission_is_invalid_when_start_is_obstacle():
    environment = Environment(5, 5)
    mission = Mission((2, 2), (4, 4))

    environment.add_obstacle(2, 2)

    assert mission.is_valid(environment) is False


def test_mission_is_invalid_when_destination_is_obstacle():
    environment = Environment(5, 5)
    mission = Mission((0, 0), (2, 2))

    environment.add_obstacle(2, 2)

    assert mission.is_valid(environment) is False


def test_mission_is_valid_when_start_and_destination_are_free():
    environment = Environment(5, 5)
    mission = Mission((0, 0), (4, 4))

    environment.add_obstacle(2, 2)

    assert mission.is_valid(environment) is True


def test_mission_is_invalid_when_start_is_outside_environment():
    environment = Environment(5, 5)
    mission = Mission((-1, 0), (4, 4))

    environment.add_obstacle(2, 2)

    assert mission.is_valid(environment) is False


def test_mission_is_invalid_when_destination_is_outside_environment():
    environment = Environment(5, 5)
    mission = Mission((0, 0), (5, 4))

    environment.add_obstacle(2, 2)

    assert mission.is_valid(environment) is False


def test_mission_is_invalid_when_start_and_destination_are_obstacles():
    environment = Environment(5, 5)
    mission = Mission((1, 1), (3, 3))

    environment.add_obstacle(1, 1)
    environment.add_obstacle(3, 3)

    assert mission.is_valid(environment) is False
