import tkinter as tk
from taskmanager import TaskManager

BG = "#d3d3d3"


def main():
    ##  window  ##
    window = tk.Tk()
    window.title("My Task Manager")
    window.configure(background=BG)
    window.resizable(False, False)

    tm = TaskManager(window)
    tm.run()

    window.mainloop()


if __name__ == "__main__":
    main()
