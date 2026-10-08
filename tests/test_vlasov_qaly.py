import tempfile
import unittest
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

import scripts.generate_course_figures as figures

NS = {"svg": "http://www.w3.org/2000/svg"}


class QalyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.original_out = figures.OUT
        figures.OUT = Path(self.tmp.name)
        figures.qaly()
        self.path = figures.OUT / "vlasov-qaly.svg"
        self.root = ET.parse(self.path).getroot()

    def tearDown(self):
        figures.OUT = self.original_out
        self.tmp.cleanup()

    def test_exact_total_and_increment(self):
        treatment = figures.qaly_total(figures.QALY_TREATMENT)
        comparator = figures.qaly_total(figures.QALY_COMPARATOR)
        self.assertEqual(treatment, Fraction(14, 5))
        self.assertEqual(comparator, Fraction(19, 10))
        self.assertEqual(treatment - comparator, Fraction(9, 10))

    def test_shaded_svg_areas_match_qaly_difference(self):
        areas = []
        for poly in self.root.findall("svg:polyline", NS):
            if poly.attrib.get("fill") not in (figures.RED, figures.TEAL):
                continue
            points = [tuple(map(float, pair.split(","))) for pair in poly.attrib["points"].split()]
            twice_area = sum(x1*y2-x2*y1 for (x1,y1),(x2,y2) in zip(points,points[1:]+points[:1]))
            # One year is 145 px horizontally; one utility unit is 300 px vertically.
            areas.append(abs(twice_area) / 2 / (145 * 300))
        self.assertEqual(len(areas), 3)
        for actual, expected in zip(areas, (.3, .4, .8)):
            self.assertAlmostEqual(actual, expected)
        self.assertAlmostEqual(-areas[0]+areas[1]+areas[2], .9)

    def test_trajectories_use_correct_coordinates(self):
        polylines = self.root.findall("svg:polyline", NS)
        for segments, color in ((figures.QALY_TREATMENT, figures.BLUE), (figures.QALY_COMPARATOR, figures.ORANGE)):
            line = next(p for p in polylines if p.attrib.get("stroke") == color and p.attrib.get("fill") == "none")
            points = [tuple(map(float, pair.split(","))) for pair in line.attrib["points"].split()]
            expected = [(90+145*t,480-300*float(u)) for start,end,u in segments for t in (start,end)]
            self.assertEqual(points, expected)

    def test_metadata_and_deterministic_output(self):
        original = self.path.read_bytes()
        figures.qaly()
        self.assertEqual(original, self.path.read_bytes())
        self.assertEqual(self.root.attrib["role"], "img")
        self.assertEqual(self.root.attrib["viewBox"], "0 0 760 670")
        self.assertIsNotNone(self.root.find("svg:title", NS))
        self.assertIsNotNone(self.root.find("svg:desc", NS))
        self.assertFalse(self.root.findall(".//svg:script", NS))
        self.assertFalse(self.root.findall(".//svg:image", NS))


if __name__ == "__main__":
    unittest.main()
