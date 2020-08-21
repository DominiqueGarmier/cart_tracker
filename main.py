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
import json

# local imports
from classes import IOHandler
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

    config['ExcelToPdf'] = {
        'pdf_folder_path':'path/to/folder/',
        'excel_file_path':'path/to/file.xlsx',
        'excel_sheets':[1,2],
        'pdf_names':['sheet-1', 'sheet-2']
    }

    with open(config_path, 'w') as configfile:
        config.write(configfile)

    print('config.ini generated!')
    exit()

# read form config to set constants
data_path = config['DEFAULT']['data_path']
debug = config.getboolean('DEFAULT', 'debug')

pdf_folder_path = config['ExcelToPdf']['pdf_folder_path']
excel_file_path = config['ExcelToPdf']['excel_file_path']

excel_sheets = config.get('ExcelToPdf', 'excel_sheets')
pdf_names = config.get('ExcelToPdf', 'pdf_names')

excel_sheets = eval(excel_sheets)
pdf_names = eval(pdf_names)

# create iohandler
handler = IOHandler(data_path)

# main function
if __name__ == '__main__':
    # create window and start it
    window = gui.Window(handler, debug)
    window.main_loop()
