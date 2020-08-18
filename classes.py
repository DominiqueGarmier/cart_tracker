#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------
# cart tracker (c) 2020 Dominique F. Garmier MIT licence
#-------------------------------------------------------

'''
most important classes
'''

# Standardlibarary imports
import re
import os
import datetime

# local imports

# 3rd party imports
import pandas as pd

class IOCache:
    def __init__(self):
        self.raw_initals = None
        self.raw_initals = None
        self.recent_entries = None

class IOHandler:
    
    def __init__(self, data_path):
        '''
        inits the IOCache and the Data object
        '''
        self._cache = IOCache()
        self._data = Data(data_path)

    def ask_for_input(self):
        '''
        args: None,b

        retruns: None

        asks for cart numbers and signature
        trows errors if none are given

        stores input as class variable of self.cache
        '''

        self._cache.raw_numbers = input("\n -> Welche(n) Wagen haben Sie beladen?\n")
        self._cache.raw_signature = input("\n -> Was sind Ihre Initialen?\n")

    def grab_input(self, raw_numbers, raw_signature):
        '''
        grabs inputs directrly from args
        '''
        self._cache.raw_numbers = raw_numbers
        self._cache.raw_signature = raw_signature

    def process_input(self):
        '''
        args: None

        returns: list of NewEntry Objects
        
        processes raw inputs and creates a NewEntry object for every Cart given by raw_numbers
        '''

        # process cart_numbers
        cart_numbers = re.split(',|;', self._cache.raw_numbers)
        cart_numbers = [cart_number.strip() for cart_number in cart_numbers]

        # process signatue
        signatrue = self._cache.raw_signature

        # creates Entry objects for all new entries
        recent_entries = []
        for cart_number in cart_numbers:
            if cart_number:
                _ = Entry(cart_number=cart_number, state='done', signatrue=signatrue)
                recent_entries.append(_)

        # stores all new entries
        self._cache.recent_entries = recent_entries
    

    def print_recent_entries(self):
        '''
        prints out all new entries for debugging
        '''
        for entry in self._cache.recent_entries:
            print(entry)

    def save_recent_entries(self):
        '''
        pulls edits and pushes database to add new entries
        '''
        
        self._data.pull()
        self._data.edit(self._cache.recent_entries)
        self._data.push()
        
class Entry:

    def __init__(self, cart_number=None, state=None, signatrue=None):
        '''
        Creats Entry Object

        cart_number: the number of the cart
        state: the state of said cart: i.e. "done"
        signature: signature of the person who loaded that cart
        timestamp: time when the entry was registereds
        '''
        self._cart_number = cart_number # string
        self._state = state             # string: "done" or "pending" #TODO use bool?
        self._signature = signatrue     # string
        
        _ = datetime.datetime.now().time()

        min = _.minute
        if len(min) == 1:
            min = '0' + min

        self._timestamp = "{}:{}".format(_.hour, min) # timestamp to see when a cart was completed

    def __str__(self):
        '''
        defines str() method on Entry object
        '''
        _ = 'Cart Number: ' + str(self._cart_number) + ' | '
        _ += 'State: ' + str(self._state) + ' | '
        _ += 'Signature: ' + str(self._signature) + ' | '
        _ += 'Timestamp: ' + self._timestamp + '\n'
        return _

class Data:
    
    def __init__(self, file_path):
        '''
        creates Data object mirroring the csv files contents.
        '''

        # create default file in case pull doesnt return anything
        self._file_path = file_path
        self._df = pd.DataFrame(data={
            'cart_number':['-'],
            'state':['-'],
            'signature':['-'],
            'timestamp':['-']
        })
    
    def pull(self):
        '''
        updates pandas df by pulling from csv file

        only pulls if cvs file exists and isnt empty
        '''
        if os.path.exists(self._file_path) and os.stat(self._file_path).st_size > 0:
            self._df = pd.read_csv(self._file_path)

    def push(self):
        '''
        saves pandas df as csv file

        creates the file if it doesnt exist already
        '''
        self._df.to_csv(self._file_path, index=False)

    def edit(self, new_entries):
        '''
        edits contents of df, to append new entries
        '''
        new_entries = pd.DataFrame(data={
            'cart_number':[entry._cart_number for entry in new_entries],
            'state':[entry._state for entry in new_entries],
            'signature':[entry._signature for entry in new_entries],
            'timestamp':[entry._timestamp for entry in new_entries]
        })
        
        self._df = self._df.append(new_entries, ignore_index=True)