import filecmp
import hashlib
import os


def files_walker(top):

    if not os.path.exists(top):
        raise Exception('The directory "{}" does not exist.'.format(top))

    for (root, dirs, filenames) in os.walk(top):
        for filename in filenames:
            full_path = os.path.join(root, filename)
            yield full_path


def unique_files_walker(top):

    if not os.path.exists(top):
        raise Exception('The directory "{}" does not exist.'.format(top))

    crc_map = {}
    for full_path in files_walker(top):
        crc = md5sum(full_path)

        candidate = None
        duplicate = False
        if crc in crc_map:
            candidates = crc_map[crc]
            candidate = next((x for x in candidates if filecmp.cmp(x, full_path, shallow=False)), None)
            if candidate is not None:
                duplicate = True
            else:
                crc_map[crc].append(full_path)                 
        else:
            crc_map[crc] = []
            crc_map[crc].append(full_path)
        yield (full_path, duplicate, candidate)


def md5sum(filename):
    f = file(filename, 'r')
    hasher = hashlib.md5()
    hasher.update(f.read(1024))
    hash_value = hasher.digest()
    f.close()
    return hash_value


def exists_file_by_content(dir_name, filename):

    # The result
    result = False

    # Get the entries of the directory and compare each of them to the file
    entries = os.listdir(dir_name)
    
    for entry in entries:
        entry_full_path = os.path.join(dir_name, entry)
        if not os.path.isfile(entry_full_path):
            continue
        if filecmp.cmp(entry_full_path, filename, shallow=False):
            result = True
            break

    return result