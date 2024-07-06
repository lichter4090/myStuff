import tkinter as tk
from tkinter import ttk
import psutil
from rowprocess import RowProcess
from time import sleep
import threading


TITLE_FONT_SIZE = 23
BTN_FONT_SIZE = 18
ENT_FONT_SIZE = 20

TITLE_FONT = ("Comic Sans MS", TITLE_FONT_SIZE)
ENT_FONT = ("David", ENT_FONT_SIZE)
BTN_FONT = ("Comic Sans MS", BTN_FONT_SIZE)

BG = "#d3d3d3"
BORDER_WIDTH = 7

ENT_WIDTH = 30
PAD_WIDGET = 20


def a(d: dict, val) -> int:
    for idx, dict_val in enumerate(d.keys()):
        if dict_val == val:
            return idx


def update(tree: ttk.Treeview):
    processes = dict()
    col_id_pid = dict()

    while True:
        for proc in psutil.process_iter(['pid', 'name', 'username']):
            try:
                col = RowProcess(proc)

                if col.id in processes.keys():
                    tree.delete(col_id_pid[col.id])
                    del col_id_pid[col.id]

                processes[col.id] = col.percent
                processes = dict(sorted(processes.items(), key=lambda val: val[1], reverse=True))

                col_id = tree.insert("", a(processes, col.id), values=col.get_col())
                col_id_pid[col.id] = col_id

            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        print("Update done")
        sleep(0.5)


def main():
    ##  window  ##
    window = tk.Tk()
    window.title("My Task Manager")
    window.configure(background=BG)
    window.resizable(False, False)

    cols = RowProcess.get_titles()
    tree = ttk.Treeview(window, columns=cols, show="headings", height=20)
    scroll_bar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll_bar.set)

    style = ttk.Style()
    style.configure("Treeview.Heading", font=TITLE_FONT)  # Change font and size as needed

    for col in cols:
        tree.heading(col, text=col)

    tree.pack(side="left", expand=True)
    scroll_bar.pack(side="right", fill="y")

    update_thread = threading.Thread(target=update, args=(tree,), daemon=True)
    update_thread.start()

    window.mainloop()


if __name__ == "__main__":
    main()
