# Standardlibarary imports

# local imports
from classes import IOHandler, Data

# 3rd party imports
import pandas
import matplotlib.pyplot as plt

file_path = './data.csv' # path to csv file on NAS

data = Data(file_path)
handler = IOHandler(data)


if __name__ == '__main__':
    #handler.ask_for_input()
    #handler.process_input()
    #handler.print_recent_entries()

    data.pull()
    data.edit()
    data.push()
    