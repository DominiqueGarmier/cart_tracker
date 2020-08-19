#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------
# cart tracker (c) 2020 Dominique F. Garmier MIT licence
#-------------------------------------------------------

'''
all gui related classes for cart tracker
'''

# standard library imports
import re
import time
import os

# 3rd party imports
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from classes import IOHandler
from autocomplete_entry import AutocompleteEntry

class Window:
    '''
    Class for the GUI of the cart tracker
    '''

    def __init__(self, io_handler, debug=False):
        '''
        initializes all the displayable objects, doesnt display them yet
        and defines all the focus transfer functions
        '''
        
        # define root
        self._root = tk.Tk()
        self._root.title('KSA Wäscheversorgung - Wagen Tracker')
        self._root.iconbitmap('./src/_.ico')

        # define constants
        self._lfont = ("Calibri", 24, "bold")
        self._sfont = ("Calibri", 12)
        self._ulfont = ("Calibri", 12, "underline")
        self._debug = debug

        # io handler
        self._io_handler = io_handler

        # define menu buttons
        self._to_correct = tk.Button(self._root, text='Korrektur', command=self.display_correct, font=self._sfont)
        self._back_to_main = tk.Button(self._root, text='Zurück', command=self.display_main, font=self._sfont)


        # define labels
        self._main_label_top = tk.Label(self._root, text='Welche(n) Wagen haben Sie beladen?', font=self._lfont)
        self._main_label_bottom = tk.Label(self._root, text='Was sind Ihre Initialen?', font=self._lfont)
        self._correction_label = tk.Label(self._root, text='Welche(r) Wagen soll(en) aus den erledigten entfernt werden?', font=self._lfont)


        # define regular entries
        self._signature_textbox_main = tk.Entry(self._root, width=80, font=self._lfont)
        
        # save buttons
        self._main_save_button = tk.Button(text='Speichern', command=self.main_button_click, font=self._lfont)
        self._correct_save_button = tk.Button(text='Speichern', command=self.correct_button_click, font=self._lfont)
        
        # register new carts button   
        self._new_carts_button = tk.Label(self._root, text='Neue Wagennummern registrieren.', font=self._ulfont, cursor="hand2")
 
        # copyright button
        self._copyright_label = tk.Label(self._root) #, text='Copyright (c) Dominique Garmier 2020', font=self._sfont)

        # focus transfer functions and focus relevant functions
        def focus_to_signature_textbox(event):
            self._signature_textbox_main.focus_set()

        def focus_to_main_save_button(event):
            self._main_save_button.focus_set()

        def focus_to_correct_save_button(event):
            self._correct_save_button.focus_set()
        
        def focus_main_button_click(event):
            self.main_button_click()

        def focus_correct_button_click(event):
            self.correct_button_click()

        def new_carts_button_click(event):
            os.startfile(os.path.abspath('./cart_names.txt'))

        # read already entered cart names for autocompletion
        self._io_handler._data.pull()
        entered_carts = self._io_handler._data._df.get('cart_number').to_list()[1:]

        # autocomplete source functions
        def main_autocomplete_source():
            with open('./cart_names.txt') as cart_names:
                return cart_names.read().splitlines()

        # this could be replaced directly with the list, but will be changed in the future probably
        def correct_autocomplete_source():
            return entered_carts

        # define autocomplete entries
        self._autocomplete_textbox_main = AutocompleteEntry(master=self._root, ac_list_source=main_autocomplete_source, leave_function=focus_to_signature_textbox, lb_length=4, width=80, font=self._lfont)
        self._autocomplete_textbox_correct = AutocompleteEntry(master=self._root, ac_list_source=correct_autocomplete_source, leave_function=focus_to_correct_save_button, lb_length=2, width=80, font=self._lfont)

        # bind focus related functions to inputs
        self._signature_textbox_main.bind('<Return>', focus_to_main_save_button)
        self._main_save_button.bind('<Return>', focus_main_button_click)
        self._correct_save_button.bind('<Return>', focus_correct_button_click)
        self._new_carts_button.bind("<Button-1>", new_carts_button_click)

    def main_loop(self):
        '''
        Display the window and display the main page
        '''

        # switch to display main page
        self.display_main()
        self._root.mainloop()

    def display_main(self):
        '''
        clear the display and show the gui elements of the "main" page
        '''

        # clear previous page
        self.clear_display()

        # menu button
        self._to_correct.grid(column=0, row=0, sticky=tk.NW)

        # labels
        self._main_label_top.grid(column=0, row=0)
        self._main_label_bottom.grid(column=0, row=2)

        # autocomplete entry
        self._autocomplete_textbox_main.grid(column=0, row=1)
        self._autocomplete_textbox_main.focus_set()

        # regular entry
        self._signature_textbox_main.grid(column=0, row=3)

        # save button
        self._main_save_button.grid(column=0, row=4, pady=5)

        # new carts button
        self._new_carts_button.grid(column=0, row=4, sticky=tk.SE)

        # copyright label
        self._copyright_label.grid(column=0, row=4, sticky=tk.SW)


    def display_correct(self):
        '''
        clear the display and show the gui elements of the "correct" page
        '''

        # clear previous page
        self.clear_display()
        
        # menu button
        self._back_to_main.grid(column=0, row=0, sticky=tk.NW)

        # labels
        self._correction_label.grid(column=0, row=0)

        # autocomplete entry
        self._autocomplete_textbox_correct.grid(column=0, row=1)
        self._autocomplete_textbox_correct.focus_set()

        # save button
        self._correct_save_button.grid(column=0, row=2, pady=5)

        # new carts button
        self._new_carts_button.grid(column=0, row=2, sticky=tk.SE)

        # copyright label
        self._copyright_label.grid(column=0, row=2, sticky=tk.SW)

    def clear_display(self):
        '''
        clear the display by hiding all gui elements
        '''
        for element in self._root.grid_slaves():
            element.grid_forget()

    def main_button_click(self):
        '''
        what happens when you press the save button on the main page:

        check if you entered something,
        grab what you entered, format it, ask for confirmation and then
        add new entries to the csv file.
        finally it also closes the window.
        '''

        '''
        # formats entry to only contain valid namess
        _ = self._autocomplete_textbox_main._blob_text_display.get_all_text.split(',')
        curr_words = [word.strip() for word in _]

        new_words = ''
        for word in  curr_words:
            if word in self._autocomplete_textbox_main._ac_list and word:
                new_words += word + ', '

        # set entry to contain formated strings
        self._autocomplete_textbox_main._var.set(new_words)
        '''

        # remove listbox
        self._autocomplete_textbox_main.hide_lb()

        # grab strings from the entry fields
        cart_numbers = self._autocomplete_textbox_main._blob_text_display.get_all_text()
        signature = self._signature_textbox_main.get()

        # warning messages if entries arent filled properly
        if not cart_numbers and not signature:
            messagebox.showwarning("Warnung", "Es wurden nicht alle Felder ausgefüllt.")

        elif not cart_numbers:
            messagebox.showwarning("Warnung", "Es wurde keine (existierende) Wagennummer angegeben.")
            
        elif not signature:
            messagebox.showwarning("Warnung", "Es wurden keine Initialen angegeben.")

        # if everything is entered correclty ask for confirmation
        else:
            answer = messagebox.askokcancel("Frage", "Der/Die Wagen: " + cart_numbers[:-2] + " als erledigt Speichern?")

            if answer:

                # let the io handler process the inputs
                self._io_handler.grab_input(cart_numbers, signature)
                self._io_handler.process_input()

                # prints out new entries if debug=True
                if self._debug:
                    self._io_handler.print_recent_entries()

                self._io_handler.save_recent_entries()

                self._root.destroy()
            
            else:
                pass

    def correct_button_click(self):
        '''
        what happens when you hit the save button the the "correct" page:

        checks if you entered something, asks you to confirm,
        then it updates the csv by deleting the chosen entries.
        finally it closes the window.
        '''
        '''
        # formats entry to only contain valid names
        _ = self._autocomplete_textbox_correct._var.get().split(',')
        curr_words = [word.strip() for word in _]

        new_words = ''
        for word in  curr_words:
            if word in self._autocomplete_textbox_correct._ac_list and word:
                new_words += word + ', '

        # puts formated strings into the entries text field
        self._autocomplete_textbox_correct._var.set(new_words)
        '''
        # remove the listbox if it exists
        self._autocomplete_textbox_correct.hide_lb()

        # read the entry and process the string
        cart_numbers_to_delete_str = self._autocomplete_textbox_correct._blob_text_display.get_all_text()
        cart_numbers_to_delete = cart_numbers_to_delete_str.split(',')
        cart_numbers_to_delete = [number.strip() for number in cart_numbers_to_delete if number.strip()]

        # trow warning if nothing was entered
        if not cart_numbers_to_delete_str:
            messagebox.showwarning("Warnung", "Es wurde keine (existierende) Wagennummer angegeben.")

        # ask for confirmation
        else:
            answer = messagebox.askokcancel("Frage", "Der/Die Wagen: " + cart_numbers_to_delete_str[:-2] +" aus den erledigten Wagen entfernen?")

            if answer:

                # grab a copy of the existing entries from the io handler
                self._io_handler._data.pull()
                df = self._io_handler._data._df

                cart_numbers = df.get('cart_number').to_list()

                # find the entries to remove and remove them
                indices_to_delete = []
                for cart_number_to_delete in cart_numbers_to_delete:

                    # default entry is '-' this should never be deleted, it keeps excel from crashing
                    # if the file is empty otherwise
                    if cart_number_to_delete != '-' and cart_number_to_delete in cart_numbers:
                        indices = [i for i, x in enumerate(cart_numbers) if x == cart_number_to_delete]
                        indices_to_delete += indices

                # remove entries from df
                df = df.drop(indices_to_delete)

                # save change to csv file
                self._io_handler._data._df = df
                self._io_handler._data.push()

                # close the window
                self._root.destroy()
            
            else:
                pass
