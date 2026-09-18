from rover.rover import Rover
from environment.environment import Environment
from mission.mission import Mission
from mission.mission_runner import run_mission
from navigation.navigation import Navigation
from mission.mission_result import MissionFailureReason


def test_run_mission_reaches_destination():
    environment = Environment(10, 10)
    mission = Mission((0, 0), (5, 5))
    navigation = Navigation()
    rover = Rover(0, 0, "WEST", 1)
    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.final_position == (5, 5)
    assert result.mission_completed is True
    assert result.failure_reason is None


def test_run_mission_when_already_at_destination():
    environment = Environment(10, 10)
    mission = Mission((5, 5), (5, 5))
    navigation = Navigation()
    rover = Rover(5, 5, "EAST", 1)
    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.final_position == (5, 5)
    assert result.mission_completed is True
    assert result.failure_reason is None


def test_run_mission_navigates_around_obstacle():
    environment = Environment(5, 5)
    mission = Mission((0, 2), (4, 2))
    navigation = Navigation()
    rover = Rover(0, 2, "EAST", 1)

    environment.add_obstacle(2, 2)

    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.final_position == (4, 2)
    assert result.mission_completed is True
    assert result.failure_reason is None


def test_navigation_path_never_enters_obstacle():
    environment = Environment(5, 5)
    mission = Mission((0, 2), (4, 2))
    navigation = Navigation()
    rover = Rover(0, 2, "EAST", 1)

    environment.add_obstacle(2, 2)

    positions = [(rover.x, rover.y)]

    while not mission.is_destination_reached((rover.x, rover.y)):
        direction = navigation.choose_direction(
            (rover.x, rover.y),
            mission.destination,
            environment
        )

        rover.change_direction(direction)
        rover.move(environment)

        positions.append((rover.x, rover.y))

        if len(positions) > 25:
            break

    assert (4, 2) in positions
    assert (2, 2) not in positions


def test_run_mission_navigates_around_multiple_obstacles():
    environment = Environment(5, 5)
    mission = Mission((0, 2), (4, 2))
    navigation = Navigation()
    rover = Rover(0, 2, "EAST", 1)

    environment.add_obstacle(2, 1)
    environment.add_obstacle(2, 2)
    environment.add_obstacle(2, 3)

    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.final_position == (4, 2)
    assert result.mission_completed is True
    assert result.failure_reason is None


def test_run_mission_stops_when_destination_is_unreachable():
    environment = Environment(3, 3)
    mission = Mission((1, 1), (2, 2))
    navigation = Navigation()
    rover = Rover(1, 1, "EAST", 1)

    environment.add_obstacle(0, 1)
    environment.add_obstacle(2, 1)
    environment.add_obstacle(1, 0)
    environment.add_obstacle(1, 2)

    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.final_position == (1, 1)
    assert result.mission_completed is False
    assert result.failure_reason == MissionFailureReason.DESTINATION_UNREACHABLE


def test_unreachable_mission_keeps_rover_in_place():
    environment = Environment(3, 3)
    mission = Mission((1, 1), (2, 1))
    navigation = Navigation()
    rover = Rover(1, 1, "EAST", 1)

    environment.add_obstacle(0, 1)
    environment.add_obstacle(2, 1)
    environment.add_obstacle(1, 0)
    environment.add_obstacle(1, 2)

    run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert (rover.x, rover.y) == (1, 1)


def test_run_mission_accepts_max_steps():
    environment = Environment(5, 5)
    mission = Mission((0, 0), (4, 4))
    navigation = Navigation()
    rover = Rover(0, 0, "EAST", 1)

    result = run_mission(
        rover,
        mission,
        navigation,
        environment,
        max_steps=10
    )

    assert result.final_position == (4, 4)
    assert result.mission_completed is True
    assert result.failure_reason is None


def test_run_mission_stops_after_max_steps():
    environment = Environment(5, 5)
    mission = Mission((0, 0), (4, 4))
    navigation = Navigation()
    rover = Rover(0, 0, "EAST", 1)

    result = run_mission(
        rover,
        mission,
        navigation,
        environment,
        max_steps=3
    )

    assert result.final_position != (4, 4)
    assert result.mission_completed is False
    assert result.failure_reason == MissionFailureReason.MAX_STEPS_REACHED


def test_run_mission_detects_repeated_position():
    class LoopingNavigation:
        def __init__(self):
            self.directions = ["EAST", "WEST"]
            self.index = 0
            self.calls = 0

        def choose_direction(self, position, destination, environment):
            self.calls += 1
            direction = self.directions[self.index]
            self.index = (self.index + 1) % len(self.directions)
            return direction

    environment = Environment(3, 3)
    mission = Mission((0, 0), (2, 2))
    navigation = LoopingNavigation()
    rover = Rover(0, 0, "EAST", 1)

    result = run_mission(
        rover,
        mission,
        navigation,
        environment,
        max_steps=100
    )

    assert result.final_position == (0, 0)
    assert result.mission_completed is False
    assert result.failure_reason == MissionFailureReason.REPEATED_POSITION
    assert navigation.calls < 100


def test_run_mission_rejects_invalid_mission():
    environment = Environment(5, 5)
    mission = Mission((2, 2), (4, 4))
    navigation = Navigation()
    rover = Rover(2, 2, "EAST", 1)

    environment.add_obstacle(2, 2)

    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.final_position == (2, 2)
    assert result.mission_completed is False
    assert result.failure_reason == MissionFailureReason.INVALID_MISSION


def test_run_mission_rejects_invalid_destination():
    environment = Environment(5, 5)
    mission = Mission((0, 0), (4, 4))
    navigation = Navigation()
    rover = Rover(0, 0, "EAST", 1)

    environment.add_obstacle(4, 4)

    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.final_position == (0, 0)
    assert result.mission_completed is False
    assert result.failure_reason == MissionFailureReason.INVALID_MISSION


def test_run_mission_stops_when_rover_movement_is_blocked():
    environment = Environment(3, 1)
    mission = Mission((0, 0), (2, 0))
    rover = Rover(0, 0, "EAST", 1)

    environment.add_obstacle(1, 0)

    class BlockedNavigation:
        def choose_direction(self, position, destination, environment):
            return "EAST"

    navigation = BlockedNavigation()

    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.final_position == (0, 0)
    assert result.mission_completed is False
    assert result.failure_reason == MissionFailureReason.MOVEMENT_BLOCKED
