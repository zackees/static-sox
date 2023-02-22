"""
Unit test file.
"""

import os
import unittest


class MainTester(unittest.TestCase):
    """Main tester class."""

    def test_imports(self) -> None:
        """Test command line interface (CLI)."""
        os.system("echo my test")


if __name__ == "__main__":
    unittest.main()
