# GeoSecure Rover

**A Simulated Autonomous Rover Operating in a Realistic Environment with Navigation, Communication, and Cybersecurity Monitoring.**

GeoSecure Rover is a long-term robotics and cybersecurity portfolio project that explores how an autonomous rover can operate safely in an environment while navigating toward a mission destination, responding to obstacles, recording mission telemetry, and eventually integrating communication and cybersecurity monitoring.

The project is being developed incrementally, starting with a reliable simulation foundation and progressing toward a more realistic geospatial environment.

## Current Stage

**Phase 2 — Environment & Obstacle-Aware Rover**

The current implementation provides a tested simulation foundation for:

* Environment and boundary management
* Obstacle representation and detection
* Rover movement and collision awareness
* Obstacle-aware navigation
* Mission validation and execution
* Failure detection and safe stopping
* Mission execution telemetry
* Structured mission results
* Automated unit and integration testing

The current project is intentionally **not yet the final GeoSecure Rover system**. Advanced capabilities such as realistic GIS environments, terrain modeling, sophisticated path planning, communication systems, cybersecurity monitoring, and the final graphical interface will be developed in later phases.



## Project Vision

The long-term goal of GeoSecure Rover is to build a simulated autonomous rover that operates within a realistic environment and combines robotics, geospatial data, networking, and cybersecurity.

The planned system will evolve from a simple grid-based simulation into a more realistic environment where a user can define or select an operating area and observe the rover performing a mission.

The long-term architecture is intended to support:

* Autonomous navigation and path planning
* Realistic geographic environments
* Terrain and environmental constraints
* GIS and geospatial data
* Rover-to-control-server communication
* Mission telemetry and history
* Cybersecurity monitoring and threat detection
* Mission visualization and replay
* A graphical mission-control interface

The project is being developed incrementally so that each layer has a reliable and testable foundation before more complex capabilities are introduced.



## Architecture

GeoSecure Rover is organized into separate components, with each component responsible for a specific part of the rover simulation.

```text
                    GeoSecure Rover
                           |
        +------------------+------------------+
        |                  |                  |
   Environment          Mission          Navigation
        |                  |                  |
   Boundaries         Definition        Direction
   Obstacles          Validation        Selection
   Free Space
        |                  |                  |
        +------------------+------------------+
                           |
                         Rover
                           |
                     Movement
                     Collision
                     Status
                           |
                           v
                    Mission Runner
                           |
             +-------------+-------------+
             |                           |
        MissionResult              Mission Events
             |                           |
      Success / Failure        Movement / Status
      Final Position              Telemetry
             |
             v
        Mission History
```

### Component Responsibilities

| Component            | Responsibility                                                                   |
| -------------------- | -------------------------------------------------------------------------------- |
| `Environment`        | Defines the environment boundaries, obstacles, and free/blocked positions        |
| `Rover`              | Represents the rover and performs movement while respecting the environment      |
| `Navigation`         | Determines the rover's next movement direction while considering obstacles       |
| `Mission`            | Defines the mission start and destination and validates mission endpoints        |
| `MissionRunner`      | Controls mission execution, safety checks, failure handling, and event recording |
| `MissionResult`      | Represents the final mission outcome                                             |
| `MissionEvent`       | Records individual rover movement attempts                                       |
| `MissionStatusEvent` | Records mission-level completion or failure events                               |

### Design Principle

The project follows a separation-of-responsibilities approach.

For example:

* The `Rover` does not decide where it should go.
* `Navigation` does not execute rover movement.
* `Mission` does not perform navigation.
* `MissionRunner` coordinates the execution rather than owning every piece of logic.
* GUI and cybersecurity functionality are kept outside the core mission execution logic.

This separation is intended to make the system easier to test, extend, and integrate with future components.



## Current Capabilities

### Environment

The rover operates inside a bounded environment.

The environment system supports:

* Configurable width and height
* Boundary validation
* Obstacle placement
* Invalid obstacle rejection
* Duplicate obstacle handling
* Multiple obstacles
* Free-space detection
* Blocked-space detection
* Grid representation

### Rover

The rover supports:

* Four-direction movement
* Configurable movement speed
* Direction changes
* Environment boundary protection
* Obstacle collision protection
* Movement success/failure reporting
* Safe stopping when movement is blocked
* Rover position tracking

### Navigation

The navigation system provides obstacle-aware movement decisions.

It can:

* Move toward a mission destination
* Detect blocked directions
* Select available alternatives
* Reassess movement after an alternative route
* Handle multiple obstacles
* Report when no usable direction is available

The current navigation implementation is intentionally a lightweight obstacle-aware strategy. Advanced global path-planning algorithms such as A* are reserved for later phases.

### Mission Execution

A mission contains a start position and destination.

Mission execution supports:

* Mission endpoint validation
* Start and destination obstacle validation
* Autonomous movement toward the destination
* Successful mission completion
* Unreachable destination detection
* Maximum-step protection
* Repeated-position detection
* Blocked-movement detection
* Structured mission results

### Mission Failure Reasons

Mission failures are represented using structured failure reasons:

```text
INVALID_MISSION
DESTINATION_UNREACHABLE
MAX_STEPS_REACHED
REPEATED_POSITION
MOVEMENT_BLOCKED
```

This allows future interfaces and monitoring systems to distinguish between different types of mission failure instead of treating every failure as a generic error.

### Mission Telemetry

Mission execution produces structured events.

`MissionEvent` records individual movement attempts, including:

* Step number
* Previous position
* Direction
* New position
* Movement success/failure

`MissionStatusEvent` records mission-level outcomes such as:

* Mission completion
* Mission failure
* Failure reason

