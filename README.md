# Rectangle Analyzer

A Python library for analyzing rectangle overlaps, coverage, and spatial relationships.

## Features

- **Find Overlaps**: Identify all pairs of overlapping rectangles
- **Coverage Area**: Calculate total area covered by rectangles (union, counting overlaps only once)
- **Overlap Regions**: Get the exact rectangular regions where rectangles overlap
- **Point Coverage**: Check if a point is covered by any rectangle
- **Max Overlap Point**: Find points covered by the maximum number of rectangles
- **Statistics**: Comprehensive coverage statistics including efficiency metrics
- **Validation**: Input validation with warnings for identical rectangles

## Installation

### Using Pixi

```bash
# Install pixi if you don't have it
curl -fsSL https://pixi.sh/install.sh | bash

# Install dependencies
pixi install

# Run tests
pixi run test
```

## Usage

```python
from RectangleAnalyzer import RectangleAnalyzer

# Define rectangles
rectangles = [
    {'x': 0, 'y': 0, 'width': 4, 'height': 3},
    {'x': 2, 'y': 1, 'width': 3, 'height': 3},
]

# Create analyzer
analyzer = RectangleAnalyzer(rectangles)

# Find overlapping pairs
overlaps = analyzer.find_overlaps()
print(f"Overlapping pairs: {overlaps}")
# Output: [(0, 1)]

# Calculate total coverage area (union)
total_area = analyzer.calculate_coverage_area()
print(f"Total coverage area: {total_area}")
# Output: 17.0 (not 21, since overlap is counted once)

# Get overlap regions
overlap_regions = analyzer.get_overlap_regions()
print(f"Overlap region: {overlap_regions[0]['region']}")
# Output: {'x': 2, 'y': 1, 'width': 2, 'height': 2}

# Check if a point is covered
is_covered = analyzer.is_point_covered(3, 2)
print(f"Point (3, 2) covered: {is_covered}")
# Output: True

# Find maximum overlap point
hotspot = analyzer.find_max_overlap_point()
print(f"Max overlap point: {hotspot}")
# Output: {'x': 3.0, 'y': 2.0, 'count': 2}

# Get comprehensive statistics
stats = analyzer.get_stats()
print(f"Statistics: {stats}")
# Output: {
#   'total_rectangles': 2,
#   'overlapping_pairs': 1,
#   'total_area': 17.0,
#   'overlap_area': 4.0,
#   'coverage_efficiency': 0.8095238095238095
# }
```

## Rectangle Format

Each rectangle must be a dictionary with the following keys:

```python
{
    'x': float | int,       # X coordinate of bottom-left corner
    'y': float | int,       # Y coordinate of bottom-left corner
    'width': float | int,   # Width (must be > 0)
    'height': float | int   # Height (must be > 0)
}
```

## Validation

The analyzer validates input rectangles:

- **Required keys**: All rectangles must have `x`, `y`, `width`, `height`
- **Numeric values**: All values must be numbers (int or float)
- **Non-negative dimensions**: Width and height must be > 0
- **Warnings**: Issues warnings for identical rectangles

```python
# This will raise a ValueError
try:
    RectangleAnalyzer([{'x': 0, 'y': 0, 'width': -2, 'height': 2}])
except ValueError as e:
    print(e)  # Rectangle 0 has negative dimensions

# This will issue a warning
import warnings
rectangles = [
    {'x': 0, 'y': 0, 'width': 4, 'height': 3},
    {'x': 0, 'y': 0, 'width': 4, 'height': 3},  # Identical!
]
with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    analyzer = RectangleAnalyzer(rectangles)
    print(w[0].message)  # Rectangle 1 is identical to rectangle 0...
```

