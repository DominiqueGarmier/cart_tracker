# Standardlibarary imports
import os
import configparser

# local imports
from classes import IOHandler, Data
import gui

# 3rd party imports

config_path = './config.ini'
config = configparser.ConfigParser()

if os.path.isfile(config_path):
    config.read(config_path)

else:
    config['DEFAULT'] = {
        'data_path': './data.csv', # path to csv file on NAS
        'debug': False
    }
    with open(config_path, 'w') as configfile:
        config.write(configfile)

data_path = config['DEFAULT']['data_path']
debug = config.getboolean('DEFAULT', 'debug')
handler = IOHandler(data_path)

window = gui.Window(handler, debug)

if __name__ == '__main__':
    window.mainloop()
