import os
import sys

here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, here)

from src.day_3 import Point, LineSegment, Wire  # noqa: E402


def test_segment_intersection():
    segment_1 = LineSegment(point_1=Point(x=3, y=5), point_2=Point(x=3, y=2))
    segment_2 = LineSegment(point_1=Point(x=6, y=3), point_2=Point(x=2, y=3))
    intersection_point = segment_1.intersects(segment_2)
    assert intersection_point == Point(x=3, y=3)


def test_wire_intersections():
    raw_wire_1 = "R8,U5,L5,D3"
    wire_1 = Wire.from_raw_wire_list(raw_wire_1.split(","))

    raw_wire_2 = "U7,R6,D4,L4"
    wire_2 = Wire.from_raw_wire_list(raw_wire_2.split(","))

    intersections = wire_1.intersects(wire_2)
    sorted_intersections = list(sorted(map(Point.manhattan_distance, intersections)))

    assert sorted_intersections[0] == 6


def test_wire_intersections_2():
    raw_wire_1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    wire_1 = Wire.from_raw_wire_list(raw_wire_1.split(","))

    raw_wire_2 = "U62,R66,U55,R34,D71,R55,D58,R83"
    wire_2 = Wire.from_raw_wire_list(raw_wire_2.split(","))

    intersections = wire_1.intersects(wire_2)
    sorted_intersections = list(sorted(map(Point.manhattan_distance, intersections)))

    assert sorted_intersections[0] == 159


def test_wire_intersections_3():
    raw_wire_1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
    wire_1 = Wire.from_raw_wire_list(raw_wire_1.split(","))

    raw_wire_2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
    wire_2 = Wire.from_raw_wire_list(raw_wire_2.split(","))

    intersections = wire_1.intersects(wire_2)
    sorted_intersections = list(sorted(map(Point.manhattan_distance, intersections)))

    assert sorted_intersections[0] == 135


def test_point_on_wire_distance():
    raw_wire_1 = "R8,U5,L5,D3"
    wire_1 = Wire.from_raw_wire_list(raw_wire_1.split(","))

    raw_wire_2 = "U7,R6,D4,L4"
    wire_2 = Wire.from_raw_wire_list(raw_wire_2.split(","))

    assert sorted(wire_1.wire_intersection_distances(wire_2)) == [30, 40]


def test_point_on_wire_distance_2():
    raw_wire_1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    wire_1 = Wire.from_raw_wire_list(raw_wire_1.split(","))

    raw_wire_2 = "U62,R66,U55,R34,D71,R55,D58,R83"
    wire_2 = Wire.from_raw_wire_list(raw_wire_2.split(","))

    assert sorted(wire_1.wire_intersection_distances(wire_2))[0] == 610


def test_point_on_wire_distance_3():
    raw_wire_1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
    wire_1 = Wire.from_raw_wire_list(raw_wire_1.split(","))

    raw_wire_2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"
    wire_2 = Wire.from_raw_wire_list(raw_wire_2.split(","))

    assert sorted(wire_1.wire_intersection_distances(wire_2))[0] == 410
