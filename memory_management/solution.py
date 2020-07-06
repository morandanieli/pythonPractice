import os
import glob

UNITS = {"B": 1,
         "KB": 10**3,
         "MB": 10**6,
         "GB": 10**9,
         "TB": 10**12}


# Example inputs: "10.43 KB", "11 GB", "343.1 MB"
def parse_size(size):
    number, unit = size.split()
    return int(float(number)*UNITS[unit])


def list_nested_files(dir_name, minimal_file_size='10MB'):
    target_dir = os.path.join(dir_name, "*")

    file_list = glob.glob(target_dir)

    # filter is similar to map, but returns as list the values which are True to the function

    bytes_file_size = parse_size(minimal_file_size)
    files_with_minimal_size = filter(lambda f: os.path.isfile(f) and os.path.getsize(f) >= bytes_file_size, file_list)
    files_with_minimal_size_pretty = list(map(lambda f: (f, os.path.getsize(f)), files_with_minimal_size))

    for file_name, size in files_with_minimal_size_pretty:
        print(file_name, "\t", size)

    dirs = list(filter(lambda f: os.path.isdir(f), file_list))
    for dir in dirs:
        files_with_minimal_size_pretty += list_nested_files(dir, minimal_file_size)

    return files_with_minimal_size_pretty


if __name__ == '__main__':
    dir_name = os.path.expanduser("~")
    print(list_nested_files(dir_name, minimal_file_size='10 MB'))