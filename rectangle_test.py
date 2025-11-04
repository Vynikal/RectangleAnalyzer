import pytest
from RectangleAnalyzer import RectangleAnalyzer


def test_find_overlaps():
    """Test finding overlapping rectangle pairs."""
    rectangles = [
        {'x': 0, 'y': 0, 'width': 4, 'height': 3},
        {'x': 2, 'y': 1, 'width': 3, 'height': 3},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    overlaps = analyzer.find_overlaps()
    assert overlaps == [(0, 1)]


def test_find_overlaps_no_overlap():
    """Test with non-overlapping rectangles."""
    rectangles = [
        {'x': 0, 'y': 0, 'width': 2, 'height': 2},
        {'x': 5, 'y': 5, 'width': 2, 'height': 2},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    overlaps = analyzer.find_overlaps()
    assert overlaps == []


def test_calculate_coverage_area():
    """Test calculating total coverage area."""
    rectangles = [
        {'x': 0, 'y': 0, 'width': 4, 'height': 3},
        {'x': 2, 'y': 1, 'width': 3, 'height': 3},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    total_area = analyzer.calculate_coverage_area()
    # First rect: 4*3=12, Second rect: 3*3=9
    # Overlap: 2*2=4, Total union: 12+9-4=17
    assert total_area == 17.0


def test_get_overlap_regions():
    """Test getting overlap regions."""
    rectangles = [
        {'x': 0, 'y': 0, 'width': 4, 'height': 3},
        {'x': 2, 'y': 1, 'width': 3, 'height': 3},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    overlap_regions = analyzer.get_overlap_regions()
    assert len(overlap_regions) == 1
    assert overlap_regions[0]['rect_indices'] == (0, 1)
    assert overlap_regions[0]['region'] == {'x': 2, 'y': 1, 'width': 2, 'height': 2}


def test_is_point_covered():
    """Test checking if a point is covered."""
    rectangles = [
        {'x': 0, 'y': 0, 'width': 4, 'height': 3},
        {'x': 2, 'y': 1, 'width': 3, 'height': 3},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    assert analyzer.is_point_covered(3, 2) is True
    assert analyzer.is_point_covered(10, 10) is False


def test_find_max_overlap_point():
    """Test finding maximum overlap point."""
    rectangles = [
        {'x': 0, 'y': 0, 'width': 4, 'height': 3},
        {'x': 2, 'y': 1, 'width': 3, 'height': 3},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    hotspot = analyzer.find_max_overlap_point()
    assert hotspot['count'] == 2
    assert 2 <= hotspot['x'] < 4
    assert 1 <= hotspot['y'] < 3


def test_get_stats():
    """Test getting coverage statistics."""
    rectangles = [
        {'x': 0, 'y': 0, 'width': 4, 'height': 3},
        {'x': 2, 'y': 1, 'width': 3, 'height': 3},
    ]
    analyzer = RectangleAnalyzer(rectangles)
    stats = analyzer.get_stats()
    
    assert stats['total_rectangles'] == 2
    assert stats['overlapping_pairs'] == 1
    assert stats['total_area'] == 17.0
    assert stats['overlap_area'] == 4.0
    assert stats['coverage_efficiency'] == pytest.approx(17.0 / 21.0)


def test_empty_rectangles():
    """Test with empty rectangle list."""
    analyzer = RectangleAnalyzer([])
    assert analyzer.find_overlaps() == []
    assert analyzer.calculate_coverage_area() == 0.0
    assert analyzer.get_overlap_regions() == []
    assert analyzer.is_point_covered(0, 0) is False

if __name__ == "__main__":
    pytest.main()