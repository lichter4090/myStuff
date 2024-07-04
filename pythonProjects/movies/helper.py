from os import chdir, listdir, path
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk
from tkinter import Label


TORRENT_STEPS = "Connecting to website", "Searching movie", "Selecting torrent", "Renaming file", ""
SUBS_STEPS = "Connecting to website", "Searching movie", "Logging in", "Selecting best subtitles", "Renaming file", ""


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

    def set_end(self):
        self.val = self.max


class MonitorProcess:
    def __init__(self, pb: ttk.Progressbar, progress_val: Progress, label: Label, steps: list):
        self.pb = pb
        self.progress_val = progress_val
        self.label = label
        self.steps = steps

        self.active = progress_val.get_raw() != -1

        self.pb['value'] = 0

    def get_active(self) -> bool:
        return self.active

    def update(self) -> bool:  # returns true if done
        if self.active:
            self.pb['value'] = self.progress_val.get()
            self.label.config(text=self.steps[self.progress_val.get_raw()])

            return self.progress_val.done()

        return True


def change_dir_to(folder: str):
    new_directory = Path.home() / 'Downloads'
    chdir(new_directory)

    return str(new_directory)


def get_file(directory, func):
    for filename in listdir():
        f = path.join(directory, filename)

        if func(f):
            return f
