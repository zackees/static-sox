"""
Unit test file.
"""

import os
import unittest

from static_sox.run import get_or_fetch_platform_executables_else_raise


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        os.system("echo my test")
        sox_exe = get_or_fetch_platform_executables_else_raise()
        self.assertTrue(os.path.exists(sox_exe), f"sox_exe: {sox_exe} does not exist")


if __name__ == "__main__":
    unittest.main()
