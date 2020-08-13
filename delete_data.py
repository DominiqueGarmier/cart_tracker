#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------
# cart tracker (c) 2020 Dominique F. Garmier MIT licence
#-------------------------------------------------------

'''
script used to reset data.csv daily
'''

# Standardlibarary imports
import os

# local imports
import main

# 3rd party imports

if __name__ == '__main__':
    # delete contents of data.csv and replace it with header and placeholder list so that excel doesnt trow an error
    f = open(main.data_path, 'w')
    f.write('cart_number,state,signature,timestamp\n')
    f.write('-,-,-,-\n')
    f.close()

