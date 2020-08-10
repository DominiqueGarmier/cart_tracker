# Standardlibarary imports
import re

# local imports

# 3rd party imports
import pandas
import matplotlib.pyplot as plt

class IOCache:
    def __init__(self):
        self.raw_initals = None
        self.raw_initals = None
        self.recent_entries = None

class IOHandler:
    
    def __init__(self):
        self.cache = IOCache()

    def ask_for_input(self):
        '''
        args: None,

        retruns: None

        asks for cart numbers and signature
        trows errors if you none are given

        stores input as class variable of self.cache
        '''

        self.cache.raw_numbers = input("\n -> Welche(r) Wagen haben Sie beladen?\n")
        self.cache.raw_signature = input("\n -> Was sind Ihre Initialen?\n")

    def process_input(self):
        '''
        args. None

        returns: list of NewEntry Objects
        
        processes raw inputs and creates a NewEntry object for every Cart given by raw_numbers
        '''

        # process cart_numbers
        cart_numbers = re.split(',|, |;|; ', self.cache.raw_numbers)

        # process signatue
        signatrue = self.cache.raw_signature

        recent_entries = []
        for cart_number in cart_numbers:
            _ = Entry(cart_number=cart_number, state='done', signatrue=signatrue)
            recent_entries.append(_)

        self.cache.recent_entries = recent_entries

    def print_recent_entries(self):
        for entry in self.cache.recent_entries:
            entry.print_entry()


class Entry:

    def __init__(self, cart_number=None, state=None, signatrue=None):
        self._cart_number = cart_number # string
        self._state = state             # string: "done" or "pending" #TODO use bool?
        self._signature = signatrue       # string

    def print_entry(self):
        '''
        only for debug
        '''
        print('Cart Number: ', self._cart_number, end=' | ')
        print('State: ', self._state, end=' | ')
        print('Signature: ', self._signature, end='\n')
