# [cart_tracker](https://github.com/dominiquegarmier/cart_tracker)
by [Dominique Garmier](https://github.com/dominiquegarmier) (c) 2020

App developed for the Kantonsspital Aarau, to track the status of laundry carts.

The App ist meant to be used by the employees to check-off certain carts as "Done" once they are loaded. The Information about all the carts is then written to a remote CSV file which can be read in real-time by an excel sheet.

## How to install

[cart_tracker](https://github.com/dominiquegarmier/cart_tracker) only works for Windows (10). It can however be adapted for unix use. Namely by replacing the *.bat and *.vbs files with their respective unix counterparts.

First off [Python 3.8](https://python.org) or later needs to be installed. Using ````pip```` you can install the required packages the following way:

````
$ pip install -r requirements.txt
````
It is also advised that you add [Python](https://python.org) to your PATH. Else you would need to adjust all the *.bat and *.vbs files. Since in their current state, they rely on PATH.

Next we should take a look at the [config.ini](./config.ini) file:

````
[DEFAULT]
data_path = ./data.csv
debug = False
````

The option ````data_path```` is to specify where you want to store the raw data. In our inteded usecase this would be a remote map drive.

The ````debug```` option makes python print out entries and some other minor messages.

For this specific usecase we want our *.csv file to be cleared once per day to reset the states of all the carts. for this there exists the [delete_data.bat](./delete_data.bat) which intern runs the [delete_data.py](./delete_data.py) file.Here we can use the built in windows Task-Scheduler, or alternatively on unix a cron task, to trigger the *.bat file once per day.

## How to use

Click the shortcut you created, a window will pop up prompting you to enter one or more cart numbers separated by commas. An autocomplete dropdown menu will help you type the cartnames correctly. Use the Arrow and Return keys to navigate. The autocompletet entry will only allow you to type valid names i.e. those in the cart_names.txt file.

To navigate between textfields hit the return button. Depending on the context you may need to hit the return button more than once (to select the entry in the autocompletet and then to skip ahead)

The second textfield asks you to provide a signature, type something like the first letters of your first and last name. It's to later on identify who loaded that cart.

After hitting return again you will be asked to confirm your entries. If you do so they will be saved in a specified CSV file where they can be read in real time by an Excel spreadsheet.

If you want to remove an entry you falsely entered, you can hit the "Korrektur" Button at the top left. This will open a new Page where you only have to enter the cart name you want to remove. This Textfield also has an autocomplete feature, only autocompleting to cart names already in the entries (else it works the same as the first autocomplete entry). After hitting enter the CSV file will be updated.

## How to update

[cart_tracker](https://github.com/dominiquegarmier/cart_tracker) can be updated using ````git````. If the repo was cloned as is, you can simply run ````git pull````. The config file and the [cart_names.txt](./cart_names.txt) file are both in the [.gitignore](./gitignore). This can also be done using the ````update.py```` script, which will automatically try to pull from master.