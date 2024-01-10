#!/usr/bin/python3
# Released under GPLv3+ License
# Danial Behzadi <dani.behzi@ubuntu.com>, 2024.
"""
Unit tests for bridges
"""

import unittest
from tractor import bridges


class TestBridges(unittest.TestCase):
    """
    Main class for testing bridges
    """

    def setUp(self):
        """
        initialize class
        """
        super().setUp()
        self.lines = (
            "Bridge obfs4 162.223.88.72:43565 FADC7451A08A3B9690E38137C440C209"
            "E6683409 cert=DYku/2U6MZXDSoE9fiLmgdldLbaPjhAjdxMWPMU0Of4BL54a1cT"
            "6QDQv8V1H3onvlG80SQ iat-mode=2\n"
            "obfs4 81.169.154.212:8181 C13FE89EC22ED9DC26BC4EA40740C0DEEDC4B0D"
            "9 cert=GT7NbRmPO+2ieNlAlbhp+VFG2lHnY2ABGXAF+eaSlcw3P/v4Gpc5gjexjc"
            "mx5/sI+XWFXA iat-mode=0\n"
            "188.121.110.127:9056 F3D627AFD9EB5E1B8843733B06EBC2D3B6BAB209\n"
            "Bridge 148.121.110.127:9056 F3D627AFD9EB5E1B8843733B06EBC2D3B6BAB"
            "209\n"
        )

    def test_vanilla(self):
        """
        test vanilla bridge
        """
        expected = [
            "188.121.110.127:9056 F3D627AFD9EB5E1B8843733B06EBC2D3B6BAB209",
            "148.121.110.127:9056 F3D627AFD9EB5E1B8843733B06EBC2D3B6BAB209",
        ]
        self.assertEqual(bridges.relevant_lines(self.lines, 1), expected)

    def test_obfs(self):
        """
        test obfs4 bridge
        """
        expected = [
            "obfs4 162.223.88.72:43565 FADC7451A08A3B9690E38137C440C209E668340"
            "9 cert=DYku/2U6MZXDSoE9fiLmgdldLbaPjhAjdxMWPMU0Of4BL54a1cT6QDQv8V"
            "1H3onvlG80SQ iat-mode=2",
            "obfs4 81.169.154.212:8181 C13FE89EC22ED9DC26BC4EA40740C0DEEDC4B0D"
            "9 cert=GT7NbRmPO+2ieNlAlbhp+VFG2lHnY2ABGXAF+eaSlcw3P/v4Gpc5gjexjc"
            "mx5/sI+XWFXA iat-mode=0",
        ]
        self.assertEqual(bridges.relevant_lines(self.lines, 2), expected)

    def test_other(self):
        """
        test unknown bridge type
        """
        with self.assertRaises(ValueError):
            bridges.relevant_lines(self.lines, 0)


if __name__ == "__main__":
    unittest.main()
