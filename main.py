import os
import glob
import sqlite3 as sql
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd

class Model():
    def __init__(self):
        self.con = sql.connect('.cache.db')
        self.cur = self.con.cursor()
        self.initTable()
        
    def initTable(self):
        #self.cur.execute("CREATE TABLE IF NOT EXISTS Settings (tpDir TEXT, tpName TEXT, rDir TEXT, rName TEXT, update BOOLEAN, type BOOLEAN)")
        self.con.commit()

    def addDataToTable(self):
        self.con.commit()

    def deleteDataFromTable(self):
        self.con.commit()

    def updateDataInTable(self):
        #self.cur.execute('Update settings Set tpdir = @tpdir, tpname = @tpname, rdir = @rdir, rname = @rname, update = @update, type = @type')
        self.con.commit()

    def getDataFromTable(self):
        self.con.commit()

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

        self.labelTPD = ttk.Label(self.root, text='Test Procedure Directory')
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

        self.variableTP = tk.StringVar(self.root)
        self.variableTP.set("Test Procedure") 

        self.optionMenuTP = tk.OptionMenu(self.root, self.variableTP, None)
        self.optionMenuTP.grid(row=2, column=0, padx=5, pady=5)

        self.variableSB = tk.StringVar(self.root)
        self.variableSB.set("Software Build")

        self.optionMenuSB = tk.OptionMenu(self.root, self.variableSB, None)
        self.optionMenuSB.grid(row=2, column=1, padx=5, pady=5)

    def getTPDEntry(self):
        return self.entryTPD.get()



class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.buttonTPD["command"] = self.updateTPDEntry
        self.view.buttonRD["command"] = self.updateRDEntry

    def updateTPDEntry(self):
        self.view.entryTPD.delete(1, tk.END)
        self.view.entryTPD.insert(0, fd.askdirectory())
        self.updateTPOptionMenu()

    def updateRDEntry(self):
        self.view.entryRD.delete(1, tk.END)
        self.view.entryRD.insert(0, fd.askdirectory())

    def getTPs(self):
        return [f for f in glob.glob("%s/*.py" % self.view.getTPDEntry())]
	

    def updateTPOptionMenu(self):
        menu = self.view.optionMenuTP["menu"]
        menu.delete(0, "end")
        for string in self.getTPs():
            print(string)
            menu.add_command(label=string, command=lambda value=string: self.view.variableTP.set(value))
	

if __name__ == '__main__':
    root = tk.Tk()
    model = Model()
    view = View(root)
    controller = Controller(model, view)
    root.mainloop()

