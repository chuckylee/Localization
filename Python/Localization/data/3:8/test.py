import xlrd
import xlsxwriter
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
FILE_NAME = ("10-8", "16-11", "20-8", "22-2", "29-8", "31-4")

workbook = xlsxwriter.Workbook("result.xlsx")
worksheet = workbook.add_worksheet()
# loc = ("6-8.xlsx")

# # To open Workbook
# wb = xlrd.open_workbook(loc)
# sheet = wb.sheet_by_index(0)

# # For row 0 and column 0
# print(sheet.cell_value(0, 1))
# print(sheet.nrows)
result = []
count = 1
count2 = 1
for i in range(len(FILE_NAME)):
    wb = xlrd.open_workbook(FILE_NAME[i] + ".xlsx")
    sheet = wb.sheet_by_index(0)
    # print(sheet.nrows)
    realLocation = []
    temp = ""
    for k in range(len(FILE_NAME[i])):
        if FILE_NAME[i][k] != "-":
            temp += FILE_NAME[i][k]
        elif FILE_NAME[i][k] == "-":
            realLocation.append(int(temp)*0.4)
            temp = ""
    realLocation.append(int(temp)*0.4)
    print(realLocation)
    worksheet.write('A'+str(count), "Test " + str(i))
    worksheet.write('A'+str(count+1), realLocation[0])
    worksheet.write('B'+str(count+1), realLocation[1])
    worksheet.write('H'+str(count2), realLocation[0])
    worksheet.write('I'+str(count2), realLocation[1])
    count2 += 1
    for j in range(sheet.nrows):
        # if math.sqrt(pow(realLocation[0]-sheet.cell_value(
        #         j, 0), 2)+pow(realLocation[1]-sheet.cell_value(j, 1), 2)) < 3:
        worksheet.write('D'+str(count), sheet.cell_value(j, 0))
        worksheet.write('E'+str(count), sheet.cell_value(j, 1))
        worksheet.write('G'+str(count), math.sqrt(pow(realLocation[0]-sheet.cell_value(
            j, 0), 2)+pow(realLocation[1]-sheet.cell_value(j, 1), 2)))
        result.append(round(math.sqrt(pow(realLocation[0]-sheet.cell_value(
            j, 0), 2)+pow(realLocation[1]-sheet.cell_value(j, 1), 2)), 5))
        count += 1
    count += 1
print("Save successful")
# print(len(FILE_NAME))
# print(result)
print(min(result))
print(max(result))
print(sum(result)/len(result))
# count = 0

# while count < 10:
#     string = ""
#     string = str(result[count]) + "&"+str(result[count+10])+"&"+str(result[count+20]) + \
#         "&"+str(result[count+30])+"&"+str(result[count+40]) + \
#         "&"+str(result[count+50])
#     count += 1
#     print(string)
# workbook.close()
count05 = 0
count1 = 0
count15 = 0
count2 = 0
count25 = 0
count3 = 0
count35 = 0
count4 = 0
count5 = 0
for i in range(len(result)):
    if result[i] < 0.5:
        count05 += 1
    elif 0.5 <= result[i] < 1:
        count1 += 1
    elif 1 <= result[i] < 1.5:
        count15 += 1
    elif 1.5 <= result[i] < 2:
        count2 += 1
    elif 2 <= result[i] < 2.5:
        count25 += 1
    elif 2.5 <= result[i] < 3:
        count3 += 1
    elif 3 <= result[i] < 3.5:
        count35 += 1
    elif 3.5 <= result[i] < 4:
        count4 += 1
    elif result[i] >= 4:
        count5 += 1
s = count05+count1+count15+count2+count25+count3+count35+count4+count5
print(count05+count1+count15+count2+count25+count3+count35+count4+count5)
b = ['0-0.5', '0.5-1', '1-1.5', '1.5-2', '2-2.5',
     '2.5-3', '3-3.5', '3.5-4', '4-4.5', '4.5-5', '5-5.5']
c = []
c.append((count05*100)/60)
c.append((count1*100)/60)
c.append((count15*100)/60)
c.append((count2*100)/60)
c.append((count25*100)/60)
c.append((count3*100)/60)
c.append((count35*100)/60)
c.append((count4*100)/60)
c.append((count5*100)/60)
c.append(0)
c.append(0)
plt.bar(b, c,  color='blue')
# plt.plot(range(len(c)), c)
# plt.plot(h, label="Human")
# plt.plot(h, label="Human")
# plt.ylim(-80, 80)
print(sum(c))
plt.xlabel('Sai số (m)')
plt.ylabel('Tỉ lệ (%)')
print(result)
# plt.show()
