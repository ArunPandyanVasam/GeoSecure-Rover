def run_mission(rover, mission, navigation, environment):
    while not mission.is_destination_reached((rover.x, rover.y)):
        direction = navigation.choose_direction(
            (rover.x, rover.y),
            mission.destination
        )

        rover.change_direction(direction)

        moved = rover.move(environment)

        if not moved:
            break

    mission_completed = mission.is_destination_reached(
        (rover.x, rover.y)
    )

    return rover.x, rover.y, mission_completed