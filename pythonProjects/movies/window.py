import tkinter as tk

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

movie_name = str()


def on_click(window: tk.Tk, movie: str):
    global movie_name
    window.destroy()
    movie_name = movie


def main():
    ##  window  ##
    window = tk.Tk()
    window.title("Downloading Subtitles")
    window.resizable(False, False)
    window.configure(background=BC)

    ##  Label frame  ##
    lbl_frm = tk.Frame()
    lbl_frm.configure(background=BC)

    movie_name_lbl = tk.Label(master=lbl_frm, text="What movie?", font=TITLE_FONT, background=BC)
    movie_name_lbl.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)

    ## buttons frame ##
    input_frame = tk.Frame()
    input_frame.configure(background=BC)

    input_box = tk.Entry(master=input_frame, font=ENT_FONT, width=ENT_WIDTH)
    send_btn = tk.Button(master=input_frame, text="Enter", font=BTN_FONT, command=lambda: on_click(window, input_box.get()))
    input_box.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)
    send_btn.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)

    ## place frames ##
    lbl_frm.pack()
    input_frame.pack()

    window.bind("<Return>", lambda a: on_click(window, input_box.get()))
    window.mainloop()

    return movie_name


if __name__ == "__main__":
    print(main())
