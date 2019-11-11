from ex02.geometry import Point, Arc


class Translation:

    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.length = self._get_length()
        self.vector = (end - start).normalize()

    def _get_length(self):
        return Point.distance(self.start, self.end)

    def get_length(self):
        return self.length

    def is_parallel_with(self, other: 'Translation'):
        return self.vector.is_collinear(other.vector)

    def __repr__(self):
        return f'start={self.start}, end={self.end}, len={self.length}, vector={self.vector}'


class Rotation:

    def __init__(self, start: Point, end: Point, start_vector: Point, end_vector: Point):
        self.arc = Arc(start, end, start_vector, end_vector)

    def get_length(self):
        return self.arc.length

    def is_on_the_spot(self) -> bool:
        """
        Indicates if rotation is on _the spot, i.e. with a radius == 0
        :return: True if is on the spot
        """
        return self.arc.radius == 0

    @classmethod
    def new_from_translations(cls, previous_move, move):
        return Rotation(previous_move.end, move.start, previous_move.vector, move.vector)

    def __repr__(self):
        return f'start={self.arc.start}, end={self.arc.end}, radius={self.arc.radius}, ' \
               f'start_vector={self.arc.start_tangent},' \
               f'end_vector={self.arc.end_tangent}'