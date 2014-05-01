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
parser.add_argument('-s','--source-directory', metavar='directory', required=True,
                        help='The source directory')
parser.add_argument('-t','--target-directory', metavar='directory', required=True,
                        help='The target directory')

args = parser.parse_args()

source_directory = args.source_directory
target_directory = args.target_directory

options = dict()
options['dir.target'] = target_directory
options['dir.unmanaged'] = os.path.join(target_directory, "unmanaged")
options['dir.template'] = "$year/$month"
options['file.template'] = '$year-$month-$day.$hour.$minute.$second.$extension'

path_mapper = mapper.ImagePathMapper(options)
file_processor = fileprocessor.FileProcessor(options)

processor = processor.Processor(path_mapper, file_processor)
processor.process(source_directory, ['.jpg', '.psd'])
