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

    if subs:
        subtitles = multiprocessing.Process(target=getSubtitles.main, args=(movie_name,))
        subtitles.start()

    if movie:
        torrent = multiprocessing.Process(target=getTorrent.main, args=(movie_name,))
        torrent.start()

    if subtitles:
        subtitles.join()

    if torrent:
        torrent.join()

    if movie:
        downloadMovie.main(movie_name, subs)


if __name__ == "__main__":
    main()
