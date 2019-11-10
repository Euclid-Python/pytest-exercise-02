from ex02.geometry import Point
from math import sin, pi, cos, exp, log


def test_add():
    a = Point(0.5, 0.5)
    b = Point(-1, 1)
    c = a + b
    assert c.x == -0.5
    assert c.y == 1.5


def test_equal():
    a = Point(0.5, 0.5)
    b = Point(0.5, 0.5)
    assert a == b

def test_equal_float():
    a = Point(1,1)
    approx= 1+1e-14
    assert a == Point(approx, approx)


def test_equal_tuple():
    a = Point(1.0, 4.0)
    assert a == (1, 4)


def test_are_orthogonal():
    a = Point(0.5, 0.5)
    b = Point(-1, 1)
    assert a.is_orthogonal(b)


def test_are_not_orthogonal():
    a = Point(1, 0.7)
    b = Point(0.5, 1)
    assert not a.is_orthogonal(b)


def test_are_collinear():
    a = Point(0.5, 0.5)
    b = Point(1, 1)
    assert a.is_collinear(b)
