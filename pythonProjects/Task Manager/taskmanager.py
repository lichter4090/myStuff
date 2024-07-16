from rowprocess import RowProcess
import tkinter as tk
from tkinter import ttk
import psutil
import threading
from time import sleep


BTN_FONT_SIZE = 15
BTN_FONT = ("Comic Sans MS", BTN_FONT_SIZE)


class TaskManager:
    def __init__(self, window: tk.Tk):
        cols = RowProcess.get_titles()

        self.window = window
        self.tree = ttk.Treeview(window, height=20)
        self.scroll_bar = ttk.Scrollbar(window, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scroll_bar.set)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=BTN_FONT)  # Change font and size as needed

        self.tree["columns"] = cols

        self.tree.column("#0", minwidth=125, width=150, anchor=tk.W)
        self.tree.heading("#0", text="Name", anchor=tk.CENTER)

        for col, width in zip(cols, RowProcess.get_width_of_cols()):
            self.tree.column(col, anchor=tk.CENTER, width=width)
            self.tree.heading(col, text=col, anchor=tk.CENTER)

        self.tree.pack(side="left")
        self.scroll_bar.pack(side="right", fill="y")

        self.processes = dict()

    def update(self):
        while True:
            for proc in psutil.process_iter():
                col = RowProcess(proc)

                if col.id == 0:  # system idle process
                    cpu_usage = 100 - col.get_cpu_usage()
                    self.tree.heading("CPU", text=f"CPU: {cpu_usage:.2f}", anchor=tk.CENTER)
                    continue

                if col.get_has_parent():
                    continue  # if it has parent, the parent will display the process

                self.processes[col.id] = col.get_cpu_usage()
                current_idx = list(self.processes.keys()).index(col.id)
                new = current_idx == len(self.processes) - 1

                self.processes = dict(sorted(list(self.processes.items()), key=lambda a: a[RowProcess.get_cpu_idx()], reverse=True))

                if new:
                    self.tree.insert("", index=list(self.processes.keys()).index(col.id), iid=col.id, text=col.get_name(), values=col.get_col())
                else:
                    self.tree.move(col.id, "", list(self.processes.keys()).index(col.id))

                for child in col.get_children():
                    self.tree.insert(str(col.id), index=tk.END, iid=child.id, text=child.get_name(), values=child.get_col())

            sleep(0.5)

    def run(self):
        thread = threading.Thread(target=self.update, args=(), daemon=True)
        thread.start()
