import os
import glob
import sqlite3 as sql
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as fd
from tkinter import messagebox

class Model():
    def __init__(self):
        self.database = os.path.dirname(os.path.abspath(__file__)) + "/.cache.db"
        self.con = sql.connect(self.database)
        self.cur = self.con.cursor()
        self.initTable()
        
    def initTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS settings (key varchar PRIMARY KEY, value varchar NOT NULL);")
        self.con.commit()

    def addDataToTable(self, settings):
        for setting in settings:
            self.cur.execute("INSERT INTO settings (key, value) VALUES (?, ?);", setting)
        self.con.commit()

    def deleteDataFromTable(self, keys):
        for key in keys:
            self.cur.execute("DELETE FROM settings WHERE key = ?;", [key])
        self.con.commit()
        
    def getDataFromTable(self, keys):
        values = []
        for key in keys:
            self.cur.execute("SELECT value FROM settings WHERE key = ?;", [key])
            values.append(self.cur.fetchone())
        self.con.commit()
        return values
    
    def getAllDataFromTable(self):
        self.cur.execute("SELECT * FROM settings;")
        values = self.cur.fetchall()
        self.con.commit()
        return values

    def updateDataInTable(self, settings):
        for setting in settings:
            print(setting)
            self.cur.execute("UPDATE settings SET value = ? WHERE key = ?;", setting)
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

        self.defaultVariableTPText = 'Software Builds'
        self.variableTP = tk.StringVar(self.root)
        self.variableTP.set(self.defaultVariableTPText) 

        self.optionMenuTP = tk.OptionMenu(self.root, self.variableTP, None)
        self.optionMenuTP.grid(row=2, column=0, padx=5, pady=5)

        self.defaultVariableSBText = 'Test Procedure'
        self.variableSB = tk.StringVar(self.root)
        self.variableSB.set(self.defaultVariableSBText)

        self.optionMenuSB = tk.OptionMenu(self.root, self.variableSB, None)
        self.optionMenuSB.grid(row=2, column=1, padx=5, pady=5)
        
        self.radioButton = tk.IntVar()
        self.radioButton.set(1)

        self.radioButtonType1 = tk.Radiobutton(self.root, text="Type 1", variable=self.radioButton, value=1)
        self.radioButtonType1.grid(row=2, column=2, padx=5, pady=5)

        self.radioButtonType2 = tk.Radiobutton(self.root, text="Type 2", variable=self.radioButton, value=2)
        self.radioButtonType2.grid(row=2, column=3, padx=5, pady=5)
        
        self.checkButton = tk.IntVar()
        self.checkButtonErase = tk.Checkbutton(self.root, text='Erase',variable=self.checkButton, onvalue=1, offvalue=0)
        self.checkButtonErase.grid(row=3, column=0, padx=5, pady=5)
        
        self.buttonExecute = tk.Button(self.root, text ="OK")
        self.buttonExecute.grid(row=3, column=3, padx=5, pady=5)


    def getTPDEntry(self):
        return self.entryTPD.get()
    
    def setTPDEntry(self,value):
        self.entryTPD.delete(0,"end")
        self.entryTPD.insert(0,value)
    
    def getRDEntry(self):
        return self.entryRD.get()
    
    def setRDEntry(self,value):
        self.entryRD.delete(0,"end")
        self.entryRD.insert(0,value)
    
    def getOptionsMenuTP(self):
        return self.variableTP.get()
    
    def setOptionsMenuTP(self, value):
        self.variableTP.set(value)
    
    def getOptionsMenuSB(self):
        return self.variableSB.get()
    
    def setOptionsMenuSB(self, value):
        self.variableSB.set(value)
    
    def getRadioButton(self):
        return self.radioButton.get()
    
    def setRadioButton(self, value):
        self.radioButton.set(value)
    
    def getCheckButton(self):
        return self.checkButton.get()
    
    def setCheckButton(self, value):
        self.checkButton.set(value)

