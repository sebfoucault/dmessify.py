import common
import filecmp
import logging
import os

class Processor:

    def __init__(self, mapper, file_processor):
        self._mapper = mapper
        self._file_processor = file_processor

    def process(self, top, extensions):

        stats = {
            "processed": 0,
            "sourceDuplicate": 0,
            "targetDuplicate": 0,
            "unknownFileFormat": 0,
            "handled": 0,
            "error":0,
        }

        for source_path, source_duplicate, duplicated_path in common.unique_files_walker(top):

            stats['processed'] += 1

            if source_duplicate:
                logging.debug('Skipping duplicate "{}" (same as {}).'.format(source_path, duplicated_path))
                stats['sourceDuplicate'] += 1
                continue

            filename, file_ext = os.path.splitext(source_path)

            if file_ext.lower() in extensions:

                logging.debug('Processing "{}"'.format(source_path))
                target_path = self._map(source_path, with_suffix = False)
                target_dir = os.path.dirname(target_path)
                
                target_duplicate = False

                if os.path.exists(target_path):
                    if os.path.isfile(target_path) and filecmp.cmp(source_path, target_path, shallow=False):
                        logging.warning("The file {} already exist in {} with the same content. Skipping the file.".format(
                                        source_path, target_path))
                        target_duplicate = True
                    elif common.exists_file_by_content(target_dir, source_path):
                        logging.warning("The file {} already exist in {} with the same content. Skipping the file.".format(
                                        source_path, target_dir))                        
                        target_duplicate = True
                    else:
                        target_path = self._map(source_path, with_suffix=True)

                if target_duplicate == False:
                    self._file_processor.process(source_path, target_path)
                    stats['handled'] += 1
                else:
                    self._file_processor.ignore(source_path)
                    stats['targetDuplicate'] += 1

            else:
                logging.warning("Invalid file format: {}".format(source_path))
                stats['unknownFileFormat'] += 1

        print(stats)

    def _map(self, source_path, with_suffix):
        target_path = None
        if not with_suffix:
            target_path = self._mapper.map(source_path)
        else:
            suffix = 1
            while True:
                target_path = self._mapper.map(source_path, "{}".format(suffix))
                if not os.path.isfile(target_path):
                    break
                suffix += 1
        return target_path
