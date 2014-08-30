import mapper
import processor
import fileprocessor

import argparse

import os
import logging
import logging.config
import time

#
# Main app start
#
print('Hello & welcome to dmessifier')

# Configure logging
logging_conf_filename = 'logging.conf'
if os.path.isfile(logging_conf_filename):
    logging.config.fileConfig(logging_conf_filename)
else:
    logging.basicConfig(level=logging.DEBUG)
    logging.warning('No logging.conf file found. Switching to default logging configuration.')

# Parse arguments
parser = argparse.ArgumentParser(description='Sort photo files.')
parser.add_argument('-s', '--source-directory', metavar='directory', required=True,
                    help='The source directory')
parser.add_argument('-t', '--target-directory', metavar='directory', required=True,
                    help='The target directory')

args = parser.parse_args()

options = dict()
options['dir.source'] = args.source_directory
options['dir.target'] = args.target_directory
options['dir.unmanaged'] = os.path.join(args.target_directory, "unmanaged")
options['dir.template'] = "$year/$month"
options['file.template'] = '$year-$month-$day.$hour.$minute.$second.$extension'

path_mapper = mapper.ImagePathMapper(options['dir.target'], options['dir.template'], options['file.template'])
file_processor = fileprocessor.FileProcessor(options['dir.source'], options['dir.unmanaged'])

processor = processor.Processor(path_mapper, file_processor)
processor.process(options['dir.source'], ['.jpg', '.psd'])
