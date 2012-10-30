"""
Remember that vim.current.window.cursor returns tuple with (row, col),
however row starts with 1 and col starts with 0.
"""
import os
import sys
import unittest
from vimmock import VimMock

abspath = lambda *p: os.path.abspath(os.path.join(*p))
THIS = abspath(os.path.dirname(__file__))
ROOT_DIR = abspath(THIS, '..')

sys.modules['vim'] = VimMock()
sys.path.insert(0, ROOT_DIR)

TEST_MOD = abspath(THIS, 'unittestdata', 'mod.py')
TEST_MOD_BODY = open(TEST_MOD).read()

import superpy
import vim


class TestVimpy(unittest.TestCase):

    def setUp(self):
        vim.setup_text(TEST_MOD_BODY)

    def test_custom_self_id(self):
        "this is used instead of self"
        vim.current.window.cursor = (16, 8)
        superpy.get_super()
        self.assertEqual(vim.current.buffer[15],
            ' ' * 8 + 'super(Student, this).get_name()')

    def test_simplest_case(self):
        vim.current.window.cursor = (19, 8)
        superpy.get_super()
        self.assertEqual(vim.current.buffer[18],
            ' ' * 8 + 'super(Student, self).get_full_name()')

    def test_various_args(self):
        vim.current.window.cursor = (22, 8)
        superpy.get_super()
        self.assertEqual(vim.current.buffer[21],
            ' ' * 8 + 'super(Student, self).get_foo(name, *args, **kwargs)')


if __name__ == '__main__':
    unittest.main()

