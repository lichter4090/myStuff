import window
import getSubtitles


def main():
    movie_name = window.main()
    
    if movie_name == "":
        return
        
    getSubtitles.main(movie_name)


if __name__ == "__main__":
    main()
