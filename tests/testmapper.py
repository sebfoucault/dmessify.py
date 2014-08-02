import mapper
import shutil
import testutils
import os
import unittest


class TestMapper(unittest.TestCase):

    def setUp(self):
        self._output_directory = testutils.resource("output")
        if not os.path.exists(self._output_directory):
            os.makedirs(self._output_directory)

    def tearDown(self):
        shutil.rmtree(self._output_directory)

    def test_simple_mapping(self):
        options = self._create_default_options()
        path_mapper = mapper.ImagePathMapper(options)
        result = path_mapper.map(testutils.resource("resources/mapper/IMG-01.JPG"))
        rel_result = os.path.relpath(result, self._output_directory)
        self.assertEqual("2008/12/2008-12-06.14.11.06.JPG", rel_result)

    def test_simple_mapping_with_suffix(self):
        options = self._create_default_options()
        path_mapper = mapper.ImagePathMapper(options)
        result = path_mapper.map(testutils.resource("resources/mapper/IMG-01.JPG"), "1")
        rel_result = os.path.relpath(result, self._output_directory)
        self.assertEqual("2008/12/2008-12-06.14.11.06-1.JPG", rel_result)


    def _create_default_options(self):
        options = dict()
        options['dir.target'] = self._output_directory;
        options['dir.unmanaged'] = os.path.join(self._output_directory, "unmanaged")
        options['dir.template'] = "$year/$month"
        options['file.template'] = '$year-$month-$day.$hour.$minute.$second.$extension'
        return options