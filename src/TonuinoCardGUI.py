import os
import tkinter as tk
from tkinter import ttk
import pathlib
import eyed3
import re


def listOfmp3s(folder: pathlib.Path):
    return list(pathlib.Path(folder).glob("*\\*.mp3"))


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("1280x1024")
        # self.master.height = 1024
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.updateFolderTree
        self.hi_there.grid(row=0)

        # here is the application variable
        self.sdcardfolder = tk.StringVar()
        # set it to some value
        self.sdcardfolder.set("C:\\Users\\Joe\\Music")

        self.sdcardtree = tk.ttk.Treeview(self, columns=("#0", "#1", "#2"), show="tree")
        self.sdcardtree.column("#0", width=100)
        self.sdcardtree.column("#1", width=100)
        self.ysb = ttk.Scrollbar(self, orient='vertical', command=self.sdcardtree.yview)
        self.xsb = ttk.Scrollbar(self, orient='horizontal', command=self.sdcardtree.xview)
        self.sdcardtree.configure(yscroll=self.ysb.set, xscroll=self.xsb.set)
        self.sdcardtree.grid(row=1,column=1)
        self.ysb.grid(row=1, column=2, sticky='ns')
        self.xsb.grid(row=2, column=1, sticky='ew')
        #self.sdcardtree.heading('#0', text=self.sdcardfolder.get(), anchor='w')

        #self.sdcardtree.pack()
        self.sdcardfolderEntry = tk.Entry(self)
        self.sdcardfolderEntry.grid(row=0,column=1)
        #self.sdcardfolderEntry.pack()
 
        # tell the entry widget to watch this variable
        self.sdcardfolderEntry["textvariable"] = self.sdcardfolder

        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.sdcardfolderEntry.bind('<Key-Return>',
                                    self.updateFolderTree)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.grid(row=2)

    def updateFolderTree(self, event):
        # Delete all old items
        self.sdcardtree.delete(*self.sdcardtree.get_children())

        # Go through all directories
        self.process_directory('', self.sdcardfolder.get())

        self.sdcardtree.tag_configure('wrongfolderorfile', background='orange')
        self.sdcardtree.tag_configure('wrongfileandfolder', background='red')
        self.sdcardtree.tag_configure('rightfolder', background='green')

    # Iterate recursively through all direcoties and update the treeview
    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = os.path.join(path, p)
            isdir = os.path.isdir(abspath)
            oid = self.sdcardtree.insert(parent, 'end', text=p, open=False)
            if re.match("^([0-9]{3})",path) is not None:
                self.sdcardtree.item(oid, tags=("rightfolder",))

            if isdir:
                self.process_directory(oid, abspath)
            elif os.path.isfile(abspath):
                if os.path.splitext(abspath)[1] == ".mp3":
                    print(abspath)
                    mp3file = eyed3.load(abspath)
                    print(mp3file.tag.title)
                    self.sdcardtree.item(oid,values = mp3file.tag.title)
                    if mp3file.tag.title is not None:
                        pass
                # Get the mp3-tag info

    def say_hi(self):
        print("hi there, everyone!")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
