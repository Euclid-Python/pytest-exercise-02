import math

from ex02.geometry import Arc, Point


class TestArcExercise_2_4:
    def test_45deg_arc(self):
        candidate = Arc(Point(1, 0),
                        Point(0, 1),
                        Point(0, 1))

        assert math.isclose(candidate.angle, math.pi / 2)
        assert candidate.center == Point(0, 0)
        assert math.isclose(candidate.radius, 1)
        assert candidate.direction == Arc.DIRECT

    def test_reverse_45deg_arc_BUG(self):
        candidate = Arc(start=Point(1, 0),
                        end=Point(0, 1),
                        start_tangent=Point(0, -1))

        assert candidate.center == Point(0, 0)
        assert math.isclose(candidate.radius, 1)
        assert candidate.end_tangent == Point(1, 0)
        assert math.isclose(candidate.angle, -3 * math.pi / 2)
        assert candidate.direction == Arc.INDIRECT
        assert candidate.length > 0
