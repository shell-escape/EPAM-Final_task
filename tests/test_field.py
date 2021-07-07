import numpy as np

from task.field import Field


def test_wall_added(test_field):
    """Testing that walls are added properly."""
    field_with_walls = np.array(
        [
            [2, 2, 2, 2, 2],
            [2, 1, 0, 1, 2],
            [2, 0, 0, 0, 2],
            [2, 1, 0, 1, 2],
            [2, 2, 2, 2, 2],
        ]
    )

    assert np.array_equal(test_field.field, field_with_walls) is True


def test_get_closest_to_center_available_point_method(test_field):
    """Testing 'get_closest_to_center_available_point' method."""
    closest_point = test_field.get_closest_to_center_available_point()
    assert closest_point == (2, 2)

    odd_matrix_with_barier_in_center = np.array(
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0],
        ]
    )
    odd_test_field = Field(odd_matrix_with_barier_in_center)
    closest_point = odd_test_field.get_closest_to_center_available_point()
    assert closest_point == (1, 2)

    even_matrix = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
    even_test_field = Field(even_matrix)
    closest_point = even_test_field.get_closest_to_center_available_point()
    assert closest_point == (2, 2)


def test_get_row_view_method(test_field):
    """Testing 'get_row_view' method."""
    row = test_field.field[1]
    view = test_field.get_row_view(row)

    space = test_field.space_view
    wall = test_field.wall_view
    barier = test_field.barier_view

    assert view == [wall, barier, space, barier, wall]


def test_get_matrix_view_method(test_field):
    """Testing 'get_matrix_view' method."""
    field = test_field.field
    view = test_field.get_matrix_view(field)

    space = test_field.space_view
    wall = test_field.wall_view
    barier = test_field.barier_view

    assert view == [
        [wall, wall, wall, wall, wall],
        [wall, barier, space, barier, wall],
        [wall, space, space, space, wall],
        [wall, barier, space, barier, wall],
        [wall, wall, wall, wall, wall],
    ]
