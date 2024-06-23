from os import chdir, listdir, path
from pathlib import Path


def change_dir_to(folder: str):
    new_directory = Path.home() / 'Downloads'
    chdir(new_directory)

    return str(new_directory)


def get_file(directory, func):
    for filename in listdir():
        f = path.join(directory, filename)

        if func(f):
            return f
