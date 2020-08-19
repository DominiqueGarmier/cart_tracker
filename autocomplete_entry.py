import tkinter as tk
import time
import re

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
class AutocompleteEntry(tk.Entry):
    
    def __init__(self, ac_list_source, leave_function, lb_length, *args, **kwargs):

        # init parent obj
        tk.Entry.__init__(self, *args, **kwargs)

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
        self._var = self['textvariable']
        if not self._var:
            self._var = self['textvariable'] = tk.StringVar()

        # track changes in self._var
        self._var.trace('w', self.changed)

        # map buttons
        self.bind('<Up>', self.scroll_up)
        self.bind('<Down>', self.scroll_down)
        self.bind('<Return>', self._leave_function)

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

            self._lb_up = True
            self._lb = tk.Listbox(width=self['width'], font=self['font'])
            self._lb.place(x = self.winfo_x(), y = self.winfo_y() + self.winfo_height())
            self._lb.bind('<Double-Button-1>', self.selection)
            self._lb.bind('<ButtonRelease-1>', self.mouse_click)
            self.bind('<Return>', self.selection)

        # shrink lb if there arent enought words
        self._lb.configure(height=min(self._lb_length, len(words)))

        # if lb is already up, only update the contents
        # first remove old words, then add the new ones
        self._lb.delete(0, tk.END)
        for word in words:
            self._lb.insert(tk.END, word)

    def hide_lb(self):
        if self._lb_up:
            self._lb_up = False
            self._lb.destroy()
            self.bind('<Return>', self._leave_function)

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
            
            words = [word.strip() for word in self._var.get().split(',')[:-1]]

            if not self._lb_name_not_found:
                
                words.append(self._lb.get(tk.ACTIVE))
                string = ''
                for word in words:
                    if word and word in self._ac_list:
                        string += word + ', '

                self._var.set(string)
                self.hide_lb()
                self.icursor(tk.END)
            
            else:

                string = ''
                for word in words:
                    if word and word in self._ac_list:
                        string += word + ', '
                
                self._var.set(string)
                self.hide_lb()
                self.icursor(tk.END)
            
    def scroll_up(self, event):

        if self._lb_up:

            if self._lb.curselection() == ():

                index = '1'

            else:

                index = self._lb.curselection()[0]

            if index != '0':

                self._lb.selection_clear(first=index)
                index = str(int(index) - 1)
                self._lb.select_set(first=index)
                self._lb.activate(index)
                self._lb.see(index)
            
    def scroll_down(self, event):

        if self._lb_up:

            if self._lb.curselection() == ():

                index = '-1'

            else:

                index = self._lb.curselection()[0]

            if index != tk.END:

                self._lb.selection_clear(first=index)
                index = str(int(index) + 1)
                self._lb.select_set(first=index)
                self._lb.activate(index)
                self._lb.see(index)

    def mouse_click(self, event):
        self.focus()

    def ac_query(self):

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
        
        pattern = re.compile('.*' + last_word + '.*', re.IGNORECASE)
        return [w for w in self._ac_list if re.match(pattern, w)]

    def grid_forget(self):
        
        self.hide_lb()
        super().grid_forget()

if __name__ == '__main__':
    root = tk.Tk()

    lista = ['a', 'actions', 'additional', 'also', 'an', 'and', 'angle', 'are', 'as', 'be', 'bind', 'bracket', 'brackets', 'button', 'can', 'cases', 'configure', 'course', 'detail', 'enter', 'event', 'events', 'example', 'field', 'fields', 'for', 'give', 'important', 'in', 'information', 'is', 'it', 'just', 'key', 'keyboard', 'kind', 'leave', 'left', 'like', 'manager', 'many', 'match', 'modifier', 'most', 'of', 'or', 'others', 'out', 'part', 'simplify', 'space', 'specifier', 'specifies', 'string;', 'that', 'the', 'there', 'to', 'type', 'unless', 'use', 'used', 'user', 'various', 'ways', 'we', 'window', 'wish', 'you']
    
    entry = AutocompleteEntry(lista, lf, root)
    entry.grid(row=0, column=0)
    tk.Button(text='nothing').grid(row=1, column=0)
    tk.Button(text='nothing').grid(row=2, column=0)
    tk.Button(text='nothing').grid(row=3, column=0)

    root.mainloop()