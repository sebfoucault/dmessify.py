import logging
import os
import shutil


class FileProcessor:

    MOVE = 1
    COPY = 2

    def __init__(self, mode):

        self._mode = mode

    def process(self, source, target):

        # Prepares the operation by creating the potentially unexisting directories
        (target_dir, target_file) = os.path.split(target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        # Runs the actual operation
        if self._mode == FileProcessor.COPY:
            logging.info('Copying "{}" to "{}"'.format(source, target))
            shutil.copyfile(source, target)
        elif self._mode == FileProcessor.MOVE:
            logging.info('Moving "{}" to "{}"'.format(source, target))
            shutil.move(source, target)

    def ignore(self, source):

        if self._mode == FileProcessor.COPY:
            pass
        else:
            os.remove(source)
