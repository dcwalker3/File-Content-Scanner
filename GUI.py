import tkinter as tk
from tkinter import ttk
import tkinter.filedialog as fd
from turtle import width
from FileWalker import FileWalker
import os

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GUI")
        self.geometry("1000x1000")
        self.optionButtonsExist = False

        self.FileWalker = None

        # Add a button asking for path to scan.
        self.button = tk.Button(self, text="Select Directory to Scan", command=self.selectDir)
        self.button.pack()


        self.mainloop()

    def selectDir(self):
        # Open a dialog box to select a directory.
        self.dir = fd.askdirectory()
        if self.dir:
            self.FileWalker = FileWalker(self.dir)
            self.fileList = self.FileWalker.fileList
            self.dirList = self.FileWalker.dirList
            self.fileStructure = self.FileWalker.fileStructure

            self.FileWalker.printPrettyFileStructure(self.dir)
            
            # Check if buttons exist and leave them if they do.
            if self.optionButtonsExist == False:
                print("Scan button does not exist")
                # 2 Buttons will appear after the user clicks.
                # 1.) Show Files in Table
                # 2.) Scan Files
                self.showFilesButton = tk.Button(self, text="Show Files in Table", command=self.showTree)
                self.showFilesButton.pack()

                self.scanFilesButton = tk.Button(self, text="Scan Files", command=self.scanFiles)
                self.scanFilesButton.pack()
                self.optionButtonsExist = True

    
    def scanFiles(self):
        # Create a sepeate dialog to ask user what they want to scan for and what type of files they want to scan.
        self.scanDialog = tk.Toplevel(self)
        self.scanDialog.title("Scan Files")
        self.scanDialog.geometry("500x500")
        
        # Create a multi-line text box to enter the search terms.
        self.searchTerms = tk.Text(self.scanDialog, width=400, height=400)
        self.searchTerms.pack()

        # Create a button to start the scan.
        self.scanButton = tk.Button(self.scanDialog, text="Scan", command=self.startScan)
        self.scanButton.pack()

    def startScan(self):
        # Get the search terms from the text box.
        self.searchTerms = self.searchTerms.get("1.0", tk.END)
        print(self.searchTerms)
        

        
        

    def showTree(self):
        # Clear previous treeview if it exists.
        if hasattr(self, "tree"):
            self.tree.destroy()

        # Show the files in a treeview that is scrollable and goes all
        # across the window.
        self.tree = ttk.Treeview(self, columns=("File Path", "type"), show="tree", height=80)
        self.tree.pack()
        self.tree.heading("#0", text="File Name")
        self.tree.heading("File Path", text="File Path")
        self.tree.heading("type", text="type")

        self.tree.column("#0", width=250)
        self.tree.column("File Path", width=600)
        self.tree.column("type", width=150)
        self.tree.pack()

        # Add the files to the treeview.
        for file in self.fileStructure:
            fileName = os.path.basename(file)
            filePath = file
            if(os.path.isdir(file)):
                fileType = "Directory"
            else:
                fileType = "File"
            self.tree.insert("", tk.END, text=fileName, values=(filePath, fileType))


        

        
        
    def showFiles(self):
        # Show the files in a listbox that is scrollable and goes all
        # across the window.
        self.listbox = tk.Listbox(self, width=400, height=400, yscrollcommand=True)
        self.listbox.pack()
        for file in self.fileList:
            self.listbox.insert(tk.END, file)
    
        


