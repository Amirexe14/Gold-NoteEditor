import tkinter as tk
import tkinter.font as tf
from PIL import ImageTk, Image
import pickle
from tkinter import messagebox
import socket
import easygui as gui
import sys

app = tk.Tk()
app.geometry("1100x700")
app.config(bg="#1e1e1e")
app.title("GOLD - Notes app editor")
app.resizable(False, False)
#app.iconbitmap("./img/Booster_Gold.ico")

#Fonts
WriteFont = tf.Font(family="Arial", size=12, weight="bold")
IDFont = tf.Font(family="Arial", size=24, weight="bold")
BtnFont = tf.Font(family="Arial", size=14, weight="bold")

#Globalized variables:
CurrentWindow = None

connection = gui.enterbox("Enter the IP and PORT of the server, e.g:\n192.168.38.123:4455", "CONNECTION WINDOW")
ServerIP, ServerPort = connection.split(":")
ServerPort = int(ServerPort)

#Colorization:
BGcolor = "#1e1e1e"
DarkBGcolor = "#151515"

# DUNCTIONS:
def SaveFile():
    if CurrentWindow != None:
        try:
            with(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as client:
                client.connect((ServerIP, ServerPort))
                SendContent = f"[SAVE]{CurrentWindow}[FILECONTENTS;]{prompt.get('1.0', '10000000000000.0')}"
                client.send(SendContent.encode())
                client.close()
        except Exception as e:
            print(f"Connection Terminated: {e}")
        

def LoadFile(filename):
    global CurrentWindow
    try:
        CurrentWindow = filename
        FileIDLabel.config(text=filename)

        with(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as client:
            client.connect((ServerIP, ServerPort))
            SendReq = f"[LOAD]{CurrentWindow}"
            client.send(SendReq.encode()) #Sends load req for windowname

            prompt.delete('1.0', '10000000000000.0') #Reset board
            ServerContent = client.recv(1024).decode() #Gets content as requested
            prompt.insert('1.0', ServerContent) #Writes content
            client.close()

    except Exception as e:
        print(f"Connection Terminated: {e}")


def ReloadWindow():
    for bridget in app.winfo_children():
        bridget.destroy()

    BuildAPP()

def CreateFile():
    try:
        newfilename = gui.enterbox("Enter name of new Document: ", "Create a new Document")

        with(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as client:
            client.connect((ServerIP, ServerPort))
            
            if newfilename != None:
                ServerCreateReq = f"[CREATE]{newfilename}"
                client.send(ServerCreateReq.encode())

                messagebox.showinfo(f"Create a new Document?", f'The new Document "{newfilename}" has been created, reloading the app to update it.')
                client.close()
                ReloadWindow()

            else:
                messagebox.showinfo(f"Create a new Document?", 'Your action has been canceled.')

    except Exception as e:
        print(f"Connection Terminated: {e}")
    

def DeleteFile():
    if CurrentWindow != None:

        deleteChoice = messagebox.askyesno("Delete a Document?", f"Are you sure you want to delete {CurrentWindow}?")

        if deleteChoice == True:
            try:
                with(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as client:
                    client.connect((ServerIP, ServerPort))
                    deletereq = f"[DEL]{CurrentWindow}"
                    client.send(deletereq.encode())
                    messagebox.showinfo(f"Delete a Document?", f'The Document "{CurrentWindow}" has been Deleted, reloading the app to update it.')
                
                    print(f"removed {CurrentWindow}")
                    client.close()
                ReloadWindow()

            except Exception as e:
                print(f"Connection Terminated: {e}")
        
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

    #Try getting notes from the server :D
    try:
        with(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as client:
            client.connect((ServerIP, ServerPort))
            client.send(b"[RECV]")
            data = client.recv(1024)
            files = pickle.loads(data)
            client.close()

        for i, file in enumerate(files):
            tk.Button(app, text=file,
                    bg=BGcolor, fg="White", bd=0, activebackground="Orange",
                    font=BtnFont,
                    
                    command=lambda filename=file: LoadFile(filename)).place(x=25, y=70*(i+1))

    except Exception as e:
        print("Issue with getting files")
        print(f"Issue: {e}")

        #ReloadWindow()

    prompt = tk.Text(app, height=30, width=90, bg=BGcolor, fg="White", insertbackground="white", bd=0)
    prompt.config(font=WriteFont)
    prompt.place(y=80, x=230)

BuildAPP()
app.mainloop()