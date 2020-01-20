import operator
from typing import List, Optional, Union, Tuple
from collections import namedtuple
import numbers


class Point(object):
    __slots__ = ['x', 'y']

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other: 'Point'):
        return self.x == other.x & self.y == other.y

    def __add__(self, other: 'Point'):
        if not isinstance(other, Point):
            raise NotImplemented
        return Point(self.x + other.x, self.y + other.y)


    def __sub__(self, other: 'Point'):
        if not isinstance(other, Point):
            raise NotImplemented
        return Point(self.x - other.x, self.y - other.y)


    def __mul__(self, other: numbers.Number):
        # Scalar Multiplication
        if not isinstance(other, numbers.Number):
            raise NotImplemented
        return Point(self.x * other, self.y * other)

    def __rmul__(self, other: numbers.Number):
        # Scalar Multiplication
        if not isinstance(other, numbers.Number):
            raise NotImplemented
        return Point(self.x * other, self.y * other)

    def __repr__(self) -> str:
        return(f'{self.__class__.__name__}(x={self.x}, y={self.y})')

    def manhattan_distance(self) -> int:
        other = Point(0,0)
        return abs(self.x - other.x) + abs(self.y - other.y)

    def on_segment(self, line_segment: 'LineSegment') -> Optional['LineSegment']:
        # If point is on the segment, return a LineSegment between point_1 and this point
        if isinstance(line_segment, LineSegment):
            if (line_segment.orientation == 'V' and self.x == line_segment.point_1.x) or (line_segment.orientation == 'H' and self.y == line_segment.point_1.y):
                return LineSegment(line_segment.point_1, self)
            else:
                return None
        else:
            return NotImplemented


class LineSegment(object):
    __slots__ = ['point_1', 'point_2', 'orientation']

    def __init__(self, point_1: Point, point_2: Point):
        self.point_1 = point_1
        self.point_2 = point_2
        if point_1.x == point_2.x and point_1.y != point_2.y:
            self.orientation = 'V'
        elif point_1.y == point_2.y and point_1.x != point_2.x:
            self.orientation = 'H'

    def __repr__(self) -> str:
        return(f'{self.__class__.__name__}(point_1={repr(self.point_1)}, point_2={repr(self.point_2)})')

    
    @classmethod
    def from_manhattan_vector(cls, origin: Point, vector: str):
        # Vector begins with UDLR and then an integer
        direction_map = {
            'U': Point(0,1),
            'D': Point(0,-1),
            'R': Point(1,0),
            'L': Point(-1,0),
        }
        if vector[0] not in direction_map.keys() or not vector[1:].isdigit():
            raise NotImplemented
        destination = direction_map[vector[0]] * int(vector[1:]) + origin
        return cls(origin, destination)

    @property
    def length(self) -> int:
        if self.orientation == 'H':
            return abs(self.point_2.x - self.point_1.x)
        else:
            return abs(self.point_2.y - self.point_1.y)


    def intersects(self, other_linesegment: 'LineSegment') -> Optional[Point]:
        # If this LineSegment intersects another LineSegment, then return the point that they intersect. Otherwise return None
        # If line segments are colinear, or start and end on each other we should return None
        if not isinstance(other_linesegment, LineSegment):
            raise NotImplementedError
        # TODO Fix this yucky mess pls
        if self.orientation == 'H' and other_linesegment.orientation == 'V':
            if ((self.point_1.x < other_linesegment.point_1.x < self.point_2.x) or \
            (self.point_1.x > other_linesegment.point_1.x > self.point_2.x)) and \
            ((other_linesegment.point_1.y < self.point_1.y < other_linesegment.point_2.y) or \
            (other_linesegment.point_1.y > self.point_1.y > other_linesegment.point_2.y)):
                return Point(x=other_linesegment.point_1.x, y=self.point_2.y)
        elif self.orientation == 'V' and other_linesegment.orientation == 'H':
            if ((self.point_1.y < other_linesegment.point_1.y < self.point_2.y) or \
            (self.point_1.y > other_linesegment.point_1.y > self.point_2.y)) and \
            ((other_linesegment.point_1.x < self.point_1.x < other_linesegment.point_2.x) or \
            (other_linesegment.point_1.x > self.point_1.x > other_linesegment.point_2.x)):
                return Point(x=self.point_1.x, y=other_linesegment.point_1.y)
        else:
            return None



class Wire(object):
    __slots__ = ['segments']

    def __init__(self, segments: List[LineSegment]):
        self.segments = segments

    @classmethod
    def from_raw_wire_list(cls, raw_wire: List[str]):
        initial_point = Point(0,0)
        segments = [LineSegment.from_manhattan_vector(initial_point, raw_wire.pop(0))]
        for this_segment in raw_wire:
            segments.append(LineSegment.from_manhattan_vector(segments[-1].point_2, this_segment))
        return cls(segments)

    def __repr__(self) -> str:
        return(f'{self.__class__.__name__}({repr(self.segments)})')

    def intersects(self, other: Union['Wire', LineSegment]):
        if isinstance(other, self.__class__):
            return [point for point in [this_segment.intersects(other_segment) for this_segment in self.segments for other_segment in other.segments] if point is not None]
        elif isinstance(other, LineSegment):
            return NotImplemented
        else:
            return NotImplemented


    def distance_on_wire(self, point: Point) -> Optional[int]:
        distance = 0
        for segment in self.segments:
            potential_subsegment = point.on_segment(segment)
            if potential_subsegment:
                distance += potential_subsegment.length
                return distance
            else:
                distance += segment.length
        return None

    def wire_intersection_distances(self, other_wire: 'Wire') -> List[int]:
        intersections = self.intersects(other_wire)
        return [self.distance_on_wire(p) + other_wire.distance_on_wire(p) for p in intersections]



def main():
    with open('data/day_3.txt', 'r') as day_3_file:
        raw_red_wire = day_3_file.readline().rstrip('\n').split(',')
        raw_green_wire = day_3_file.readline().split(',')
    # Turn each raw wire into a list of coordinate tuples corresponding to each endpoint

    red_wire = Wire.from_raw_wire_list(raw_red_wire)
    green_wire = Wire.from_raw_wire_list(raw_green_wire)

    intersections = red_wire.intersects(green_wire)
    sorted_intersections = list(sorted(map(Point.manhattan_distance, intersections)))
    print(f'Part 1 Answer: {sorted_intersections[0]}')

    print(f'Part 2 Answer: {sorted(red_wire.wire_intersection_distances(green_wire))[0]}')


if __name__ == '__main__':
    main()