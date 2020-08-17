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

class Window:
    '''
    Class for the GUI of the cart tracker
    '''

    def __init__(self, io_handler, debug, autocomplete_list, cart_names_path):
        '''
        prepares all the window elements and binds buttons to functions

        builds:

        two entry fields with each one label
        one button at the bottom
        and a small clickable lable at the far bottom right corner
        '''

        # class aggregation with the io_handler from classes.py
        self._io_handler = io_handler

        # run in debug mode, debug=True will print new entries before writing to csv
        self._debug = debug

        # list of strings to autocomplete in the first entry field
        self._autocomplete_list = autocomplete_list
        
        # set a global font
        self._font = ("Calibri", 24, "bold")

        # define tk window
        self._window = tk.Tk()
        self._window.title("KSA Wäscheversorgung")
        self._window.iconbitmap('./src/_.ico') # ksa logo

        # menu button
        self._correct_button = tk.Button(self._window, text='Korrektur', command=self.goto_correct)
        self._correct_button.grid(column=0, row=0, sticky=tk.NW)

        # create first label
        self._label1 = tk.Label(self._window, text="Welche(n) Wagen haben Sie beladen?", font=self._font)
        self._label1.grid(column=0, row=0, pady=10, columnspan=1)

        # create 2nd entry: for the signature
        self._text2 = tk.Entry(self._window, width=80, font=self._font)
        self._text2.grid(column=0, row=3, pady=10, columnspan=1)

        # change focus function using return
        def focus_shift_1(event):
            self._text2.focus_set()

        # create 1st entry (autocomplete entry): for the cart numbers
        self._text1 = AutocompleteEntry(self._autocomplete_list, leave_func=focus_shift_1, width=80, font=self._font)
        self._text1.grid(column=0, row=1, pady=10, columnspan=1)
        self._text1.focus_set()

        # create 2nd label
        self._label2 = tk.Label(self._window, text="Was sind Ihre Initialen?", font=self._font)
        self._label2.grid(column=0, row=2, pady=10, columnspan=1)

        # create save button
        self._button = tk.Button(self._window, text="Speichern!", font=self._font, command=self.on_click)
        self._button.grid(column=0, row=4, pady=10, columnspan=1)

        # change focus function using return
        def focus_shift_2(event):
            self._button.focus_set()
        self._text2.bind('<Return>', focus_shift_2)

        # change focus function using return
        def focus_shift_3(event):
            self.on_click()
        self._button.bind('<Return>', focus_shift_3)

        # clickable label to open cart_names.txt
        self._small_button = tk.Label(self._window, text=r"neue Wagennummern regisitrieren", fg="black", cursor="hand2", font=("Calibri", 12, "underline"))
        self._small_button.grid(column=0, row=4, sticky=tk.SE)

        # open cart_names.txt and close window
        def open_file(event):
            os.startfile(os.path.abspath(cart_names_path))
            self._window.destroy()

        self._small_button.bind("<Button-1>", open_file)

    def mainloop(self):
        '''
        Displays the window and starts listening for events
        '''
        self._window.mainloop()

    def goto_correct(self):
        '''
        changes to remove entry view
        with one entry field, one confirm button
        and different autocomplete
        '''

        # hide menu button
        self._correct_button.grid_forget()

        new_autocomplete_list = ['test','test','test']
        
        # change autocomplete keywords and number of entries shown at once to not overflow the window
        self._text1.change_autocomplete_list(new_autocomplete_list)
        self._text1.listboxLength = 2

        # hide other entry
        self._text2.grid_forget()

        # change label text
        self._label1['text'] = 'Welcher Eintrag soll gelöscht werden?'

        # hide 2nd label
        self._label2.grid_forget()

        # bind new function to button


    def on_click(self):
        '''
        Button click event

        Grabs and checks both entry fields

        saves entries via io_handler

        trows warning if one or more fileds is not filled
        asks for confirmation if not

        closes the window afterwards
        '''

        # get bot entry fieds
        cart_numbers = self._text1.get()
        signature = self._text2.get()

        # trows warning if either is empty
        if not cart_numbers or not signature:
            messagebox.showwarning("Warnung", "Es wurden nicht alle Felder ausgefüllt!")

        else:
            # asks for confirmation
            answer = messagebox.askokcancel("Frage", "Der/Die Wagen: " + cart_numbers +" als erledigt abspeichern?")
            if answer:

                # saves to io_handler which processes and saves them, until finally closing the window
                self._io_handler.grab_input(cart_numbers, signature)
                self._io_handler.process_input()

                # prints out new entries if debug=True
                if self._debug:
                    self._io_handler.print_recent_entries()

                self._io_handler.save_recent_entries()
                self._window.destroy()
            else:
                pass

class AutocompleteEntry(tk.Entry):
    '''
    AutocompleteEntry widget, uses autocompletelist to propose cart numbers
    
    mouse interaction doesnt fully work use keyboard instead

    create dropdown list of possible autocompletes, use arrow keys to navigate up and down, return to select
    '''
    def __init__(self, autocompleteList, leave_func, *args, **kwargs):
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

        self.autocompleteList = autocompleteList
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

    def change_autocomplete_list(self, autocomplete_list):
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
        