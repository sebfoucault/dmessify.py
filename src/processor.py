import common
import filecmp
import logging
import os

class Processor:

    def __init__(self, mapper, file_processor):
        self._mapper = mapper
        self._file_processor = file_processor

    def process(self, top, extensions):

        error = 0
        bypassed = 0
        processed = 0

        for source_path in common.unique_files_walker(top):

            filename, file_ext = os.path.splitext(source_path)

            if file_ext.lower() in extensions:

                logging.debug('Processing "{}"'.format(source_path))
                target_path = self._map(source_path, with_suffix = False)
                target_dir = os.path.dirname(target_path)
                
                duplicate = False

                if os.path.exists(target_path):
                    if os.path.isfile(target_path) and filecmp.cmp(source_path, target_path, shallow=False):
                        logging.warning("The file {} already exist in {} with the same content. Skipping the file.".format(
                                        source_path, target_path))
                        duplicate = True
                    elif common.exists_file_by_content(target_dir, source_path):
                        logging.warning("The file {} already exist in {} with the same content. Skipping the file.".format(
                                        source_path, target_dir))                        
                        duplicate = True
                    else:
                        target_path = self._map(source_path, with_suffix=True)

                if duplicate == False:            
                    processed += 1
                    self._file_processor.process(source_path, target_path)
                else:
                    self._file_processor.ignore(source_path)
                    bypassed += 1

            else:
                logging.warning("Invalid file format: {}".format(source_path))
                bypassed += 1

        print("Processed files : {}".format(processed))
        print("Bypassed files : {}".format(bypassed))
        print("Error files : {}".format(error))

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
