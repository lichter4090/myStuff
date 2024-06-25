import window
import getSubtitles
import getTorrent
import downloadMovie
import threading
from time import sleep
import helper


def main():
    movie_name, subs, movie = window.choosing_window()

    if movie_name == "" or (not subs and not movie):
        return

    progress_torrent = helper.Progress(4, -1)
    progress_subs = helper.Progress(5, -1)

    subtitles = None
    torrent = None

    if subs:
        subtitles = threading.Thread(target=getSubtitles.call_main, args=(movie_name, progress_subs,), daemon=True)
        subtitles.start()

    if movie:
        torrent = threading.Thread(target=getTorrent.call_main, args=(movie_name, progress_torrent,), daemon=True)
        torrent.start()

    sleep(1)
    window.monitoring_window(progress_torrent, progress_subs)

    if subtitles is not None:
        subtitles.join()

    if torrent is not None:
        torrent.join()

        downloadMovie.main(movie_name, subs)


if __name__ == "__main__":
    main()
