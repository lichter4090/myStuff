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

val = None


def closing(window):
    global val
    val = False
    window.destroy()
    return False


def cond(window):
    if val is not None:
        window.destroy()

    else:
        window .after(100, lambda: cond(window))


def main():
    ##  window  ##
    window = tk.Tk()
    window.title("Continue?")
    window.resizable(False, False)
    window.configure(background=BC)

    ##  Label frame  ##
    lbl_frm = tk.Frame()
    lbl_frm.configure(background=BC)

    url_lbl = tk.Label(master=lbl_frm, text="Continue?", font=TITLE_FONT, background=BC)

    url_lbl.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)

    ## buttons frame ##
    btn_frm = tk.Frame()
    btn_frm.configure(background=BC)

    yes = tk.Button(master=btn_frm, text="yes", font=BTN_FONT, borderwidth=BORDER_WIDTH,
                    command=lambda: globals().update(val=True))
    no = tk.Button(master=btn_frm, text="no", font=BTN_FONT, borderwidth=BORDER_WIDTH,
                   command=lambda: globals().update(val=False))

    yes.grid(padx=PAD_WIDGET, pady=PAD_WIDGET, row=0, column=0)
    no.grid(padx=PAD_WIDGET, pady=PAD_WIDGET, row=0, column=PAD_WIDGET)

    ## place frames ##
    lbl_frm.pack()
    btn_frm.pack()

    cond(window)
    window.protocol("WM_DELETE_WINDOW", lambda: closing(window))

    window.mainloop()

    return val


if __name__ == "__main__":
    main()
