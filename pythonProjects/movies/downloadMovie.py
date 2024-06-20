from os import system, chdir, path, listdir
from pathlib import Path
import subprocess
from time import sleep
import psutil


def check_process(name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.name() == name:
            return True

    return False


def wait_until_process_finished(name):
    while check_process(name):
        sleep(1)


def main(movie_name):
    exe = "utweb.exe"
    new_directory = Path.home() / 'Downloads'
    chdir(new_directory)
    directory = str(new_directory)

    full_movie_name = directory + "\\" + movie_name

    cmd_line = f'{exe} "{full_movie_name}.torrent"'

    subprocess.Popen(cmd_line, shell=True)

    folder = ""

    while folder == "":
        for filename in listdir():
            f = path.join(directory, filename)

            if path.isdir(f) and movie_name in f.lower():
                folder = f

    system(f'MOVE "{full_movie_name}.torrent" "{folder}"')
    system(f'MOVE "{full_movie_name}.srt" "{folder}"')

    wait_until_process_finished(exe)

    chdir(folder)

    for filename in listdir():
        f = path.join(directory, filename)

        if path.isfile(f) and f.endswith(".mp4"):
            system(f'ren "{f}" "{movie_name}.mp4"')

    for filename in listdir():
        f = path.join(directory, filename)

        if path.isfile(f) and movie_name not in f:
            system(f'delete "{f}"')


if __name__ == "__main__":
    main("forrest gump")
