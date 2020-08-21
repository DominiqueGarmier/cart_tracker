
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------
# cart tracker (c) 2020 Dominique F. Garmier MIT licence
#-------------------------------------------------------

'''
script to export excel file as pdf
'''

# standard library imports
import os
import subprocess

# local imports
import main

def get_strings(sheet_numbers, sheet_names):

    sheet_numbers_str = ''
    for number in sheet_numbers:
        sheet_numbers_str += str(number) + ', '

    sheet_numbers_str = sheet_numbers_str[:-2]

    sheet_names_str = ''
    for name in sheet_names:
        sheet_names_str +='"' + name + '"' + ', '

    sheet_names_str = sheet_names_str[:-2]

    inds = ''
    for ind in range(len(sheet_numbers)):
        inds += str(ind + 1) + ', '

    inds = inds[:-2]

    return sheet_numbers_str, sheet_names_str, inds

def get_path(file_path, folder_path):

    file_path = file_path.replace('/', '\\')
    folder_path = folder_path.replace('/', '\\')

    return file_path, folder_path

if __name__ == '__main__':
    sheet_numbers = main.excel_sheets
    sheet_names = main.pdf_names
    file_path = main.excel_file_path
    folder_path =  main.pdf_folder_path


    sheet_numbers, sheet_names, inds = get_strings(sheet_numbers, sheet_names)
    file_path, folder_path = get_path(file_path, folder_path)

    cmd = '''
    $xlFixedFormat = "Microsoft.Office.Interop.Excel.xlFixedFormatType" -as [type]
    $xlQualityStandard = "Microsoft.Office.Interop.Excel.xlQualityStandard" -as [type]
    $excelFiles = Get-ChildItem -Path $path -include *.xls, *.xlsx -recurse
    $objExcel = New-Object -ComObject excel.application
    $objExcel.visible = $false

    <#
    here you need to specify which sheets of the excel sheet you want to save each day
    aswell as the names they should have once saved
    you also need to provide a list of indices so starting from 1,.... to however many sheets you want to save

    example:

    you might wanna save sheets 1,3,4,5 from you excel sheet:

    $sheetnumbers = 1,3,4,5
    $sheetnames = "mynameforsheet1", ... , "mynameforsheet2"
    $inds = 1, 2, 3, 4  <--- Note that this is still just 1-4
    #>
    $sheetnumbers = {sheet_numbers}
    $sheetnames = {sheet_names}
    $inds = {inds}

    function Select-Nth {{
        param([int]$N) 

        $Input | Select-Object -First $N | Select-Object -Last 1
    }}


    <#
    here you need to specify the paths to the excelfile, and the outputfolder where it will create a subfolder everyday.
    #>
    $excelfilepath = "{file_path}"
    $outputfolder = "{folder_path}"

    $workbook = $objExcel.workbooks.open($excelfilepath, 3)
    $workbook.Saved = $true
    $datetimestr = (get-date (get-date).addDays(-1) -UFormat "%d-%m-%y")

    $temp = $outputfolder + $datetimestr
    New-Item -Path $temp -ItemType Directory

    $outputpath = $outputfolder + $datetimestr + "\\"


    foreach($ind in $inds)
    {{

    $temp = $sheetnames | Select-Nth $ind
    $pdfpath = $outputpath + $temp + ".pdf"
    
    $temp = $sheetnumbers | Select-Nth $ind
    $worksheet = $workbook.Worksheets($temp)
    $worksheet.PageSetup.Zoom = $false
    $worksheet.ExportAsFixedFormat($xlFixedFormat::xlTypePDF, $pdfpath, $xlQualityStandard, $true, $true)
    
    }}

    $objExcel.Workbooks.close()
    $objExcel.Quit()
    '''.format(
        sheet_names=sheet_names,
        sheet_numbers=sheet_numbers,
        inds=inds,
        file_path=file_path,
        folder_path=folder_path
    )

    # create temprorary ps script file
    with open('./temp.ps1', 'w+') as f:
        f.write(cmd)

    try:
        script_path = os.path.abspath('./temp.ps1')
        subprocess.call('Powershell -Command {}'.format(script_path))

    except:
        print('F')

    os.remove('./temp.ps1')