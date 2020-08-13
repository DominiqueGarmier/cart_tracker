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

    def __init__(self, io_handler, debug=False):
            
        # define root
        self._root = tk.Tk()
        self._root.title('KSA Wäscheversorgung - Wagen Tracker')
        self._root.iconbitmap('./src/_.ico')

        # define constants
        self._lfont = ("Calibri", 24, "bold")
        self._sfont = ("Calibri", 12)
        self._ulfont = ("Calibri", 12, "underline")
        self._io_handler = io_handler
        self._debug = debug

        # define menu buttons
        self._to_correct = tk.Button(self._root, text='Korrektur', command=self.display_correct, font=self._sfont)
        self._back_to_main = tk.Button(self._root, text='Zurück', command=self.display_main, font=self._sfont)


        # define labels
        self._main_label_top = tk.Label(self._root, text='Welche(n) Wagen haben Sie beladen?', font=self._lfont)
        self._main_label_bottom = tk.Label(self._root, text='Was sind Ihre Initialen?', font=self._lfont)
        self._correction_label = tk.Label(self._root, text='Welcher Eintrag soll gelöst werden?', font=self._lfont)


        # define regular entries
        self._signature_textbox_main = tk.Entry(self._root, width=80, font=self._lfont)
        
        # save buttons
        self._main_save_button = tk.Button(text='Speichern', font=self._lfont)
        self._correct_save_button = tk.Button(text='Speichern', font=self._lfont)

        # focus transfer functions
        def focus_to_signature_textbox(event):
            self._signature_textbox_main.focus_set()

        def focus_to_main_save_button(event):
            self._main_save_button.focus_set()

        def focus_to_correct_save_button(event):
            self._correct_save_button.focus_set()

        # define autocomplete entries
        test = ['test','test','test','test','test']
        self._autocomplete_textbox_main = AutocompleteEntry(test, leave_func=focus_to_signature_textbox, width=80, font=self._lfont, listboxLength=4)
        self._autocomplete_textbox_correct = AutocompleteEntry(test, leave_func=focus_to_correct_save_button, width=80, font=self._lfont, listboxLength=2)

        # register new carts button
        self._new_carts_button = tk.Label(self._root, text='neue Wagennummern registrieren', font=self._ulfont, cursor="hand2")

    def main_loop(self):
        '''
        Display the window and display the main page
        '''
        self.display_main()
        self._root.mainloop()

    def display_main(self):
        self.clear_display()

        # menu button
        self._to_correct.grid(column=0, row=0, sticky=tk.NW)

        # labels
        self._main_label_top.grid(column=0, row=0)
        self._main_label_bottom.grid(column=0, row=2)

        # autocomplete entry
        self._autocomplete_textbox_main.grid(column=0, row=1)

        # regular entry
        self._signature_textbox_main.grid(column=0, row=3)

        # save button
        self._main_save_button.grid(column=0, row=4, pady=5)

        # new carts button
        self._new_carts_button.grid(column=0, row=4, sticky=tk.SE)


    def display_correct(self):
        self.clear_display()
        
        # menu button
        self._back_to_main.grid(column=0, row=0, sticky=tk.NW)

        # labels
        self._correction_label.grid(column=0, row=0)

        # autocomplete entry
        self._autocomplete_textbox_correct.grid(column=0, row=1)

        # save button
        self._correct_save_button.grid(column=0, row=2, pady=5)

        # new carts button
        self._new_carts_button.grid(column=0, row=2, sticky=tk.SE)

    def clear_display(self):
        for element in self._root.grid_slaves():
            element.grid_forget()






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
    
    def grid_forget(self):
        if self.listboxUp:
            self.listbox.destroy()
            self.listboxLength = False

        super().grid_forget()

w = Window(None)
w.main_loop()