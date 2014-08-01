import exifread
import logging
import os
import string 
from time import gmtime

# ImagePathMapper
#
class ImagePathMapper:
    def __init__(self, options):

        self._options = options
        self._sequence_number = 0

    def map(self, image_path, suffix=None):

        logging.debug('Mapping "{} [suffix={}]"...'.format(image_path, suffix))
        f = open(image_path, 'rb')
        exif_tags = exifread.process_file(f, details=False)
        f.close()
        result = self._map(image_path, exif_tags, suffix)
        logging.debug('Mapped "{}" to "{}"'.format(image_path, result))
        return result

    def _map(self, image_path, exif_tags, suffix):

        # Create the templates
        file_template_string = self._options['file.template']
        file_template = string.Template(file_template_string)

        dir_template_string = self._options['dir.template']
        dir_template = string.Template(dir_template_string)

        # Prepare the binding for template substitution
        bindings = self._prepare_bindings(image_path, exif_tags)

        self._sequence_number += 1

        # Apply the template
        dir_target_result = self._options['dir.target']
        dir_result = dir_template.substitute(bindings)
        file_result = file_template.substitute(bindings)

        # Merge the result
        result = os.path.join(dir_target_result, dir_result, file_result)

        # Apply the suffix
        result = self._apply_suffix(result, suffix)

        return result

    def _prepare_bindings(self, image_path, exif_tags):

        filename, file_ext = os.path.splitext(image_path)

        date = None
        if 'EXIF DateTimeOriginal' in exif_tags.keys():
            date = self._parse_exif_date(str(exif_tags['EXIF DateTimeOriginal']))
        elif 'Image DateTime' in exif_tags.keys():
            date = self._parse_exif_date(str(exif_tags['Image DateTime']))
        else:
            logging.warning('No date available for "{}"'.format(image_path))
            date = self._parser_creation_time(image_path)

        bindings = dict()
        bindings['targetDir'] = self._options['dir.target']
        bindings['sequenceNumber'] = self._sequence_number
        bindings['extension'] = file_ext[1:]
        for date_key in date:
            bindings[date_key] = date[date_key]
        
        return bindings        

    def _parse_exif_date(self, date):

        # format YYYY:MM:DD HH:MM:SS
        #        0123456789012345678

        result = dict()

        result['year'] = date[0:4]
        result['month'] = date[5:7]
        result['day'] = date[8:10]
        result['hour'] = date[11:13]
        result['minute'] = date[14:16]
        result['second'] = date[17:]

        return result

    def _parser_creation_time(self, path):
        sec = os.path.getctime(path)
        time = gmtime(sec)

        return {
            'year': "{:04}".format(time.tm_year),
            'month': "{:02}".format(time.tm_mon),
            'day': "{:02}".format(time.tm_mday),
            'hour': "{:02}".format(time.tm_hour),
            'minute': "{:02}".format(time.tm_min),
            'second': "{:02}".format(time.tm_sec)
        }

    def _apply_suffix(self, raw_result, suffix):
        result = raw_result
        if suffix is not None:
            root, ext = os.path.splitext(raw_result)
            result = root + "-" + suffix + ext
        return result    