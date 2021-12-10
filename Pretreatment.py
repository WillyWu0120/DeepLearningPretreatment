import cv2
import tkinter as tk
from tkinter import ttk
from pathlib import Path
import os
from os import listdir
from os.path import isfile, join
import json
import numpy as np
picName = ""
result = []
def SelectFile():
    Path("./Pictures").mkdir(exist_ok=True)
    files = [f for f in listdir('./Pictures') if isfile(join('./Pictures', f))]
    
    def Confirm():
        global picName
        picName = fileLocation.get()
        app.destroy()
    app = tk.Tk() 
    app.geometry('142x70')
    labelTop = tk.Label(app,text = "Choose your Picture")
    labelTop.grid(column=0, row=0)
    
    fileLocation = tk.ttk.Combobox(app, values = files)
    fileLocation.grid(column=0, row=1)
    fileLocation.current(0)
    
    ConfirmButton = tk.Button(app, text="Done", width=8,
                                  command=Confirm)
    ConfirmButton.grid(column=0, row=2)
    
    app.mainloop()

def Gui():
    
    def Done():
        result.append({
            "id": len(result)+1,
            "pitch": pitch.get(),
            "duration": duration.get(),
            "dots": dots.get(),
            "accidental" : accidental.get()
        })
        app.destroy()
    
    app = tk.Tk() 
    app.geometry('250x500')
    pitch = tk.IntVar()
    noteList = ["Re", "Do", "Si", "La", "So", "Fa", "Mi", "Re", "Do", "Si", "La", "So", "Fa", "Mi", "Re", "Do", "Si", "La", "So"]
    for i in range(9, -10,-1):
        button = tk.ttk.Radiobutton(app, text=noteList[-(i-9)], variable=pitch, value=i)
        button.grid(column=0, row=-(i-9))
    
    durations = [4,2,1,0.5,0.25,0.125]
    duration = tk.IntVar()
    for i in durations:
        button = tk.ttk.Radiobutton(app, text=i, variable=duration, value=i)
        button.grid(column=1, row=durations.index(i))
        
    dots = tk.IntVar()
    for i in range(0,3):
        button = tk.ttk.Radiobutton(app, text=i, variable=dots, value=i)
        button.grid(column=2, row=i)
        
    accidental = tk.IntVar()
    accidental_labels = ['bb', 'b', '', '#', '##']
    for i in range(2,-3 ,-1):
        button = tk.ttk.Radiobutton(app, text=accidental_labels[i+2], variable=accidental, value=i)
        button.grid(column=3, row=-(i-2))
    
    doneButton = tk.Button(app, text="Done", width=8,
                              command=Done)
    doneButton.grid(column=0, row=19)
    
    app.mainloop()

def SaveNote(src, bbox):
    nr,nc = src.shape[:2]
    note = src[int(bbox[1]*nr/700):int((bbox[1]+bbox[3])*nr/700), int(bbox[0]*nr/700):int((bbox[0]+bbox[2])*nr/700)]
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
    
    cv2.imwrite("./Labels/"+str(picName)+"/"+str(len(result))+".png", resultImg)

if __name__ == '__main__' :
    SelectFile()
    src = cv2.imread("./Pictures/" + str(picName), cv2.IMREAD_COLOR)
    nr,nc = src.shape[:2]
    image = cv2.resize(src, (int(nc*(700/nr)), 700), interpolation=cv2.INTER_AREA)
    Path("./Labels/").mkdir(exist_ok=True)
    Path("./Labels/"+ str(picName)).mkdir(exist_ok=True)
    if (os.path.isfile("./Labels/" + str(picName) + "/" + "data.json")):
        with open("./Labels/" + str(picName) + "/" + "data.json", 'r') as data:
            if os.stat("./Labels/" + str(picName) + "/" + "data.json").st_size > 0:
                result = json.load(data)        
    else:
        open("./Labels/" + str(picName) + "/" + "data.json", 'w+')
    
    while True:
        bbox = cv2.selectROI(image, False)
        print(cv2.getWindowProperty('just_a_window', cv2.WND_PROP_VISIBLE))
    
        Gui()
        SaveNote(src,bbox)
        with open("./Labels/" + str(picName) + "/" + "data.json", 'w') as outfile:
            json.dump(result, outfile)
        
        k = cv2.waitKey(0) & 0xff
        
        if k == ord('q') : 
            break
    
    cv2.destroyAllWindows()