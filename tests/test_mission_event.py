from mission.mission_event import MissionEvent


def test_mission_event_stores_movement_information():
    event = MissionEvent(
        1,
        (0, 0),
        "EAST",
        (1, 0),
        True
    )

    assert event.step == 1
    assert event.position == (0, 0)
    assert event.direction == "EAST"
    assert event.new_position == (1, 0)
    assert event.movement_successful is True


def test_mission_result_stores_events():
    from mission.mission_result import MissionResult

    events = ["event1", "event2"]

    result = MissionResult(
        (2, 3),
        True,
        events=events
    )

    assert result.events == events


def test_mission_status_event_stores_status_information():
    from mission.mission_status_event import MissionStatusEvent

    event = MissionStatusEvent(
        5,
        "FAILED",
        "MOVEMENT_BLOCKED"
    )

    assert event.step == 5
    assert event.status == "FAILED"
    assert event.reason == "MOVEMENT_BLOCKED"