from __future__ import absolute_import, unicode_literals

import unittest

from mopidy.local import commands
import pytest

@pytest.fixture(scope="session",autouse=True)
def my_fixture():
    print("/" + "run coverage" + str(100*sum(commands.cov)/len(commands.cov)) + "%")
class command_tests(unittest.TestCase):
    def test_Test(self):
        self.assertTrue(True)
