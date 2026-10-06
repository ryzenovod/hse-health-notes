import tempfile
import unittest
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

import scripts.generate_seminar3_figures as figures


NS = {"svg": "http://www.w3.org/2000/svg"}


def point(x: int, y: int) -> tuple[Fraction, Fraction]:
    return Fraction(x), Fraction(y)


def svg_fraction(value: str) -> Fraction:
    return Fraction(value)


class Seminar3FigureTests(unittest.TestCase):
    def svg_text(self, root: ET.Element) -> str:
        return " ".join("".join(node.itertext()) for node in root.iter())

    def assert_has_any(self, text: str, values: tuple[str, ...]) -> None:
        self.assertTrue(any(value in text for value in values), f"missing one of {values!r} in {text!r}")

    def parse_svg(self, path: Path) -> ET.Element:
        return ET.parse(path).getroot()

    def svg_points(self, value: str) -> list[tuple[Fraction, Fraction]]:
        points = []
        for raw_pair in value.split():
            x, y = raw_pair.split(",")
            points.append((svg_fraction(x), svg_fraction(y)))
        return points

    def attr_fraction(self, value: str) -> Fraction:
        return Fraction(value)

    def assert_close_fraction(self, actual: Fraction, expected: Fraction, tolerance: Fraction = Fraction(1, 1000)) -> None:
        self.assertLessEqual(abs(actual - expected), tolerance, f"{actual!r} != {expected!r} within {tolerance!r}")

    def polygon_pixel_area(self, points: list[tuple[Fraction, Fraction]]) -> Fraction:
        total = Fraction(0)
        for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1]):
            total += x1 * y2 - x2 * y1
        return abs(total) / 2

    def external_refs(self, root: ET.Element) -> list[str]:
        refs: list[str] = []
        for element in root.iter():
            for name, value in element.attrib.items():
                local_name = name.rsplit("}", 1)[-1].lower()
                if local_name in {"href", "src"} and value.startswith(("http://", "https://")):
                    refs.append(value)
        return refs

    def test_polygon_and_lorenz_math_use_exact_fractions(self) -> None:
        before = [(Fraction(0), Fraction(0)), (Fraction(3, 5), Fraction(1, 5)), (Fraction(1), Fraction(1))]
        after = [(Fraction(0), Fraction(0)), (Fraction(3, 5), Fraction(9, 25)), (Fraction(1), Fraction(1))]

        self.assertEqual(figures.polygon_area([point(0, 0), point(3, 0), point(0, 2)]), Fraction(3, 1))
        self.assertEqual(figures.polygon_area([point(0, 0), point(0, 2), point(3, 0)]), Fraction(3, 1))
        self.assertEqual(figures.lorenz_area(before), Fraction(3, 10))
        self.assertEqual(figures.gini_from_lorenz(before), Fraction(2, 5))
        self.assertEqual(figures.lorenz_area(after), Fraction(19, 50))
        self.assertEqual(figures.gini_from_lorenz(after), Fraction(6, 25))

    def test_lorenz_area_is_independent_of_input_order(self) -> None:
        scrambled = [(Fraction(1), Fraction(1)), (Fraction(0), Fraction(0)), (Fraction(3, 5), Fraction(1, 5))]

        self.assertEqual(figures.lorenz_area(scrambled), Fraction(3, 10))

    def test_task7_before_after_exposes_component_areas_and_gini_change(self) -> None:
        result = figures.task7_before_after()

        self.assertEqual(result["before_points"], [(Fraction(0), Fraction(0)), (Fraction(3, 5), Fraction(1, 5)), (Fraction(1), Fraction(1))])
        self.assertEqual(result["after_points"], [(Fraction(0), Fraction(0)), (Fraction(3, 5), Fraction(9, 25)), (Fraction(1), Fraction(1))])
        self.assertEqual(result["before_left_area"], Fraction(3, 50))
        self.assertEqual(result["before_right_area"], Fraction(6, 25))
        self.assertEqual(result["before_lorenz_area"], Fraction(3, 10))
        self.assertEqual(result["before_gini"], Fraction(2, 5))
        self.assertEqual(result["after_left_area"], Fraction(27, 250))
        self.assertEqual(result["after_right_area"], Fraction(34, 125))
        self.assertEqual(result["after_lorenz_area"], Fraction(19, 50))
        self.assertEqual(result["after_gini"], Fraction(6, 25))
        self.assertEqual(result["gini_change"], Fraction(4, 25))
        self.assertEqual(result["gini_relative_reduction"], Fraction(2, 5))

    def test_task8_tax_rows_match_the_six_observed_rates(self) -> None:
        rows = figures.task8_tax_rows()
        compact = [
            (
                row["rate"],
                row["hours"],
                row["gross_a"],
                row["tax_revenue"],
                row["net_a"],
                row["income_b"],
                row["total_income"],
            )
            for row in rows
        ]

        self.assertEqual(
            compact,
            [
                (Fraction(0), Fraction(6), Fraction(600), Fraction(0), Fraction(600), Fraction(0), Fraction(600)),
                (Fraction(15), Fraction(7), Fraction(700), Fraction(105), Fraction(595), Fraction(105), Fraction(700)),
                (Fraction(30), Fraction(5), Fraction(500), Fraction(150), Fraction(350), Fraction(150), Fraction(500)),
                (Fraction(50), Fraction(5, 2), Fraction(250), Fraction(125), Fraction(125), Fraction(125), Fraction(250)),
                (Fraction(80), Fraction(1), Fraction(100), Fraction(80), Fraction(20), Fraction(80), Fraction(100)),
                (Fraction(100), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0), Fraction(0)),
            ],
        )
        for row in rows:
            self.assertEqual(row["net_a"] + row["income_b"], row["gross_a"])

    def test_task8_choice_criteria_use_table_values_not_a_smooth_curve(self) -> None:
        rows = figures.task8_tax_rows()

        utilitarian = max(rows, key=lambda row: row["total_income"])
        observed_revenue = max(rows, key=lambda row: row["tax_revenue"])
        rawls = figures.table_maximin(rows)
        equal_positive_rows = [row for row in rows if row["net_a"] == row["income_b"] and row["total_income"] > 0]
        libertarian = rows[0]

        self.assertEqual((utilitarian["rate"], utilitarian["total_income"]), (Fraction(15), Fraction(700)))
        self.assertEqual((observed_revenue["rate"], observed_revenue["tax_revenue"]), (Fraction(30), Fraction(150)))
        self.assertEqual((rawls["rate"], min(rawls["net_a"], rawls["income_b"])), (Fraction(30), Fraction(150)))
        self.assertEqual([(row["rate"], row["net_a"]) for row in equal_positive_rows], [(Fraction(50), Fraction(125))])
        self.assertEqual((libertarian["rate"], libertarian["net_a"]), (Fraction(0), Fraction(600)))

    def test_table_maximin_breaks_ties_by_source_order_and_switches_poorer_person(self) -> None:
        rows = figures.task8_tax_rows()

        self.assertEqual(figures.table_maximin(rows)["rate"], Fraction(30))
        self.assertEqual(min(rows[4]["net_a"], rows[4]["income_b"]), Fraction(20))
        self.assertEqual(figures.table_maximin(rows[4:])["rate"], Fraction(80))
        self.assertEqual(
            figures.table_maximin(
                [
                    {"rate": Fraction(1), "net_a": Fraction(10), "income_b": Fraction(10)},
                    {"rate": Fraction(2), "net_a": Fraction(10), "income_b": Fraction(40)},
                ]
            )["rate"],
            Fraction(1),
        )

    def test_render_all_writes_deterministic_accessible_vector_svgs(self) -> None:
        expected_names = {
            "geometry-areas.svg",
            "lorenz-before.svg",
            "lorenz-after-tax.svg",
            "lorenz-before-after.svg",
            "tax-revenue-discrete.svg",
        }

        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_paths = figures.render_all(Path(first))
            second_paths = figures.render_all(Path(second))

            self.assertEqual({path.name for path in first_paths}, expected_names)
            self.assertEqual({path.name for path in second_paths}, expected_names)

            first_bytes = {path.name: path.read_bytes() for path in first_paths}
            second_bytes = {path.name: path.read_bytes() for path in second_paths}
            self.assertEqual(first_bytes, second_bytes)

            for path in first_paths:
                root = self.parse_svg(path)
                self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
                self.assertEqual(root.attrib.get("role"), "img")
                self.assertIn("viewBox", root.attrib)
                width = float(root.attrib["viewBox"].split()[2])
                self.assertGreaterEqual(width, 700)
                self.assertIsNotNone(root.find("svg:title", NS))
                self.assertIsNotNone(root.find("svg:desc", NS))
                self.assertEqual(root.findall(".//svg:image", NS), [])
                self.assertEqual(root.findall(".//svg:script", NS), [])
                self.assertEqual(self.external_refs(root), [])

    def test_rendered_svgs_label_the_exact_areas_and_discrete_tax_maximum(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            figures.render_all(Path(temp_dir))
            before_text = self.svg_text(self.parse_svg(Path(temp_dir) / "lorenz-before.svg"))
            after_text = self.svg_text(self.parse_svg(Path(temp_dir) / "lorenz-after-tax.svg"))
            combined_text = self.svg_text(self.parse_svg(Path(temp_dir) / "lorenz-before-after.svg"))
            geometry_text = self.svg_text(self.parse_svg(Path(temp_dir) / "geometry-areas.svg"))
            revenue_text = self.svg_text(self.parse_svg(Path(temp_dir) / "tax-revenue-discrete.svg"))
            revenue_root = self.parse_svg(Path(temp_dir) / "tax-revenue-discrete.svg")

        self.assert_has_any(before_text, ("600",))
        self.assert_has_any(before_text, ("2 400", "2400"))
        self.assert_has_any(before_text, ("G = 0,40", "G = 0.40", "G=0,40", "G=0.40"))
        self.assert_has_any(after_text, ("1 080", "1080"))
        self.assert_has_any(after_text, ("2 720", "2720"))
        self.assert_has_any(after_text, ("G = 0,24", "G = 0.24", "G=0,24", "G=0.24"))
        self.assert_has_any(combined_text, ("60;20", "60; 20", "(60;20)", "(60; 20)"))
        self.assert_has_any(combined_text, ("60;36", "60; 36", "(60;36)", "(60; 36)"))
        self.assert_has_any(geometry_text, ("600",))
        self.assert_has_any(geometry_text, ("2 400", "2400"))
        self.assert_has_any(revenue_text, ("30%", "30 %"))
        self.assert_has_any(revenue_text, ("150",))
        self.assertGreaterEqual(len(revenue_root.findall(".//svg:circle", NS)), 6)

    def test_lorenz_svgs_encode_correct_physical_square_and_area_polygons(self) -> None:
        cases = {
            "lorenz-before.svg": Fraction(3, 50) + Fraction(6, 25),
            "lorenz-after-tax.svg": Fraction(27, 250) + Fraction(34, 125),
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            figures.render_all(Path(temp_dir))
            for name, expected_area in cases.items():
                root = self.parse_svg(Path(temp_dir) / name)
                data_points: dict[str, tuple[Fraction, Fraction]] = {}
                for circle in root.findall(".//svg:circle", NS):
                    data_point = circle.attrib.get("data-point")
                    if data_point:
                        data_points[data_point] = (svg_fraction(circle.attrib["cx"]), svg_fraction(circle.attrib["cy"]))

                left_bottom = data_points["0,0"]
                right_top = data_points["1,1"]
                square_width = right_top[0] - left_bottom[0]
                square_height = left_bottom[1] - right_top[1]
                self.assert_close_fraction(square_width, square_height)

                actual_area = Fraction(0)
                for polygon in root.findall(".//svg:polygon", NS):
                    metadata_area = polygon.attrib.get("data-area")
                    if not metadata_area:
                        continue
                    polygon_points = self.svg_points(polygon.attrib["points"])
                    normalized_area = self.polygon_pixel_area(polygon_points) / (square_width * square_height)
                    self.assert_close_fraction(normalized_area, self.attr_fraction(metadata_area))
                    actual_area += normalized_area

                self.assert_close_fraction(actual_area, expected_area)

    def test_geometry_area_svg_shapes_match_the_formula_dimensions(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            figures.render_all(Path(temp_dir))
            root = self.parse_svg(Path(temp_dir) / "geometry-areas.svg")

        shapes = {polygon.attrib["data-shape"]: self.svg_points(polygon.attrib["points"]) for polygon in root.findall(".//svg:polygon", NS)}
        triangle = shapes["triangle"]
        trapezoid = shapes["trapezoid"]

        triangle_base = abs(triangle[1][0] - triangle[0][0])
        triangle_height = abs(triangle[2][1] - triangle[1][1])
        self.assert_close_fraction(triangle_base / triangle_height, Fraction(3))

        vertical_edges: list[Fraction] = []
        for (x1, y1), (x2, y2) in zip(trapezoid, trapezoid[1:] + trapezoid[:1]):
            if x1 == x2:
                vertical_edges.append(abs(y2 - y1))

        self.assertEqual(len(vertical_edges), 2)
        short_side, long_side = sorted(vertical_edges)
        perpendicular_width = max(x for x, _ in trapezoid) - min(x for x, _ in trapezoid)
        self.assert_close_fraction(short_side / long_side, Fraction(1, 5))
        self.assert_close_fraction(perpendicular_width / long_side, Fraction(2, 5))

    def test_tax_revenue_svg_maps_all_six_points_to_linear_axes(self) -> None:
        expected_points = {
            0: 0,
            15: 105,
            30: 150,
            50: 125,
            80: 80,
            100: 0,
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            figures.render_all(Path(temp_dir))
            root = self.parse_svg(Path(temp_dir) / "tax-revenue-discrete.svg")

        circles = {}
        for circle in root.findall(".//svg:circle", NS):
            data_point = circle.attrib.get("data-tax-point")
            if data_point:
                rate, tax = (int(value) for value in data_point.split(","))
                circles[rate] = (tax, svg_fraction(circle.attrib["cx"]), svg_fraction(circle.attrib["cy"]))

        self.assertEqual(set(circles), set(expected_points))
        self.assertEqual({rate: tax for rate, (tax, _, _) in circles.items()}, expected_points)

        x_zero = circles[0][1]
        y_zero = circles[0][2]
        x_scale = (circles[100][1] - x_zero) / 100
        y_scale = (y_zero - circles[30][2]) / 150

        for rate, expected_tax in expected_points.items():
            actual_tax, x, y = circles[rate]
            self.assertEqual(actual_tax, expected_tax)
            self.assert_close_fraction(x, x_zero + rate * x_scale)
            self.assert_close_fraction(y, y_zero - expected_tax * y_scale)


if __name__ == "__main__":
    unittest.main()
