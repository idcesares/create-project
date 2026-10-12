import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import wordtally


class WordTallyTests(unittest.TestCase):
    def test_total(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.txt"
            path.write_text("The cat and the hat. It's the end.", encoding="utf-8")
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                wordtally.main([str(path)])
            self.assertEqual(out.getvalue().strip(), "8")


if __name__ == "__main__":
    unittest.main()
