import tempfile
import unittest
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

import scripts.generate_course_figures as figures

NS = {"svg": "http://www.w3.org/2000/svg"}


class CourseFigureTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.old_out, self.old_old = figures.OUT, figures.OLD
        figures.OUT = Path(self.tmp.name) / "oct-2026"
        figures.OLD = Path(self.tmp.name) / "eos-materials"

    def tearDown(self) -> None:
        figures.OUT, figures.OLD = self.old_out, self.old_old
        self.tmp.cleanup()

    def svg(self, relative: str) -> ET.Element:
        return ET.parse(Path(self.tmp.name) / relative).getroot()

    def text(self, root: ET.Element) -> str:
        return " ".join("".join(node.itertext()) for node in root.iter())

    def circles(self, root: ET.Element) -> list[tuple[float, float]]:
        return [(float(c.attrib["cx"]), float(c.attrib["cy"])) for c in root.findall(".//svg:circle", NS)]

    def assert_point(self, points: list[tuple[float, float]], q: Fraction, p: Fraction, xmax: int, ymax: int, height: int = 325) -> None:
        expected = (90 + 570 * float(q) / xmax, 78 + height * (1 - float(p) / ymax))
        self.assertTrue(any(abs(x - expected[0]) < 0.01 and abs(y - expected[1]) < 0.01 for x, y in points))

    def test_numerical_tax_equilibrium_surplus_and_svg_points(self) -> None:
        tax = Fraction(5)
        p0 = Fraction(300 + 200, 2 + 3)
        q0 = 300 - 2 * p0
        ps = Fraction(300 + 200 - 2 * tax, 2 + 3)
        pd = ps + tax
        qt = 3 * ps - 200
        self.assertEqual((q0, p0, qt, pd, ps), (100, 100, 94, 103, 98))
        self.assertEqual(tax * qt, 470)
        self.assertEqual(
            (Fraction(1, 2) * (150 - p0) * q0, Fraction(1, 2) * (p0 - Fraction(200, 3)) * q0),
            (2500, Fraction(5000, 3)),
        )
        self.assertEqual(
            (Fraction(1, 2) * (150 - pd) * qt, Fraction(1, 2) * (ps - Fraction(200, 3)) * qt),
            (2209, Fraction(4418, 3)),
        )
        self.assertEqual(Fraction(1, 2) * tax * (q0 - qt), 15)
        figures.numerical()
        points = self.circles(self.svg("oct-2026/tax-numerical-equilibrium.svg"))
        for q, p in [(q0, p0), (qt, pd), (qt, ps)]:
            self.assert_point(points, Fraction(q), Fraction(p), 150, 160)
        figures.numerical(True)
        text = self.text(self.svg("oct-2026/tax-numerical-surplus.svg"))
        self.assertIn("CS = 2 209", text)
        self.assertIn("Бюджет: 5 × 94 = 470", text)
        self.assertIn("DWL: ½ × 5 × (100 − 94) = 15", text)

    def test_lorenz_curve_points_and_gini_are_calculated_from_groups(self) -> None:
        groups = [10, 20, 30, 40, 100]
        total = sum(groups)
        cumulative = [(0, 0)]
        income = 0
        for index, value in enumerate(groups, start=1):
            income += value
            cumulative.append((20 * index, 100 * income // total))
        area = sum(
            Fraction(x2 - x1, 100) * Fraction(y1 + y2, 200)
            for (x1, y1), (x2, y2) in zip(cumulative, cumulative[1:])
        )
        self.assertEqual(cumulative, [(0, 0), (20, 5), (40, 15), (60, 30), (80, 50), (100, 100)])
        self.assertEqual(1 - 2 * area, Fraction(2, 5))
        figures.lorenz()
        root = self.svg("oct-2026/eos-lorenz-gini.svg")
        points = self.circles(root)
        for q, p in cumulative:
            self.assert_point(points, Fraction(q), Fraction(p), 100, 100)
        self.assertIn("G = 1 − 2 × 0,30 = 0,40", self.text(root))

    def test_diagnostic_bayes_positive_predictive_value_drives_bar_width(self) -> None:
        population, prevalence = 10000, Fraction(1, 100)
        sensitivity = specificity = Fraction(95, 100)
        sick = population * prevalence
        tp = sick * sensitivity
        fp = (population - sick) * (1 - specificity)
        ppv = tp / (tp + fp)
        self.assertEqual((tp, fp, ppv), (95, 495, Fraction(19, 118)))
        figures.bayes()
        root = self.svg("oct-2026/diagnostic-bayes.svg")
        widths = [float(r.attrib["width"]) for r in root.findall(".//svg:rect", NS) if r.attrib.get("fill") == figures.TEAL]
        self.assertTrue(any(abs(width - 660 * float(ppv)) < 0.01 for width in widths))
        self.assertIn("Истинно положительные: 95; ложноположительные: 495", self.text(root))

    def test_poverty_trap_discontinuity_and_gradual_taper_metr(self) -> None:
        tax, benefit, threshold = Fraction(13, 100), 12, 20
        d20 = threshold * (1 - tax) + benefit
        d21 = 21 * (1 - tax)
        self.assertEqual((d20, d21, tax + Fraction(3, 10)), (Fraction(147, 5), Fraction(1827, 100), Fraction(43, 100)))
        self.assertEqual(1 - (d21 - d20), Fraction(1213, 100))
        figures.trap()
        root = self.svg("oct-2026/eos-poverty-trap.svg")
        points = self.circles(root)
        for q, p in [(20, d20), (21, d21)]:
            self.assert_point(points, Fraction(q), Fraction(p), 50, 48, 330)
        self.assertIn("предельную нагрузку43%", self.text(root))

    def test_rawls_and_equal_absolute_sacrifice_points_are_both_drawn(self) -> None:
        rawls_ta, total_tax = Fraction(2), Fraction(6)
        ua = 5 - rawls_ta / 2
        ub = 2 + rawls_ta
        equal_ta = Fraction(4)
        self.assertEqual((min(ua, ub), total_tax - rawls_ta, 5 - equal_ta / 2, 2 + equal_ta), (4, 4, 3, 6))
        figures.sacrifice()
        root = self.svg("oct-2026/tax-sacrifice.svg")
        points = self.circles(root)
        for q, p in [(rawls_ta, 4), (equal_ta, 3), (equal_ta, 6)]:
            self.assert_point(points, Fraction(q), Fraction(p), 6, 8, 330)
        self.assertIn("Равная абсолютная жертва: Tₐ = 4, Tᵦ = 2", self.text(root))


if __name__ == "__main__":
    unittest.main()
