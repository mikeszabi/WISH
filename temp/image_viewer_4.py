# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:41:29 2017

@author: SzMike
"""

from tkinter import *
from tkinter.filedialog import askopenfilenames
from tkinter.messagebox import showerror
from PIL import Image, ImageTk


class MainWindow:
    def __init__(self, master):
        self.canvas = Canvas(master,bg="red", width=400, height=400)
        self.canvas.pack()
        #self.canvas.grid(row = 0, column = 0)

        self.button = Button(canvas, text="Browse", command=self.load_file, width=10)
        self.button.grid(row=1, column=0, sticky=W)

    def load_file(self):
        file_path_list = askopenfilenames(filetypes=(("JPEG", "*.jpg"),
                                           ("PNG", "*.png"),
                                           ("BMP", "*.bmp") ))
        for file_path in file_path_list:
            image = Image.open(file_path)
            image.show()



if __name__ == "__main__":
    root = Tk() 
    x = MainWindow(root)
    root.mainloop()
    