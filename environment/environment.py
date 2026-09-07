class Environment:
    # Define the size of the environment and create an empty obstacle set.
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.obstacles = set()

    # Add an obstacle only if its position is inside the environment.
    def add_obstacle(self, x, y):
        if not self.is_within_bounds(x, y):
            raise ValueError("Obstacle is outside environment")
        self.obstacles.add((x, y))

    # Check whether an obstacle exists at the given position.
    def has_obstacle(self, x, y):
        return (x, y) in self.obstacles

    # Check whether a position is inside the environment boundaries.
    def is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height