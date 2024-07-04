import threading
import tkinter as tk
from tkinter import ttk
from time import sleep
import helper

TITLE_FONT_SIZE = 23
BTN_FONT_SIZE = 18
ENT_FONT_SIZE = 20

TITLE_FONT = ("Comic Sans MS", TITLE_FONT_SIZE)
ENT_FONT = ("David", ENT_FONT_SIZE)
BTN_FONT = ("Comic Sans MS", BTN_FONT_SIZE)

BC = "#61b52a"
BORDER_WIDTH = 7

ENT_WIDTH = 30
PAD_WIDGET = 20

movie_name = str()


def on_click(window: tk.Tk, movie: str):
    global movie_name
    window.destroy()
    movie_name = movie


def choosing_window():
    ##  window  ##
    window = tk.Tk()
    window.title("Downloading movie and subtitles")
    window.resizable(False, False)
    window.configure(background=BC)

    ## check box things ##
    subs = tk.IntVar()
    movie = tk.IntVar()

    ##  Label frame  ##
    lbl_frm = tk.Frame()
    lbl_frm.configure(background=BC)

    movie_name_lbl = tk.Label(master=lbl_frm, text="What movie?", font=TITLE_FONT, background=BC)
    movie_name_lbl.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)

    ## Checkbox frame ##
    check_box_frame = tk.Frame()
    check_box_frame.configure(background=BC)
    subs_chb = tk.Checkbutton(check_box_frame, text="Subtitles", variable=subs, onvalue=0, offvalue=1, relief="raised")
    movie_chb = tk.Checkbutton(check_box_frame, text="Movie", variable=movie, onvalue=0, offvalue=1, relief="raised")

    subs_chb.grid(padx=PAD_WIDGET, pady=PAD_WIDGET, row=0, column=0)
    movie_chb.grid(padx=PAD_WIDGET, pady=PAD_WIDGET, row=0, column=PAD_WIDGET)

    ## button frame ##
    input_frame = tk.Frame()
    input_frame.configure(background=BC)

    input_box = tk.Entry(master=input_frame, font=ENT_FONT, width=ENT_WIDTH)
    input_box.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)

    ## place frames ##
    lbl_frm.pack()
    input_frame.pack()
    check_box_frame.pack()

    send_btn = tk.Button(master=window, text="Enter", font=BTN_FONT, command=lambda: on_click(window, input_box.get()))
    send_btn.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)

    window.bind("<Return>", lambda a: on_click(window, input_box.get()))
    window.mainloop()

    return movie_name, not subs.get(), not movie.get()


def start_progress(window: tk.Tk, monitor_torrent: helper.MonitorProcess, monitor_subs: helper.MonitorProcess):
    window.update_idletasks()

    subs_finished = False
    movie_finished = False

    while not (subs_finished and movie_finished):
        subs_finished = monitor_subs.update()
        movie_finished = monitor_torrent.update()

        window.update_idletasks()

        sleep(0.05)

    helper.pop_msg("Done", "Finished downloading")
    window.destroy()


def monitoring_window(progress_torrent=helper.Progress(1, -1), progress_subs=helper.Progress(1, -1)):
    ##  window  ##
    window = tk.Tk()
    window.title("Downloading")
    window.resizable(False, False)
    window.configure(background=BC)

    ##  title  ##
    title = tk.Label(text="Downloading...", font=TITLE_FONT, background=BC)

    ##  movie frame  ##
    movie_frame = tk.Frame()
    movie_frame.configure(background=BC)

    movie_lbl = tk.Label(movie_frame, text="Movie Progress", font=TITLE_FONT, bg=BC)
    pb_movie = ttk.Progressbar(movie_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
    txt_torrent_monitor = tk.Label(movie_frame, text="", font=BTN_FONT, bg=BC)

    movie_lbl.pack()
    pb_movie.pack()
    txt_torrent_monitor.pack()

    ##  subtitles frame  ##
    subs_frame = tk.Frame()
    subs_frame.configure(background=BC)

    subs_lbl = tk.Label(subs_frame, text="Subtitles Progress", font=TITLE_FONT, bg=BC)
    pb_subs = ttk.Progressbar(subs_frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
    txt_subs_monitor = tk.Label(subs_frame, text="", font=BTN_FONT, bg=BC)

    subs_lbl.pack()
    pb_subs.pack()
    txt_subs_monitor.pack()

    ## place frames ##
    title.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)

    if progress_subs.get_raw() != -1:
        subs_frame.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)

    if progress_torrent.get_raw() != -1:
        movie_frame.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)

    monitor_torrent = helper.MonitorProcess(pb_movie, progress_torrent, txt_torrent_monitor, helper.TORRENT_STEPS)
    monitor_subs = helper.MonitorProcess(pb_subs, progress_subs, txt_subs_monitor, helper.SUBS_STEPS)

    ##  monitor thread  ##
    monitor = threading.Thread(target=start_progress, args=(window, monitor_torrent, monitor_subs),
                               daemon=True)
    monitor.start()

    window.mainloop()


if __name__ == "__main__":
    monitoring_window()
    # choosing_window()
