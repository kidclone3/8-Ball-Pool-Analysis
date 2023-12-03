"""Dijkstra Graph"""

from collections import defaultdict

import math
import numpy as np


class DijkstraGraph:
    """
    Responsible for Dijkstra Graph
    """

    def __init__(self):

        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, from_node, to_node, weight):
        """
        Responsible for adding an edge to the graph
        Args:
            from_node (list[float]): The from node
            to_node (list[float]): The to node
            weight (int): The weight of the edge

        Returns:

        """
        _to_node = (to_node[0], to_node[1])
        _from_node = (from_node[0], from_node[1])

        self.edges[_from_node].append(_to_node)
        self.edges[_to_node].append(_from_node)
        self.weights[(from_node, to_node)] = weight
        self.weights[(to_node, from_node)] = weight

    def find_any_goal_path(self, start, goals):
        """
        Responsible for finding the optimal path for a goal
        Args:
            start (list[float]): The start node
            goals (list[list[float]]): The goals

        Returns:

        """

        paths = []
        distances = []

        _start = (start[0], start[1])
        _goals = [(goal[0], goal[1]) for goal in goals]

        for goal in _goals:
            path, distance = self.find_a_goal_path(_start, goal)

            if distance != math.inf:
                paths.append(path)
                distances.append(distance)

        if paths:
            return paths[np.argmin(distances)]

        return []

    def find_a_goal_path(self, initial, end):
        """
        Responsible for finding the optimal path for a goal
        Args:
            initial (tuple(float, float)): The initial node
            end (tuple(float, float)): The end node

        Returns:

        """

        shortest_paths = {initial: (None, 0)}
        current_node = initial
        visited = set()

        while current_node != end:
            visited.add(current_node)
            destinations = self.edges[current_node]
            weight_to_current_node = shortest_paths[current_node][1]

            for next_node in destinations:
                weight = self.weights[(current_node, next_node)] + weight_to_current_node
                if next_node not in shortest_paths:
                    shortest_paths[next_node] = (current_node, weight)
                else:
                    current_shortest_weight = shortest_paths[next_node][1]
                    if current_shortest_weight > weight:
                        shortest_paths[next_node] = (current_node, weight)

            next_destinations = {node: shortest_paths[node] for node in shortest_paths if node not in visited}
            if not next_destinations:
                return [], math.inf

            # Next node is the destination with the lowest weight
            current_node = min(next_destinations, key=lambda k: next_destinations[k][1])

        # Work back through destinations in the shortest path
        path = []
        path_weight = 0

        while current_node is not None:
            path.append(current_node)

            next_node = shortest_paths[current_node][0]
            path_weight += shortest_paths[current_node][1]

            current_node = next_node

        # Reverse path
        path = path[::-1]

        return path, path_weight
