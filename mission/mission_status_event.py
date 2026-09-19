class MissionStatusEvent:
    def __init__(self, step, status, reason=None):
        self.step = step
        self.status = status
        self.reason = reason