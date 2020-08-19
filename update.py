# standard libary imports
import subprocess

# try to pull from git repo
try:
    # this pulls the maser branch from origin
    subprocess.call('Powershell -command "git pull origin master"')
except:
    pass
