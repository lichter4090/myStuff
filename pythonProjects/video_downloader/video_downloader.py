import yt_dlp
import os
      

DOWNLOADS_PATH = os.path.expanduser('~/Downloads/')


def cls_command():
    os.system("cls")


def download_youtube_video(url, output_path):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_path + '%(title)s.%(ext)s',
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_youtube_audio(url, output_path):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path + '%(title)s.%(ext)s',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main():
    url = input("Enter url: ")
    choice = input("Enter 0 for mp3 or any other key for mp4: ")
    print()

    try:
        if int(choice) == 0:
            func = download_youtube_audio
        else:
            func = download_youtube_video

    except ValueError:
        func = download_youtube_video

    cls_command()

    try:
        print(f"Downloading video from URL: {url}")
        func(url, DOWNLOADS_PATH)
        cls_command()
        print(f"Downloaded successfully to: {DOWNLOADS_PATH[:-1]}")

    except Exception as e:
        print("Error: " + str(e))


if __name__ == "__main__":
    main()