class Controller():
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        self.view.root.protocol("WM_DELETE_WINDOW", self.deleteFun)

        self.view.buttonTPD["command"] = self.updateTPDEntry
        self.view.buttonRD["command"] = self.updateRDEntry
        self.view.buttonExecute["command"] = self.setup
        
        self.loadSettings()
        
    def deleteFun(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.saveSettings()
            self.model.cur.close()
            self.view.root.destroy()
   
    def loadSettings(self):
        result = self.model.getDataFromTable(["entryTPD"])
        if result[0] is not None and len(result[0][0]) > 0:
                self.view.setTPDEntry(result[0])
                
        result = self.model.getDataFromTable(["entryRD"])
        if result[0] is not None and len(result[0][0]) > 0:
                self.view.setRDEntry(result[0])
                
#        result = self.model.getDataFromTable(["checkButton"])
#        if result[0] is not None and len(result[0][0]) > 0:
#                self.view.setCheckButton(result[0])
    
    def saveSettings(self):
        key = "entryTPD"
        value = self.view.getTPDEntry()
        result = self.model.getDataFromTable([key])
        if result[0] is not None:
            self.model.updateDataInTable([(value, key)])
        else:
            self.model.addDataToTable([(key, value)])
            
        key = "entryRD"
        value = self.view.getRDEntry()
        result = self.model.getDataFromTable([key])
        if result[0] is not None:
            self.model.updateDataInTable([(value, key)])
        else:
            self.model.addDataToTable([(key, value)])
            
        key = "checkButton"
        value = self.view.getCheckButton()
        result = self.model.getDataFromTable([key])
        if result[0] is not None:
            self.model.updateDataInTable([(value, key)])
        else:
            self.model.addDataToTable([(key, value)])
            
        key = "radioButton"
        value = self.view.getRadioButton()
        result = self.model.getDataFromTable([key])
        if result[0] is not None:
            self.model.updateDataInTable([(value, key)])
        else:
            self.model.addDataToTable([(key, value)])
            
        key = "optionsMenuSB"
        value = self.view.getOptionsMenuSB()
        result = self.model.getDataFromTable([key])
        if result[0] is not None:
            self.model.updateDataInTable([(value, key)])
        else:
            self.model.addDataToTable([(key, value)])
                                                   
        key = "optionsMenuTP"
        value = self.view.getOptionsMenuTP()
        result = self.model.getDataFromTable([key])
        if result[0] is not None:
            self.model.updateDataInTable([(value, key)])
        else:
            self.model.addDataToTable([(key, value)])                                                 
                                                         
    def setup(self):
        print(self.view.getRadioButton())

    def updateTPDEntry(self):
        self.view.entryTPD.delete(1, tk.END)
        self.view.entryTPD.insert(0, fd.askdirectory())
        self.updateTPOptionMenu()

    def updateRDEntry(self):
        self.view.entryRD.delete(1, tk.END)
        self.view.entryRD.insert(0, fd.askdirectory())
        self.updateSBOptionMenu()
        
    def getSBs(self):
        return [f.path for f in os.scandir(self.view.getRDEntry()) if f.is_dir()]

    def getTPs(self):
        return [f for f in glob.glob("%s/*.py" % self.view.getTPDEntry())]

    def updateTPOptionMenu(self):
        menu = self.view.optionMenuTP["menu"]
        menu.delete(0, "end")
        for string in [self.view.defaultVariableTPText] + self.getTPs():
            basename = os.path.basename(string)
            menu.add_command(label=basename, command=lambda value=basename: self.view.variableTP.set(value))
            
    def updateSBOptionMenu(self):
        menu = self.view.optionMenuSB["menu"]
        menu.delete(0, "end")
        for string in [self.view.defaultVariableSBText] + self.getSBs():
            basename = os.path.basename(string)
            menu.add_command(label=basename, command=lambda value=basename: self.view.variableSB.set(value))       
    

if __name__ == '__main__':
    root = tk.Tk()
    model = Model()
    view = View(root)
    controller = Controller(model, view)
    root.mainloop()

