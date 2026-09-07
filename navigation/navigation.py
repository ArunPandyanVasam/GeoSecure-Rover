class Navigation:
    # Choose the direction that moves the rover closer to its destination.
    def choose_direction(self, current_position, destination):

        # Both positions are required to calculate a direction.
        if current_position is None:
            raise ValueError("Current position cannot be None")

        if destination is None:
            raise ValueError("Destination cannot be None")

        current_x, current_y = current_position
        destination_x, destination_y = destination

        if current_x < destination_x:
            return "EAST"
        elif current_x > destination_x:
            return "WEST"
        elif current_y < destination_y:
            return "NORTH"
        elif current_y > destination_y:
            return "SOUTH"