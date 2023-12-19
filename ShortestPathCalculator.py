import json
import sys

nodes_and_connections = json.load(open("paths.json"))
# Necessary for get_cardinal_directions_of_path
letters_from_north_to_south = ["A", "C", "D", "E", "F", "G", "B"]


# Returns all nodes for the shortest path as an array.
def get_shortest_path_from_to(start_node, target_node):
    previous_nodes, shortest_path_to = dijkstra_algorithm(start_node)
    path = []
    node = target_node
    while node != start_node:
        path.append(node)
        node = previous_nodes[node]
    path.append(start_node)
    path = reversed(path)
    print(" -> ".join(path))
    return path


# Removes the path between two nodes from nodes_and_connections.
def remove_path(from_node, to_node):
    del nodes_and_connections[from_node][to_node]
    del nodes_and_connections[to_node][from_node]


def dijkstra_algorithm(start_node):
    # https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
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


def get_cardinal_direction_of_path(start_node, end_node):
    letters = [start_node[0], end_node[0]]
    numbers = [start_node[1], end_node[1]]
    # Horizontal:
    if letters[0] is letters[1]:
        if numbers[0] > numbers[1]:
            return "East"
        else:
            return "West"
    # Vertical:
    else:
        if letters_from_north_to_south.index(letters[0]) >letters_from_north_to_south.index(letters[1]):
            return "South"
        else:
            return "North"


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
get_shortest_path_from_to("B4", "A3")
print(get_cardinal_direction_of_path("A1", "A2"))
print(get_cardinal_direction_of_path("C2", "D2"))
print(get_cardinal_direction_of_path("A3", "A2"))
print(get_cardinal_direction_of_path("E2", "D2"))
