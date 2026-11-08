import tkinter as tk


def on_click():
    label.config(text="Hello, button clicked!")


root = tk.Tk()
root.title("Tkinter Hello - Lungten Choden (14)")
label = tk.Label(root, text="Hello")
label.pack(padx=20, pady=10)
tk.Button(root, text="Click me", command=on_click).pack(pady=10)
root.mainloop()