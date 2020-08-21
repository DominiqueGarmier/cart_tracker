#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------
# cart tracker (c) 2020 Dominique F. Garmier MIT licence
#-------------------------------------------------------

'''
script to update cart tracker with git pull
'''

# standard libary imports
import subprocess

if __name__ == '__main__':

    # try to pull from git repo
    try:
        # this pulls the maser branch from origin
        subprocess.call('Powershell -command "git pull origin master"')
    except:
        pass
