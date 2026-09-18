class Mission:
    # Define the starting position and destination for the mission.
    def __init__(self, start_position, destination):
        self.start_position = start_position
        self.destination = destination

    # Check whether the rover has reached the mission destination.
    def is_destination_reached(self, position):
        return position == self.destination

    # Check whether the start and destination are inside the environment and free.
    def is_valid(self, environment):
        start_is_valid = environment.is_position_free(
            self.start_position[0],
            self.start_position[1]
        )
        destination_is_valid = environment.is_position_free(
            self.destination[0],
            self.destination[1]
        )
        return start_is_valid and destination_is_valid