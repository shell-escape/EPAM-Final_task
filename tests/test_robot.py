import pytest

from task.robot import FieldError


def test_put_in_field_method(test_robot, test_field):
    """Testing 'put_in_field' method."""
    test_robot.put_in_field(test_field)

    assert test_robot.field == test_field
    assert test_robot.x == 2
    assert test_robot.y == 2
    assert test_robot.direction == "up"
    assert test_robot.step == 0


def test_check_field_method(test_robot):
    """Testing "check_field" method."""

    with pytest.raises(FieldError, match="The robot should be in the field."):
        test_robot.left()


def test_verify_cell_and_move_if_possible_method(test_robot, test_field):
    """Testing 'verify_cell_and_move_if_possible' method."""
    test_robot.put_in_field(test_field)

    upper_cell = (1, 2)
    test_robot.verify_cell_and_move_if_possible(upper_cell)

    assert test_robot.x == 1
    assert test_robot.y == 2

    left_barier_cell = (1, 1)
    test_robot.verify_cell_and_move_if_possible(left_barier_cell)

    assert test_robot.x == 1
    assert test_robot.y == 2

    upper_wall_cell = (1, 1)
    test_robot.verify_cell_and_move_if_possible(upper_wall_cell)

    assert test_robot.x == 1
    assert test_robot.y == 2


def test_save_and_print_path_method(test_robot, test_field, capsys):
    """Testing 'save_and_print_path' method."""
    test_robot.put_in_field(test_field)
    test_robot.left()

    step_log = test_robot.movement_history[0]

    previous_position = step_log["previous_position"]
    previous_direction = step_log["previous_direction"]
    current_position = step_log["current_position"]
    current_direction = step_log["current_direction"]

    assert previous_position == (2, 2)
    assert previous_direction == "up"
    assert current_position == (2, 1)
    assert current_direction == "up"

    out, _ = capsys.readouterr()
    out = out.split("\n")

    assert out[0] == "Previous position: (2, 2)"
    assert out[1] == "Previous direction: up"
    assert out[2] == "Current position: (2, 1)"
    assert out[3] == "Current direction: up"

    assert test_robot.step == 1


def test_left_command(test_robot, test_field):
    """Testing left command."""
    test_robot.put_in_field(test_field)
    test_robot.left()

    assert test_robot.x == 2
    assert test_robot.y == 1


def test_right_command(test_robot, test_field):
    """Testing right command."""
    test_robot.put_in_field(test_field)
    test_robot.right()

    assert test_robot.x == 2
    assert test_robot.y == 3


def test_up_command(test_robot, test_field):
    """Testing up command."""
    test_robot.put_in_field(test_field)
    test_robot.up()

    assert test_robot.x == 1
    assert test_robot.y == 2


def test_down_command(test_robot, test_field):
    """Testing down command."""
    test_robot.put_in_field(test_field)
    test_robot.down()

    assert test_robot.x == 3
    assert test_robot.y == 2


def test_turn_left_command(test_robot, test_field):
    """Testing turn_left command."""
    test_robot.put_in_field(test_field)

    test_robot.turn_left()
    assert test_robot.direction == "left"

    test_robot.turn_left()
    assert test_robot.direction == "down"

    test_robot.turn_left()
    assert test_robot.direction == "right"

    test_robot.turn_left()
    assert test_robot.direction == "up"


def test_turn_right_command(test_robot, test_field):
    """Testing turn_right command."""
    test_robot.put_in_field(test_field)

    test_robot.turn_right()
    assert test_robot.direction == "right"

    test_robot.turn_right()
    assert test_robot.direction == "down"

    test_robot.turn_right()
    assert test_robot.direction == "left"

    test_robot.turn_right()
    assert test_robot.direction == "up"


def test_turn_back_command(test_robot, test_field):
    """Testing turn_back command."""
    test_robot.put_in_field(test_field)

    test_robot.turn_back()
    assert test_robot.direction == "down"

    test_robot.turn_back()
    assert test_robot.direction == "up"


def test_look_around_method(test_robot, test_field, capsys):
    """Testing 'look_around' method."""
    test_robot.put_in_field(test_field)

    test_robot.look_around()

    out, _ = capsys.readouterr()
    out = out.split("\n")

    def in_color(value):
        r_view = test_robot.direction_view[test_robot.direction]
        color = test_robot.robot_color if value == r_view else test_robot.light_color
        return color + value + "\033[0m"

    space = test_field.space_view
    wall = test_field.wall_view
    barier = test_field.barier_view
    r_view = test_robot.direction_view[test_robot.direction]

    assert out[0] == " " + in_color(space) + " "
    assert out[1] == in_color(space) + in_color(r_view) + in_color(space)
    assert out[2] == " " + in_color(space) + " "

    test_robot.right()
    out, _ = capsys.readouterr()

    test_robot.look_around()
    out, _ = capsys.readouterr()
    out = out.split("\n")

    assert out[0] == " " + in_color(barier) + " "
    assert out[1] == in_color(space) + in_color(r_view) + in_color(wall)
    assert out[2] == " " + in_color(barier) + " "
