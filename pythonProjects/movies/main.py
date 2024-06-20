import window
import getSubtitles
import getTorrent
import downloadMovie
import multiprocessing


def main():
    movie_name = window.main()
    
    if movie_name == "":
        return
        
    subtitles = multiprocessing.Process(target=getSubtitles.main, args=(movie_name,))
    torrent = multiprocessing.Process(target=getTorrent.main, args=(movie_name,))

    subtitles.start()
    torrent.start()

    subtitles.join()
    torrent.join()

    downloadMovie.main(movie_name)


if __name__ == "__main__":
    main()
