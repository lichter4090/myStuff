from os import system, path, listdir
import helper


def main(movie_name, with_subs=True):
    exe = "utweb.exe"
    directory = helper.change_dir_to('Downloads')

    full_movie_name = directory + "\\" + movie_name

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

    """
    chdir(folder)
    for filename in listdir():
        f = path.join(directory, filename)

        if path.isfile(f) and f.endswith(".mp4"):
            system(f'ren "{f}" "{movie_name}.mp4"')

    for filename in listdir():
        f = path.join(directory, filename)

        if path.isfile(f) and movie_name not in f:
            system(f'delete "{f}"')
    """


if __name__ == "__main__":
    main("forrest gump")
