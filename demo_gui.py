# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 21:31:04 2017

@author: SzMike
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename
import os
from PIL import Image, ImageTk


class ImageViewer(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, background="green")

        # for now, don't use images. This, so that we can get
        # the basic structure working
        #self.im = None

#        self.query_img=None  
#        self.query_panel = tk.Label(self, image = self.img)
#        self.query_panel.grid(row=0,column=0)

        # these three widgets make up our main layout
        #label = tk.Label(self, image=self.tkim, text="label")
        #e1 = Enhance1(self, None)

        browse_button = tk.Button(self, text="Browse", command=self.load_file, width=10)
        browse_button.grid(row=0, column=0, sticky=tk.W)
        find_button = tk.Button(self, text="Find Similar", command=self.find_similar, width=10)
        find_button.grid(row=0, column=1, sticky=tk.W)
       
        #e1.grid(row=3,column=1)
        
    def load_file(self):
        query_path = askopenfilename(filetypes=(("JPEG", "*.jpg"),
                                           ("PNG", "*.png"),
                                           ("BMP", "*.bmp") ))
        self.query_im=Image.open(query_path)
        self.query_im.thumbnail((300,300))
        self.query_img = ImageTk.PhotoImage(self.query_im)
        self.query_panel = tk.Label(self, image = self.query_img)
        self.query_panel.grid(row=1,column=0)
        
    def find_similar(self):
      
        self.sim_img = ImageTk.PhotoImage(self.query_im)
        self.sim_panel = tk.Label(self, image = self.sim_img)
        self.sim_panel.grid(row=1,column=1)

class Enhance1(tk.Label):
    def __init__(self, master, image):
        # we will be operating on this image, so save a 
        # reference to it
        self.image = image

        # width, height, and color are only temporary, they
        # make it easy to see the frames before they have
        # any content
        tk.Frame.__init__(self, master, background="blue", width=300, height=300)

if __name__ == "__main__":
    root = tk.Tk()
    ImageViewer(root).pack(fill="both", expand=True)
    root.mainloop()