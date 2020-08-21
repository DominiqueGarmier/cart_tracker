# [cart_tracker](https://github.com/dominiquegarmier/cart_tracker)
by [Dominique Garmier](https://github.com/dominiquegarmier) (c) 2020

## readme für [Kantonsspital Aarau](https://www.ksa.ch/)

Dies ist die Anleitung für die Installation von [cart_tracker](https://github.com/dominiquegarmier/cart_tracker) spezifisch für die Anwendung am KSA. Bevor wir beignnen sollte das allgemeine [README.md](./README.md) durchgelesen und studiert werden.

## Installation

Das Programm wurde im Root-Verzeichnis ````C:\User\ksawaeschever\AppData\Roaming\cart_tracker```` installiert. Die [config.ini](./config.ini)-Datei wurde wie folgt gespeichert:
````
[DEFAULT]
data_path = U:/ksakleider/WagenTracker/data.csv
debug = False

[ExcelToPdf]
pdf_folder_path = U:/ksakleider/WagenTracker/Tagesabschluss/
excel_file_path = U:/ksakleider/WagenTracker/Touren-1-2-Sauberwagen.xlsx
excel_sheets = [1, 2]
pdf_names = ['Tour-1', 'Tour-2']
````

## git Repository

Da ````git```` ebenfalls installiert wurde kann das Programm dirket vom [GitHub-Repo](https://github.com/dominiquegarmier/cart_tracker) mit ````git pull```` aktuallisiert werden, sofern eine neuere Version vorliegt. Für externe Weiterentwicklung kann das Repository mit ````git fork```` abgespalten und gemäss der [Lizenz](./LICENSE) weiterentwickelt werden.

## Excel-Anknüpfung

Die *.xlsx- und *.csv-Datei wurde auf dem NAS unter dem Pfad ````U:\ksakleider\WagenTracker```` gespeichert. Die Ordnerstruktur ist wie folg:
```
...\WagenTracker
    │   Touren-1-2-Sauberwagen.xlsx
    │   data.csv
    │
    └───Tagesabschluss
       |
       └───19-08-20
       |   │   Tour-1.pdf
       |   └───Tour-2.pdf
       |
       | ...
  
```
Damit in der *.xlsx-Datei die Angaben immer aktuell sind wurde data.csv als live "Data Source" Verknüpft.

Im unterordner ````Tagesabschluss```` wird jeden Tag einen neuen Ordner erstellt mit dem jeweiligen Datum als Name, welcher zwei *.pdf-Dateien enthält. Diese beiden Dateien zeigen den Endzustand der *.xlsx-Datei am Ende des Tages.

## Windows-Task-Scheduler

Damit die data.csv-Datei jeden Tag richtig zurückgesetzt wird, wurde eine Windows-Aufgabe geplant, welche jeden Morgen um 6 Uhr die [daily_task.bat](./daily_task.bat) ausführt. Diese Datei speichert zuerst die *.xlsx-Datei als *.pdf ab und löscht schliesslich die Einträge in der *.csv-Datei. 
