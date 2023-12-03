"""Ball Detection Module"""

import numpy as np
import cv2

from Logic import constants


class BallDetection:
    """Responsible for detecting game balls and holes"""

    @staticmethod
    def board_boundary(holes):
        """
        Responsible for returning the boundary of the board

        Args:
            holes (list): The holes to be used
        """

        min_x = min(holes, key=lambda t: t[0])[0]
        min_y = min(holes, key=lambda t: t[1])[1]
        max_x = max(holes, key=lambda t: t[0])[0]
        max_y = max(holes, key=lambda t: t[1])[1]

        return [min_x, min_y, max_x, max_y]

    @staticmethod
    def find_corner_holes(entire_frame):
        """
        Responsible for returning an array of hole positions

        Args:
            entire_frame (np.ndArray): The entire frame to find the holes in
        """

        detected_holes = []

        gray_image = cv2.cvtColor(entire_frame, cv2.COLOR_BGR2GRAY)

        holes = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 20, param1=150, param2=16,
                                 minRadius=constants.CORNER_RADIUS, maxRadius=constants.CORNER_RADIUS+2)

        if holes is not None:
            holes = np.round(holes[0, :]).astype("int")

            for (x_position, y_position, _) in holes:
                detected_holes.append((x_position, y_position))

        return detected_holes

    @staticmethod
    def find_balls(board_frame_edges):
        """
        Responsible for returning an array of ball positions

        Args:
            board_frame_edges (np.ndArray): The board frame edges to find the balls in
        """

        detected_balls = []

        circles = cv2.HoughCircles(board_frame_edges, cv2.HOUGH_GRADIENT, 1, constants.BALL_RADIUS-3, param1=300, param2=11, minRadius=constants.BALL_RADIUS-1, maxRadius=constants.BALL_RADIUS+3)

        if circles is not None:
            circles = np.round(circles[0, :]).astype("int")

            for (x_position, y_position, _) in circles:
                detected_balls.append((x_position, y_position, _))

        return detected_balls
