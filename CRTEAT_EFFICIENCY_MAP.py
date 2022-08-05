##   This script is used for generating the Efficiency MAP
##   Designer: Sylvain
##   email:jasonshake@163.com
##   Date: 10/27/2021

from openpyxl import load_workbook
import numpy as np
# import pandas as pd
import matplotlib.pyplot as plt


path = r'D:\SourceCode\NxxSy_RaceInverterR31b\Apsw\Calibration_Magelec_Motor\A03-N40S6 Inverter Software Calibration Tool_M21R5_Sylvain.xlsx'
sheet_name = 'Efficiency Map'
wb = load_workbook(filename= path, data_only= True)
sheet = wb[sheet_name]
SHEET = sheet['BI187:CF214']

data = SHEET
x = np.arange(-12000,12000,1000)
y = np.arange(-280,280,20)

X,Y = np.meshgrid(x,y)

j = len(SHEET[0])
i = len(SHEET)

raw_value= np.empty([i,j],dtype="float")
i = 0
j = 0
for col in sheet['E50:AB77']:
    for data in col:
        raw_value[i][j] = data.value
        j+=1
    i+=1
    j= 0

plt.contourf(X,Y,raw_value,70,alpha = 0.75)
C = plt.contour(X,Y,raw_value,levels =70,linewidths =0.5, colors='k')
plt.clabel(C,inline= True, fontsize = 5)
plt.show()

#         if data.value != None:
#             NumForALL+= 1
#             if data.value > 95:
#                 EFFGr95 += 1
#             if data.value > 90:
#                 EFFGr90 += 1
#             if data.value > 85:
#                 EFFGr85 += 1

# EFFGr95 = EFFGr95/NumForALL
# EFFGr90 = EFFGr90/NumForALL
# EFFGr85 = EFFGr85/NumForALL

# print(EFFGr85, EFFGr90, EFFGr95)