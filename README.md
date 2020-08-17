# cart_tracker
by [Dominique Garmier](https://github.com/dominiquegarmier) [📧](mailto:dominique@garmier.ch) (c) 2020

App developed for the Kantonsspital Aarau, to track the status of laundry carts.

The App ist meant to be used by the employees to check-off certain carts as "Done" once they are loaded.
The Information about all the carts is then written to a remote CSV file which can be read in real-time by an excel sheet.

## How to install.

This only works for Microsoft Windows environments. Minor tweaks could be made to use the app in other environments,
namely replacing all the .bat and .vbs files with their respective counterparts.

Python 3.8 or later needs to be installed and added to Path, check the .bat files to make sure they work for your system.
This means perhaps changing "python" to "python3" or even "my/path/to/python".

Next the [requirements.txt](./requirements.txt) needs to be installed.

Inside the [config.ini](./config.ini) file, the Path to the aformentionted CSV file needs to be defined.

For this specific usecase we want the CSV file to be cleared every morning, which is why we have to setup a scheduled task to execute the [delete_data.bat](./delete_data.bat) file every day.

You can now create a shortcut to the [cart_tracker.vbs](./cart_tracker.vbs), which can be used to register new carts that are "done".

## How to use.

Click the shortcut you created, a window will pop up prompting you to enter one or more cart numbers separated by commas. An autocomplete dropdown menu will help you type the cartnames correctly. Use the Arrow and Return keys to navigate.

The second textfield asks you to provide a signature, type something like the first letters for your first and last name. It's to later on identify who loaded that cart.

After hitting return again you will be asked to confirm your entries. If you do so they will be saved in a specified CSV file where they can be read in real time by an Excel spreadsheet.

If you messed up and want to remove an entry you falsely entered, you can hit the "Korrektur" Button at the top left. This will open a new Page where you only have to enter the cart name you want to remove. This Textfield also has an autocomplete feature, only autocompleting to cartnames already in the entries. After hitting enter the CSV file will be updated.