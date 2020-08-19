import tkinter as tk
from tkinter import ttk


class BlobText(tk.Frame):

    def __init__(self, master, text, font=None, *args, **kwargs):
        kwargs['highlightbackground'] = 'black'
        kwargs['highlightcolor'] = 'black'
        kwargs['highlightthickness'] = 1

        super().__init__(master, *args, **kwargs)

        self._exists = True

        self._text = text
        self._label = tk.Label(self, text=self._text, font=font)

        def close_func():
            self.destroy()
            self._exists = False

        self._button = tk.Button(self, text='x', relief='flat', command=close_func, font=("Calibri", 12, "bold"))

        self._label.grid(column=0, row=0)
        self._button.grid(column=1, row=0)

class BlobTextDisplay(tk.Frame):

    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self._blobs = []

    def add_blob_text(self, text, *args, **kwargs):
        blob = BlobText(master=self, text=text, *args, **kwargs)
        blob.pack(side=tk.LEFT, padx=1)
        self._blobs.append(blob)

if __name__ == '__main__':
    root = tk.Tk()
    
    l = tk.Label(text='', width=20)
    l.grid(column=0, row=0)

    btd = BlobTextDisplay(root)
    btd.add_blob_text('hello', font=("Calibri", 16, "bold"))
    btd.add_blob_text('my', font=("Calibri", 16, "bold"))
    btd.add_blob_text('name', font=("Calibri", 16, "bold"))
    btd.add_blob_text('is', font=("Calibri", 16, "bold"))
    btd.add_blob_text('jeff', font=("Calibri", 16, "bold"))
    btd.grid(column=0, row=0)

    def func():
        for l in btd._blobs:
            if l._exists:
                print(l._text)

    btn = tk.Button(root, text='test', command=func)
    btn.grid(column=0, row=1)

    tk.mainloop()
