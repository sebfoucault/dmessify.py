import common
import test_utils
import os
import unittest


class TestCommon(unittest.TestCase):

    def setUp(self):
        pass

    def test_unique_files_walker_empty(self):
        result = []
        for source_path in common.unique_files_walker(test_utils.resource("resources/unique-walker/empty")):
            result.append(source_path)
        self.assertEqual(0,len(result))

    def test_unique_files_walker_one(self):
        result = []
        for source_path in common.unique_files_walker(test_utils.resource("resources/unique-walker/one")):
            result.append(source_path)
        self.assertEqual(1,len(result))
        self.assertEqual("file.txt", os.path.basename(result[0]))

    def test_unique_files_walker_two(self):
        result = []
        for source_path in common.unique_files_walker(test_utils.resource("resources/unique-walker/two")):
            result.append(source_path)
        self.assertEqual(1, len(result))
        self.assertEqual("file-01.txt", os.path.basename(result[0]))