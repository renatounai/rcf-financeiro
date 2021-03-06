from unittest import TestCase

from utils.string_utils import is_not_empty, is_empty


class Test(TestCase):
    def test_is_not_empty(self):
        name = 'Renato'
        self.assertTrue(is_not_empty(name))

    def test_is_empty(self):
        text = ''
        self.assertTrue(is_empty(text))

    def test_is_empty_white_space(self):
        text = '        '
        self.assertTrue(is_empty(text))

    # noinspection PyTypeChecker
    def test_is_empty_none(self):
        text = None
        self.assertTrue(is_empty(text))
