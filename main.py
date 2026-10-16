from boundary import GRID_SIZE, is_inside_boundary

def run_simulation():
    obstacle_encounters = 0
    boundary_encounters = 0
    print("=== MARS ROVER OBSTACLE DETECTION ===")

    # Starting Position
    x = 0
    y = 0

    # Rover Movement Path
    path = [(x, y)]

    # Obstacle Locations
    obstacles = {(2, 0), (1, 2)}
    destination = (4, 4)

    print("Starting Position:", (x, y))
    print("Obstacle Locations:", obstacles)

    # Rover Movement
    for step in range(4):

        direction = input(
            "Enter direction (up/down/left/right): "
        ).lower().strip()

        # Calculate Next Position
        new_x = x
        new_y = y

        if direction == "right":
            new_x = x + 1

        elif direction == "left":
            new_x = x - 1

        elif direction == "up":
            new_y = y + 1

        elif direction == "down":
            new_y = y - 1

        else:
            print("Invalid direction!")
            continue

        # Boundary Detection
        if not is_inside_boundary(new_x, new_y):
            boundary_encounters += 1
            print("WARNING! Boundary Detected!")
            print("Rover cannot move outside the grid!")

        # Obstacle Detection
        elif (new_x, new_y) in obstacles:
            obstacle_encounters += 1
            print("WARNING! Obstacle Detected!")
            print("Rover cannot move there!")


        else:
            x = new_x
            y = new_y
            path.append((x, y))
            print("Movement Successful!")

        print("Current Position:", (x, y))

    print("Mission Completed!")
    print("Final Position:", (x, y))
    print("Complete Rover Path:", path)
    # Movement Statistics
    successful_moves = len(path) - 1

    print("Total Successful Moves:", successful_moves)
    print("Total Recorded Positions:", len(path))

    # Mission Analytics
    total_distance = 0

    for i in range(1, len(path)):
        x1, y1 = path[i - 1]
        x2, y2 = path[i]

        distance = abs(x2 - x1) + abs(y2 - y1)
        total_distance += distance

    print("Total Distance Travelled:", total_distance, "grid units")
    print("Obstacle Encounters:", obstacle_encounters)
    print("Boundary Encounters:", boundary_encounters)

    if (x, y) == destination:
        mission_status = "SUCCESS"
    else:
        mission_status = "INCOMPLETE"

    print("Destination:", destination)
    print("Mission Status:", mission_status)

    print("=== MISSION SUMMARY ===")
    print("Final Position:", (x, y))
    print("Mission Status:", mission_status)
    print("Distance:", total_distance, "grid units")
    print("Successful Moves:", successful_moves)
    print("Obstacle Encounters:", obstacle_encounters)
    print("Boundary Encounters:", boundary_encounters)

    return path, obstacles


if __name__ == "__main__":
    run_simulation()