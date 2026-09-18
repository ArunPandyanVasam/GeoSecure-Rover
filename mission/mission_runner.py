def run_mission(rover, mission, navigation, environment, max_steps=100):
    if not mission.is_valid(environment):
        return rover.x, rover.y, False

    steps = 0
    visited_positions = set()

    while (
            not mission.is_destination_reached((rover.x, rover.y))
            and steps < max_steps
    ):
        current_position = (rover.x, rover.y)

        if current_position in visited_positions:
            break

        visited_positions.add(current_position)

        direction = navigation.choose_direction(
            (rover.x, rover.y),
            mission.destination,
            environment
        )

        if direction is None:
            break

        rover.change_direction(direction)

        moved = rover.move(environment)

        steps += 1

        if not moved:
            break

    mission_completed = mission.is_destination_reached(
        (rover.x, rover.y)
    )

    return rover.x, rover.y, mission_completed