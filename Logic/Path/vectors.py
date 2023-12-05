"""Vector Handling Module"""

import sys
import math
import numpy as np
from numba import jit


class Vectors:
    """
    Responsible for handling vectors

    """

    @staticmethod
    @jit
    def distance_from_two_points(point_one, point_two):
        """
        Responsible for calculating the distance between two points
        Args:
            point_one (tuple[float, float]): The first point
            point_two (tuple[float, float]): The second point

        Returns:

        """

        return math.sqrt(((point_one[0] - point_two[0]) ** 2) + ((point_one[1] - point_two[1]) ** 2))

    @staticmethod
    @jit
    def move_from_two_points(point_one, point_two, distance):
        """
        Responsible for moving a point from another point by a distance
        Args:
            point_one (tuple[float, float]): The first point
            point_two (tuple[float, float]): The second point
            distance (int): The distance to move

        Returns:
            tuple[int, int]: The new point
        """

        point_a = np.array([point_one[0], point_one[1]])
        point_b = np.array([point_two[0], point_two[1]])

        np_v = point_b - point_a
        np_mod_v = math.sqrt(np_v[0] ** 2 + np_v[1] ** 2)

        unit_vector = np_v / np_mod_v
        target_point = point_a - (distance * unit_vector)

        return int(target_point[0]), int(target_point[1])

    @staticmethod
    @jit
    def line_from_two_points(point_one, point_two):
        """
        Responsible for calculating the line from two points
        Args:
            point_one (list[float]|np.ndArray): The first point
            point_two (list[float]|np.ndArray): The second point

        Returns:

        """

        line_a = point_one[1] - point_two[1]
        line_b = point_two[0] - point_one[0]
        line_c = (point_two[1] * point_one[0]) - (point_one[1] * point_two[0])

        if line_b == 0:
            return line_a, 0, line_c
        else:
            return (line_a / -line_b), -1, (line_c / -line_b)

    @jit
    def segment_intercept_from_four_points(self, point_a_one, point_a_two, point_b_one, point_b_two):
        """
        Responsible for calculating the intercept of two segments
        Args:
            point_a_one:
            point_a_two:
            point_b_one:
            point_b_two:

        Returns:

        """

        np_point_a_one = np.array(point_a_one[0:2])
        np_point_a_two = np.array(point_a_two[0:2])
        np_point_b_one = np.array(point_b_one[0:2])
        np_point_b_two = np.array(point_b_two[0:2])

        da = np_point_a_two[0:2] - np_point_a_one[0:2]
        db = np_point_b_two[0:2] - np_point_b_one[0:2]
        dp = np_point_a_one[0:2] - np_point_b_one[0:2]

        dap = np.array([- da[1], da[0]])
        denom = np.dot(dap, db) + sys.float_info.epsilon
        num = np.dot(dap, dp)

        intercept = (num / denom.astype(float)) * db + np_point_b_one

        point_a_gradient = self.line_from_two_points(np_point_a_one, np_point_a_two)[0]
        is_on_line_a = (intercept[1] - np_point_a_one[1]) == point_a_gradient * (intercept[0] - np_point_a_one[0])

        is_x_occluded = np.min([np_point_a_one[0], np_point_a_two[0]]) <= intercept[0] <= np.max([np_point_a_one[0], np_point_a_two[0]])
        is_y_occluded = np.min([np_point_a_one[1], np_point_a_two[1]]) <= intercept[1] <= np.max([np_point_a_one[1], np_point_a_two[1]])
        is_between_line_a = is_x_occluded and is_y_occluded

        return is_on_line_a and is_between_line_a

    @staticmethod
    @jit
    def line_intercept_circle(line_terms, circle_point, circle_radius):
        """
        Responsible for calculating the intercept of a line and a circle
        Args:
            line_terms:
            circle_point:
            circle_radius:

        Returns:

        """

        line_a = line_terms[0]
        line_b = line_terms[1]
        line_c = line_terms[2]

        centre_x = circle_point[0]
        centre_y = circle_point[1]

        distance = abs(line_a * centre_x + line_b * centre_y + line_c) / math.sqrt(line_a * line_a + line_b * line_b)

        return distance <= circle_radius
