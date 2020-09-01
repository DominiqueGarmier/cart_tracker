#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------
# cart tracker (c) 2020 Dominique F. Garmier MIT licence
# ------------------------------------------------------

'''
classes for the autocomplete elements of the gui
'''

# standard library iports
import tkinter as tk
import time
import re


class BlobText(tk.Frame):
    '''
    Class to display speechbubble like labels with a cross on
    the right side of it to remove.
    '''

    def __init__(
            self, master, display, text,
            font=("Calibri", 12, "bold"),
            *args, **kwargs
            ):

        '''
        creates a blobtext object. The blobtext is packed to the
        left side of its master
        '''
        self._master = master
        self._display = display

        # trick to give frame widget a border
        kwargs['highlightbackground'] = 'black'
        kwargs['highlightcolor'] = 'black'
        kwargs['highlightthickness'] = 1

        # init frame widget
        super().__init__(self._master, *args, **kwargs)

        # bool to keep track of if it was already deleted (using the x button)
        self._exists = True

        # create label as a child of self
        self._font = font
        self._text = text
        self._label = tk.Label(self, text=self._text, font=self._font)

        # hide blobtext and set exists to false
        def close_func():
            self.destroy()
            self._exists = False

            self._display.blob_removed()

        # button as a child of self to close the blob text
        self._button = tk.Button(
            self, text='x', relief='flat',
            command=close_func,
            font=("Calibri", 12, "bold")
            )

        # grid alignment iside of the the frame
        self._label.grid(column=0, row=0)
        self._button.grid(column=1, row=0)


class BlobTextDisplay(tk.Frame):
    '''
    class to organize multiple blobtext objects
    '''

    def __init__(self, master, root, *args, **kwargs):
        '''
        initializes list to store blobtexts in, everything is child to a frame
        '''
        super().__init__(master, *args, **kwargs)

        # create one frame for each line start with the first frame
        first_frame = tk.Frame(master=self)
        first_frame.grid(column=0, row=0, stick=tk.W)
        self._frames = [first_frame]

        self._blobs = []
        self._rows = []
        self._lines = 1

        self._root = root
        self._root_width = None
        self._all_words = []

    def add_blob_text(self, text, *args, **kwargs):
        '''
        method to add a blobtext to a btd, the new element
        will be appended to the right of the previous ones
        '''

        # the frist time we need to check how wide the window is
        if self._root_width is None:
            self._root_width = self._root.winfo_width()

        # get the last line
        last_frame = self._frames[-1]

        # create a new blobtext and place it on the last line
        blob = BlobText(
            master=last_frame,
            display=self, text=text,
            *args, **kwargs
            )

        blob.pack(side=tk.LEFT, padx=2, pady=2)
        self._root.update()

        # if the line overflows now you need to make a new line and put the
        # text blob there
        if last_frame.winfo_width() > self._root_width:

            new_frame = tk.Frame(master=self)
            new_frame.grid(column=0, row=len(self._frames), stick=tk.W)

            self._frames.append(new_frame)

            last_frame = self._frames[-1]

            # delete the old blob
            blob.destroy()
            blob = BlobText(
                master=last_frame,
                display=self, text=text,
                *args, **kwargs
                )
            blob.pack(side=tk.LEFT, padx=2, pady=2)

        # add the text blob to the others
        self._blobs.append(blob)
        self._rows.append(len(self._frames) - 1)
        self._root.update()

        self._all_words = self.get_all_words()

    def blob_removed(self):
        '''
        method to update the postioning of textblobs in the display.
        '''

        # check for already hidden blobs to delete them
        for blob in self._blobs:
            if not blob._exists:
                ind = self._blobs.index(blob)
                self._blobs.pop(ind)
                self._rows.pop(ind)

        self._root.update()
        self._all_words = self.get_all_words()

        # go through each line and check for lines which arent full
        for i, frame in enumerate(self._frames):

            # add as many blobs from the next line to the previous
            # one until its full
            while (
                    i + 1 in self._rows and
                    frame.winfo_width() < self._root_width
                    ):

                next_row_start = self._rows.index(i + 1)

                blob = self._blobs[next_row_start]
                temp_text = blob._text
                temp_font = blob._font

                # check that the blob you tried to move up would actually fit
                if blob.winfo_width() < self._root_width - frame.winfo_width():

                    # if it does fit, delete the old one and make a new one
                    # on the other line
                    blob.destroy()
                    blob._exists = False

                    new_blob = BlobText(
                        master=frame,
                        display=self,
                        text=temp_text,
                        font=temp_font
                        )
                    new_blob.pack(side=tk.LEFT, padx=2, pady=2)

                    self._blobs[next_row_start] = new_blob
                    self._rows[next_row_start] = i

                    # destroy empty lines
                    if not i + 1 in self._rows:
                        self._frames[i + 1].destroy()
                        self._frames.pop(i + 1)

                    # update to be able to get the new width
                    self._root.update()

                else:
                    break

    def get_all_text(self):
        '''
        concatenate all the strings inside all the blobtexts in a format
        compatible with previous iterations
        '''

        s = ''
        for blob in self._blobs:
            if blob._exists:
                s += blob._text + ', '

        return s

    def get_all_words(self):
        '''
        return a list of all words inside blobs
        '''

        words = []
        for blob in self._blobs:
            if blob._exists:
                words.append(blob._text)

        return words


