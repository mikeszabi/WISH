# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 17:10:42 2017

@author: SzMike
"""
import os
import tkinter
from PIL import Image, ImageTk

class MainWindow:
    def __init__(self, master):
        canvas = tkinter.Canvas(master)
        canvas.pack()
        self.pimage = Image.open(filename)
        self.cimage = tkinter.PhotoImage(self.pimage)
        self.image = canvas.create_image(0,0,image=self.cimage)

path1 = r'd:\DATA\PRAKTIKER\TestImages\Csavar_zar_vasalat'
dirlist = os.listdir(path1)

filename = os.path.join(path1,dirlist[0])
root = tkinter.Tk()
x = MainWindow(root)
root.mainloop()

import tkinter

class Test:
    def __init__(self, master):
        canvas = tkinter.Canvas(master)
        canvas.grid(row = 0, column = 0)
        path1 = r'd:\DATA\PRAKTIKER\TestImages\Csavar_zar_vasalat'
        filename = os.path.join(path1,dirlist[0])
        self.photo = tkinter.PhotoImage(file = filename)
        tkinter.label.image = self.photo
        tkinter.label.grid(row = 3, column = 1, padx = 5, pady = 5)

root = tkinter.Tk()
test = Test(root)
root.mainloop()



root = tkinter.Tk()

path1 = r'd:\DATA\PRAKTIKER\TestImages\Csavar_zar_vasalat'
dirlist = os.listdir(path1)

filename = os.path.join(path1,dirlist[0])
photo = Image.open(filename)
label = tkinter.Label(image = filename)
label.image = photo # keep a reference!
label.grid(row = 3, column = 1, padx = 5, pady = 5)

root.mainloop()