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
from tkinter import messagebox

from classes import IOHandler

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
        self._correction_label = tk.Label(self._root, text='Welche(r) Wagen soll aus den erledigten entfernt werden?', font=self._lfont)


        # define regular entries
        self._signature_textbox_main = tk.Entry(self._root, width=80, font=self._lfont)
        
        # save buttons
        self._main_save_button = tk.Button(text='Speichern', command=self.main_button_click, font=self._lfont)
        self._correct_save_button = tk.Button(text='Speichern', command=self.correct_button_click, font=self._lfont)
        
        # register new carts button   
        self._new_carts_button = tk.Label(self._root, text='neue Wagennummern registrieren', font=self._ulfont, cursor="hand2")

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
            self._root.destroy()

        # define autocomplete entries
        self._autocomplete_textbox_main = AutocompleteEntry(leave_func=focus_to_signature_textbox, width=80, font=self._lfont, listboxLength=4)
        self._autocomplete_textbox_correct = AutocompleteEntry(leave_func=focus_to_correct_save_button, width=80, font=self._lfont, listboxLength=2)

        # bind focus related functions to inputs
        self._signature_textbox_main.bind('<Return>', focus_to_main_save_button)
        self._main_save_button.bind('<Return>', focus_main_button_click)
        self._correct_save_button.bind('<Return>', focus_correct_button_click)
        self._new_carts_button.bind("<Button-1>", new_carts_button_click)

    def main_loop(self):
        '''
        Display the window and display the main page
        '''

        with open('./cart_names.txt') as cart_names:
            possible_carts = cart_names.read().splitlines()

        self._io_handler._data.pull()
        entered_carts = self._io_handler._data._df.get('cart_number').to_list()[1:]

        self._autocomplete_textbox_main.set_autocomplete_list(possible_carts)
        self._autocomplete_textbox_correct.set_autocomplete_list(entered_carts)

        self.display_main()
        self._root.mainloop()

    def display_main(self):
        '''
        clear the display and show the gui elements of the "main" page
        '''
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


    def display_correct(self):
        '''
        clear the display and show the gui elements of the "correct" page
        '''
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
        cart_numbers = self._autocomplete_textbox_main.get()
        signature = self._signature_textbox_main.get()

        if not cart_numbers or not signature:
            messagebox.showwarning("Warnung", "Es wurden nicht alle Felder ausgefüllt!")

        else:
            answer = messagebox.askokcancel("Frage", "Der/Die Wagen: " + cart_numbers +" als erledigt Speichern?")

            if answer:
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
        cart_numbers_to_delete_str = self._autocomplete_textbox_correct.get()
        cart_numbers_to_delete = re.split(',|;', cart_numbers_to_delete_str)
        cart_numbers_to_delete = [number.strip() for number in cart_numbers_to_delete]

        if not cart_numbers_to_delete:
            messagebox.showwarning("Warnung", "Das Feld wurde nicht ausgefüllt!")

        else:
            answer = messagebox.askokcancel("Frage", "Der/Die Wagen: " + cart_numbers_to_delete_str +" aus den erledigten Wagen entfernen?")

            if answer:
                self._io_handler._data.pull()
                df = self._io_handler._data._df

                cart_numbers = df.get('cart_number').to_list()

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

