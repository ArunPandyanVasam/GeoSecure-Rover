class MissionEvent:
    def __init__(
        self,
        step,
        position,
        direction,
        new_position,
        movement_successful
    ):
        self.step = step
        self.position = position
        self.direction = direction
        self.new_position = new_position
        self.movement_successful = movement_successful