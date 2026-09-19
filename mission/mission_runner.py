from mission.mission_event import MissionEvent
from mission.mission_status_event import MissionStatusEvent
from mission.mission_result import MissionResult, MissionFailureReason


def run_mission(rover, mission, navigation, environment, max_steps=100):
    if not mission.is_valid(environment):
        events = [
            MissionStatusEvent(
                0,
                "FAILED",
                MissionFailureReason.INVALID_MISSION
            )
        ]

        return MissionResult(
            (rover.x, rover.y),
            False,
            MissionFailureReason.INVALID_MISSION,
            events
        )

    steps = 0
    visited_positions = set()
    events = []

    while (
            not mission.is_destination_reached((rover.x, rover.y))
            and steps < max_steps
    ):
        current_position = (rover.x, rover.y)

        if current_position in visited_positions:
            events.append(
                MissionStatusEvent(
                    steps,
                    "FAILED",
                    MissionFailureReason.REPEATED_POSITION
                )
            )

            return MissionResult(
                (rover.x, rover.y),
                False,
                MissionFailureReason.REPEATED_POSITION,
                events
            )

        visited_positions.add(current_position)

        direction = navigation.choose_direction(
            (rover.x, rover.y),
            mission.destination,
            environment
        )

        if direction is None:
            events.append(
                MissionStatusEvent(
                    steps,
                    "FAILED",
                    MissionFailureReason.DESTINATION_UNREACHABLE
                )
            )

            return MissionResult(
                (rover.x, rover.y),
                False,
                MissionFailureReason.DESTINATION_UNREACHABLE,
                events
            )

        rover.change_direction(direction)

        moved = rover.move(environment)

        steps += 1

        events.append(
            MissionEvent(
                steps,
                current_position,
                direction,
                (rover.x, rover.y),
                moved
            )
        )

        if not moved:
            events.append(
                MissionStatusEvent(
                    steps,
                    "FAILED",
                    MissionFailureReason.MOVEMENT_BLOCKED
                )
            )

            return MissionResult(
                (rover.x, rover.y),
                False,
                MissionFailureReason.MOVEMENT_BLOCKED,
                events
            )

    mission_completed = mission.is_destination_reached(
        (rover.x, rover.y)
    )

    if mission_completed:
        events.append(
            MissionStatusEvent(
                steps,
                "COMPLETED"
            )
        )

        return MissionResult(
            (rover.x, rover.y),
            True,
            events=events
        )

    if steps >= max_steps:
        events.append(
            MissionStatusEvent(
                steps,
                "FAILED",
                MissionFailureReason.MAX_STEPS_REACHED
            )
        )

        return MissionResult(
            (rover.x, rover.y),
            False,
            MissionFailureReason.MAX_STEPS_REACHED,
            events
        )

    return MissionResult(
        (rover.x, rover.y),
        False,
        MissionFailureReason.DESTINATION_UNREACHABLE
    )