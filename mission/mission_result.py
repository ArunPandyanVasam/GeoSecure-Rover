from enum import Enum


class MissionFailureReason(Enum):
    INVALID_MISSION = "INVALID_MISSION"
    DESTINATION_UNREACHABLE = "DESTINATION_UNREACHABLE"
    MAX_STEPS_REACHED = "MAX_STEPS_REACHED"
    REPEATED_POSITION = "REPEATED_POSITION"
    MOVEMENT_BLOCKED = "MOVEMENT_BLOCKED"


class MissionResult:
    def __init__(self, final_position, mission_completed, failure_reason=None):
        self.final_position = final_position
        self.mission_completed = mission_completed
        self.failure_reason = failure_reason