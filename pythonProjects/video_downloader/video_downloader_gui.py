import tkinter as tk
import video_downloader
import os
import pop_allert

TITLE_FONT_SIZE = 23
BTN_FONT_SIZE = 18
ENT_FONT_SIZE = 20

TITLE_FONT = ("Comic Sans MS", TITLE_FONT_SIZE)
ENT_FONT = ("David", ENT_FONT_SIZE)
BTN_FONT = ("Times New Roman", BTN_FONT_SIZE)

BC = "#61b52a"
BORDER_WIDTH = 7

ENT_WIDTH = 30
PAD_WIDGET = 20

DEFAULT_ENTRY_VALUE = "Enter url here"

DOWNLOADS_PATH = os.path.join(os.environ['USERPROFILE'], 'Downloads')


def execute_command(url, func):
    try:
        func(url, video_downloader.DOWNLOADS_PATH)
        pop_allert.pop_msg("Success", "Saved video, check in downloads folder")

    except Exception as e:
        pop_allert.pop_msg("Error", f"Failed to save video:\n{e}")

    video_downloader.cls_command()


def main():
    ##  window  ##
    window = tk.Tk()
    window.title("Youtube Videos Downloader")
    window.resizable(False, False)
    window.configure(background=BC)

    ##  url frame  ##
    url_frm = tk.Frame()
    url_frm.configure(background=BC)

    url_lbl = tk.Label(master=url_frm, text="Youtube Video Downloader", font=TITLE_FONT, background=BC)
    url_ent = tk.Entry(master=url_frm, font=ENT_FONT, width=ENT_WIDTH)

    url_ent.insert(0, DEFAULT_ENTRY_VALUE)

    url_ent.bind("<FocusIn>", lambda event: url_ent.delete(0, tk.END))  # Bind event handler for clicking on the Entry

    url_lbl.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)
    url_ent.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)

    ## buttons frame ##
    btn_frm = tk.Frame()
    btn_frm.configure(background=BC)

    mp3_btn = tk.Button(master=btn_frm, text="mp3 (audio)", font=BTN_FONT, borderwidth=BORDER_WIDTH, command=lambda: execute_command(url_ent.get(), video_downloader.download_youtube_audio))
    mp4_btn = tk.Button(master=btn_frm, text="mp4 (video)", font=BTN_FONT, borderwidth=BORDER_WIDTH, command=lambda: execute_command(url_ent.get(), video_downloader.download_youtube_video))

    mp3_btn.grid(padx=PAD_WIDGET, pady=PAD_WIDGET, row=0, column=0)
    mp4_btn.grid(padx=PAD_WIDGET, pady=PAD_WIDGET, row=0, column=PAD_WIDGET)

    ## place frames ##
    url_frm.pack()
    btn_frm.pack()

    window.mainloop()


if __name__ == "__main__":
    main()
