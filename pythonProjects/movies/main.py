import window
import getSubtitles
import getTorrent
import downloadMovie
import multiprocessing


def main():
    movie_name, subs, movie = window.main()

    if movie_name == "" or (not subs and not movie):
        return

    subtitles = None
    torrent = None

    progress_torrent = multiprocessing.Value('i', 0)
    progress_subs = multiprocessing.Value('i', 0)

    if subs:
        subtitles = multiprocessing.Process(target=getSubtitles.main, args=(movie_name, progress_subs,))
        subtitles.start()

    if movie:
        torrent = multiprocessing.Process(target=getTorrent.main, args=(movie_name, progress_torrent,))
        torrent.start()

    if subs and movie:
        while torrent.is_alive() and subtitles.is_alive():
            pass  # monitor both

    elif subs:
        while subtitles.is_alive():
            pass  # monitor only subs

    else:
        while torrent.is_alive():
            pass  # monitor torrent only

    #  if movie:
    #    downloadMovie.main(movie_name, subs)


if __name__ == "__main__":
    main()
