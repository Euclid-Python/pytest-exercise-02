import pytest

from ex02.geometry import Point, Geometry

NORTH = Point(0, 1)
SOUTH = Point(0, -1)
WEST = Point(-1, 0)
EAST = Point(1, 0)
NORTH_EAST = (NORTH + EAST).normalize()
NORTH_WEST = (NORTH + WEST).normalize()
SOUTH_EAST = (SOUTH + EAST).normalize()
SOUTH_WEST = (SOUTH + WEST).normalize()


@pytest.mark.parametrize("vector, reference, expected", [
    (NORTH, EAST, NORTH),
    (NORTH, NORTH, EAST),
    (WEST, NORTH, NORTH),
    (EAST, NORTH, SOUTH),
    (SOUTH, NORTH, WEST),
    (NORTH, SOUTH, WEST),
    (WEST, SOUTH, SOUTH),
    (EAST, SOUTH, NORTH),
    (SOUTH, SOUTH, EAST),
    (NORTH * 2, EAST, NORTH * 2),
    (NORTH * -5, NORTH, EAST * -5),
    (NORTH, NORTH_EAST, NORTH_EAST),
    (NORTH, SOUTH_WEST, SOUTH_WEST),
])
def test_rotate_from_axe(vector, reference, expected):
    assert Geometry.transpose_rotation_relative_to(vector, reference) == expected
    # Reverse
    assert Geometry.transpose_rotation_relative_to(expected, Point(reference.x, - reference.y)) == vector


def test_rotate_from_axe_with_null():
    # when
    vector = Point(0, 0)
    reference = NORTH_WEST
    assert Geometry.transpose_rotation_relative_to(vector, reference) == vector


def test_rotate_from_axe_with_reference_null():
    # when
    vector = NORTH
    reference = Point(0, 0)
    with pytest.raises(ZeroDivisionError):
        Geometry.transpose_rotation_relative_to(vector, reference)


@pytest.mark.parametrize("vector, axe, expected", [
    (NORTH, EAST, SOUTH),
    (NORTH, NORTH, NORTH),
    (NORTH, NORTH_EAST, EAST),
    (NORTH, SOUTH_WEST, EAST),
    (NORTH_EAST, NORTH, NORTH_WEST),
    (NORTH_EAST * 2.3, NORTH, NORTH_WEST * 2.3),
])
def test_geometry_get_symmetrical(vector, axe, expected):
    assert expected == Geometry.get_symmetrical(vector, axe)
