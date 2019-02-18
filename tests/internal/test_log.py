from __future__ import absolute_import, unicode_literals

import unittest

from mopidy.internal import log


class LogTest(unittest.TestCase):

    def setUp(self):
        self.csh = log.ColorizingStreamHandler({})

    # returned message is the same if no options are passed in
    def test_colorize_returns_unchanged_when_no_args(self):
        message = ""
        result = self.csh.colorize(message)
        self.assertEqual(message, result)

    # the returned message should contain the value of the
    # background/foreground color that is passed in
    def test_colorize_contains_color(self):
        message = ""

        # test for bg colors
        for color in log.COLORS:
            result = self.csh.colorize(message, color)
            colorValue = str(log.COLORS.index(color) + 40)
            self.assertTrue(colorValue in result)

        # test for fg colors
        for color in log.COLORS:
            result = self.csh.colorize(message, None, color)
            colorValue = str(log.COLORS.index(color) + 30)
            self.assertTrue(colorValue in result)
