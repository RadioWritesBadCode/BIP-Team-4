import json
import sys

nodes_and_connections = json.load(open("paths.json"))
# Necessary for get_cardinal_directions_of_path.
letters_from_north_to_south = ["A", "C", "D", "E", "F", "G", "B"]
# Necessary to calculate rotations.
cardinal_directions = ["North", "East", "South", "West"]
turns = ["Forward", "Turn Left", "Backward", "Turn Right"]
# This is the orientation to physical robot has in the real world.
current_orientation = cardinal_directions[0]


# Returns all nodes for the shortest path as an array.
def get_shortest_route_from_to(start_node, target_node):
    previous_nodes, shortest_path_to = dijkstra_algorithm(start_node)
    path = []
    node = target_node
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
    path.append(start_node)
    return list(reversed(path))


# Removes the path between two nodes from nodes_and_connections.
def remove_path(from_node, to_node):
    del nodes_and_connections[from_node][to_node]
    del nodes_and_connections[to_node][from_node]


# Calculates the shortest path using an implementation of Dijkstra's algorithm I stole from the internet.
# Source: https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
def dijkstra_algorithm(start_node):
    unvisited_nodes = list(nodes_and_connections.keys())
    shortest_path_to = {}
    previous_nodes = {}

    for node in nodes_and_connections.keys():
        shortest_path_to[node] = sys.maxsize
    shortest_path_to[start_node] = 0

    while unvisited_nodes:
        current_min_node = None
        for node in unvisited_nodes:
            if current_min_node is None:
                current_min_node = node
            elif shortest_path_to[node] < shortest_path_to[current_min_node]:
                current_min_node = node

        neighbors = nodes_and_connections[current_min_node].keys()
        for neighbor in neighbors:
            tentative_value = shortest_path_to[current_min_node] + nodes_and_connections[current_min_node][neighbor]
            if tentative_value < shortest_path_to[neighbor]:
                shortest_path_to[neighbor] = tentative_value
                previous_nodes[neighbor] = current_min_node

        unvisited_nodes.remove(current_min_node)
    return previous_nodes, shortest_path_to


# Calculates the cardinal direction two neighboring nodes have to each other.
def get_cardinal_direction_of_path(start_node, end_node):
    letters = [start_node[0], end_node[0]]
    numbers = [start_node[1], end_node[1]]
    # Horizontal:
    if letters[0] is letters[1]:
        if numbers[0] < numbers[1]:
            return "East"
        else:
            return "West"
    # Vertical:
    else:
        if letters_from_north_to_south.index(letters[0]) < letters_from_north_to_south.index(letters[1]):
            return "South"
        else:
            return "North"


# Calculates the cardinal directions of all the connections in the final route.
def get_cardinal_directions_of_route(nodes):
    all_cardinal_directions = []
    for x in range(0, len(nodes) - 1):
        all_cardinal_directions.append(get_cardinal_direction_of_path(nodes[x], nodes[x+1]))
    return all_cardinal_directions


# Calculates the turn the robot will have to make in order to face the direction of the next path.
# robot_orientation is the expected orientation the robot would have at this point in time,
#   not the actual physical direction.
def get_turn(path_direction, robot_orientation):
    path_orientation_value = cardinal_directions.index(path_direction)
    robot_orientation_value = cardinal_directions.index(robot_orientation)
    # Attaches a value between 0 and 3 to both direction and turn.
    # North -> North = 0-0 = 0 -> forward = 0
    # North -> South = 0-2 = -2 -> backward = -2 = +2
    # North -> East = 0-1 = -1 -> right = -1 = +3
    # North -> West = 0-3 = -3 -> left = -3 = +1
    return turns[(robot_orientation_value - path_orientation_value) % 4]


def get_turns_of_route(route_directions):
    orders = []
    hypothetical_orientation = current_orientation
    for cardinal_direction in route_directions:
        orders.append(get_turn(cardinal_direction, hypothetical_orientation))
        hypothetical_orientation = cardinal_direction
    return orders


# Just for manual tests, please ignore.
def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
    path.append(start_node)
    print("The path from", start_node, "to", target_node, "is", shortest_path[target_node],
          "long and goes the following way:")
    print(" -> ".join(reversed(path)))


# === BEHAVIOR ===
remove_path("G6", "F3")
remove_path("G2", "F2")
remove_path("F2", "F3")
remove_path("F3", "E3")
remove_path("E1", "E2")
remove_path("E1", "D1")
remove_path("E2", "D2")
remove_path("C5", "C4")
route = get_shortest_route_from_to("B4", "A3")
directions = get_cardinal_directions_of_route(route)
print(route)
print(directions)
print(get_turns_of_route(directions))
