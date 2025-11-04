# Example 1: Simple overlap case
from RectangleAnalyzer import RectangleAnalyzer

rectangles = [
    {'x': 0, 'y': 0, 'width': 4, 'height': 3},
    {'x': 2, 'y': 1, 'width': 3, 'height': 3},
]

analyzer = RectangleAnalyzer(rectangles)

overlaps = analyzer.find_overlaps()
print(f"Overlapping pairs: {overlaps}") # [(0, 1)]

total_area = analyzer.calculate_coverage_area()
print(f"Total coverage: {total_area}") # Should be less than 12 + 9 = 21

overlap_regions = analyzer.get_overlap_regions()
print(f"Overlap region: {overlap_regions[0]['region']}")
# {'x': 2, 'y': 1, 'width': 2, 'height': 2}

# Example 2: Point checking
is_covered = analyzer.is_point_covered(3, 2)
print(f"Point (3, 2) covered: {is_covered}") # True

hotspot = analyzer.find_max_overlap_point()
print(f"Max overlap point: {hotspot}") # {'x': 3, 'y': 2, 'count': 2}