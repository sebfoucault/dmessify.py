import common
import filecmp
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
            "error": 0,
        }

        for (source_path, source_duplicate, duplicated_path) in common.unique_files_walker(top):

            stats['processed'] += 1

            # Check if the file is part of the files to be processed
            if source_duplicate:
                self.log("SKIPPING_DUP_SOURCE", source_path, duplicated_path)
                stats['sourceDuplicate'] += 1
                continue

            filename, file_ext = os.path.splitext(source_path)

            # Check is the file extension is manageable by the application
            if not file_ext.lower() in extensions:
                stats['unknownFileFormat'] += 1
                self._file_processor.ignore(source_path)
                continue

            # Computing the path name
            target_path = self._map(source_path, with_suffix=False)
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
                    target_path = self._map(source_path, with_suffix=True)

            if not target_duplicate:
                self.log("PROCESSING", source_path)
                self._file_processor.process(source_path, target_path)
                stats['handled'] += 1
            else:
                stats['targetDuplicate'] += 1

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

    def log(self, event, filename, extra_info=None):
        print("[{}] {}".format(event, filename))