class AutocompleteEntry(tk.Frame):
    '''
    new autocomplete entry class, it has a search field where you can search
    for terms inside of an autocomplete when selected using either Return or
    Double LMB the term is added to a blobtextdisplay, where each term is
    shown as a bubble which can be deleted with a cross next to it
    '''

    def __init__(
            self, master, ac_list_source,
            leave_function, lb_length,
            no_clear_if_kw_match=True,
            show_kw_in_lb=True,
            *args, **kwargs
            ):
        '''
        initalizes the autocomplete entry and blob text display,
        aligning everything relative to a Frame
        '''

        # init parent obj
        super().__init__(master)

        # the entry for the search function
        self._entry = tk.Entry(master=self, *args, **kwargs)

        # the btd
        self._blob_text_display = BlobTextDisplay(master=self, root=master)

        # align them on top of each other #TODO perhaps better alternatives
        self._entry.grid(column=0, row=1)
        self._blob_text_display.grid(column=0, row=0, stick=tk.W)

        # autocomplete list source
        self._ac_list_source = ac_list_source
        self._leave_function = leave_function

        # check for two types for possible ac list sources
        # either list directly in which case the source is the list
        # or a function that when called returns a list
        # this allows the refreshing of the ac list
        if type(self._ac_list_source) == list:
            self._ac_list = self._ac_list_source
            self._ac_list_refresh = False

        elif callable(self._ac_list_source):
            self._ac_list = self._ac_list_source()
            self._ac_list_refresh = True
            self._last_refresh = time.time()

        else:
            raise TypeError(str(self._ac_list_source) + ' has to be either a list of a callable object that returns a list') # noqa

        # content of the entrys
        self._var = self._entry['textvariable']
        if not self._var:
            self._var = self._entry['textvariable'] = tk.StringVar()

        # track changes in self._var
        self._var.trace('w', self.changed)

        # map buttons
        self._entry.bind('<Up>', self.scroll_up)
        self._entry.bind('<Down>', self.scroll_down)
        self._entry.bind('<Return>', self._leave_function)

        # list box is not up by default
        self._lb_up = False

        # number of autocompletes shown
        self._lb_length = lb_length

        # clear the search field when a word is searched by exact match
        self._no_clear_if_kw_match = no_clear_if_kw_match
        self._show_kw_in_lb = show_kw_in_lb

    def show_lb(self, words, key_words={}):
        '''
        creates or updates listbox
        '''

        # only create lb if it doesnt already exist
        if not self._lb_up:

            # create lisbox obj
            # bind buttons
            self._lb_up = True

            self._lb = tk.Listbox(
                width=self._entry['width'],
                font=self._entry['font']
                )

            self._lb.place(
                x=self.winfo_x(),
                y=self.winfo_y() + self.winfo_height()
                )

            self._lb.bind('<Double-Button-1>', self.selection)
            self._lb.bind('<ButtonRelease-1>', self.mouse_click)
            self._entry.bind('<Return>', self.selection)

        # shrink lb if there arent enought words
        self._lb.configure(height=min(self._lb_length, len(words)))

        # if lb is already up, only update the contents
        # first remove old words, then add the new ones
        self._lb.delete(0, tk.END)

        # remove multiples
        words = list(dict.fromkeys(words))
        for word in words:
            self._lb.insert(tk.END, word)

    def hide_lb(self):
        '''
        method to hide the listbox
        '''

        # only hide if its not already hidden
        if self._lb_up:
            self._lb_up = False
            self._lb.destroy()
            self._entry.bind('<Return>', self._leave_function)

    def changed(self, name, index, mode):
        '''
        dispalys and updates the contents of the listbox
        '''

        # hide lb if entry is empty

        # only autocomplete the last word in a series of comma separated words
        last_word = self._var.get().split(',')[-1].strip()

        if not last_word:
            self.hide_lb()
            self._lb_name_not_found = False

        # show lb if entry is not empty
        else:
            words, kws = self.ac_query()
            if words:
                self.show_lb(words, kws)
                self._lb_name_not_found = False

            # hide lb if there are not ac matches
            else:
                self.show_lb(['Name nicht gefunden!'])
                self._lb_name_not_found = True

    def selection(self, event):
        '''
        pastes the selected item from the listbox into the entry
        '''
        if self._lb_up:

            if self._ac_list_refresh and time.time() - self._last_refresh > 5:
                self._ac_list = self._ac_list_source()
                self._last_refresh = time.time()

            if not self._lb_name_not_found:

                # grab the text out of the btd, since its already formated
                # and correct there is for checking like in older version
                word = self._lb.get(tk.ACTIVE)
                self._blob_text_display.add_blob_text(
                    text=word,
                    font=("Calibri", 16, "bold")
                    )

                # set the search space to empty

                self.hide_lb()
                self._entry.icursor(tk.END)

                words, _ = self.ac_query(duplicates=True)
                kw_match = words[word]

                words, kws = self.ac_query()
                if self._no_clear_if_kw_match and kw_match and words:

                    self.show_lb(words, kws)

                else:

                    self._var.set('')

            else:

                # if there is no matching word in the ac list, then just
                # empty the search box
                self._var.set('')
                self.hide_lb()
                self._entry.icursor(tk.END)

    def scroll_up(self, event):
        '''
        manages the scrolling inside the listbox
        '''

        # only scroll if lb is showing
        if self._lb_up:

            # if no element inside the lb is selected start at index 1
            if self._lb.curselection() == ():

                index = '1'

            else:

                # else start at the current selection
                index = self._lb.curselection()[0]

            # if not already at the top
            if index != '0':

                # scroll up
                self._lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self._lb.select_set(first=index)
                self._lb.activate(index)

                # make sure the lb scrolls if you reach the top of the screen
                # but not the top of the list
                self._lb.see(index)

    def scroll_down(self, event):
        '''
        downward scrolling of the lb
        '''

        # only scrll if the lb is up
        if self._lb_up:

            # if there is no selected element start at index -1
            # (so that when you scroll it goes to 0)
            if self._lb.curselection() == ():

                index = '-1'

            else:

                # use the current selected object as index
                index = self._lb.curselection()[0]

            # if not all the way at the bottom
            if index != tk.END:

                # scroll down
                self._lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self._lb.select_set(first=index)
                self._lb.activate(index)

                # have the lb scroll if you reach the bottom of
                # the screen but not the lb
                self._lb.see(index)

    def mouse_click(self, event):
        '''
        handle the special chase of a mousclick selecting a word from the list,
        to refocus on the entry
        '''
        self._entry.focus()

    def ac_query(self, duplicates=False):
        '''
        queries all the ac list to return a list of possible autocompletes
        '''

        # refresh the ac list if refresh is set to true
        if self._ac_list_refresh and time.time() - self._last_refresh > 5:
            self._ac_list = self._ac_list_source()
            self._last_refresh = time.time()

        # only autocompletet the last word in a series of comma separated words
        last_word = self._var.get().split(',')[-1].strip()

        # escape all regex sensitive characters
        regex_chars = '[](){}*+?|^$.\\'

        _ = ''
        for letter in last_word:
            if letter in regex_chars:
                _ += '\\' + letter
            else:
                _ += letter

        last_word = _

        # parse using regex to find matches
        pattern = re.compile('.*' + last_word + '.*', re.IGNORECASE)

        # checks for any matches inside the key word list and appends the
        # first element of the keyword list if any kw matches
        #
        # return a dict with the key being the word and the value being
        # a bool saying if the match was triggered by a direct match
        # or a keyword match
        matches = {}
        matches_with_kw = {}
        for w in self._ac_list:

            # dont show words already in blob text
            if w in self._blob_text_display._all_words and not duplicates:
                continue

            if re.match(pattern, w):
                matches[w] = False
                matches_with_kw[w] = self._ac_list[w]

            pattern_match = False
            for kw in self._ac_list[w]:

                if re.match(pattern, kw):
                    pattern_match = True
                    break

            if pattern_match:
                matches[w] = True
                matches_with_kw[w] = self._ac_list[w]

        return matches, matches_with_kw

    def grid_forget(self):
        '''
        hide the autocomplete entry
        '''
        self.hide_lb()
        super().grid_forget()
