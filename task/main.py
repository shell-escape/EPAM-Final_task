import argparse

from task.field import Field
from task.robot import Robot

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A robot simulation.")

    parser.add_argument(
        "--n_rows", type=int, help="The number of rows in a generated field."
    )
    parser.add_argument(
        "--n_cols", type=int, help="The number of columns in a generated field."
    )
    parser.add_argument(
        "--p",
        type=float,
        help="The probability that a cell will be a barrier. Shoul be in [0, 1] range.",
    )
    parser.add_argument("--radius", type=int, help="The radius the robot can see.")
    parser.add_argument(
        "--logfile",
        default="./robot_path.json",
        help="The path to the json file to store the movement information.",
    )

    args = parser.parse_args()

    field = Field.generate_field(n_rows=args.n_rows, n_cols=args.n_cols, p=args.p)
    robot = Robot(light_radius=args.radius, logfile_path=args.logfile)

    robot.put_in_field(field)

    commands = {
        "left": robot.left,
        "right": robot.right,
        "up": robot.up,
        "down": robot.down,
        "turn_left": robot.turn_left,
        "turn_right": robot.turn_right,
        "turn_back": robot.turn_back,
        "look": robot.look_around,
        "save": robot.save_path,
    }

    while True:
        command = input()

        if command in ["exit", "stop", "quit"]:
            break

        if command not in commands:
            print("wrong command")
            continue

        commands[command]()
