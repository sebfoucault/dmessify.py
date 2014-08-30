import logging
import os
import shutil


class FileProcessor:
    def __init__(self, source_directory, unmanaged_directory):
        self._source_directory = source_directory
        self._unmanaged_directory = unmanaged_directory

    def process(self, source, target):
        logging.info('Copying "{}" to "{}"'.format(source, target))
        target_dir, target_file = os.path.split(target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copyfile(source, target)

    def ignore(self, source):

        relpath = os.path.relpath(source, self._source_directory)
        (_, ext) = os.path.splitext(source)

        target = os.path.join(self._unmanaged_directory, ext[1:], relpath)
        target_dir, target_file = os.path.split(target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copyfile(source, target)
