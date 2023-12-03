"""Bot Handling Module"""

import cv2
import numpy as np

from Logic.Detection.ball_classification import BallClassification
from Logic.Detection.ball_colour import BallColour
from Logic.Detection.ball_detection import BallDetection
from Logic.Path.ball_path import BallPath
from Logic.Path.vectors import Vectors


class Bot:
    """
    Responsible for handling the 8 balls game bot

    """

    balls = []
    holes = []

    vector = Vectors()
    ball_detection = BallDetection()
    ball_classification = BallClassification()

    def find_holes(self, frame):
        """
        Responsible for finding the holes if not set

        Args:
            frame (np.ndArray): The frame to find the holes in
        Returns:
            None
        """

        if not self.holes:
            corner_holes = self.ball_detection.find_corner_holes(frame)

            if len(corner_holes) == 4:
                self.holes = corner_holes

                board_positions = self.ball_detection.board_boundary(self.holes)

                self.holes.append(
                    (int(board_positions[0] + ((board_positions[2] - board_positions[0]) / 2)), board_positions[1]))
                self.holes.append(
                    (int(board_positions[0] + ((board_positions[2] - board_positions[0]) / 2)), board_positions[3]))

            # Debug only
            return corner_holes

    def find_balls(self, frame, options):
        """
        Responsible for finding the balls

        Args:
            frame (np.ndArray): The frame to find the balls in
            options (Options): The options to be used
        """

        board_positions = self.ball_detection.board_boundary(self.holes)

        board_frame = frame[board_positions[1]:board_positions[3], board_positions[0]:board_positions[2]]
        # board_frame_edges = cv2.Canny(board_frame, 200, 300)
        # Sharpening the image to increase ball detect accuracy
        blur = cv2.GaussianBlur(board_frame, (0, 0), 3)

        sharp_foreground = cv2.addWeighted(board_frame, 2, blur, -1, 0)
        sharp_foreground = np.maximum(sharp_foreground, 10)

        board_frame_edges = cv2.Canny(sharp_foreground, 200, 300)

        detected_balls = self.ball_detection.find_balls(board_frame_edges)

        if len(detected_balls) < 18:
            self.update_ball_structure(frame, board_positions, detected_balls, options)

    def update_ball_structure(self, frame, board_positions, detected_balls, options):
        """
        Responsible for handling updating the ball structure to assist the bot
        Args:
            frame (numpy): The frame to find the balls in
            board_positions (tuple): The board positions
            detected_balls (list): The detected balls
            options (Options): The options to be used

        """

        self.balls = []

        for ball in detected_balls:
            if ball is not None:
                new_ball_position = self.update_ball_positions(board_positions, ball)
                ball_colour = self.classify_ball_colours(frame, new_ball_position, options)

                self.balls.append((int(new_ball_position[0]), int(new_ball_position[1]), ball_colour))

    @staticmethod
    def update_ball_positions(board_positions, detected_ball):
        """
        Responsible for updating the ball position to map from board coordinates to entire frame coordinates

        Args:
            board_positions (tuple): The board positions
            detected_ball (tuple): The detected ball
        """

        return detected_ball[0] + board_positions[0], detected_ball[1] + board_positions[1]

    def classify_ball_colours(self, frame, detected_ball, options):
        """
        Responsible for classifying a ball

        Args:
            frame (numpy): The frame to find the balls in
            detected_ball (tuple): The detected ball
            options (Options): The options to be used
        """

        ball_colour = None

        ball_pixels = self.ball_classification.get_ball_pixels(frame, detected_ball, options)

        white_count = self.ball_classification.get_white_count(ball_pixels)
        black_count = self.ball_classification.get_black_count(ball_pixels) + 1  # avoid division by zero
        color_count = len(ball_pixels) - white_count - black_count
        total = len(ball_pixels)

        if self.ball_classification.is_white_ball(white_count, total):
            ball_colour = BallColour.White
        elif self.ball_classification.is_black_ball(black_count, total):
            ball_colour = BallColour.Black
        elif self.ball_classification.is_solid_ball(color_count, total):
            ball_colour = BallColour.Solid
        elif self.ball_classification.is_striped_ball(color_count, total):
            ball_colour = BallColour.Strip

        print(f"{ball_colour=}, {total=} {white_count=} {black_count=} {detected_ball=}")
        return ball_colour

    def find_optimal_path(self, options):
        """
        Responsible for initiating the find optimal path method

        Args:
            options (Options): The options to be used
        """

        # optimal_path = []
        # all_objects = self.balls + self.holes

        ball_path = BallPath(self.balls, self.holes, options)
        optimal_path = ball_path.find_path(options)

        return optimal_path
