import os
import pickle

import tkinter as tk
from tkinter import messagebox
import face_recognition


def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
                        window,
                        text=text,
                        activebackground="black",
                        activeforeground="white",
                        fg=fg,
                        bg=color,
                        command=command,
                        height=2,
                        width=20,
                        font=('Times New Roman', 22),
                        relief="groove",
                    )

    return button


def get_img_label(window):
    label = tk.Label(window, bg="white")
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 15), justify="left")
    return label

def get_text_labelstylish(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("Georgia", 22), justify="left")
    return label

def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=1,
                       width=15, font=("Arial", 32))
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)


def recognize(img, db_path):
    # it is assumed there will be at most 1 match in the db

    embeddings_unknown = face_recognition.face_encodings(img)
    if len(embeddings_unknown) == 0:
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        file = open(path_, 'rb')
        data = pickle.load(file)
        embedding=data["embedding"]
        match = face_recognition.compare_faces([embedding], embeddings_unknown)[0]
        j += 1

    if match:
        return data["info"][0]
    else:
        return 'unknown_person'

