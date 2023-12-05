import tkinter as tk


TITLE_FONT_SIZE = 23
BTN_FONT_SIZE = 18

TITLE_FONT = ("Comic Sans MS", TITLE_FONT_SIZE)
BTN_FONT = ("Times New Roman", BTN_FONT_SIZE)

BC = "#61b52a"
BORDER_WIDTH = 7

ENT_WIDTH = 30
PAD_WIDGET = 20


def execute_command(window, selected_option, option_var):
    selected_option.set(option_var.get())
    window.destroy()


def main(lst_of_options, current):
    ##  window  ##
    window = tk.Tk()
    window.title("Settings")
    window.resizable(False, False)
    window.configure(background=BC)

    option_var = tk.StringVar()
    selected_option = tk.StringVar()

    option_var.set(current)  # Set the default selected option

    url_lbl = tk.Label(master=window, text="Settings", font=TITLE_FONT, background=BC)
    option_menu = tk.OptionMenu(window, option_var, *lst_of_options)

    option_menu.bind("<Return>", lambda event: execute_command(window, selected_option, option_var))

    url_lbl.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)
    option_menu.pack(pady=PAD_WIDGET, padx=PAD_WIDGET)

    window.bind("<Return>", lambda event: execute_command(window, selected_option, option_var))
    window.mainloop()

    return option_var.get()
