from tkinter import *
import tkinter.ttk as ttk

root = Tk()

tree = ttk.Treeview(root)

tree["columns"] = ("Name", "ID", "Pizza")

tree.column("#0", minwidth=20, width=120)
tree.column("Name", anchor=W, width=120)
tree.column("ID", anchor=W, width=80)
tree.column("Pizza", anchor=W, width=120)

tree.heading("#0", text="", anchor=W)
tree.heading("Name", text="Name", anchor=W)
tree.heading("ID", text="ID", anchor=CENTER)
tree.heading("Pizza", text="Pizza", anchor=W)

tree.insert(parent="", index="end", iid=0, text="Parent", values=("John", 1, "Dominos"))
tree.insert(parent="", index="end", iid=1, text="Parent", values=("Al", 2, "Dominos"))
tree.insert(parent="", index="end", iid=2, text="", values=("Erl", 3, "Papa john's"))
tree.insert(parent="", index="end", iid=3, text="", values=("Walt", 4, "Domino"))
tree.insert(parent="1", index="end", iid=4, text="", values=("Steve", 5, "Domino"))

tree.pack()
root.mainloop()
