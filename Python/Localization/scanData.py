import subprocess
import datetime
import math
import json
import xlsxwriter
command = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport scan'
name = []
rssi = []
count = 0
NameESP = []
RSSI = []
sumRSS = []
yRSS = []
oRSS = []
RSS = []
RSSfinal = []

distanceValue = []
TriangleValue = []
TriangleChoosen = 0
locationTrila = [0, 0]
# nameTriangle = [['ESP32-1', 'ESP32-2', 'ESP32-3'], ['ESP32-4', 'ESP32-2', 'ESP32-3'], ['ESP32-5',
#                                                                                        'ESP32-2', 'ESP32-4'], ['ESP32-4', 'ESP32-5', 'ESP32-6'], ['ESP32-5', 'ESP32-6', 'ESP32-7']]

nameTriangle = [['ESP32-1', 'ESP32-2', 'ESP32-3']]


def config(string):
    global NameESP, RSSI
    name = []
    rssi = []
    data = []
    data1 = []
    value = ""
    string = string.decode()
    string = string.replace('\n', '')
    string = string.replace(' SSID', '')
    string = string.replace(' BSSID', '')
    string = string.replace(' RSSI', '')
    string = string.replace(' CHANNEL', '')
    string = string.replace(' HT', '')
    string = string.replace(' CC', '')
    string = string.replace(' SECURITY (auth/unicast/group)', '')
    string = string.replace('--', '')
    for x in range(len(string)):
        if string[x] != " ":
            value += string[x]
        else:
            # print(value)
            data.append(value)
            value = ""

    for x in range(len(data)):
        if len(data[x]) != 0:
            data1.append(data[x])
            print
    # print(data1)
    for x in range(len(data1)):
        if data1[x] == "ESP32-11" or data1[x] == "ESP32-2" or data1[x] == "ESP32-33" or data1[x] == "ESP32-4" or data1[x] == "ESP32-5" or data1[x] == "ESP32-6" or data1[x] == "ESP32-7":
            # if data1[x] == "ESP32-3":
            name.append(data1[x])
            rssi.append(int(data1[x+2]))

    if len(NameESP) == 0:
        for x in range(len(name)):
            NameESP.append(name[x])
            RSSI.append([])
            RSSI[x].append(rssi[x])
    else:
        for x in range(len(name)):
            status = True
            for y in range(len(NameESP)):
                if name[x] == NameESP[y]:
                    RSSI[y].append(rssi[x])
                    status = False
                    break
            if status:
                NameESP.append(name[x])
                RSSI.append([])
                RSSI[x].append(rssi[x])


def calculateRSS():
    global sumRSS, oRSS, yRSS, RSSfinal, RSS, RSSI, NameESP
    print(NameESP)
    print(RSSI)
    for x in range(len(NameESP)):
        if len(sumRSS) < len(NameESP):
            sumRSS.append(0)
            yRSS.append(0)
        for y in range(len(RSSI[x])):
            if sumRSS[x] == 0:
                sumRSS[x] = RSSI[x][y]
            else:
                sumRSS[x] = sumRSS[x] + RSSI[x][y]
        yRSS[x] = sumRSS[x]/len(RSSI[x])

    for x in range(len(NameESP)):
        if len(oRSS) < len(NameESP):
            oRSS.append(0)
        for y in range(len(RSSI[x])):
            if oRSS[x] == 0:
                oRSS[x] = (RSSI[x][y]-yRSS[x])*(RSSI[x][y]-yRSS[x])
            else:
                oRSS[x] = oRSS[x]+(RSSI[x][y]-yRSS[x]) * \
                    (RSSI[x][y]-yRSS[x])
        if len(RSSI[x]) != 1:
            oRSS[x] = math.sqrt(oRSS[x]/(len(RSSI[x])-1))

    for x in range(len(NameESP)):
        if len(RSS) < len(NameESP):
            RSS.append([0])
        for y in range(len(RSSI[x])):
            if RSSI[x][y] > yRSS[x]-oRSS[x] and RSSI[x][y] < yRSS[x]+oRSS[x]:
                if RSS[x][0] == 0:
                    RSS[x][0] = RSSI[x][y]
                else:
                    c = False
                    for k in range(len(RSS[x])):
                        if RSS[x][k] == RSSI[x][y]:
                            c = True
                            break
                    if c == False:
                        RSS[x].append(RSSI[x][y])
    for x in range(len(RSS)):
        if len(RSSfinal) < len(RSS):
            RSSfinal.append(0)
        for y in range(len(RSS[x])):
            if RSSfinal[x] == 0:
                RSSfinal[x] = RSS[x][y]
            else:
                RSSfinal[x] = RSSfinal[x] + RSS[x][y]
        RSSfinal[x] = RSSfinal[x]/len(RSS[x])

    for x in range(len(NameESP)):
        if oRSS[x] == 0 or len(RSSI[x]) == 1:
            RSSfinal[x] = RSSI[x][0]

    print("RSSfinal: ", RSSfinal)


def cleanData():
    global TriangleValue, locationTrila, TriangleChoosen, distanceValue, sumRSS, yRSS, oRSS, RSS, RSSfinal
    TriangleValue = []
    locationTrila = [0, 0]
    TriangleChoosen = 0
    distanceValue = []
    sumRSS = []
    yRSS = []
    oRSS = []
    RSS = []
    RSSfinal = []


count_ex = 1


def saveExcel(x, y):
    global count_ex, workbook, worksheet
    if count_ex == 1:
        print("Enter file name: ")
        name = input()
        workbook = xlsxwriter.Workbook("test.xlsx")
        worksheet = workbook.add_worksheet()
        worksheet.write('A'+str(count_ex), str(name))
        worksheet.write('B'+str(count_ex), x)
        worksheet.write('C'+str(count_ex), y)
        # worksheet.write('D'+str(count_ex), z)
        # worksheet.write('E'+str(count_ex), g)
        # worksheet.write('F'+str(count_ex), h)
        # worksheet.write('G'+str(count_ex), t)
    else:
        print("Enter file name: ")
        name = input()
        worksheet.write('A'+str(count_ex), str(name))
        worksheet.write('B'+str(count_ex), x)
        worksheet.write('C'+str(count_ex), y)
        # worksheet.write('D'+str(count_ex), z)
        # worksheet.write('E'+str(count_ex), g)
        # worksheet.write('F'+str(count_ex), h)
        # worksheet.write('G'+str(count_ex), t)
    count_ex += 1


check = True
while check:
    while count <= 10:
        result = subprocess.check_output(command, shell=True)
        config(result)
        print("------------------------------------------------")
        print(datetime.datetime.now(), NameESP, RSSI)
        status = True
        if count == 10:
            calculateRSS()
        count += 1
    saveExcel(NameESP[0],
              RSSfinal[0])
    print("Continue or not (y/n): ")
    x = input()
    if x == "y":
        count = 0

    elif x == "n":
        print("Save successful")
        workbook.close()
        # count = 0
        check = False
    NameESP = []
    RSSI = []
    cleanData()
