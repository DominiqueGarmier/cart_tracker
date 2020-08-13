#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------
# cart tracker (c) 2020 Dominique F. Garmier MIT licence
#-------------------------------------------------------

'''
execute this file as __main__s
'''

# Standardlibarary imports
import os
import configparser

# local imports
from classes import IOHandler, Data
import gui

# 3rd party imports

# define config path and config parser
config_path = './config.ini'
config = configparser.ConfigParser()

# create config if it doesnt already exist
if os.path.isfile(config_path):
    config.read(config_path)

else:
    config['DEFAULT'] = {
        'data_path': './data.csv', # path to csv file on NAS
        'debug': False
    }
    with open(config_path, 'w') as configfile:
        config.write(configfile)

# read form config to set constants
data_path = config['DEFAULT']['data_path']
debug = config.getboolean('DEFAULT', 'debug')

# create iohandler
handler = IOHandler(data_path)

# read cart_names.txt for the autocomplete list
with open('./cart_names.txt') as cart_names:
    autocomplete_list = cart_names.read().splitlines()

# main function
if __name__ == '__main__':
    # create window and start it
    window = gui.Window(handler, debug, autocomplete_list, './cart_names.txt')
    window.mainloop()
