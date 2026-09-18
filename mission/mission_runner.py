from mission.mission_result import MissionResult, MissionFailureReason


def run_mission(rover, mission, navigation, environment, max_steps=100):
    if not mission.is_valid(environment):
        return MissionResult(
            (rover.x, rover.y),
            False,
            MissionFailureReason.INVALID_MISSION
        )

    steps = 0
    visited_positions = set()

    while (
            not mission.is_destination_reached((rover.x, rover.y))
            and steps < max_steps
    ):
        current_position = (rover.x, rover.y)

        if current_position in visited_positions:
            return MissionResult(
                (rover.x, rover.y),
                False,
                MissionFailureReason.REPEATED_POSITION
            )

        visited_positions.add(current_position)

        direction = navigation.choose_direction(
            (rover.x, rover.y),
            mission.destination,
            environment
        )

        if direction is None:
            return MissionResult(
                (rover.x, rover.y),
                False,
                MissionFailureReason.DESTINATION_UNREACHABLE
            )

        rover.change_direction(direction)

        moved = rover.move(environment)

        steps += 1

        if not moved:
            return MissionResult(
                (rover.x, rover.y),
                False,
                MissionFailureReason.MOVEMENT_BLOCKED
            )

    mission_completed = mission.is_destination_reached(
        (rover.x, rover.y)
    )

    if mission_completed:
        return MissionResult(
            (rover.x, rover.y),
            True
        )

    if steps >= max_steps:
        return MissionResult(
            (rover.x, rover.y),
            False,
            MissionFailureReason.MAX_STEPS_REACHED
        )

    return MissionResult(
        (rover.x, rover.y),
        False,
        MissionFailureReason.DESTINATION_UNREACHABLE
    )