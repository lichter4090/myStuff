from os import system, chdir, environ
from pathlib import Path


def main(movie_name):
    print("Torrent" in environ['PATH'])

    return
    new_directory = Path.home() / 'Downloads'
    chdir(new_directory)

    cmd_line = "utweb.exe " + movie_name + ".torrent"

    system(cmd_line)


if __name__ == "__main__":
    main("forrest gump")
