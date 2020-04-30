import os
import tkinter as tk
from tkinter import ttk
import pathlib
import eyed3
import re
from PIL import ImageTk, Image
import io

def listOfmp3s(folder: pathlib.Path):
    return list(pathlib.Path(folder).glob("*\\*.mp3"))


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.geometry("1280x800")
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=9)  # columns will split space

        self.create_widgets()

    def create_widgets(self):
        # configure internal left Frame
        self.left_frame = tk.Frame(self, borderwidth=2, relief=tk.SUNKEN)
        self.left_frame.grid_rowconfigure(0, weight=1)  # rows will split space
        self.left_frame.grid_rowconfigure(1, weight=1)  # rows will split space
        self.left_frame.grid_columnconfigure(0, weight=1)
        self.left_frame.grid(column=0, row=0, sticky='nsew')

        # configure internal right Frame
        self.right_frame = tk.Frame(self, borderwidth=2, relief=tk.SUNKEN)
        self.right_frame.grid_rowconfigure(
            0, weight=1)  # rows will split space
        self.right_frame.grid_rowconfigure(
            1, weight=8)  # rows will split space
        self.right_frame.grid_rowconfigure(
            2, weight=1)  # rows will split space
        self.right_frame.grid_columnconfigure(0, weight=99)
        self.right_frame.grid_columnconfigure(1, weight=1)
        self.right_frame.grid(column=1, row=0, sticky='nsew')

        self.hi_there = tk.Button(self.left_frame)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.updateFolderTree
        self.hi_there.grid(row=0)

        # here is the application variable
        self.sdcardfolder = tk.StringVar()
        # set it to some value
        self.sdcardfolder.set("C:\\Users\\Joe\\Music")

        self.sdcardtree = tk.ttk.Treeview(self.right_frame,columns=("#0", "#1", "#2"), show="tree")
        self.sdcardtree.column("#0", width=100)
        self.sdcardtree.column("#1", width=100)
        self.sdcardtree.bind("<Button-3>",self.OnRightMouseClick)
        self.ysb = ttk.Scrollbar(
            self.right_frame, orient='vertical', command=self.sdcardtree.yview)
        self.xsb = ttk.Scrollbar(
            self.right_frame, orient='horizontal', command=self.sdcardtree.xview)
        self.sdcardtree.configure(yscroll=self.ysb.set, xscroll=self.xsb.set)
        self.sdcardtree.grid(row=1, column=0, sticky='nsew')
        self.style = ttk.Style()
        self.style.configure("Treeview", rowheight=40)
        self.ysb.grid(row=1, column=1, sticky='nsw')
        self.xsb.grid(row=2, column=0, sticky='new')
        #self.sdcardtree.heading('#0', text=self.sdcardfolder.get(), anchor='w')


        self.popup_menu = tk.Menu(self, tearoff=0)

        #self.sdcardtree.pack()
        self.sdcardfolderEntry = tk.Entry(self.right_frame)
        self.sdcardfolderEntry.grid(row=0,column=0)
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

    # Rename the selected file from the popup menu to fit in to the scheme
    def renameFile(self):
        print("Renaming ", self.sdcardtree.item(self.curesel, "text"), " to scheme")
        tags = self.sdcardtree.item(self.curesel, "values")
        if os.path.isfile(tags[2]) and os.path.splitext(tags[2])[1] == ".mp3":
            mp3folder = pathlib.Path(tags[2]).parent
            listOfMp3s = list(mp3folder.glob("[0-9]{3}.mp3"))
            if len(listOfMp3s) < 1:
                os.rename(tags[2], os.path.join(mp3folder, "000.mp3"))
                self.updateFolderTree(None)
                return
            else:
                results = list(map(int, listOfMp3s))
                results = max(results)
                os.rename(tags[2], os.path.join(mp3folder, "{:03d}.mp3".format(results)))
                self.updateFolderTree(None)
        else: print("User tried to rename a none-mp3")


    def renameFolder2Scheme(self):
        print("Renaming ", self.sdcardtree.item(
            self.curesel, "text"), " to scheme")
        tags = self.sdcardtree.item(self.curesel, "values")
        if os.path.isdir(tags[2]):
            parentDir = pathlib.Path(tags[2]).parent
            listOfFolders = [f.path for f in os.scandir(parentDir) if f.is_dir()]
            if len(listOfFolders) < 1:
                os.rename(tags[2], os.path.join(parentDir, "00"))
                self.updateFolderTree(None)
                return
            else:
                results = list(map(int, listOfFolders))
                results = max(results)
                os.rename(tags[2], os.path.join(
                    parentDir, "{:02d}.mp3".format(results)))
                self.updateFolderTree(None)

    def renameFolder2Mp3(self):
        tags = self.sdcardtree.item(self.curesel, "values")

    def renameFolder2Advert(self):
        pass

    def debugPrint(self):
        print("Test")

    def OnRightMouseClick(self, event):
        self.curesel = self.sdcardtree.identify('item', event.x, event.y)
        print("You clicked on", self.sdcardtree.item(self.curesel, "text"))
        if "error" not in self.sdcardtree.item(self.curesel, 'tags'):
            print("There is no renaming to be done here")
        tags = self.sdcardtree.item(self.curesel, "values")
        if os.path.isfile(tags[2]) and os.path.splitext(tags[2])[1] == ".mp3":
            try:
                
                self.popup_menu.add_command(label="Rename MP3 to scheme",
                                command=self.renameFile)
                self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
                print("User clicked on something")
            finally:
                self.popup_menu.grab_release()
                self.popup_menu.delete("Rename MP3 to scheme")
        elif os.path.isdir(tags[2]):
            
            try:
                self.popup_menu.add_command(label = "Folder to scheme",
                                            command=print("Option A"))
                self.popup_menu.add_command(label = "B",
                                            command=print("Option B"))
                self.popup_menu.add_command(label = "C",
                                            command=print("Option C"))
                self.popup_menu.tk_popup(
                                event.x_root, event.y_root, 0)
                print("User clicked on something")
            finally:
                self.popup_menu.grab_release()
                self.popup_menu.delete("Folder to scheme")
                self.popup_menu.delete("B")
                self.popup_menu.delete("C")

    def updateFolderTree(self, event):
        # Delete all old items
        self.sdcardtree.delete(*self.sdcardtree.get_children())

        # Go through all directories
        self.process_directory('', pathlib.Path(self.sdcardfolder.get()))

        self.sdcardtree.tag_configure('error', background='red')
        self.sdcardtree.tag_configure('ok', background='green')

    # Iterate recursively through all direcoties and update the treeview
    def process_directory(self, parent, path):
        for p in os.listdir(path):
            abspath = pathlib.Path(path).resolve().joinpath(p)
            print("Checking ",abspath)
            isdir = os.path.isdir(abspath)
            oid = self.sdcardtree.insert(parent, 'end', text=p, open=False)

            # Check if it matches the general naming scheme and flag it okay
            if (re.match("^([0-9]{3})",p) is not None) or (p == "advert") or (p == "mp3"):
                #print(path)
                self.sdcardtree.item(oid, values = ("","",abspath), tags=("ok",))
            else: 
                self.sdcardtree.item(oid, values=("", "", abspath),tags=("error",))
            # Call recursive if it's a dir
            if isdir:
                self.process_directory(oid, abspath)
                continue
            
            # Seems to be a file
            if os.path.isfile(abspath):
                # But is it an mp3?
                if os.path.splitext(abspath)[1] == ".mp3":
                    #print(abspath)
                    mp3file = eyed3.load(abspath)

                    if mp3file is None or mp3file.tag is None:
                        print("The file is not a real mp3-File. Please check content")
                        return
                    #print(mp3file.tag.title)
                    try:
                        self.sdcardtree.item(oid,
                        values = (mp3file.tag.title,mp3file.tag.album,abspath))
                    except: 
                        pass

                    if mp3file.tag.images is not None and len(mp3file.tag.images) > 0:
                        self.image = Image.open(io.BytesIO(mp3file.tag.images[0].image_data))
                        self.image = ImageTk.PhotoImage(
                            self.image.resize((40, 40)))
                        self.sdcardtree.item(oid
                                             , image=self.image)
                        pass
                # Get the mp3-tag info

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
