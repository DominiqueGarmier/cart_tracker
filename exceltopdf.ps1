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
$sheetnumbers = 1,2
$sheetnames = "Tour-1", "Tour-2"
$inds = 1, 2

function Select-Nth {
    param([int]$N) 

    $Input | Select-Object -First $N | Select-Object -Last 1
}


<#
here you need to specify the paths to the excelfile, and the outputfolder where it will create a subfolder everyday.
#>
$excelfilepath = "C:\Users\Domig\Desktop\excel file save test\excelfiles\Touren Suaberwagen New.xlsx"
$outputfolder = "C:\Users\Domig\Desktop\excel file save test\excelfiles\"

$workbook = $objExcel.workbooks.open($excelfilepath, 3)
$workbook.Saved = $true
$datetimestr = Get-Date -Format "dd-MM-yyyy"

$temp = $outputfolder + $datetimestr
New-Item -Path $temp -ItemType Directory

$outputpath = $outputfolder + $datetimestr + "\"


foreach($ind in $inds)
{
 $temp = $sheetnames | Select-Nth $ind
 $pdfpath = $outputpath + $temp + ".pdf"
 
 $temp = $sheetnumbers | Select-Nth $ind
 $worksheet = $workbook.Worksheets($temp)
 $worksheet.PageSetup.Zoom = $false
 $worksheet.ExportAsFixedFormat($xlFixedFormat::xlTypePDF, $pdfpath, $xlQualityStandard, $true, $true)
 
}

$objExcel.Workbooks.close()
$objExcel.Quit()