import logging
import os
import shutil


class FileProcessor:
    def __init__(self):
        pass

    def process(self, source, target):
        logging.info('Copying "{}" to "{}"'.format(source, target))
        target_dir, target_file = os.path.split(target)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copyfile(source, target)
