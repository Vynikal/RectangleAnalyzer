import warnings


class RectangleAnalyzer:
    def __init__(self, rectangles: list[dict]):
        """Initialize analyzer with list of rectangles."""
        self.rectangles = rectangles
        self._validate_rectangles()

    def _validate_rectangles(self):
        """Validate rectangle data."""
        for i, rect in enumerate(self.rectangles):
            # Check required keys
            required = {"x", "y", "width", "height"}
            if not required.issubset(rect.keys()):
                raise ValueError(
                    f"Rectangle {i} missing required keys: {required - rect.keys()}"
                )

            # Check for valid numeric values
            for key in required:
                if not isinstance(rect[key], (int, float)):
                    raise TypeError(f"Rectangle {i} has non-numeric {key}: {rect[key]}")

            # Check for non-negative dimensions
            if rect["width"] < 0 or rect["height"] < 0:
                raise ValueError(f"Rectangle {i} has negative dimensions")

            # Check for zero-area rectangles
            if rect["width"] == 0 or rect["height"] == 0:
                raise ValueError(f"Rectangle {i} has zero area")

        # Check for identical rectangles
        self._check_identical_rectangles()

    def _check_identical_rectangles(self):
        """Check for and warn about identical rectangles."""
        seen = {}
        for i, rect in enumerate(self.rectangles):
            # Create a hashable key from rectangle properties
            key = (rect["x"], rect["y"], rect["width"], rect["height"])

            if key in seen:
                warnings.warn(
                    f"Rectangle {i} is identical to rectangle {seen[key]}: "
                    f"x={rect['x']}, y={rect['y']}, width={rect['width']}, height={rect['height']}",
                    UserWarning,
                    stacklevel=3,
                )
            else:
                seen[key] = i

    def find_overlaps(self) -> list[tuple]:
        """
        Find all pairs of overlapping rectangles.
        Returns: List of tuples (i, j) where i < j are indices
        Example: [(0, 1), (0, 2), (1, 2)]
        """
        overlaps = []
        for i in range(len(self.rectangles)):
            for j in range(i + 1, len(self.rectangles)):
                if self._rectangles_overlap(self.rectangles[i], self.rectangles[j]):
                    overlaps.append((i, j))
        return overlaps

    def _rectangles_overlap(self, r1: dict, r2: dict) -> bool:
        """Helper method to check if two given rectangles overlap."""
        # No overlap if one rectangle is to the left of the other
        if r1["x"] + r1["width"] <= r2["x"] or r2["x"] + r2["width"] <= r1["x"]:
            return False
        # No overlap if one rectangle is above the other
        if r1["y"] + r1["height"] <= r2["y"] or r2["y"] + r2["height"] <= r1["y"]:
            return False
        return True

    def calculate_coverage_area(self) -> float:
        """
        Calculate total area covered by all rectangles.
        Overlapping areas should be counted only once.
        Returns: float/int representing total area
        """
        if not self.rectangles:
            return 0.0

        # Collect all unique x and y coordinates
        x_coords = set()
        y_coords = set()

        for rect in self.rectangles:
            x_coords.add(rect["x"])
            x_coords.add(rect["x"] + rect["width"])
            y_coords.add(rect["y"])
            y_coords.add(rect["y"] + rect["height"])

        x_coords = sorted(x_coords)
        y_coords = sorted(y_coords)

        # Calculate area by checking each cell in the grid
        total_area = 0.0
        for i in range(len(x_coords) - 1):
            for j in range(len(y_coords) - 1):
                cell_x = x_coords[i]
                cell_y = y_coords[j]
                cell_width = x_coords[i + 1] - x_coords[i]
                cell_height = y_coords[j + 1] - y_coords[j]

                # Check if this cell is covered by any rectangle
                for rect in self.rectangles:
                    if (
                        rect["x"] <= cell_x
                        and cell_x + cell_width <= rect["x"] + rect["width"]
                        and rect["y"] <= cell_y
                        and cell_y + cell_height <= rect["y"] + rect["height"]
                    ):
                        total_area += cell_width * cell_height
                        break

        return total_area

    def get_overlap_regions(self) -> list[dict]:
        """
        Find actual overlap regions between rectangles.
        Returns: List of dicts containing:
        - 'rect_indices': tuple of rectangle indices
        - 'region': dict with x, y, width, height of overlap
        """
        overlap_regions = []
        for i in range(len(self.rectangles)):
            for j in range(i + 1, len(self.rectangles)):
                region = self._get_overlap_region(
                    self.rectangles[i], self.rectangles[j]
                )
                if region:
                    overlap_regions.append({"rect_indices": (i, j), "region": region})
        return overlap_regions

    def _get_overlap_region(self, r1: dict, r2: dict) -> dict | None:
        """Helper method to get the overlap region between two rectangles."""
        if not self._rectangles_overlap(r1, r2):
            return None

        x = max(r1["x"], r2["x"])
        y = max(r1["y"], r2["y"])
        x_max = min(r1["x"] + r1["width"], r2["x"] + r2["width"])
        y_max = min(r1["y"] + r1["height"], r2["y"] + r2["height"])

        return {"x": x, "y": y, "width": x_max - x, "height": y_max - y}

    def is_point_covered(self, x: int | float, y: int | float) -> bool:
        """
        Check if a point is covered by any rectangle.
        Returns: boolean
        """
        for rect in self.rectangles:
            if (
                rect["x"] <= x <= rect["x"] + rect["width"]
                and rect["y"] <= y <= rect["y"] + rect["height"]
            ):
                return True
        return False

    def find_max_overlap_point(self) -> dict:
        """
        Find a point covered by maximum number of rectangles.
        Returns: dict with 'x', 'y', 'count' keys
        Note: There might be multiple such points, return any one.
        """
        if not self.rectangles:
            return {"x": 0, "y": 0, "count": 0}

        # Collect all unique x and y coordinates
        x_coords = set()
        y_coords = set()

        for rect in self.rectangles:
            x_coords.add(rect["x"])
            x_coords.add(rect["x"] + rect["width"])
            y_coords.add(rect["y"])
            y_coords.add(rect["y"] + rect["height"])

        x_coords = sorted(x_coords)
        y_coords = sorted(y_coords)

        # Check center of each cell for maximum overlap
        max_count = 0
        max_point = {"x": 0, "y": 0, "count": 0}

        for i in range(len(x_coords) - 1):
            for j in range(len(y_coords) - 1):
                # Use center of cell
                test_x = (x_coords[i] + x_coords[i + 1]) / 2
                test_y = (y_coords[j] + y_coords[j + 1]) / 2

                count = sum(
                    1
                    for rect in self.rectangles
                    if rect["x"] <= test_x <= rect["x"] + rect["width"]
                    and rect["y"] <= test_y <= rect["y"] + rect["height"]
                )

                if count > max_count:
                    max_count = count
                    max_point = {"x": test_x, "y": test_y, "count": count}

        return max_point

    def get_stats(self) -> dict:
        """
        Get coverage statistics.
        Returns: dict with:
        - 'total_rectangles': int
        - 'overlapping_pairs': int
        - 'total_area': float (union area)
        - 'overlap_area': float (sum of all overlap regions)
        - 'coverage_efficiency': float (total_area / sum_of_individual_areas)
        """
        total_rectangles = len(self.rectangles)
        overlapping_pairs = len(self.find_overlaps())
        total_area = self.calculate_coverage_area()

        # Calculate overlap area (sum of all overlap regions)
        overlap_regions = self.get_overlap_regions()
        overlap_area = sum(
            region["region"]["width"] * region["region"]["height"]
            for region in overlap_regions
        )

        # Calculate sum of individual areas
        sum_of_individual_areas = sum(
            rect["width"] * rect["height"] for rect in self.rectangles
        )

        # Calculate coverage efficiency
        coverage_efficiency = (
            total_area / sum_of_individual_areas if sum_of_individual_areas > 0 else 0.0
        )

        return {
            "total_rectangles": total_rectangles,
            "overlapping_pairs": overlapping_pairs,
            "total_area": total_area,
            "overlap_area": overlap_area,
            "coverage_efficiency": coverage_efficiency,
        }
