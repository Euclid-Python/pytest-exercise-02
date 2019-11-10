from ex02.geometry import Point, Line
import pytest
from math import sin, pi, cos, exp, log


def test_coordinate_belongs_to_Line():
    A = Point(1, 2)
    line = Line(point=A, vector=Point(1, 1))
    assert line.contains(Point(2, 3))

def test_intersection():
    line_a = Line(point=Point(0, 0), vector=Point(1, 0))
    line_b = Line(point=Point(0, 0), vector=Point(0, 1))
    assert line_a.intersection(line_b) == Point(0, 0)


def test_intersection_2():
    line_a = Line(point=Point(3, 1), vector=Point(1, 1))
    line_b = Line(point=Point(0, 2), vector=Point(1, 0))
    intersection = line_a.intersection(line_b)
    expected = Point(4, 2)
    assert intersection == expected, f'{intersection} != {expected}'


def test_intersection_of_parallel_lines():
    line_a = Line(point=Point(0, 1), vector=Point(0, 1))
    line_b = Line(point=Point(1, 1), vector=Point(0, 1))

    with pytest.raises(ValueError):
        line_a.intersection(line_b)
