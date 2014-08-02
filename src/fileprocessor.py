import logging
import os
import shutil


class FileProcessor:
    def __init__(self, options):
        self._options = options

    def process(self, source, target):
        logging.info('Copying "{}" to "{}"'.format(source, target))
        target_dir, target_file = os.path.split(target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copyfile(source, target)

    def ignore(self, source):

        source_dir = self._options['dir.source']
        unmanaged_dir = self._options['dir.unmanaged']

        relpath = os.path.relpath(source, source_dir)
        _, ext = os.path.splitext(source)

        target = os.path.join(unmanaged_dir, ext[1:], relpath)
        target_dir, target_file = os.path.split(target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copyfile(source, target)
