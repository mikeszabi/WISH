# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 15:34:55 2017

@author: SzMike
"""

from tkinter import *
import tkinter.messagebox
from PIL import ImageTk, Image
import glob

global all_images
all_images = []

def photo_browse ():

    def add_photo (screen, column_num):

        if not "pic" in globals ():
            tkMessageBox.showerror ("Error!", "No picture selected!")
            screen.lift ()
        else:
            screen.image = pic
            can = Label(screen, image = pic)
            can.grid(row = 0, column = column_num)
            Label(screen, text = chosen_photo).grid (row = 1, column = column_num)

    def selection_listbox (evt):    
        global chosen_photo
        chosen_photo = str (photo_listbox.get (photo_listbox.curselection ()))
        print(chosen_photo)
        global pict
        pict = Image.open (chosen_photo)
        global pic
        pic = ImageTk.PhotoImage (pict)

        # adding all the images to a list has worked for me in the past
        global all_images
        all_images = all_images + [chosen_photo, pic, pict]


    photo_browse_screen = Toplevel()
    photo_browse_screen.title ("Photo browse")
    photo_browse_screen.geometry ("1000x600")
    photo_browse_screen.resizable (0, 0)
    photo_listbox = Listbox(photo_browse_screen, width = 50, height = 35)
    photo_listbox.grid (columnspan = 3)
    photo_listbox.bind ('<<ListboxSelect>>', selection_listbox)
    name_list = glob.glob (r'C:\Users\SzMike\OneDrive\WISH\TestImages\Csavar_zar_vasalat\*.jpg')
    #name_list.sort ()
    n = 1
    m = 0
    for i in name_list:
        photo_listbox.insert (n, name_list [m])
        n += 1
        m += 1
    Button(photo_browse_screen, text = "PIC 1", command = lambda: add_photo (photo_browse_screen, 4)).grid (row = 1, column = 0)
    Button(photo_browse_screen, text = "PIC 2", command = lambda: add_photo (photo_browse_screen, 5)).grid (row = 1, column = 1)
    Button(photo_browse_screen, text = "EXIT", command = photo_browse_screen.destroy).grid (row = 1, column = 2)
    can_pic_1 = Label (photo_browse_screen, text = "Pic 1", font= "-weight bold")
    can_pic_1.grid (row = 0, column = 4, padx = (200, 100), sticky = N)
    can_pic_2 = Label (photo_browse_screen, text = "Pic 2", font= "-weight bold")
    can_pic_2.grid (row = 0, column = 5, padx = (100, 150), sticky = N)

root = Tk()
root.title("Main menu")
root.geometry("1000x600")
root.resizable(0, 0)
main_menu = Menu(root)

photos_menu = Menu(main_menu, tearoff = 0)

main_menu.add_cascade (label = "Photos", menu = photos_menu)
photos_menu.add_command (label = "Browse photos", command = photo_browse)

root.config (menu = main_menu)

root.mainloop ()