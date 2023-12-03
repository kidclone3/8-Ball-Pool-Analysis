"""Ball Classification Module"""

import math


class BallClassification:
    """Responsible for classifying game balls"""

    @staticmethod
    def get_ball_radius(x_position, y_position, options):
        """
        Calculate radius from ball point

        Args:
            x_position (int): The x position of the ball
            y_position (int): The y position of the ball
            options (Options): The options to be used
        """

        return math.sqrt(math.pow(options.ball_radius - x_position, 2) + math.pow(options.ball_radius - y_position, 2))

    def get_ball_pixels(self, frame, position, options):
        """
        Responsible for returning an array of pixels that represent the circle

        Args:
            frame (numpy): The frame to find the balls in
            position (tuple): The position of the ball
            options (Options): The options to be used
        """

        ball_pixels = []

        min_x_position = int(position[0] - options.ball_radius)
        min_y_position = int(position[1] - options.ball_radius)
        max_x_position = int(position[0] + options.ball_radius)
        max_y_position = int(position[1] + options.ball_radius)

        ball_frame = frame[min_y_position:max_y_position, min_x_position:max_x_position].copy()

        for x_position, _ in enumerate(ball_frame[0:-1]):
            for y_position, _ in enumerate(ball_frame[0:-1]):
                if self.get_ball_radius(x_position, y_position, options) < options.ball_radius:
                    ball_pixels.append(ball_frame[x_position][y_position])

        return ball_pixels

    @staticmethod
    def get_white_count(ball_pixels):
        """
        Finding the number of white pixels within the ball pixels

        Args:
            ball_pixels (list): The ball pixels
        """

        white_count = 0

        for pixel in ball_pixels:
            is_b_valid = 192 <= pixel[0] <= 255
            is_g_valid = 192 <= pixel[1] <= 255
            is_r_valid = 192 <= pixel[2] <= 255

            if is_b_valid and is_g_valid and is_r_valid:
                white_count += 1

        return white_count

    @staticmethod
    def get_black_count(ball_pixels):
        """
        Finding the number of black pixels within the ball pixels

        Args:
            ball_pixels (list): The ball pixels
        """

        black_count = 0

        for pixel in ball_pixels:
            is_b_valid = 0 <= pixel[0] <= 64
            is_g_valid = 0 <= pixel[1] <= 64
            is_r_valid = 0 <= pixel[2] <= 64

            if is_b_valid and is_g_valid and is_r_valid:
                black_count += 1

        return black_count

    @staticmethod
    def is_solid_ball(color_count, total):
        """
        Checking whether the pixel count is a solid ball

        Args:
            color_count (int): The color pixel count
            total (int): The total pixel count
        """

        return color_count / total >= 0.8

    @staticmethod
    def is_striped_ball(color_count, total):
        """
        Checking whether the pixel count is a striped ball

        Args:
            color_count (int): The color pixel count
            total (int): The total pixel count
        """

        return color_count / total >= 0.2

    @staticmethod
    def is_black_ball(black_count, total):
        """
        Checking whether the pixel count is a black ball

        Args:
            black_count (int): The black pixel count
            total (int): The total pixel count
        """

        return black_count / total >= 0.5

    @staticmethod
    def is_white_ball(white_count, total):
        """
        Checking whether the pixel count is a white ball

        Args:
            white_count (int): The white pixel count
            total (int): The total pixel count
        """

        return white_count / total >= 0.95

