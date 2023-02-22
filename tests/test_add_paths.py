"""
Unit test file.
"""

# pylint: disable=R0801

import os
import unittest
from subprocess import check_call

from static_sox import add_paths

HERE = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(HERE, "test_data")
BELL_WAV = os.path.join(TEST_DATA_DIR, "bell.wav")
OUT_WAV = os.path.join(HERE, "out", "output.wav")
os.makedirs(os.path.dirname(OUT_WAV), exist_ok=True)


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_add_paths(self) -> None:
        """Test setting the gain on an mp3 file."""
        self.assertTrue(os.path.exists(BELL_WAV), f"bell_wav: {BELL_WAV} does not exist")
        if os.path.exists(OUT_WAV):
            os.remove(OUT_WAV)
        add_paths(weak=False)
        check_call(f'sox "{BELL_WAV}" "{OUT_WAV}" gain -3', shell=True)
        os.remove(OUT_WAV)


if __name__ == "__main__":
    unittest.main()
