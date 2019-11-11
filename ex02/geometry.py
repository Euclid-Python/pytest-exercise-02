import math
from math import cos, sin, acos, asin, sqrt, isclose, fabs, pi

""""
Module for simple geometry in 2D
"""


class Point:

    def __init__(self, x, y=None):
        self.x = float(x)
        self.y = float(y)

    @classmethod
    def new(cls, xy):
        return Point(xy[0], xy[1])

    def normal(self):
        """
        Make a pi/2 rotation of Point
        :return: another Point
        """
        return Point(-self.y, self.x)

    def reverse(self):
        """
        Inverse Point x -> -x, y -> -y
        :return: another Point
        """
        return Point(-self.x, -self.y)

    def normalize(self, d=0):
        """
        Normalize vector compared to distance d.
        if d is 0, d is the norm of Point (i.e. Distance)
        :param d:
        :return: another Point
        """
        if d == 0:
            d = sqrt(self.x * self.x + self.y * self.y)
        return Point(self.x / d, self.y / d)

    def scalar_product(self, other: 'Point'):
        return self.x * other.x + self.y * other.y

    def vectorial_product(self, other: 'Point'):
        return self.x*other.y - self.y*other.x

    def is_orthogonal(self, other: 'Point'):
        product = self.scalar_product(other)
        return isclose(product, 0)

    def is_collinear(self, other: 'Point'):
        return self.is_orthogonal(other.normal())

    def __add__(self, other: 'Point'):
        r = NotImplemented
        if isinstance(other, Point):
            r = Point(self.x + other.x, self.y + other.y)
        return r

    def __sub__(self, other: 'Point'):
        r = NotImplemented
        if isinstance(other, Point):
            r = Point(self.x - +other.x, self.y - other.y)
        return r

    def __mul__(self, other):
        r = NotImplemented
        if isinstance(other, float) or isinstance(other, int):
            factor = float(other)
            r = Point(self.x * factor, self.y * factor)
        return r

    def __eq__(self, other: 'Point'):
        r = NotImplemented
        if isinstance(other, tuple):
            other = Point.new(other)
        if isinstance(other, Point):
            r = isclose(self.x, other.x, abs_tol=1e-9) and isclose(self.y, other.y, abs_tol=1e-9)
        return r

    def __repr__(self):
        return f'p({self.x}, {self.y})'

    @staticmethod
    def distance(a: 'Point', b: 'Point') -> float:
        dx = a.x - b.x
        dy = a.y - b.y
        return sqrt(dx * dx + dy * dy)

class Line:
    def __init__(self, point: Point, vector: Point):
        self.point = point
        self.vector = vector.normalize()

    def contains(self, point: Point):
        a = self.point
        b = point
        v_ab = Point(a.x - b.x, a.y - b.y)
        return v_ab.is_collinear(self.vector)

    def intersection(self, line: 'Line') -> 'Point':
        """
        Find intersection between two lines
        :param line:
        :return:intersection point
        """
        v0 = self.vector
        p0 = self.point

        v1 = line.vector
        p1 = line.point

        v1_v0 = v1.scalar_product(v0)

        dp = p1 - p0

        dp_vo = dp.scalar_product(v0)
        dp_v1 = dp.scalar_product(v1)

        if isclose(fabs(v1_v0), 1.):
            raise ValueError('Lines are parallel')
        else:
            coef0 = (dp_vo - dp_v1 * v1_v0) / (1 - v1_v0 * v1_v0)

        return v0 * coef0 + p0

    def __repr__(self):
        return f'line({self.point}, {self.vector})'

class Arc:
    INDIRECT = "indirect"
    DIRECT = "direct"

    def __init__(self, start: Point, end: Point, start_tangent: Point, end_tangent: Point = None):
        self.start = start
        self.end = end
        if end_tangent is None:
            end_tangent = Geometry.get_symmetrical(start_tangent, (start - end))

        self.start_tangent = start_tangent
        self.end_tangent = end_tangent

        self.center = Arc.compute_center_from_both_tangents(start, end, start_tangent, end_tangent)
        self.check_center_and_tangents_coherence()

        self.radius = Point.distance(self.center, self.start)
        distance = Point.distance(start, end)
        if distance:
            self.angle = 2 * asin(distance / (2 * self.radius))
        else:
            self.angle = acos(start_tangent.scalar_product(end_tangent))

        self.direction = Arc.compute_direction(self)
        if self.direction is Arc.INDIRECT:
            self.angle = self.angle - 2*pi
        self.length = math.fabs(self.angle * pi * self.radius)


    @staticmethod
    def compute_center_from_both_tangents(p0, p1, tangent_p0, tangent_p1):
        try:
            center = Arc.compute_intersection_with_each_tangent(p0, p1, tangent_p0, tangent_p1)
        except ValueError:
            center = Point((p1.x + p0.x) / 2, (p1.y + p0.y) / 2)

        assert isclose(Point.distance(p0, center), Point.distance(p1, center))
        return center

    @staticmethod
    def compute_intersection_with_each_tangent(p0, p1, tangent_p0, tangent_p1):
        """
        Computes center from both tangents, from the fist point and the second point.
        :param p0: Point the first point of the Arc
        :param p1: Point  the second point of the Arc
        :param tangent_p0: Point the tangent vector of first point of the Arc
        :param tangent_p1: Point the tangent vector of 2nd point of the Arc
        :return: intersection of normal lines to vectors, aka the center
        """
        radial_p0 = tangent_p0.normal()
        radial_p1 = tangent_p1.normal()
        line_p0 = Line(p0, radial_p0)
        line_p1 = Line(p1, radial_p1)
        center = line_p0.intersection(line_p1)
        d0 = Point.distance(p0, center)
        d1 = Point.distance(p1, center)
        return center

    @staticmethod
    def find_angle_and_chord_vector(start, end, tangent):
        a = start
        b = end
        v = tangent

        distance = Point.distance(a, b)
        u = Point(b.x - a.x, b.y - a.y)
        u = u.normalize(distance)
        v = v.normalize()
        angle = acos(u.scalar_product(v))
        sign = u.x * v.y + u.y * v.x
        angle = 2 * angle * sign

        return angle, u, distance

    def check_center_and_tangents_coherence(self):
        """
        Tangents have to turn in the same direction from the center.
        :return:
        """
        v_start = (self.start -self.center).vectorial_product(self.start_tangent)
        v_end = (self.end -self.center).vectorial_product(self.end_tangent)
        if not isclose(v_start, v_end):
            raise ValueError()

    @staticmethod
    def compute_direction(arc: 'Arc'):
        v = (arc.center - arc.start).vectorial_product(arc.start_tangent)
        if v > 0:
            return Arc.INDIRECT
        return Arc.DIRECT




class Geometry:

    @staticmethod
    def transpose_rotation_relative_to(vector, reference):
        reference = reference.normalize()
        cos_ = reference.x
        sin_ = reference.y
        x = vector.x * cos_ + vector.y * sin_
        y = - vector.x * sin_ + vector.y * cos_
        return Point(x, y)


    @staticmethod
    def get_symmetrical(vector, axe):
        symmetrical = Geometry.transpose_rotation_relative_to(vector, axe)
        symmetrical = Point(symmetrical.x, -symmetrical.y)
        return Geometry.transpose_rotation_relative_to(symmetrical, Point(axe.x, - axe.y))



