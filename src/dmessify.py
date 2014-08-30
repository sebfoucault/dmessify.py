import mapper
import processor
import fileprocessor

import argparse

import os
import logging
import logging.config

#
# Main app start
#
print('Hello & welcome to dmessifier')

#
# Configures logging
#
logging_conf_filename = 'logging.conf'
if os.path.isfile(logging_conf_filename):
    logging.config.fileConfig(logging_conf_filename)
else:
    logging.basicConfig(level=logging.DEBUG)
    logging.warning('No logging.conf file found. Switching to default logging configuration.')

#
# Parses the application arguments
#
parser = argparse.ArgumentParser(description='Sort photo files.')
parser.add_argument('-s', '--source-directory', metavar='directory', required=True,
                    help='The source directory')
parser.add_argument('-t', '--target-directory', metavar='directory', required=True,
                    help='The target directory')

args = parser.parse_args()

source_dir = args.source_directory

target_dir = args.target_directory
target_dir_template = "$year/$month"
target_file_template = '$year-$month-$day.$hour.$minute.$second.$extension'

unmanaged_dir = os.path.join(target_dir, "unmanaged")
unmanaged_dir_template = "$extension/$year/$month"

std_mapper = mapper.ImagePathMapper(target_dir, target_dir_template, target_file_template)
unmanaged_mapper = mapper.ImagePathMapper(unmanaged_dir, unmanaged_dir_template, target_file_template)

file_processor = fileprocessor.FileProcessor()

processor = processor.Processor(std_mapper, unmanaged_mapper, file_processor)
processor.process(source_dir, ['.jpg', '.psd'])
