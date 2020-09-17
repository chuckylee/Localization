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
nameTriangle = [['ESP32-1', 'ESP32-2', 'ESP32-3'], ['ESP32-4', 'ESP32-2', 'ESP32-3'], ['ESP32-5',
                                                                                       'ESP32-2', 'ESP32-4'], ['ESP32-4', 'ESP32-5', 'ESP32-6'], ['ESP32-5', 'ESP32-6', 'ESP32-7']]


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
        if data1[x] == "ESP32-1" or data1[x] == "ESP32-2" or data1[x] == "ESP32-3" or data1[x] == "ESP32-4" or data1[x] == "ESP32-5" or data1[x] == "ESP32-6" or data1[x] == "ESP32-7":
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


def calculateDistance():
    global NameESP, distanceValue, RSSfinal
    for x in range(len(NameESP)):
        with open('dataTrila.json') as json_file:
            data = json.load(json_file)
            for y in data:
                if NameESP[x] == y['name']:
                    distanceValue.append(
                        pow(10, (y['level']-float(RSSfinal[x]))/25))
    print('distanceValue: ' + str(distanceValue))


def defineTriangle():
    global nameTriangle, TriangleValue, TriangleChoosen, NameESP
    for i in range(len(nameTriangle)):
        TriangleValue.append(0)

    for i in range(len(nameTriangle)):
        for j in range(len(NameESP)):
            for k in range(len(nameTriangle[i])):
                if NameESP[j] == nameTriangle[i][k]:
                    TriangleValue[i] = TriangleValue[i] + distanceValue[j]
    # print(TriangleValue)
    for i in range(len(TriangleValue)):
        if TriangleValue[i] == min(TriangleValue):
            TriangleChoosen = i
    print('TriangleChoosen: ' + str(TriangleChoosen) +
          ' ' + str(nameTriangle[TriangleChoosen]))


def defineLocation():
    global nameTriangle, TriangleValue, TriangleChoosen, locationTrila, NameESP, distanceValue
    A = 0
    B = 0
    C = 0
    D = 0
    E = 0
    F = 0
    location = [[], [], []]
    distance = [0, 0, 0]
    for i in range(len(nameTriangle[TriangleChoosen])):
        with open('dataTrila.json') as json_file:
            data = json.load(json_file)
            for j in data:
                if nameTriangle[TriangleChoosen][i] == j['name']:
                    location[i].append(j['location_x'])
                    location[i].append(j['location_y'])
            for j in range(len(NameESP)):
                if nameTriangle[TriangleChoosen][i] == NameESP[j]:
                    distance[i] = distanceValue[j]
    print('loc: ' + str(location))
    print('dis: ' + str(distance))

    A = location[0][0] - location[1][0]
    B = location[0][1] - location[1][1]
    D = location[0][0] - location[2][0]
    E = location[0][1] - location[2][1]
    C = pow(distance[1], 2) - pow(distance[0], 2) + pow(location[0][0], 2) - \
        pow(location[1][0], 2) + pow(location[0]
                                     [1], 2) - pow(location[1][1], 2)
    F = pow(distance[2], 2) - pow(distance[0], 2) + pow(location[0][0], 2) -\
        pow(location[2][0], 2) + pow(location[0]
                                     [1], 2) - pow(location[2][1], 2)
    print('A: '+str(A))
    print('B: '+str(B))
    print('C: '+str(C))
    print('D: '+str(D))
    print('E: '+str(E))
    print('F: '+str(F))
    if A == 0:
        locationTrila[1] = C/(2*B)
        locationTrila[0] = (F-2*E*locationTrila[1])/(2*D)
    elif B == 0:
        locationTrila[0] = C/(2*A)
        locationTrila[1] = (F-2*D*locationTrila[0])/(2*E)
    elif D == 0:
        locationTrila[1] = F/(2*E)
        locationTrila[0] = (C-2*B*locationTrila[1])/(2*A)
    elif E == 0:
        locationTrila[0] = F/(2*D)
        locationTrila[1] = (C-2*A*locationTrila[0])/(2*B)
    else:
        locationTrila[1] = (A * F - D * C) / (2 * A * E - 2 * D * B)
        locationTrila[0] = (C - 2 * B * locationTrila[1]) / (2 * A)

    print('Location: ' + str(locationTrila))
    saveExcel(locationTrila[0], locationTrila[1])


count_ex = 1


def saveExcel(x, y):
    global count_ex, workbook, worksheet
    if count_ex == 1:
        print("Enter file name: ")
        name = input()
        workbook = xlsxwriter.Workbook(str(name) + ".xlsx")
        worksheet = workbook.add_worksheet()
        worksheet.write('A'+str(count_ex), x)
        worksheet.write('B'+str(count_ex), y)
    else:
        worksheet.write('A'+str(count_ex), x)
        worksheet.write('B'+str(count_ex), y)
    count_ex += 1


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


check = True
while check:
    while count < 10:
        result = subprocess.check_output(command, shell=True)
        config(result)
        print(datetime.datetime.now(), NameESP, RSSI)
        status = True
        for i in range(len(RSSI)):
            if len(RSSI[i]) == 0:
                status = False
                break
        if status:
            calculateRSS()
            calculateDistance()
            defineTriangle()
            defineLocation()
            cleanData()
            count += 1
    print("Save successful")
    workbook.close()
    count = 0
    check = False
    # i = input()
    # if str(i) == "y":
    #     check = True
    # else:
    #     print("Saved successful")
    #     check = False
    NameESP = []
    RSSI = []
