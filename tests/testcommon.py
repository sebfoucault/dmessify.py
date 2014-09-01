import common
import testutils
import os
import unittest


class TestCommon(unittest.TestCase):

    def setUp(self):
        pass

    def test_unique_files_walker_empty(self):
        result = []
        for source_path in common.unique_files_walker(testutils.resource("resources/unique-walker/empty"), True):
            result.append(source_path)
        self.assertEqual(0,len(result))

    def test_unique_files_walker_one(self):
        result = []
        for source_path in common.unique_files_walker(testutils.resource("resources/unique-walker/one"), True):
            result.append(source_path)
        self.assertEqual(1, len(result))
        self.assertEqual("file.txt", os.path.basename(result[0][0]))

    def test_unique_files_walker_two(self):
        result = []
        for source_path in common.unique_files_walker(testutils.resource("resources/unique-walker/two"), True):
            result.append(source_path)
        self.assertEqual(2, len(result))
        self.assertEqual("file-01.txt", os.path.basename(result[0][0]))
        self.assertEqual(False, result[0][1])
        self.assertEqual("file-02.txt", os.path.basename(result[1][0]))
        self.assertEqual(True, result[1][1])
