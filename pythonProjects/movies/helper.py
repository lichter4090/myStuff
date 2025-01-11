import selenium.webdriver.remote.webelement
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import OperationSystemManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from time import sleep
import requests
from os import chdir, listdir, path
from pathlib import Path
from tkinter import messagebox
from tkinter import ttk
from tkinter import Label
import json

TORRENT_STEPS = "Connecting to website", "Searching movie", "Selecting torrent", "Downloading torrent", "File is in Downloads directory"
SUBS_STEPS = "Connecting to website", "Searching movie", "Logging in", "Selecting best subtitles", "Downloading Subtitles", "File is in Downloads directory"
WAIT = 5

DOWNLOADS_PATH = str(Path.home() / 'Downloads')


def execute(driver: webdriver.Chrome, command: str):
    return driver.execute_script(command)


def get_element(driver: webdriver.Chrome, kind: By, search: str, clear: bool = False, multiple: bool = False, wait=WAIT) \
        -> list[selenium.webdriver.remote.webelement.WebElement] | selenium.webdriver.remote.webelement.WebElement:

    WebDriverWait(driver, wait).until(ec.presence_of_element_located((kind, search)))

    if multiple:
        e = driver.find_elements(kind, search)
    else:
        e = driver.find_element(kind, search)

    if clear:
        e.clear()

    return e


def get_element_if_contains(driver: webdriver.Chrome, kind: By, search: str, contain: str,
                            func=lambda a, b: a.text == b) -> selenium.webdriver.remote.webelement.WebElement | None:
    elements = get_element(driver, kind, search, False, True)
    element = None

    for elem in elements:
        if func(elem, contain):
            element = elem
            break

    return element


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


def get_file(directory, func):
    for filename in listdir():
        f = path.join(directory, filename)

        if func(f):
            return f
