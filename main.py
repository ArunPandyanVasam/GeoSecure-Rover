# Set up the environment, mission, rover, and navigation, then run the mission.

from rover.rover import Rover
from environment.environment import Environment
from mission.mission import Mission
from navigation.navigation import Navigation
from mission.mission_runner import run_mission


# Create the mission.
mission = Mission((0, 0), (9, 9))
start_x, start_y = mission.start_position

# Create the environment
environment = Environment(10, 10)
navigation = Navigation()

mission_is_valid = mission.is_valid(environment)

print(f"Mission valid: {mission_is_valid}")

if mission_is_valid:
    rover = Rover(start_x, start_y, "EAST", 1)

    result = run_mission(
        rover,
        mission,
        navigation,
        environment
    )

    print(f"Final position: {result.final_position}")
    print(f"Mission completed: {result.mission_completed}")
    print(f"Failure reason: {result.failure_reason}")
else:
    print("Mission cannot start.")