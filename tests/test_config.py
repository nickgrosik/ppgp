import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from ppgp.config import _time_string, generate_timestamped_name


class ConfigTests(unittest.TestCase):
    def test_time_string_formats_without_leading_zero(self):
        self.assertEqual(_time_string(datetime(2026, 3, 30, 15, 49)), "3-49pm")

    def test_generate_timestamped_name_versions_when_collision_exists(self):
        with tempfile.TemporaryDirectory() as td:
            directory = Path(td)
            first = generate_timestamped_name("encrypted", ".bin", directory)
            first.write_bytes(b"x")
            second = generate_timestamped_name("encrypted", ".bin", directory)

            self.assertNotEqual(first, second)
            self.assertIn("_v2", second.name)


if __name__ == "__main__":
    unittest.main()
