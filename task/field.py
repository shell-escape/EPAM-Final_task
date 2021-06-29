from typing import List, Tuple

import numpy as np


class Field:
    """
    A field that robot will explore.

    This class represents a field of [x, y] size. The field contains
    barriers that cannot be passed by a robot. A field can be generated
    via 'generate_field' classmethod or given by a numpy array.

    Args:
        matrix: an array that represents field. '0' means empty space,
                '1' means barrier.

    Attributes:
        field: full matrix (with 'walls' on the border).
               'Wall' is denoted by '2' in the array.
        space_view: ascii sign for empty space view.
        wall_view: ascii sign for wall view.
        barier_view: ascii sign for barier view.
        cell_value_views: a dictionary that maps numbers in
                          array to ascii views.
    """

    def __init__(self, matrix: np.ndarray):
        matrix_with_walls = np.full((matrix.shape[0] + 2, matrix.shape[1] + 2), 2)
        matrix_with_walls[1:-1, 1:-1] = matrix

        self.field: np.dnarray = matrix_with_walls

        self.space_view = "."
        self.wall_view = "x"
        self.barier_view = "+"

        self.cell_value_views = {
            0: self.space_view,
            1: self.barier_view,
            2: self.wall_view,
        }

    @classmethod
    def generate_field(cls, n_rows: int, n_cols: int, p: float) -> "Field":
        """Generates a Field object with random matrix
        of size ['n_rows', 'n_cols'].

        Args:
            n_rows: the number of rows in generated matrix.
            n_cols: the number of columns in generated matrix.
            p: the probability that a cell will be a barrier.
               Should be in [0, 1] range.

        Returns:
            A Field object.
        """
        matrix = np.random.choice(np.array([0, 1]), size=(n_rows, n_cols), p=[1 - p, p])
        return cls(matrix)

    def get_closest_to_center_available_point(self) -> Tuple[int]:
        """Finds the coordinates of the empty point closest
        to the center of the field.

        Returns:
            Corresponding coordinates.
        """
        zero_rows, zero_columns = np.where(self.field == 0)
        pairs_of_indices_where_zeros = zip(zero_rows, zero_columns)

        center = ((self.field.shape[0] - 1) / 2, (self.field.shape[1] - 1) / 2)

        def distance_to_center(cell: Tuple[int]) -> float:
            """Finds the distance from 'cell' to the field center.

            Args:
                cell: cell coordinates.

            Returns:
                the distance from the center.
            """
            return np.sqrt((cell[0] - center[0]) ** 2 + (cell[1] - center[1]) ** 2)

        return min(pairs_of_indices_where_zeros, key=distance_to_center)

    def get_row_view(self, row: np.ndarray) -> List[str]:
        """Represents a numpy array row as ascii symbols.

        Args:
            row: 1-dimensional numpy array (a field row).

        Returns:
            a list with a row as ascii symbols
            from 'self.cell_value_views'.
        """
        return [self.cell_value_views[cell_value] for cell_value in row]

    def get_matrix_view(self, matrix: np.ndarray) -> List[List[str]]:
        """Represents a numpy array as ascii symbols.

        Args:
            matrix: 2-dimensional numpy array (a field).

        Returns:
            a list with a matrix as ascii symbols
            from 'self.cell_value_views'.
        """
        return [self.get_row_view(row) for row in matrix]
