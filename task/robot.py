import json
from collections import defaultdict
from functools import wraps
from typing import Callable, Tuple

import numpy as np

from task.field import Field


class FieldError(Exception):
    """Exception that raises when a robot not in a field
    but should be."""


class Robot:
    """
    A class for robot simulation.

    Robot instance can perform* the folowing commands:
        - left: move to the left cell.
        - right: move to the right cell.
        - up: move to the upper cell.
        - down: move to the bottom cell.
        - turn_left: turn counterclockwise.
        - turn_right: turn clockwise.
        - turn_back: turn 180 degrees.
        - look: look at the field along the radius
                specified by the 'light_radius' argument.
        - save: save all informations about robot movement to
                json file.

    * To perform commands, the robot should be putted in a field
      via 'put_in_field' method.

    After each movement command the robot report information:
    previous and current position and direction.

    Args:
        light_radius: radius the robot can see. The robot can see cells
                      to which the Euclidean distance does not exceed
                      the radius.
        logfile_path: the path to the json file to store
                      the movement information.

    Attributes:
        x, y**: current coordinates of the robot.
        field**: the field where the robot is located.
        direction**: current direction of the robot. Can be
                   'up', 'down', 'left' and 'right'.
        step**: current step. Step is incremented each time the robot
              moves or turns.
        movement_history**: dictionary to store information about
                            movements and turns.
        robot_code: the number to represent robot in a field matrix.
                    Should be different from numbers for walls and
                    bariers in a field. (Needed for 'look' method).
        logfile_path: same that 'logfile_path' in Args.
        light_radius: same that 'light_radius' in Args.
        light_color: the color that will display the radius
                     of the robot's view.
        robot_color: the color of a cell with a robot.
        direction_view: the dictionary that maps robot's direction and
                        its representation.

        ** All these attributes are None if the robot not in any field.
    """

    def __init__(self, light_radius: int, logfile_path: str = "./robot_path.json"):
        self.x, self.y = None, None
        self.field = None
        self.direction = None
        self.step = None
        self.movement_history = None

        self.robot_code = 3
        self.logfile_path = logfile_path

        self.light_radius = light_radius
        self.light_color = "\33[43m"
        self.robot_color = "\33[42m"

        self.direction_view = {"up": "^", "down": "=", "right": ">", "left": "<"}

    def put_in_field(self, field: Field):
        """Put the robot in the field.

        Args:
            field: the field to put robot in.
        """
        self.field = field
        self.x, self.y = field.get_closest_to_center_available_point()
        self.direction = "up"
        self.step = 0
        self.movement_history = defaultdict(dict)

    def check_field(self):
        """Checks if the robot is putted in a field.

        Raises:
            FieldError: if the robot not in a field.
        """
        if self.field is None:
            raise FieldError("The robot should be in the field.")

    def verify_cell_and_move_if_possible(self, cell: Tuple[int]):
        """Check 'cell'. If it is wall or barier, the robot
        stays in place. If not, the robot moves in it.

        Args:
            cell: cell the robot is trying to move to.
        """
        cell_value = self.field.field[cell]

        wall_or_barier = {1: "barier", 2: "wall"}

        if cell_value in (1, 2):
            print(f"There is a {wall_or_barier[cell_value]} where you want to go.")
            print(f"Stay on ({self.x}, {self.y}) position.")
            return

        self.x, self.y = cell

    def print_step_log(self, step_log: dict):
        """Prints information about current step movements and turns.

        Args:
            step_log: dictionary that stores information about
                      current step movements and turns.
        """
        print(f"Previous position: {step_log['previous_position']}")
        print(f"Previous direction: {step_log['previous_direction']}")
        print(f"Current position: {step_log['current_position']}")
        print(f"Current direction: {step_log['current_direction']}")

    class Decorators:
        @staticmethod
        def save_and_print_path(func) -> Callable:
            """Decorator that prints and saves report information.
            Also checks if the robot in a field. If not, raises
            FieldError.

            Args:
                func: movement function.

            Returns:
                changed function.
            """

            @wraps(func)
            def wrapper(*args, **kwargs):
                self = args[0]
                self.check_field()
                step_log = self.movement_history[self.step]
                step_log["previous_position"] = (int(self.x), int(self.y))
                step_log["previous_direction"] = self.direction
                func(*args, **kwargs)
                step_log["current_position"] = (int(self.x), int(self.y))
                step_log["current_direction"] = self.direction
                self.print_step_log(step_log)
                self.step += 1

            return wrapper

    def look_around(self):
        """Prints the robot's area of visibility to the terminal."""

        def make_radius_slice(coord: Tuple[int]) -> slice:
            """Make slice for minimal rectangle side that includes
            robot's visiability. Will not capture anything behind
            the walls.

            Args:
                coord: coordinate with the robot.

            Returns:
                corresponding slice.
            """
            return slice(
                max(0, coord - self.light_radius), coord + self.light_radius + 1
            )

        field = self.field.field
        field[self.x, self.y] = self.robot_code

        # Making minimal rectangle that includes robot's visiability.
        x_slice = make_radius_slice(self.x)
        y_slice = make_radius_slice(self.y)
        rectange_around_robot = field[x_slice, y_slice]

        # Finding robot position in the rectangle around robot.
        robot_rectange_x, robot_rectange_y = np.where(
            rectange_around_robot == self.robot_code
        )
        robot_rectange_x, robot_rectange_y = robot_rectange_x[0], robot_rectange_y[0]

        field[self.x, self.y] = 0

        # Calculating the distance from the robot for each
        # cell in the rectangle.
        rectangle_x_size, rectangle_y_size = rectange_around_robot.shape
        x_grid, y_grid = np.ogrid[:rectangle_x_size, :rectangle_y_size]
        dist_from_robot = np.sqrt(
            (x_grid - robot_rectange_x) ** 2 + (y_grid - robot_rectange_y) ** 2
        )

        # Bool array with the same shape as rectangle.
        # Represents cells the robot can see.
        mask = dist_from_robot <= self.light_radius

        # Making rectangle representation.
        view = self.field.get_matrix_view(rectange_around_robot)
        view[robot_rectange_x][robot_rectange_y] = self.direction_view[self.direction]

        def in_color(value, flag):
            current_view = self.direction_view[self.direction]
            color = self.robot_color if value == current_view else self.light_color
            return color + value + "\033[0m" if flag else " "

        print(
            "\n".join(
                [
                    "".join(
                        [in_color(value, flag) for value, flag in zip(row, mask_row)]
                    )
                    for row, mask_row in zip(view, mask)
                ]
            )
        )

    @Decorators.save_and_print_path
    def left(self):
        """Moves the robot to the left cell."""
        left_cell = (self.x, self.y - 1)
        self.verify_cell_and_move_if_possible(left_cell)

    @Decorators.save_and_print_path
    def right(self):
        """Moves the robot to the right cell."""
        right_cell = (self.x, self.y + 1)
        self.verify_cell_and_move_if_possible(right_cell)

    @Decorators.save_and_print_path
    def up(self):
        """Moves the robot to the upper cell."""
        upper_cell = (self.x - 1, self.y)
        self.verify_cell_and_move_if_possible(upper_cell)

    @Decorators.save_and_print_path
    def down(self):
        """Moves the robot to the bottom cell."""
        bottom_cell = (self.x + 1, self.y)
        self.verify_cell_and_move_if_possible(bottom_cell)

    @Decorators.save_and_print_path
    def turn_back(self):
        """Turns the robot 180 degrees."""
        halfturn = {"up": "down", "down": "up", "left": "right", "right": "left"}
        self.direction = halfturn[self.direction]

    @Decorators.save_and_print_path
    def turn_left(self):
        """Turns the robot counterclockwise."""
        counterclockwise = {
            "up": "left",
            "left": "down",
            "down": "right",
            "right": "up",
        }
        self.direction = counterclockwise[self.direction]

    @Decorators.save_and_print_path
    def turn_right(self):
        """Turns the robot clockwise."""
        clockwise = {"up": "right", "right": "down", "down": "left", "left": "up"}
        self.direction = clockwise[self.direction]

    def save_path(self):
        """Saves movement history to 'self.logfile_path'."""
        with open(self.logfile_path, "w") as file:
            json.dump(self.movement_history, file, indent=4)
