import tkinter as tk
import time
import re

class BlobText(tk.Frame):
    '''
    Class to display speechbubble like labels with a cross on the right side of it to remove.
    '''

    def __init__(self, master, text, font=None, *args, **kwargs):
        '''
        creates a blobtext object. The blobtext is packed to the left side of its master
        '''

        # trick to give frame widget a border
        kwargs['highlightbackground'] = 'black'
        kwargs['highlightcolor'] = 'black'
        kwargs['highlightthickness'] = 1

        # init frame widget
        super().__init__(master, *args, **kwargs)

        # bool to keep track of if it was already deleted (using the x button)
        self._exists = True

        # create label as a child of self
        self._text = text
        self._label = tk.Label(self, text=self._text, font=font)

        # hide blobtext and set exists to false
        def close_func():
            self.destroy()
            self._exists = False

        # button as a child of self to close the blob text
        self._button = tk.Button(self, text='x', relief='flat', command=close_func, font=("Calibri", 12, "bold"))

        # grid alignment iside of the the frame
        self._label.grid(column=0, row=0)
        self._button.grid(column=1, row=0)

class BlobTextDisplay(tk.Frame):
    '''
    class to organize multiple blobtext objects
    '''

    def __init__(self, master, *args, **kwargs):
        '''
        initializes list to store blobtexts in, everything is child to a frame
        '''
        super().__init__(master, *args, **kwargs)

        self._blobs = []

    def add_blob_text(self, text, *args, **kwargs):
        '''
        method to add a blobtext to a btd, the new element will be appended to the right of the previous ones
        '''
        blob = BlobText(master=self, text=text, *args, **kwargs)
        blob.pack(side=tk.LEFT, padx=1)
        self._blobs.append(blob)

    def get_all_text(self):
        '''
        concatenate all the strings inside all the blobtexts in a format compatible with previous iterations
        '''

        s = ''
        for blob in self._blobs:
            if blob._exists:
                s += blob._text + ', '
        
        return s

class AutocompleteEntry(tk.Frame):
    '''
    new autocomplete entry class, it has a search field where you can search for terms inside of an autocomplete list
    when selected using either Return or Double LMB the term is added to a blobtextdisplay, where each term
    is shown as a bubble which can be deleted with a cross next to it
    '''
    
    def __init__(self, master, ac_list_source, leave_function, lb_length, *args, **kwargs):
        '''
        initalizes the autocomplete entry and blob text display, aligning everything relative to a Frame
        '''

        # init parent obj
        super().__init__(master)

        # the entry for the search function
        self._entry = tk.Entry(master=self, *args, **kwargs)

        # the btd
        self._blob_text_display = BlobTextDisplay(master=self, width=50)

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
            raise TypeError(str(self._ac_list_source) + ' has to be either a list of a callable object that returns a list')

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
        

    def show_lb(self, words):
        '''
        creates or updates listbox
        '''

        # only create lb if it doesnt already exist
        if not self._lb_up:

            # create lisbox obj
            # bind buttons
            self._lb_up = True
            self._lb = tk.Listbox(width=self._entry['width'], font=self._entry['font'])
            self._lb.place(x = self.winfo_x(), y = self.winfo_y() + self.winfo_height())
            self._lb.bind('<Double-Button-1>', self.selection)
            self._lb.bind('<ButtonRelease-1>', self.mouse_click)
            self._entry.bind('<Return>', self.selection)

        # shrink lb if there arent enought words
        self._lb.configure(height=min(self._lb_length, len(words)))

        # if lb is already up, only update the contents
        # first remove old words, then add the new ones
        self._lb.delete(0, tk.END)
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
            if words := self.ac_query():
                self.show_lb(words)
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
            
            # words = [word.strip() for word in self._var.get().split(',')[:-1]]

            if not self._lb_name_not_found:
                
                # grab the text out of the btd, since its already formated and correct there is for checking
                # like in older version
                word = self._lb.get(tk.ACTIVE)
                self._blob_text_display.add_blob_text(text=word, font=("Calibri", 16, "bold"))
                
                # set the search space to empty
                self._var.set('')
                self.hide_lb()
                self._entry.icursor(tk.END)
           
            else:
                
                # if there is no matching word in the ac list, then just empty the search box
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

                # make sure the lb scrolls if you reach the top of the screen but not the top of the list
                self._lb.see(index)
            
    def scroll_down(self, event):
        '''
        downward scrolling of the lb
        '''

        # only scrll if the lb is up
        if self._lb_up:

            # if there is no selected element start at index -1 (so that when you scroll it goes to 0)
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

                # have the lb scroll if you reach the bottom of the screen but not the lb
                self._lb.see(index)

    def mouse_click(self, event):
        '''
        handle the special chase of a mousclick selecting a word from the list, to refocus on the entry
        '''
        self._entry.focus()

    def ac_query(self):
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
        return [w for w in self._ac_list if re.match(pattern, w)]

    def grid_forget(self):
        '''
        hide the autocomplete entry
        '''
        self.hide_lb()
        super().grid_forget()
