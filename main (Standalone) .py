import tkinter as tk
import tkinter.font as tf
from PIL import ImageTk, Image
import os
from tkinter import messagebox
import subprocess
import easygui as gui

app = tk.Tk()
app.geometry("1100x700")
app.config(bg="#1e1e1e")
app.title("GOLD - Notes app editor")
app.resizable(False, False)
app.iconbitmap("./img/Booster_Gold.ico")

#Fonts
WriteFont = tf.Font(family="Arial", size=12, weight="bold")
IDFont = tf.Font(family="Arial", size=24, weight="bold")
BtnFont = tf.Font(family="Arial", size=14, weight="bold")

#Globalized variables:
CurrentWindow = None
SetDirectory = "./Docs/"

#Colorization:
BGcolor = "#1e1e1e"
DarkBGcolor = "#151515"


# DUNCTIONS:
def SaveFile():
    if CurrentWindow != None:
        with open(f"{SetDirectory}{CurrentWindow}", 'w') as file:
            #print(f"Saved contents of Doc{CurrentWindowIndex}")
            file.write(prompt.get('1.0', '10000000000000.0')) #start to finish
            file.close()

def LoadFile(filename):
    global CurrentWindow
    with open(f"{SetDirectory}{filename}", 'r') as file:
        prompt.delete('1.0', '10000000000000.0') #delete everything
        #print(f"inserting contents of Doc{i}")
        prompt.insert('1.0', file.read())
        file.close()
    CurrentWindow = filename

    FileIDLabel.config(text=filename)

def ReloadWindow():
    for bridget in app.winfo_children():
        bridget.destroy()

    BuildAPP()

def CreateFile():
    global NewDocIndex
    NewDocIndex = 1
    for index in os.listdir(SetDirectory):
        NewDocIndex += 1

    newfilename = gui.enterbox("Enter name of new Document: ", "Create a new Document", f"Doc{NewDocIndex}")

    if newfilename != None:
        with open(f"{SetDirectory}{newfilename}", 'w') as file:
            file.close()
        messagebox.showinfo(f"Create a new Document?", f'The new Document "{newfilename}" has been created, reloading the app to update it.')
    else:
        messagebox.showinfo(f"Create a new Document?", 'Your action has been canceled.')
    
    ReloadWindow()

def DeleteFile():
    if CurrentWindow != None:

        deleteChoice = messagebox.askyesno("Delete a Document?", f"Are you sure you want to delete {CurrentWindow}?")

        if deleteChoice == True:
            messagebox.showinfo(f"Delete a Document?", f'The Document "{CurrentWindow}" has been Deleted, reloading the app to update it.')
            os.remove(f"{SetDirectory}{CurrentWindow}")
            print(f"removed {CurrentWindow}")
            ReloadWindow()
        
        else:
            messagebox.showinfo(f"Delete a Document?", 'Your action has been canceled.')


def BuildAPP():
    global FileIDLabel, prompt

    #Static settings for design purposes:
    FileIDLabel = tk.Label(app, text=f"", font=IDFont, fg="White", bg=BGcolor)
    FileIDLabel.place(x=230, y=15)


    L_Wall = tk.Label(app, width=28, height=1000, fg=DarkBGcolor, bg=DarkBGcolor)
    L_Wall.place(x=0)

    #Buttons and interactives:
    SaveBtn = tk.Button(app, text="💾", font=IDFont, fg="White", bg=BGcolor, highlightthickness=0, bd=0, activebackground=BGcolor)
    SaveBtn.config(command=SaveFile)
    SaveBtn.place(x=950, y=5)

    RemoveBtn = tk.Button(app, text="x", font=IDFont,fg="White", bg=DarkBGcolor, highlightthickness=0, bd=0, activebackground="Red")
    RemoveBtn.config(command=DeleteFile)
    RemoveBtn.place(x=140, y=5)

    CreateBtn = tk.Button(app, text="+", font=IDFont,fg="White", bg=DarkBGcolor, highlightthickness=0, bd=0, activebackground="Green")
    CreateBtn.config(command=CreateFile)
    CreateBtn.place(x=15, y=5)
    #Buttons and interactivse

    #Existing notes turned into buttons you can access
    for i, file in enumerate(os.listdir(SetDirectory)):
        #print(file)
        tk.Button(app, text=file, #uesd to be text=f"Document {i}"
                bg=BGcolor, fg="White", bd=0, activebackground="Orange", font=BtnFont,
                
                command=lambda filename=file: LoadFile(filename)).place(x=25, y=70*(i+1))

    prompt = tk.Text(app, height=30, width=90, bg=BGcolor, fg="White", insertbackground="white", bd=0)
    prompt.config(font=WriteFont)
    prompt.place(y=80, x=230)

BuildAPP()
app.mainloop()