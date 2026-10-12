import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from pager import page


class PagerTests(unittest.TestCase):
    def test_first_page_starts_at_first_item(self):
        self.assertEqual(page(list(range(10)), 1, 3), [0, 1, 2])


if __name__ == "__main__":
    unittest.main()
