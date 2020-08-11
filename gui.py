import tkinter as tk
from tkinter import messagebox

class Window:

    def __init__(self, io_handler, debug):

        self._io_handler = io_handler
        self._debug = debug

        self._font = ("Calibri", 24, "bold")
        self._window = tk.Tk()
        self._window.title("KSA Wäscheversorgung")
        self._window.iconbitmap('./src/_.ico')

        self._label1 = tk.Label(self._window, text="Welche(n) Wagen haben Sie beladen?", font=self._font)
        self._label1.grid(column=0, row=0)

        self._text1 = tk.Entry(self._window,width=40, font=self._font)
        self._text1.grid(column=0, row=1)
        self._text1.focus_set()

        self._label2 = tk.Label(self._window, text="Was sind Ihre Initialen?", font=self._font)
        self._label2.grid(column=0, row=2)

        self._text2 = tk.Entry(self._window,width=40, font=self._font)
        self._text2.grid(column=0, row=3)
        def _1(event):
            self._text2.focus_set()
        self._text1.bind('<Return>', _1)

        self._button = tk.Button(self._window, text="Speichern!", font=self._font, command=self.on_click)
        self._button.grid(column=0, row=4, pady=10)
        def _2(event):
            self._button.focus_set()
        self._text2.bind('<Return>', _2)

        def _3(event):
            self.on_click()
        self._button.bind('<Return>', _3)
        
    def mainloop(self):
        self._window.mainloop()

    def on_click(self):
        cart_numbers = self._text1.get()
        signature = self._text2.get()

        if not cart_numbers or not signature:
            messagebox.showwarning("Warnung", "Es wurden nicht alle Felder ausgefüllt!")

        else:

            answer = messagebox.askokcancel("Frage", "Der/Die Wagen: " + cart_numbers +" als erledigt abspeichern?")
            if answer:
                self._io_handler.grab_input(cart_numbers, signature)
                self._io_handler.process_input()

                if self._debug:
                    self._io_handler.print_recent_entries()

                self._io_handler.save_recent_entries()
                self._window.destroy()
            else:
                pass
