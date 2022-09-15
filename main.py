import os
import sqlite3 as sql
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd


class Model():
    def __init__(self):
        pass

class View():
    def __init__(self, root):
        self.root = root
        self.root.title("Setup Testing Environment")
        self.root.geometry("800x200+0+0")
        self.createWidgets()

    def createWidgets(self):
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)
        self.root.columnconfigure(4, weight=1)
        self.root.rowconfigure(3, weight=1)

        self.labelTPD = ttk.Label(self.root, text='Test Prodecure Directory')
        self.labelTPD.grid(row=0, column=0, padx=5, pady=5)

        self.entryTPD = ttk.Entry(self.root, text="", width=50)
        self.entryTPD.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

        self.buttonTPD = ttk.Button(self.root, text="Browse")
        self.buttonTPD.grid(row=0, column=3, padx=5, pady=5)

        self.labelRD = ttk.Label(self.root, text='Repository Directory')
        self.labelRD.grid(row=1, column=0, padx=5, pady=5)

        self.entryRD = ttk.Entry(self.root, text="", width=50)
        self.entryRD.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

        self.buttonRD = ttk.Button(self.root, text="Browse")
        self.buttonRD.grid(row=1, column=3, padx=5, pady=5)

class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.buttonTPD["command"] = self.updateTPDEntry
        self.view.buttonRD["command"] = self.updateRDEntry

    def updateTPDEntry(self):
        self.view.entryTPD.delete(1, tk.END)
        self.view.entryTPD.insert(0, fd.askdirectory())

    def updateRDEntry(self):
        self.view.entryRD.delete(1, tk.END)
        self.view.entryRD.insert(0, fd.askdirectory())


if __name__ == '__main__':
    root = tk.Tk()
    model = Model()
    view = View(root)
    controller = Controller(model, view)
    root.mainloop()
