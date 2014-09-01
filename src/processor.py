import filecmp
import os
import common

class Processor:

    def __init__(self,
                 source_files_enumerator,
                 standard_mapper, unmanaged_mapper,
                 file_processor):

        self._standard_mapper = standard_mapper
        self._unmanaged_mapper = unmanaged_mapper
        self._file_processor = file_processor
        self._source_files_enumerator = source_files_enumerator

    def process(self, top, extensions):

        stats = {
            "processed": 0,
            "sourceDuplicate": 0,
            "targetDuplicate": 0,
            "unknownFileFormat": 0,
            "handled": 0,
            "error": 0,
        }

        for (source_path, source_duplicate, duplicated_path) in self._source_files_enumerator(top):

            stats['processed'] += 1

            # Check if the file is part of the files to be processed
            if source_duplicate:
                self.log("SKIPPING_DUP_SOURCE", source_path, duplicated_path)
                stats['sourceDuplicate'] += 1
                self._file_processor.ignore(source_path)
                continue

            (filename, file_ext) = os.path.splitext(source_path)

            # Checks is the file extension is manageable by the application
            # and selects the correct mapper accordingly
            mapper = self._standard_mapper
            if not file_ext.lower() in extensions:
                stats['unknownFileFormat'] += 1
                mapper = self._unmanaged_mapper

            # Computes the path name
            target_path = self._map(mapper, source_path, with_suffix=False)
            target_dir = os.path.dirname(target_path)

            target_duplicate = False

            # Check if the computed path already exists
            if os.path.exists(target_path):
                # Same path and same content
                if os.path.isfile(target_path) and filecmp.cmp(source_path, target_path, shallow=False):
                    self.log("SKIPPING_DUP_TARGET", source_path, target_path)
                    target_duplicate = True
                # Something else with the same name but already exist under a different name
                elif common.exists_file_by_content(target_dir, source_path):
                    self.log("SKIPPING_DUP_TARGET", source_path, target_dir)
                    target_duplicate = True
                # Same path used by another file, need to add a suffix
                else:
                    self.log("PROCESSING", source_path)
                    target_path = self._map(mapper, source_path, with_suffix=True)
            else:
                self.log("PROCESSING", source_path)

            if not target_duplicate:
                self._file_processor.process(source_path, target_path)
                stats['handled'] += 1
            else:
                self._file_processor.ignore(source_path)
                stats['targetDuplicate'] += 1

        print(stats)

    def _map(self, mapper, source_path, with_suffix):
        target_path = None
        if not with_suffix:
            target_path = mapper.map(source_path)
        else:
            suffix = 1
            while True:
                target_path = mapper.map(source_path, "{}".format(suffix))
                if not os.path.isfile(target_path):
                    break
                suffix += 1
        return target_path

    def log(self, event, filename, extra_info=None):
        if extra_info is None:
            print("[{}] {}".format(event, filename))
        else:
            print("[{}] {} ({})".format(event, filename, extra_info))