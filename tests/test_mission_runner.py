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


def test_successful_mission_records_completion_event():
    from mission.mission_status_event import MissionStatusEvent

    environment = Environment(5, 5)
    mission = Mission((0, 0), (2, 0))
    rover = Rover(0, 0, "EAST", 1)
    navigation = Navigation()

    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.mission_completed is True
    assert isinstance(result.events[-1], MissionStatusEvent)
    assert result.events[-1].step == 2
    assert result.events[-1].status == "COMPLETED"
    assert result.events[-1].reason is None


def test_blocked_movement_records_failure_event():
    from mission.mission_status_event import MissionStatusEvent

    class BlockedNavigation:
        def choose_direction(self, current_position, destination, environment):
            return "EAST"

    environment = Environment(3, 1)
    environment.add_obstacle(1, 0)

    mission = Mission((0, 0), (2, 0))
    rover = Rover(0, 0, "EAST", 1)
    navigation = BlockedNavigation()

    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.mission_completed is False
    assert result.failure_reason == MissionFailureReason.MOVEMENT_BLOCKED
    assert isinstance(result.events[-1], MissionStatusEvent)
    assert result.events[-1].status == "FAILED"
    assert result.events[-1].reason == MissionFailureReason.MOVEMENT_BLOCKED


def test_mission_events_are_recorded_in_order():
    from mission.mission_event import MissionEvent
    from mission.mission_status_event import MissionStatusEvent

    environment = Environment(5, 1)
    mission = Mission((0, 0), (2, 0))
    rover = Rover(0, 0, "EAST", 1)
    navigation = Navigation()

    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.mission_completed is True
    assert len(result.events) == 3

    assert isinstance(result.events[0], MissionEvent)
    assert result.events[0].step == 1
    assert result.events[0].position == (0, 0)
    assert result.events[0].new_position == (1, 0)

    assert isinstance(result.events[1], MissionEvent)
    assert result.events[1].step == 2
    assert result.events[1].position == (1, 0)
    assert result.events[1].new_position == (2, 0)

    assert isinstance(result.events[2], MissionStatusEvent)
    assert result.events[2].step == 2
    assert result.events[2].status == "COMPLETED"


def test_failure_event_is_recorded_after_movement_event():
    from mission.mission_event import MissionEvent
    from mission.mission_status_event import MissionStatusEvent

    class BlockedNavigation:
        def choose_direction(self, current_position, destination, environment):
            return "EAST"

    environment = Environment(3, 1)
    environment.add_obstacle(1, 0)

    mission = Mission((0, 0), (2, 0))
    rover = Rover(0, 0, "EAST", 1)
    navigation = BlockedNavigation()

    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.mission_completed is False
    assert len(result.events) == 2

    assert isinstance(result.events[0], MissionEvent)
    assert result.events[0].step == 1
    assert result.events[0].position == (0, 0)
    assert result.events[0].new_position == (0, 0)
    assert result.events[0].movement_successful is False

    assert isinstance(result.events[1], MissionStatusEvent)
    assert result.events[1].step == 1
    assert result.events[1].status == "FAILED"
    assert result.events[1].reason == MissionFailureReason.MOVEMENT_BLOCKED


def test_unreachable_destination_records_failure_event():
    from mission.mission_status_event import MissionStatusEvent

    environment = Environment(3, 3)

    environment.add_obstacle(1, 0)
    environment.add_obstacle(0, 1)

    mission = Mission((0, 0), (2, 2))
    rover = Rover(0, 0, "EAST", 1)
    navigation = Navigation()

    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.mission_completed is False
    assert result.failure_reason == MissionFailureReason.DESTINATION_UNREACHABLE
    assert isinstance(result.events[-1], MissionStatusEvent)
    assert result.events[-1].status == "FAILED"
    assert result.events[-1].reason == MissionFailureReason.DESTINATION_UNREACHABLE


def test_max_steps_failure_records_failure_event():
    from mission.mission_status_event import MissionStatusEvent

    environment = Environment(10, 1)
    mission = Mission((0, 0), (9, 0))
    rover = Rover(0, 0, "EAST", 1)
    navigation = Navigation()

    result = run_mission(
        rover,
        mission,
        navigation,
        environment,
        max_steps=3
    )

    assert result.mission_completed is False
    assert result.failure_reason == MissionFailureReason.MAX_STEPS_REACHED
    assert isinstance(result.events[-1], MissionStatusEvent)
    assert result.events[-1].status == "FAILED"
    assert result.events[-1].reason == MissionFailureReason.MAX_STEPS_REACHED


def test_repeated_position_failure_records_failure_event():
    from mission.mission_status_event import MissionStatusEvent

    class LoopingNavigation:
        def choose_direction(self, current_position, destination, environment):
            if current_position == (0, 0):
                return "EAST"
            return "WEST"

    environment = Environment(3, 1)
    mission = Mission((0, 0), (2, 0))
    rover = Rover(0, 0, "EAST", 1)
    navigation = LoopingNavigation()

    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.mission_completed is False
    assert result.failure_reason == MissionFailureReason.REPEATED_POSITION
    assert isinstance(result.events[-1], MissionStatusEvent)
    assert result.events[-1].status == "FAILED"
    assert result.events[-1].reason == MissionFailureReason.REPEATED_POSITION


def test_invalid_mission_records_failure_event():
    from mission.mission_status_event import MissionStatusEvent

    environment = Environment(3, 3)
    environment.add_obstacle(0, 0)

    mission = Mission((0, 0), (2, 2))
    rover = Rover(0, 0, "EAST", 1)
    navigation = Navigation()

    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    assert result.mission_completed is False
    assert result.failure_reason == MissionFailureReason.INVALID_MISSION
    assert isinstance(result.events[-1], MissionStatusEvent)
    assert result.events[-1].step == 0
    assert result.events[-1].status == "FAILED"
    assert result.events[-1].reason == MissionFailureReason.INVALID_MISSION