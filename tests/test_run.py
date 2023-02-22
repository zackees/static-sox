"""
Unit test file.
"""

import os
import unittest
from subprocess import check_call

from static_sox.run import get_or_fetch_platform_executables_else_raise

HERE = os.path.dirname(os.path.abspath(__file__))
TEST_DATA_DIR = os.path.join(HERE, "test_data")
BELL_WAV = os.path.join(TEST_DATA_DIR, "bell.wav")
OUT_WAV = os.path.join(HERE, "out", "output.wav")
os.makedirs(os.path.dirname(OUT_WAV), exist_ok=True)


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        os.system("echo my test")
        sox_exe = get_or_fetch_platform_executables_else_raise()
        self.assertTrue(os.path.exists(sox_exe), f"sox_exe: {sox_exe} does not exist")

    def test_gain_alteration(self) -> None:
        """Test setting the gain on an mp3 file."""
        self.assertTrue(
            os.path.exists(BELL_WAV), f"bell_wav: {BELL_WAV} does not exist"
        )
        if os.path.exists(OUT_WAV):
            os.remove(OUT_WAV)
        check_call(f'static_sox "{BELL_WAV}" "{OUT_WAV}" gain -3', shell=True)
        os.remove(OUT_WAV)


if __name__ == "__main__":
    unittest.main()
