import unittest
import os
import sys


sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import setup
from tests import concurrences_var


class TestGitApi(unittest.TestCase):

    def test_multipage_starred(self):
        test_user_multipage = 'Nerevarsoul'
        git_api = setup.GitApi(test_user_multipage)
        git_api.run()
        self.assertEqual(git_api.get_result(), concurrences_var.multipage_concurrences)

    def test_unopage_starred(self):
        test_user_unopage = 'Toouren'
        git_api = setup.GitApi(test_user_unopage)
        git_api.run()
        self.assertEqual(git_api.get_result(), concurrences_var.unopage_concurrences)

    def test_nopage_starred(self):
        test_user_nopage = 'WalkingCake'
        git_api = setup.GitApi(test_user_nopage)
        self.assertEqual(git_api.run(), 1)

    def test_unknow_user(self):
        test_unknown_user = 'cbuij'
        git_api = setup.GitApi(test_unknown_user)
        self.assertEqual(git_api.run(), 3)


if __name__ == '__main__':
    unittest.main()
