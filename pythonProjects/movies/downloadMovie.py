import os.path
from os import system, path, listdir
import helper


def main(movie_name: str, with_subs: bool = True):
    exe = "utweb.exe"
    directory = helper.change_dir_to('Downloads')

    full_movie_name = directory + "\\" + movie_name

    if not os.path.exists(full_movie_name):
        return

    cmd_line = f'{exe} "{full_movie_name}.torrent"'

    system(cmd_line)

    folder = ""

    while folder == "":
        for filename in listdir():
            f = path.join(directory, filename)

            if path.isdir(f) and movie_name in f.lower():
                folder = f

    system(f'MOVE "{full_movie_name}.torrent" "{folder}"')

    if with_subs:
        system(f'MOVE "{full_movie_name}.srt" "{folder}"')


if __name__ == "__main__":
    main("forrest gump")
