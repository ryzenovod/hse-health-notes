import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SVGS_DIR = ROOT / "docs/assets/social-sector"


class SocialSectorFigureTests(unittest.TestCase):
    def test_svg_files_exist_and_are_valid_xml(self) -> None:
        expected_files = [
            "social-sector-gdp-spending.svg",
            "hospital-acute-care-mix.svg",
            "public-institutions-rf-structure.svg",
            "english-trust-governance.svg",
        ]
        for filename in expected_files:
            path = SVGS_DIR / filename
            self.assertTrue(path.exists(), f"Missing SVG file: {filename}")
            root = ET.parse(path).getroot()
            self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
            title = root.find("{http://www.w3.org/2000/svg}title")
            self.assertIsNotNone(title, f"Missing title in {filename}")
            self.assertTrue(len(title.text) > 5)