These events are stored in `MissionResult.events`, providing an execution history that can later support visualization, replay, logging, and security monitoring.



## Testing

GeoSecure Rover uses automated tests to verify the behavior of its core components.

The test suite covers:

* Environment validation
* Boundary handling
* Obstacle management
* Free and blocked positions
* Rover movement
* Collision prevention
* Direction changes
* Navigation decisions
* Obstacle avoidance
* Mission validation
* Mission execution
* Unreachable missions
* Loop protection
* Maximum-step protection
* Repeated-position detection
* Movement failures
* Structured mission results
* Mission events
* Mission status events
* Event ordering
* Integration behavior
* Failure scenarios
* Regression behavior

### Test Structure

```text
tests/
├── test_environment.py
├── test_mission.py
├── test_mission_event.py
├── test_mission_runner.py
├── test_navigation.py
└── test_rover.py
```

### Running the Tests

The complete test suite can be executed with:

```bash
python -m pytest -q
```

### Phase 2 Regression Result

At the completion of the Phase 2 capability audit:

```text
188 passed
```

The full test suite passes successfully, providing the regression baseline for the next development phase.



## How to Run

### Requirements

The current Phase 2 implementation requires:

* Python 3
* A Python virtual environment
* `pytest` for running the automated tests

### Run the Rover Simulation

From the project root:

```bash
python main.py
```

The current demonstration creates:

* A `10 × 10` environment
* A mission from `(0, 0)` to `(9, 9)`
* A rover starting at `(0, 0)`
* Obstacle-aware navigation
* Mission execution through `MissionRunner`

The program reports whether the mission is valid, the final rover position, mission completion status, and any failure reason.

### Run the Test Suite

From the project root:

```bash
python -m pytest -q
```

A successful Phase 2 test run currently reports:

```text
188 passed
```

### Development Environment

The project is developed using Python and is structured so that the core rover, environment, navigation, mission, and testing components can be developed independently.

## Example Output

Running the current Phase 2 demonstration produces:

```text
Mission valid: True
Final position: (9, 9)
Mission completed: True
Failure reason: None
```



## Project Structure

```text
GeoSecure-Rover/
├── environment/
│   └── environment.py
├── mission/
│   ├── mission.py
│   ├── mission_event.py
│   ├── mission_status_event.py
│   ├── mission_result.py
│   └── mission_runner.py
├── navigation/
│   └── navigation.py
├── rover/
│   └── rover.py
├── tests/
│   ├── test_environment.py
│   ├── test_mission.py
│   ├── test_mission_event.py
│   ├── test_mission_runner.py
│   ├── test_navigation.py
│   └── test_rover.py
├── docs/
├── main.py
├── README.md
└── .gitignore
```


## Design Decisions

Several design decisions were made during Phase 2 to keep the project reliable, testable, and extensible.

### Separation of Responsibilities

Each component has a focused responsibility.

- `Environment` manages boundaries, obstacles, and spatial validity.
- `Rover` manages movement and rover state.
- `Navigation` decides which direction the rover should attempt to move.
- `Mission` defines and validates mission endpoints.
- `MissionRunner` coordinates mission execution and safety checks.
- `MissionResult` represents the final outcome of a mission.
- `MissionEvent` and `MissionStatusEvent` provide structured mission telemetry.

This separation reduces coupling between components and makes individual parts easier to test and replace.

### Safety Before Complexity

The project prioritizes reliable behavior before introducing advanced algorithms.

The current navigation system uses a lightweight obstacle-aware strategy rather than a global path-planning algorithm such as A*.

This allows the project to establish a reliable simulation foundation before introducing more sophisticated navigation.

### Explicit Failure Handling

Mission failures are represented using structured failure reasons rather than generic errors.

This makes it possible for future systems to distinguish between situations such as:

- Invalid mission
- Unreachable destination
- Maximum-step limit reached
- Repeated position
- Movement blocked

This approach will also make future visualization, logging, and cybersecurity monitoring easier to implement.

### Observability

Mission execution records structured events instead of only returning a final position.

The execution history can later support:

- Mission replay
- GUI visualization
- Debugging
- Telemetry
- Logging
- Security monitoring

### Test-Driven Incremental Development

New capabilities are developed together with automated tests.

The project uses the test suite as a regression baseline so that future changes can be made without unnecessarily breaking previously implemented behavior.



## Current Limitations & Future Roadmap

GeoSecure Rover is being developed incrementally. The current Phase 2 implementation establishes the core simulation and obstacle-aware mission execution foundation.

The following capabilities are intentionally reserved for future phases.

### Current Limitations

The current implementation:

- Uses a grid-based environment
- Uses discrete coordinates for rover positioning
- Uses a lightweight obstacle-aware navigation strategy
- Does not yet use global path-planning algorithms such as A*
- Does not yet model terrain types or terrain costs
- Does not yet use real-world GIS or geospatial datasets
- Does not yet include rover-to-server communication
- Does not yet include cybersecurity monitoring or threat detection
- Does not yet provide the final graphical user interface
- Does not yet simulate a complete real-world geographic location

These limitations are intentional because the project is being developed layer by layer.

### Planned Evolution

The long-term development direction includes:

```text
Phase 1
Basic Rover Simulation
        ↓
Phase 2
Environment & Obstacle-Aware Rover
        ↓
Phase 3
Advanced Navigation & Path Planning
        ↓
Phase 4
Terrain & Environment Modeling
        ↓
Phase 5
GIS / Real-World Geographic Environment
        ↓
Phase 6
Rover Communication & Networking
        ↓
Phase 7
Cybersecurity Monitoring & Threat Detection
        ↓
Phase 8
Graphical Mission-Control Interface
        ↓
Future
Integrated GeoSecure Rover Simulation
```
