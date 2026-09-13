class Navigation:
    # Create a priority order for directions based on the destination.
    def get_direction_priority(self, current_position, destination):

        current_x, current_y = current_position
        destination_x, destination_y = destination

        if current_x < destination_x:
            return ["EAST", "NORTH", "SOUTH", "WEST"]

        elif current_x > destination_x:
            return ["WEST", "NORTH", "SOUTH", "EAST"]

        elif current_y < destination_y:
            return ["NORTH", "EAST", "WEST", "SOUTH"]

        elif current_y > destination_y:
            return ["SOUTH", "EAST", "WEST", "NORTH"]

    # Calculate the position reached by moving one step in a direction.
    def calculate_next_position(self, current_position, direction):
        current_x, current_y = current_position

        if direction == "EAST":
            return current_x + 1, current_y
        elif direction == "WEST":
            return current_x - 1, current_y
        elif direction == "NORTH":
            return current_x, current_y + 1
        elif direction == "SOUTH":
            return current_x, current_y - 1
        else:
            raise ValueError("Invalid direction")

    # Choose the first free direction from the priority list.
    def choose_direction(
            self,
            current_position,
            destination,
            environment
    ):
        if current_position is None:
            raise ValueError("Current position cannot be None")

        if destination is None:
            raise ValueError("Destination cannot be None")

        if current_position == destination:
            return None

        priority = self.get_direction_priority(
            current_position,
            destination
        )

        for direction in priority:
            next_position = self.calculate_next_position(
                current_position,
                direction
            )

            if environment.is_position_free(*next_position):
                return direction

        return None