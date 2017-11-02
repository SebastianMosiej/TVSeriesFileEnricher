import unittest
# import os

from tv_series_name_expander import parse_parameters


class ArgumentParserTest(unittest.TestCase):
    test_class = None

    def test_no_argumnet(self):
        # GIVEN
        args = []
        # WHEN
        (options, args) = parse_parameters()
        # THEN
        self.assertEqual(args)