class AutocompleteEntry(tk.Entry):
    '''
    AutocompleteEntry widget, uses autocompletelist to propose cart numbers
    
    mouse interaction doesnt fully work use keyboard instead

    create dropdown list of possible autocompletes, use arrow keys to navigate up and down, return to select
    '''
    def __init__(self, leave_func, *args, **kwargs):
        '''
        creates the widget,

        machesFunction defines the function used to determine the displayed autocomplete results at any time,
        TODO make matches function return tupel instead of string to rank the words for relevance
        '''

        # Listbox length
        if 'listboxLength' in kwargs:
            self.listboxLength = kwargs['listboxLength']
            del kwargs['listboxLength']
        else:
            self.listboxLength = 4

        # Custom matches function
        if 'matchesFunction' in kwargs:
            self.matchesFunction = kwargs['matchesFunction']
            del kwargs['matchesFunction']
        else:
            def matches(fieldValue, acListEntry):
                pattern = re.compile('.*' + re.escape(fieldValue) + '.*', re.IGNORECASE)
                return re.match(pattern, acListEntry)  
            self.matchesFunction = matches
        
        # init base Entry field
        tk.Entry.__init__(self, *args, **kwargs)
        self.focus()

        self.leave_func = leave_func
        
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()

        # bind keys to functions
        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Return>", self.leave_func)
        self.bind("<Up>", self.moveUp)
        self.bind("<Down>", self.moveDown)
        
        self.listboxUp = False

    def set_autocomplete_list(self, autocomplete_list):
        '''
        to change keywords proposed by the autocomplete
        '''
        self.autocompleteList = autocomplete_list

    def changed(self, name, index, mode):
        '''
        function called every time the contents of the Entry is changed i.e. when something is typed

        causes the autocomplete list to change
        '''
        if self.var.get() == '':
            if self.listboxUp:
                self.listbox.destroy()
                self.listboxUp = False
        else:
            words = self.comparison()
            if words:
                self.bind("<Return>", self.selection)
                if not self.listboxUp:
                    self.listbox = tk.Listbox(width=self["width"], font=self['font'], height=self.listboxLength)
                    self.listbox.bind("<ButtonRelease-1>", self.change_selected)
                    self.listbox.bind("<Right>", self.selection)
                    self.listbox.place(x=self.winfo_x(), y=self.winfo_y() + self.winfo_height())
                    self.listboxUp = True
                
                self.listbox.delete(0, tk.END)
                for w in words:
                    self.listbox.insert(tk.END, w)
            else:
                if self.listboxUp:
                    self.listbox.destroy()
                    self.listboxUp = False
        
    def selection(self, event):
        '''
        even triggered when an autocomplete word is selected

        pastes the autocomplete word into the Entry and adds commas inbetween the words

        binds return to skipping focus to next widget
        '''
        self.bind("<Return>", self.leave_func)
        if self.listboxUp:

            # reformat the cart numbers already written
            _ = re.split(',|;', self.var.get())[:-1]
            curr_words = [word.strip() for word in _]

            # add spaces after commas
            new_words = ''
            for word in  curr_words:
                new_words += word + ', '

            new_words += self.listbox.get(tk.ACTIVE)
            self.var.set(new_words)
            self.listbox.destroy()
            self.listboxUp = False
            self.icursor(tk.END)
        else:
            # if listbox wasnt displayed skip to focus next wiget imediately
            self.leave_func(False)

    def change_selected(self, event):
        self.focus()
        self.bind("<Return>", self.selection)

    def moveUp(self, event):
        '''
        scrolling up in the autocomplete list using up arrow
        '''
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '1'
                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

            else:
                index = self.listbox.curselection()[0]
                
            if index != '0':                
                self.listbox.selection_clear(first=index)
                index = str(int(index) - 1)
                
                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

    def moveDown(self, event):
        '''
        scrolling down in the autocomplete list using down arrow
        '''
        if self.listboxUp:
            if self.listbox.curselection() == ():
                index = '-1'
                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index)

            else:
                index = self.listbox.curselection()[0]
                
            if index != tk.END:                        
                self.listbox.selection_clear(first=index)
                index = str(int(index) + 1)
                
                self.listbox.see(index) # Scroll!
                self.listbox.selection_set(first=index)
                self.listbox.activate(index) 

    def comparison(self):
        '''
        generate list of words to display in the autocomplete dropdown list using the matches function
        '''
        return [w for w in self.autocompleteList if self.matchesFunction(re.split(',|;', self.var.get())[-1].strip(), w)]
    
    def grid_forget(self):
        if self.listboxUp:
            self.listbox.destroy()
            self.listboxLength = False

        super().grid_forget()