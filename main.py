# Standardlibarary imports

# local imports
from classes import IOHandler

# 3rd party imports
import pandas
import matplotlib.pyplot as plt

handler = IOHandler()

if __name__ == '__main__':
    handler.ask_for_input()
    handler.process_input()
    handler.print_recent_entries()
    