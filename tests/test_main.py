from __future__ import absolute_import, unicode_literals

import unittest

from mopidy  import __main__
import pytest

@pytest.fixture(scope="session",autouse=True)
def my_fixture():
    print("/" + "run coverage" + str(100*sum(__main__.cov)/len(__main__.cov)) + "%")
class main_test(unittest.TestCase):
    def test_Test(self):
        self.assertTrue(True)
