import tkinter as tk

window = tk.Tk()
window.title('test app')
window.geometry('400x400')

lbl = tk.Label(window, text='Hello')
lbl.grid(column=0, row=0)


btn = tk.Button(window, text="Click Me")
btn.grid(column=1, row=0)

window.mainloop()