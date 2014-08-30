import mapper
import shutil
import testutils
import os
import unittest

from time import gmtime

class TestMapper(unittest.TestCase):

    def setUp(self):
        self._output_directory = testutils.resource("output")
        if not os.path.exists(self._output_directory):
            os.makedirs(self._output_directory)

    def tearDown(self):
        shutil.rmtree(self._output_directory)

    def test_simple_mapping(self):
        path_mapper = self._create_default_mapper()
        result = path_mapper.map(testutils.resource("resources/mapper/IMG-01.JPG"))
        rel_result = os.path.relpath(result, self._output_directory)
        self.assertEqual("2008/12/2008-12-06.14.11.06.JPG", rel_result)

    def test_simple_mapping_with_suffix(self):
        path_mapper = self._create_default_mapper()
        result = path_mapper.map(testutils.resource("resources/mapper/IMG-01.JPG"), "1")
        rel_result = os.path.relpath(result, self._output_directory)
        self.assertEqual("2008/12/2008-12-06.14.11.06-1.JPG", rel_result)

    def test_no_exif_mapping(self):
        path_mapper = self._create_default_mapper()

        input = testutils.resource("resources/mapper/IMG-02.JPG")
        result = path_mapper.map(input)

        sec = os.path.getctime(input)
        time = gmtime(sec)
        fields = {
            'year': "{:04}".format(time.tm_year),
            'month': "{:02}".format(time.tm_mon),
            'day': "{:02}".format(time.tm_mday),
            'hour': "{:02}".format(time.tm_hour),
            'minute': "{:02}".format(time.tm_min),
            'second': "{:02}".format(time.tm_sec)
        }

        rel_result = os.path.relpath(result, self._output_directory)
        self.assertEqual("{}/{}/{}-{}-{}.{}.{}.{}.JPG".format(
            fields['year'], fields['month'],
            fields['year'], fields['month'], fields['day'],
            fields['hour'], fields['minute'], fields['second']), rel_result)

    def _create_default_options(self):
        options = dict()
        options['dir.target'] = self._output_directory
        options['dir.unmanaged'] = os.path.join(self._output_directory, "unmanaged")
        options['dir.template'] = "$year/$month"
        options['file.template'] = '$year-$month-$day.$hour.$minute.$second.$extension'
        return options

    def _create_default_mapper(self):
        opts = self._create_default_options()
        m = mapper.ImagePathMapper(opts['dir.target'], opts['dir.template'], opts['file.template'])
        return m