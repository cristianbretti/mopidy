import unittest
from mopidy.local import commands
import argparse
import pytest

class LocalCommandTest(unittest.TestCase):
    def test_RunTest(self):
        cmd = commands.ScanCommand()
        config ={ 'local': {'media_dir': 0,'scan_timeout':0,'scan_flush_threshold':0,'excluded_file_extensions':[],'library':0}}
        result = cmd.parse([])
        val = False;
        try:
            cmd.run(result,config)
        except:
            val = True
        self.assertTrue(val)

