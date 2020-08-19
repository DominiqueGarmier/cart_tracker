# standard libary imports
import subprocess

# try to pull from git repo
try:
    subprocess.call('Powershell -command "git pull"')
except:
    pass