"""Options Module"""

from Logic.Detection.ball_colour import BallColour


class Options:
    """
    Responsible for handling the program options

    Parameters:
    - args: argparse.Namespace
        An argparse namespace containing the following attributes:

        - ball_radius: List[float]
            Radius of the billiard balls.
        - hole_radius: List[float]
            Radius of the pockets (holes) on the billiard table.
        - border_distance: List[float]
            Distance between the table border and the playing area.
        - target_balls: List[str]
            Type of target balls, either 'solid' or 'stripe'.
        - input_video: str
            Path to the input video file.
        - output_video: str
            Path to save the output video file.
        - skip_frame: List[int]
            Number of frames to skip in the input video processing.
        - show_video: bool
            Flag indicating whether to display the processed video.
        - save_video: bool
            Flag indicating whether to save the processed video.


    """
    def __init__(self, args):
        self.ball_radius = args.ball_radius[0]
        self.ball_diameter = args.ball_radius[0] * 2.2

        self.hole_radius = args.hole_radius[0]
        self.border_distance = args.border_distance[0]

        self.middle_hole_radius = int(args.border_distance[0] * 1.2)
        self.corner_hole_radius = int(args.border_distance[0] * 2.6)

        self.middle_border_radius = int(args.border_distance[0] * 0.8)
        self.corner_border_radius = int(args.border_distance[0] * 2.8)

        self.target_ball_colour = BallColour.Solid if args.target_balls[0] == 'solid' else BallColour.Strip

        self.input_video = args.input_video
        self.output_video = args.output_video

        self.skip_frame = args.skip_frame[0]

        self.show_video = args.show_video
        self.save_video = args.save_video
