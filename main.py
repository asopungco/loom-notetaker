import kivy
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.widget import Widget 

# from tkinter import *
from tkinter import Tk
from tkinter import filedialog
from tkinter import messagebox
import os

import shutil

# current: variable storing currently opened file path, to be accessed across functions
global current
current = False

class FileChoose(Popup):
    load = ObjectProperty()


class MyGridLayout(Widget):
    file_path = StringProperty("No file chosen")
    text_input = ObjectProperty()
    popup = ObjectProperty()


    def load(self, path, filename):
        with open(os.path.join(path, filename[0])) as stream:
            self.ids.text_input.text = stream.read()
        self.popup.dismiss()
    

    def open(self):
        Tk().withdraw()
        path = filedialog.askopenfilename()
        self.file_path = path
        if path:
            global current
            current = path
            self.ids.file_open.text = "Editing: " + path #shows what file is currently open
            file = open(path, 'r')
            contents = file.read()
            file.close()
            self.ids.text_input.text = contents

    def delete(self):
        Tk().withdraw()
        self.ids.text_input.text = ""

        global current
        if os.path.isfile(current):
            os.remove(current)
            messagebox.showinfo("Delete", "File successfully deleted.")
            self.ids.file_open.text = "No Open File" 

    def saveAs(self):
        Tk().withdraw() # hide tkinter window
        path = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
        if path:
            file = open(path, 'w')
            file.write(self.ids.text_input.text)
            global current
            current = path
            self.ids.file_open.text = "Editing: " + path
            messagebox.showinfo("Save As", "File successfully saved.")

        global current
        current = path


    def new(self):
        # first clear contents
        self.ids.text_input.text = ""

        # reset current to FALSE so that save will trigger as saveA
        #current = False

        # functionally the same as saveAs
        self.saveAs()

        self.ids.file_open.text = "Editing: " + current #shows what file is currently open

    def save(self):
        # checks whether a previously saved file is currently open
        global current
        if current:
            file = open(current, 'w')
            file.write(self.ids.text_input.text)
            file.close()
            messagebox.showinfo("Save", "File successfully saved.")
        else:
            self.saveAs()
    
    def moveFile(self):
        Tk().withdraw()
        global current
        if current:
            moveHere = filedialog.askdirectory()
            shutil.move(current, moveHere)
            current = False
            self.ids.file_open.text = "No Open File"
            self.ids.text_input.text = ""
            messagebox.showinfo("Move", "File successfully moved.")
        else:
            messagebox.showinfo("Move", "Please open a file and try again.")

    def moveFile(self):
        Tk().withdraw()
        global current
        if current:
            moveHere = filedialog.askdirectory()
            shutil.move(current, moveHere)
            current = False
            self.ids.file_open.text = "No Open File"
            self.ids.text_input.text = ""
            messagebox.showinfo("Move", "File successfully moved.")
        else:
            messagebox.showinfo("Move", "Please open a file and try again.")
    # terminal interface to manually select what error to trigger
    def error_trigger(self):
        
        errors = ["Read-only Error"]
        print("Please select what error you wish to trigger:")

        for i in range(len(errors)):
            print('\t{0} {1}\n'.format(str(i), errors[i]))

        whichError = int(input("Enter the index of the error: "))
        
        if whichError in range(len(errors)):
            print("You selected {0}.\n".format(errors[whichError]))
        


class MyApp(App):

    def build(self):
        return MyGridLayout()

if __name__ == "__main__":
    MyApp().run()
