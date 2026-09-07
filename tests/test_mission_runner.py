from rover.rover import Rover
from environment.environment import Environment
from mission.mission import Mission
from mission.mission_runner import run_mission
from navigation.navigation import Navigation


def test_run_mission_reaches_destination():
    environment = Environment(10, 10)
    mission = Mission((0, 0), (5, 5))
    navigation = Navigation()
    rover = Rover(0, 0, "WEST", 1)
    final_x, final_y, mission_completed = run_mission(
        rover,
        mission,
        navigation,
        environment
    )
    assert (final_x, final_y) == (5, 5)
    assert mission_completed is True


def test_run_mission_when_already_at_destination():
    environment = Environment(10, 10)
    mission = Mission((5, 5), (5, 5))
    navigation = Navigation()
    rover = Rover(5, 5, "EAST", 1)
    final_x, final_y, mission_completed = run_mission(
        rover,
        mission,
        navigation,
        environment
    )
    assert (final_x, final_y) == (5, 5)
    assert mission_completed is True