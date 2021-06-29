import numpy as np
import pytest

from task.field import Field
from task.robot import Robot


@pytest.fixture()
def test_field():
    matrix = np.array(
        [
            [1, 0, 1],
            [0, 0, 0],
            [1, 0, 1],
        ]
    )

    return Field(matrix)


@pytest.fixture()
def test_robot():
    return Robot(light_radius=1)
