import xlrd
import xlsxwriter
import math
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
FILE_NAME = ("3-16", "9-9", "15-19", "16-13", "20-13", "23-20",)
#  "20-13", "23-20", "29-13", "29-18", "32-18")

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
count = 0

while count < 10:
    string = ""
    string = str(result[count]) + "&"+str(result[count+10])+"&"+str(result[count+20]) + \
        "&"+str(result[count+30])+"&"+str(result[count+40]) + \
        "&"+str(result[count+50])
    count += 1
    print(string)
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
# plt.bar(b, c,  color='blue')
b = [3.43509, 3.02635, 3.40148, 1.84106, 1.17819, 1.09435, 1.16335, 1.05428, 0.80838, 0.77151, 1.92082, 1.22921, 2.29005, 2.39195, 2.01313, 1.53939, 1.39769, 1.12242, 1.0528, 1.0528, 1.86101, 1.20184, 0.16461, 0.16461, 0.80845, 0.60873, 0.62624, 0.66334, 0.66334,
     0.66334, 1.888, 1.47759, 0.85788, 1.30168, 1.24978, 1.20016, 1.29365, 1.3383, 1.38691, 1.38691, 2.42825, 2.44524, 2.50252, 2.53727, 2.16734, 1.91981, 1.9143, 1.9143, 2.117, 2.33516, 3.55854, 0.53349, 2.84736, 2.84736, 2.84736, 2.84736, 3.0616, 3.0616, 3.0616, 3.0616]
plt.plot(range(len(result)), result)
plt.axhline(y=1.002972, color='g', linestyle='-', label="Mean Error")
plt.axhline(y=0.2344, color='y', linestyle='-', label="Min Error")
plt.axhline(y=2.88633, color='r', linestyle='-', label="Max Error")
# plt.plot(range(len(b)), b, label="Trilatertion")
# plt.plot(h, label="Human")
# plt.plot(h, label="Human")
# plt.ylim(-80, 80)
plt.legend(bbox_to_anchor=(1.05, 1), loc='lower right')
print(sum(c))
plt.xlabel('Sample')
plt.ylabel('Sai số (m)')
plt.show()
