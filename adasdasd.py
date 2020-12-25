from openpyxl import *
workbook  = load_workbook(filename="Data.xlsx")
sheet = workbook.active
itemID = 2
print("C"+str(sheet.max_row+1))
          
