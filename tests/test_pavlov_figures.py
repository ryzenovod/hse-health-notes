import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SVGS_DIR = ROOT / "docs/assets/healthcare-economics"


class PavlovFiguresTests(unittest.TestCase):
    def test_svg_files_exist_and_are_valid_xml(self) -> None:
        expected_files = [
            "iceberg-quality-perception.svg",
            "digitalization-babylon-vs-emias.svg",
            "how-the-mighty-fall-stages.svg",
            "leadership-system-triad.svg",
            "semmelweis-innovation-triad.svg",
            "ted-lasso-leadership-model.svg",
        ]
        for filename in expected_files:
            path = SVGS_DIR / filename
            self.assertTrue(path.exists(), f"Missing SVG file: {filename}")
            root = ET.parse(path).getroot()
            self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
            title = root.find("{http://www.w3.org/2000/svg}title")
            self.assertIsNotNone(title, f"Missing title in {filename}")
            self.assertTrue(len(title.text) > 5)


if __name__ == "__main__":
    unittest.main()
