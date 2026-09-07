# A class should protect the validity of its own state.
class Rover:
    # Create a rover with a position, direction, speed, and stopped status.
    def __init__(self, x, y, direction, speed):
        self.x = x
        self.y = y

        if direction not in ["EAST", "WEST", "NORTH", "SOUTH"]:
            raise ValueError("Invalid direction")

        self.direction = direction

        if speed < 0:
            raise ValueError("Speed cannot be negative")

        self.speed = speed
        self.status = "STOPPED"

    # Calculate the rover's next position and move if the position is valid.
    def move(self, environment):

        next_x = self.x
        next_y = self.y

        # Calculate proposed position.
        if self.direction == "EAST":
            next_x = next_x + self.speed
        elif self.direction == "WEST":
            next_x = next_x - self.speed
        elif self.direction == "NORTH":
            next_y = next_y + self.speed
        elif self.direction == "SOUTH":
            next_y = next_y - self.speed

        if environment.is_within_bounds(next_x, next_y) and not environment.has_obstacle(next_x, next_y):
            self.x = next_x
            self.y = next_y
            self.status = "MOVING"
            return True
        else:
            self.status = "STOPPED"
            return False

    # Change the rover's direction after validating the new direction.
    def change_direction(self, new_direction):
        if new_direction not in ["EAST", "WEST", "NORTH", "SOUTH"]:
            raise ValueError("Invalid direction")

        self.direction = new_direction