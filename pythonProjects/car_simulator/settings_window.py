import tkinter as tk


TITLE_FONT_SIZE = 23
BTN_FONT_SIZE = 18

TITLE_FONT = ("Comic Sans MS", TITLE_FONT_SIZE)
BTN_FONT = ("Times New Roman", BTN_FONT_SIZE)

BG = "#61b52a"
BORDER_WIDTH = 7

ENT_WIDTH = 30
PAD_WIDGET = 20

manual_option = None


def execute_command(window, selected_option, option_var, manual):
    global manual_option

    selected_option.set(option_var.get())
    manual_option = manual
    window.destroy()


def main(lst_of_options, current, manual=True):
    global manual_option

    manual_option = manual

    ##  window  ##
    window = tk.Tk()
    window.title("Settings")
    window.resizable(False, False)
    window.configure(background=BG)

    option_var = tk.StringVar()
    selected_option = tk.StringVar()
    manual_var = tk.IntVar()

    option_var.set(current)  # Set the default selected option
    manual_var.set(manual)

    # title
    title_lbl = tk.Label(window, text="Settings", font=TITLE_FONT, background=BG)

    # options
    options_frame = tk.Frame(background=BG)

    option_menu = tk.OptionMenu(options_frame, option_var, *lst_of_options)
    manual_chb = tk.Checkbutton(options_frame, text="Manual", variable=manual_var, onvalue=1, offvalue=0, relief="raised")
    option_menu.grid(padx=PAD_WIDGET, pady=PAD_WIDGET, row=0, column=0)
    manual_chb.grid(padx=PAD_WIDGET, pady=PAD_WIDGET, row=0, column=PAD_WIDGET)

    # confirm button
    send_btn = tk.Button(master=window, text="Confirm", font=BTN_FONT, command=lambda: execute_command(window, selected_option, option_var, manual_var))

    title_lbl.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)
    options_frame.pack()
    send_btn.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)

    option_menu.bind("<Return>", lambda event: execute_command(window, selected_option, option_var, manual_var))
    window.bind("<Return>", lambda event: execute_command(window, selected_option, option_var, manual_var))

    window.mainloop()

    return option_var.get(), bool(manual_var.get())


if __name__ == "__main__":
    print(main(["black", "green", "yellow"], "black", False))
