import tkinter as tk

root = tk.Tk()
root.geometry("500x400")

fonts = [
    ("Helvetica", 18, "bold"),
    ("Arial Black", 20, "bold"),
    ("Comic Sans MS", 16, "italic"),
    ("Courier New", 14, "bold"),
    ("Times New Roman", 18, "italic"),
    ("Verdana", 14, "bold"),
    ("Impact", 22),
    ("Georgia", 16, "italic"),
    ("Garamond", 15),
    ("Caviar Dreams", 16),
    
]

colors = ["darkblue", "green", "purple", "red", "black"]


print(root.cget("bg"))  # prints the default background color


for i, f in enumerate(fonts):
    tk.Label(root, text=f"Sample Text - {f[0]}", font=f, fg=colors[i % len(colors)]).pack(pady=3)

root.mainloop()
