import cv2
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import os
from os import listdir
from os.path import isfile, join
import json
import numpy as np

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.result = []
        self.geometry('250x500')
        self.pitch = tk.IntVar()
        noteList = ["Re", "Do", "Si", "La", "So", "Fa", "Mi", "Re", "Do", "Si", "La", "So", "Fa", "Mi", "Re", "Do", "Si", "La", "So"]
        for i in range(9, -10,-1):
            button = tk.ttk.Radiobutton(self, text=noteList[-(i-9)], variable=self.pitch, value=i)
            button.grid(column=0, row=-(i-9))
        
        durations = [4,2,1,0.5,0.25,0.125]
        self.duration = tk.IntVar()
        for i in durations:
            button = tk.ttk.Radiobutton(self, text=i, variable=self.duration, value=i)
            button.grid(column=1, row=durations.index(i))
            
        self.dots = tk.IntVar()
        for i in range(0,3):
            button = tk.ttk.Radiobutton(self, text=i, variable=self.dots, value=i)
            button.grid(column=2, row=i)
            
        self.accidental = tk.IntVar()
        accidental_labels = ['bb', 'b', '', '#', '##']
        for i in range(2,-3 ,-1):
            button = tk.ttk.Radiobutton(self, text=accidental_labels[i+2], variable=self.accidental, value=i)
            button.grid(column=3, row=-(i-2))
        
        doneButton = tk.Button(self, text="Done", width=8,
                                command=self.done)
        doneButton.grid(column=0, row=19)
        selectButton = tk.Button(self, text="select", width=8, command=self.select)
        selectButton.grid(column=1, row=19)
        self.display = tk.StringVar(self, value="")
        label = tk.Label(self, textvariable=self.display)
        label.grid(column=0, row=20)
        self.load()
    
    def load(self):
        picName = filedialog.askopenfilename(
            parent=self,
            initialdir='./Pictures', title="select file", 
            filetypes = (("png files","*.png"),("all files","*.*"))).split('/')[-1]

        self.picName = picName
        src = cv2.imread('./Pictures/' + str(picName), cv2.IMREAD_COLOR)
        self.src = src
        nr,nc = src.shape[:2]
        self.image = cv2.resize(src, (int(nc*(700/nr)), 700), interpolation=cv2.INTER_AREA)
        self.dir = os.path.join('Labels', picName)
        self.path = os.path.join(self.dir, 'data.json')
        Path("./Labels/").mkdir(exist_ok=True)
        Path("./Labels/"+ str(picName)).mkdir(exist_ok=True)
        if (os.path.isfile("./Labels/" + str(picName) + "/" + "data.json")):
            with open("./Labels/" + str(picName) + "/" + "data.json", 'r') as data:
                if os.stat("./Labels/" + str(picName) + "/" + "data.json").st_size > 0:
                    self.result = json.load(data)        
        else:
            open("./Labels/" + str(picName) + "/" + "data.json", 'w+')
    

    def done(self):
        self.result.append({
            "id": len(self.result)+1,
            "pitch": self.pitch.get(),
            "duration": self.duration.get(),
            "dots": self.dots.get(),
            "accidental" : self.accidental.get()
        })
        self.save_note()
        with open(self.path, 'w') as outfile:
            json.dump(self.result, outfile)
        self.display.set('saved')

    def select(self):        
        self.bbox = cv2.selectROI(self.image, False)
        self.display.set('selected')

    def save_note(self):
        bbox = self.bbox
        nr,nc = self.src.shape[:2]
        note = self.src[int(bbox[1]*nr/700):int((bbox[1]+bbox[3])*nr/700), int(bbox[0]*nr/700):int((bbox[0]+bbox[2])*nr/700)]
        note = cv2.cvtColor(note, cv2.COLOR_BGR2GRAY)
        noteR,noteC = note.shape[:2]
        if noteR > noteC*2 :
            new_image_height = noteR
            new_image_width = noteR // 2
        else :
            new_image_height = noteC * 2
            new_image_width = noteC
        resultImg = np.full((new_image_height,new_image_width), 255, dtype=np.uint8)
        y_center = (new_image_height - noteR) // 2
        x_center = (new_image_width - noteC) // 2
        resultImg[y_center:y_center+noteR, x_center:x_center+noteC] = note
        
        cv2.imwrite(f"./Labels/{self.picName}/{len(self.result)}.png", resultImg)

if __name__ == '__main__' :
    app = App()
    app.mainloop()
 