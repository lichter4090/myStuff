from os import chdir, listdir, path
from pathlib import Path
from tkinter import messagebox


def pop_msg(title, text):
    messagebox.showinfo(title, text)


class Progress:
    def __init__(self, maximum: int, val=0):
        self.val = val
        self.max = maximum

    def get(self):
        return (self.val / self.max) * 100

    def get_raw(self):
        return self.val

    def done(self):
        return self.get() == 100

    def add_one(self):
        self.val += 1

    def set(self, val: int):
        self.val = val


def change_dir_to(folder: str):
    new_directory = Path.home() / 'Downloads'
    chdir(new_directory)

    return str(new_directory)


def get_file(directory, func):
    for filename in listdir():
        f = path.join(directory, filename)

        if func(f):
            return f
