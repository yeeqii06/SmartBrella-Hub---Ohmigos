import tkinter as tk
from tkinter import messagebox
import time
from PIL import Image, ImageTk
import requests #use for download with link
from io import BytesIO
import os
y=90
x=90

def greet():
    response = messagebox.askyesno("Greet", "Fun?")
    if response:
        messagebox.showinfo("Bye", "Gudluck")
    else:
        messagebox.showinfo("Bye", "Fk u!")
        response = messagebox.askokcancel("Warning", "The system will shutdown in 5 seconds.\nDo you want to cancel?")
        if not response:  # User clicked Cancel = False → shutdown
            os.system("shutdown /s /t 10")
        else:
            messagebox.showinfo("Cancelled", "Shutdown cancelled.")

    window3.destroy()

def changepos(a):
    global x,y
    x+=13
    y+=13
    a.geometry(f"400x200+{x}+{y}")

def toplevel():
    popout=tk.Toplevel(window3)
    popout.title("Gudbye")
    label = tk.Label(popout, text="nub!", font=("Helvetica", 20))
    label.pack()
    changepos(window3)
    popout.after(100, toplevel)

def presspop2():
    global window3
    window3 = tk.Tk()
    window3.title("Again?")
    label = tk.Label(window3, text="sayonara nigge!", font=("Helvetica", 20))
    label.pack()
    tk.Button(window3, text="Exit", command=greet).pack()
    window3.geometry("400x200+900+600")
    toplevel()

# main window
def presspop():
    window2 = tk.Tk()
    window2.title("SHaBi")
    window2.geometry("400x200+900+200")     #let window move
    addbutton(window2,"Stupidasnigger!",presspop2)

# add button
def addbutton(window,text,command):
    button = tk.Button(
                            window,
                            text=text,
                            activebackground="black",
                            activeforeground="white",
                            fg="purple",
                            bg="green",
                            command=command,
                            height=4,
                            width=50,
                            font=('Helvetica bold', 10)
                    )
    button.pack(side="bottom")
    
window = tk.Tk()
window.title("My First GUI")
addbutton(window,"Press to see more!",presspop)
max_width, max_height = 400, 300 
url="https://jpicpedia.com/wp-content/uploads/2024/06/img_0480-1.jpg"
#photo
# Download the image
response = requests.get(url)
img_data = response.content

# Open with PIL
img = Image.open(BytesIO(img_data))
photo = ImageTk.PhotoImage(img)

label = tk.Label(window, image=photo)
label.pack()

def say_hello():
    print("Hello!")

# def keepopen():
#     while True:
#         # time.sleep(2)
#         presspop2


window.mainloop()
