import filecmp
import md5
import logging
import os


def files_walker(top):
    for root, dirs, filenames in os.walk(top):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            yield full_path

def unique_files_walker(top):

    crc_map = {}

    for full_path in files_walker(top):
        crc = md5sum(full_path)

        duplicate = False
        if crc in crc_map:
            candidates = crc_map[crc]
            candidate = next( (x for x in candidates if filecmp.cmp(x, full_path, shallow=False)), None)
            if candidate is not None:
                logging.debug('Skipping "{}" same as {}.'.format(full_path, candidate))
                duplicate = True
            else:
                crc_map[crc].append(full_path)                 
        else:
            crc_map[crc] = []
            crc_map[crc].append(full_path)
        if not duplicate:
            yield full_path


def md5sum(filename):
    f = file(filename, 'r')
    hasher = md5.new(f.read(1024))
    hashValue = hasher.digest()
    f.close()
    return hashValue


def exists_file_by_content(dirname, filename):

    # The result
    result = False

    # Get the entries of the directory and compare each of them to the file
    entries = os.listdir(dirname)
    
    for entry in entries:
        entry_full_path = os.path.join(dirname, entry)
        if not os.path.isfile(entry_full_path):
            continue
        if filecmp.cmp(entry_full_path, filename, shallow=False):
            result = True
            break

    return result