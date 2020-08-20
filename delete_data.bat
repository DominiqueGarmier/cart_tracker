powershell -command "%~dp0exceltopdf.ps1"
PAUSE
powershell -command "cd %~dp0; python delete_data.py"