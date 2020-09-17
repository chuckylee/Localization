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
        if data1[x] == "ESP32-1" or data1[x] == "ESP32-2" or data1[x] == "ESP32-3":
            # or data1[x] == "ESP32-4" or data1[x] == "ESP32-5" or data1[x] == "ESP32-6" or data1[x] == "ESP32-7":
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


def calculateDistance():
    global NameESP, distanceValue, RSSfinal, RSSI
    # for x in range(len(NameESP)):
    #     with open('dataTrila.json') as json_file:
    #         data = json.load(json_file)
    #         for y in data:
    #             if NameESP[x] == y['name']:
    #                 distanceValue.append(
    #                     pow(10, (y['level']-RSSI[x][len(RSSI[x])-1])/23))
    for x in range(len(NameESP)):
        with open('dataTrila.json') as json_file:
            data = json.load(json_file)
            n = 25
            for y in data:
                if NameESP[x] == y['name']:
                    if RSSfinal[x] <= -65:
                        n = 30
                    else:
                        n = 25
                    distanceValue.append(
                        pow(10, (-40-float(RSSfinal[x]))/n))
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
    location = [[], [], []]
    AP = []
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

    for i in range(len(location)):
        AP.append(location[i][0])
    print('loc: ' + str(location))
    print('AP: ', AP)
    print('dis: ' + str(distance))
    x_measure = []

    for i in range(3):
        if i < 2:
            x_measure.append((pow(distance[i], 2)-pow(distance[i+1], 2) -
                              pow(AP[i], 2) + pow(AP[i+1], 2))/(2*(AP[i+1]-AP[i])))
        else:
            x_measure.append((pow(distance[i], 2)-pow(distance[i-2], 2) -
                              pow(AP[i], 2) + pow(AP[i-2], 2))/(2*(AP[i-2]-AP[i])))

    print("x_measure: ", x_measure)

    check = True
    for i in range(len(x_measure)-1):
        if x_measure[i] != x_measure[i+1]:
            check = False
            break
    if check:
        print('Best distance')
        locationTrila[0] = x_measure[0]
        locationTrila[1] = math.sqrt(
            pow(distance[0], 2)-pow(x_measure[0]-AP[0], 2))
        # print(x_measure[0], math.sqrt(
        #     pow(distance[0], 2)-pow(x_measure[0]-AP[0], 2)))
    else:
        y_measure = []
        for i in range(len(x_measure)):
            y_measure.append(pow(distance[i], 2)-pow(x_measure[i]-AP[i], 2))
        print(y_measure)
        temp_x = 0
        temp_y = 0
        count = 0
        for i in range(len(y_measure)):
            if y_measure[i] > 0:
                temp_x += x_measure[i]
                temp_y += math.sqrt(y_measure[i])
                count += 1
        if count == 3:
            locationTrila[0] = temp_x/3
            # locationTrila[1] = temp_y/3
            locationTrila[1] = math.sqrt(abs(pow(temp_y/3, 2)-pow(1, 2)))
        elif count == 2:
            locationTrila[0] = temp_x/2
            # locationTrila[1] = temp_y/2
            locationTrila[1] = math.sqrt(abs(pow(temp_y/2, 2)-pow(1, 2)))
        elif count == 1:
            locationTrila[0] = temp_x
            # locationTrila[1] = temp_y
            locationTrila[1] = math.sqrt(abs(pow(temp_y, 2)-pow(1, 2)))
        else:
            locationTrila[0] = 0
            locationTrila[1] = 0
        # locationTrila[1] = math.sqrt(abs(pow(temp_y/3, 2)-pow(2-1, 2)))
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
        print("------------------------------------------------")
        print(datetime.datetime.now(), NameESP, RSSI)
        status = True
        for i in range(len(RSSI)):
            if len(RSSI[i]) == 0:
                status = False
                break
        if status and len(NameESP) >= 3:
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
    NameESP = []
    RSSI = []
