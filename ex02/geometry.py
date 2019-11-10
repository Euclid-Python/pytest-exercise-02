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



