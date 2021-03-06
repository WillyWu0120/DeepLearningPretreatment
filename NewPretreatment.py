import cv2
import tkinter as tk
from tkinter import ttk, filedialog
from pathlib import Path
import os
import json
import numpy as np


SELECT_COLOR = '#00FF00'
ACTIVE_COLOR = '#FF0000'


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.result = []
        self.geometry('400x500')
        doneButton = tk.Button(self, text="Done", width=8,
                               command=self.done)
        doneButton.grid(column=0, row=0)
        selectButton = tk.Button(
            self, text="select", width=8, command=self.select)
        selectButton.grid(column=1, row=0)
        self.display = tk.StringVar(self, value="")
        label = tk.Label(self, textvariable=self.display)
        label.grid(column=0, row=1)
        self.load()

    def load(self):
        picName = filedialog.askopenfilename(
            parent=self,
            initialdir='./Pictures', title="select file",
            filetypes=(("all files", "*.*"),)).split('/')[-1]

        self.picName = picName
        src = cv2.imread('./Pictures/' + str(picName), cv2.IMREAD_COLOR)
        self.src = src
        nr, nc = src.shape[:2]
        self.image = cv2.resize(
            src, (int(nc*(700/nr)), 700), interpolation=cv2.INTER_AREA)
        self.dir = os.path.join('Labels', picName)
        self.path = os.path.join(self.dir, 'data.json')
        Path("./Labels/").mkdir(exist_ok=True)
        Path("./Labels/" + str(picName)).mkdir(exist_ok=True)
        if (os.path.isfile("./Labels/" + str(picName) + "/" + "data.json")):
            with open("./Labels/" + str(picName) + "/" + "data.json", 'r') as data:
                if os.stat("./Labels/" + str(picName) + "/" + "data.json").st_size > 0:
                    self.result = json.load(data)
        else:
            open("./Labels/" + str(picName) + "/" + "data.json", 'w+')

    def done(self):
        self.result.append({
            "id": len(self.result)+1,
            "pitch": 0,
            "duration": 0,
            "dots": 0,
            "accidental": 0
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
        nr, nc = self.src.shape[:2]
        note = self.src[int(bbox[1]*nr/700):int((bbox[1]+bbox[3])*nr/700),
                        int(bbox[0]*nr/700):int((bbox[0]+bbox[2])*nr/700)]
        note = cv2.cvtColor(note, cv2.COLOR_BGR2GRAY)
        noteR, noteC = note.shape[:2]
        if noteR > noteC*2:
            new_image_height = noteR
            new_image_width = noteR // 2
        else:
            new_image_height = noteC * 2
            new_image_width = noteC
        resultImg = np.full(
            (new_image_height, new_image_width), 255, dtype=np.uint8)
        y_center = (new_image_height - noteR) // 2
        x_center = (new_image_width - noteC) // 2
        resultImg[y_center:y_center+noteR, x_center:x_center+noteC] = note

        cv2.imwrite(
            f"./Labels/{self.picName}/{len(self.result)}.png", resultImg)


if __name__ == '__main__':
    app = App()
    app.mainloop()
