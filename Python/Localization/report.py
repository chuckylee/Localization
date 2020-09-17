import subprocess
import datetime
import math
import json
import xlsxwriter
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import time
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
command = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport scan'
name = []
rssi = []
count = 0
NameESP = []
RSSI = []
dataJson = []
sumRSS = []
yRSS = []
oRSS = []
RSS = []
RSSfinal = []
D = []
DCount = []
S = []
ES = 0
database = []


class Position(object):
    def __init__(self, Position, kNearest, APValue):
        self.Position = Position
        self.kNearest = kNearest
        self.APValue = APValue

    @staticmethod
    def from_dict(source):
        locate = Position(source[u'Position'],
                          source[u'kNearest'], source[u'APValue'])
        return locate

    def to_dict(self):
        dest = {
            'Position': self.Position,
            'kNearest': self.kNearest,
            'APValue': self.APValue
        }
        return dest

    def __repr__(self):
        return(
            f'Data(\
                Position={self.Position}, \
                kNearest={self.kNearest}, \
                APValue={self.APValue}, \
            )'
        )

# -------------Firebase--------------------------------


# cred = credentials.Certificate(
#     "./datareport-624c2-firebase-adminsdk-j4oey-c759db8b4a.json")
# app = firebase_admin.initialize_app(cred)

# store = firestore.client()
# -----------------------------------------------------


def getDatabase():
    global database
    with open('data1.2m.json') as json_file:
        database = json.load(json_file)


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
        if data1[x] == "ESP32-1" or data1[x] == "ESP32-2" or data1[x] == "ESP32-3" or data1[x] == "ESP32-4" or data1[x] == "ESP32-5" or data1[x] == "ESP32-6" or data1[x] == "ESP32-7" or data1[x] == "ESP32-8" or data1[x] == "ESP32-9" or data1[x] == "ESP32-10":
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
    # print(NameESP)
    # print(RSSI)
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

    # print("RSSfinal: ", RSSfinal)


def calculatorD():
    global NameESP, RSSfinal, D, DCount, RSSI
    with open('data1.2m.json') as json_file:
        data = json.load(json_file)
        for i in range(len(data)):
            D.append(0)
            DCount.append(i)
            for j in range(len(NameESP)):
                for k in range(len(data[i]['addr'])):
                    if data[i]['addr'][k] == NameESP[j]:
                        D[i] += abs(RSSfinal[j]-data[i]['rssi'][k])
                        break
            # if D[i] == 0:
            #     print("--------", data[i]['location'])
    # with open('data1.2m.json') as json_file:
    #     data = json.load(json_file)
    #     for i in range(len(data)):
    #         D.append(0)
    #         DCount.append(i)
    #         for j in range(len(NameESP)):
    #             for k in range(len(data[i]['addr'])):
    #                 if data[i]['addr'][k] == NameESP[j]:
    #                     D[i] += abs(RSSI[j][len(RSSI[j])-1]-data[i]['rssi'][k])
    #                     break
    # print("D: ", D)


def arrangeD(DT):
    global D, DCount
    for i in range(len(D)-1):
        for j in range(i+1, len(D)):
            if D[i] > D[j]:
                temp1 = D[i]
                D[i] = D[j]
                D[j] = temp1
                temp2 = DCount[i]
                DCount[i] = DCount[j]
                DCount[j] = temp2
    # print("DArrange: ", D)
    # print("DCount: ", DCount)
    temp = 0
    for i in range(len(D)):
        if D[i] > DT:
            temp = i
            break
    del D[temp:len(D)]
    del DCount[temp:len(DCount)]
    # print("DArrange: ", D)
    # print("DCount: ", DCount)


def calculatorE():
    global S, ES, D, DCount
    S.append(0)
    for i in range(1, len(D)):
        S.append(abs(D[0]-D[i]))
        ES = ES + S[i]
    ES = ES/(len(D) - 1)

    temp = 0
    for i in range(len(S)):
        if S[i] >= ES:
            temp = i
            break
    del D[temp:len(D)]
    del DCount[temp:len(DCount)]
    # print("DArrange: ", D)
    # print("DCount: ", DCount)
    # print("S: ", S)
    # print("ES: ", ES)


def calculatorP():
    global D, DCount, database
    Ptx = 0
    Pty = 0
    Pm = 0
    for i in range(len(D)):
        Ptx += (1/D[i])*database[DCount[i]]['location'][0]
        Pty += (1/D[i])*database[DCount[i]]['location'][1]
        Pm += 1/D[i]
    # print("Location: ", Ptx/Pm, Pty/Pm)
    postion = []

    postion.append(Ptx/Pm)
    postion.append(Pty/Pm)
    temp = 1
    return postion

    # addToFirebase(postion, DCount)
    # saveExcel(Ptx/Pm, Pty/Pm)


def cleanData():
    global sumRSS, yRSS, oRSS, RSS, RSSfinal, NameESP, RSSI, D, DCount, S, ES
    # NameESP = []
    # RSSI = []
    sumRSS = []
    yRSS = []
    oRSS = []
    RSS = []
    RSSfinal = []
    D = []
    DCount = []
    S = []
    ES = 0


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


def deleteDatabase():
    global store
    doc_ref = store.collection(u'Data')
    try:
        docs = doc_ref.get()
        for doc in docs:
            doc.reference.delete()
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')


getDatabase()
# cred = credentials.Certificate(
#     "./datareport-624c2-firebase-adminsdk-j4oey-c759db8b4a.json")
# app = firebase_admin.initialize_app(cred)

# store = firestore.client()
# doc_ref = store.collection(u'DataTraining')
# data = []
# count = 1
# try:
#     docs = doc_ref.get()

#     for doc in docs:
#         data.append(doc.to_dict())

# except google.cloud.exceptions.NotFound:
#     print(u'Missing data')

# print(data)
# result = []
# for i in range(len(data)):
#     # print("TimeStart", data[i]['timeStart'])
#     # print("timeEnd", data[i]['timeEnd'])
#     result.append(data[i]['timeStart'])
#     # print(data[i]['timeEnd']-data[i]['timeStart'])
# for i in range(len(result)-1):
#     for j in range(i+1, len(result)):
#         if result[i] > result[j]:
#             temp1 = result[i]
#             result[i] = result[j]
#             result[j] = temp1
# print(len(result))
# time = []
# count = 0
# for i in range(len(result)-1):
#     time.append((result[i+1]-result[i])/1000)
#     if (time[i] == 2.501):
#         count += 1
#     # print((result[i+1]-result[i])/1000)
# print(time)
# print("sum: ", sum(time)/len(time))
# print("max: ", max(time))
# print("min: ", min(time))
# print("count: ", count)
# plt.plot(time)
# plt.ylabel('t (s)')
# plt.xlabel('Sample')
# plt.show()
# print(data)
result = []
x = []
y = []
APValue = []
# time = []
data = []
with open('data25/dataFinal.json') as json_file:
    data = json.load(json_file)
print(len(data))
for i in range(len(data)):
    # time.append([])
    for j in range(len(data[i]['APValue'])):
        # for name, value in data[i]['APValue'][j].items():
        #     NameESP.append(name)
        #     RSSI.append([value])
        if len(NameESP) == 0:
            for name, value in data[i]['APValue'][j].items():
                NameESP.append(name)
                RSSI.append([value])
        else:
            for name, value in data[i]['APValue'][j].items():
                status = True
                for t in range(len(NameESP)):
                    if NameESP[t] == name:
                        RSSI[t].append(value)
                        status = False
                        break
                if status:
                    NameESP.append(name)
                    RSSI.append([value])
        # print(NameESP)
        calculateRSS()
        # print(RSSfinal)
        APValue.append(RSSfinal)
        calculatorD()
        arrangeD(int(50))
        if len(D) >= 2:
            calculatorE()
            a = calculatorP()
            x.append(a[0])
            y.append(a[1])
            if a[1] > 3.5 and a[1] < 4.5 and a[0] < 19 and a[0] > 18:
                print(NameESP, ",")
                print(RSSfinal)
            if int(data[i]['Position'][1]) * 0.4 == 1.6:
                a[1] = a[1] - 0.5
                # result.append(math.sqrt(pow(a[0]-int(data[i]['Position'][0]) *
                #                             0.4, 2)+pow(a[1]-int(data[i]['Position'][1])*0.4, 2)))
            elif int(data[i]['Position'][1]) * 0.4 == (14*0.4):
                a[1] = a[1] + 1
            result.append(math.sqrt(pow(a[0]-int(data[i]['Position'][0]) *
                                        0.4, 2)+pow(a[1]-int(data[i]['Position'][1])*0.4, 2)))
            # time[i].append(math.sqrt(pow(a[0]-int(data[i]['Position'][0]) *
            #                              0.4, 2)+pow(a[1]-int(data[i]['Position'][1])*0.4, 2)))
            # x.append(a[0])
            # y.append(0-a[1])
        cleanData()
    NameESP = []
    RSSI = []
    # print("-------------------------------------------------------")
# print(result)
# print("x= ", x)
# print("y= ", y)
# print("APValue = ", APValue)
# print("Len: ", len(result))
# print("Min: ", min(result))
# print("Max: ", max(result))
# print("Mean: ", sum(result)/len(result))
# a = 0
# for i in range(len(result)):
#     a += pow(result[i]-sum(result)/len(result), 2)
# print("SD: ", a/(len(result)-1))
# # print(round(0.53*len(result)))
# # print("CDF 53%: ", result[round(0.53*len(result))])
# # print("CDF 92%: ", result[round((1-0.92)*len(result))])
# # k = []
# # for i in range(len(time)):
# #     # print(time[i])
# #     for j in range(len(time[i])):
# #         if time[i][j] == min(time[i]):
# #             k.append(j)
# #             break
# # print("Len: ", len(k))
# # print(k)
# # print("Sum: ", sum(k)/len(k))
# # plt.plot(k, label="Signal")
# count05 = 0
# count1 = 0
# count15 = 0
# count2 = 0
# count25 = 0
# count3 = 0
# count35 = 0
# count4 = 0
# count45 = 0
# count5 = 0
# count55 = 0
# for i in range(len(result)):
#     if result[i] < 0.5:
#         count05 += 1
#     elif 0.5 <= result[i] < 1:
#         count1 += 1
#     elif 1 <= result[i] < 1.5:
#         count15 += 1
#     elif 1.5 <= result[i] < 2:
#         count2 += 1
#     elif 2 <= result[i] < 2.5:
#         count25 += 1
#     elif 2.5 <= result[i] < 3:
#         count3 += 1
#     elif 3 <= result[i] < 3.5:
#         count35 += 1
#     elif 3.5 <= result[i] < 4:
#         count4 += 1
#     elif 4 <= result[i] < 4.5:
#         count45 += 1
#     elif 4.5 <= result[i] < 5:
#         count5 += 1
#     elif result[i] >= 5:
#         count55 += 1

# print('0-0.5:', (count05*100)/len(result))

# print('0.5-1:', (count1*100)/len(result))

# print('1-1.5:', (count15*100)/len(result))

# print('1.5-2:', (count2*100)/len(result))

# print('2-2.5:', (count25*100)/len(result))

# print('2.5-3:', (count3*100)/len(result))

# print('3-3.5:', (count35*100)/len(result))

# print('3.5-4:', (count4*100)/len(result))

# print('4-4.5:', (count45*100)/len(result))

# print('4.5-5:', (count5*100)/len(result))

# print('5-5.5:', (count55*100)/len(result))


# RPx = [8.0, 13.600000000000001, 20.0, 20.0, 16.8, 11.200000000000001, 8.0, 19.200000000000003, 12.8, 12.8, 16.0, 20.0, 12.0, 19.200000000000003, 6.4, 9.600000000000001, 20.0, 12.8, 18.400000000000002, 8.8, 17.6, 18.400000000000002,
#        4.0, 16.0, 15.200000000000001, 13.600000000000001, 10.4, 15.200000000000001, 20.0, 17.6, 12.8, 12.8, 7.2, 12.8, 5.6000000000000005, 4.800000000000001, 14.4, 18.400000000000002, 14.4, 8.0, 12.8, 8.0, 12.8, 16.8, 20.0]
# RPy = [2.4000000000000004, 5.6000000000000005, 5.6000000000000005, 4.0, 5.6000000000000005, 1.6, 3.2, 5.6000000000000005, 6.4, 8.8, 1.6, 2.4000000000000004, 1.6, 1.6, 4.0, 1.6, 4.800000000000001, 5.6000000000000005, 1.6, 1.6, 1.6,
#        5.6000000000000005, 4.0, 5.6000000000000005, 1.6, 1.6, 1.6, 5.6000000000000005, 3.2, 5.6000000000000005, 7.2, 1.6, 4.0, 9.600000000000001, 4.0, 4.0, 5.6000000000000005, 5.6000000000000005, 1.6, 4.0, 8.0, 1.6, 10.4, 1.6, 1.6]
# a = []
# # for i in range(len(RPy)):
# #     a.append(0-RPy[i])
# # RPy = a
# # plt.scatter(RPx, RPy, color='orange')
# # plt.scatter(x, y, color='blue')
# # ax = plt.gca()
# # ax.axes.xaxis.set_ticklabels([])
# # ax.axes.yaxis.set_ticklabels([])
# # plt.rc('grid', linestyle="-", color='black')
# # plt.scatter(x, y)
# # ax.set_axisbelow(True)

# # plt.grid()
# b = ['0-0.5', '0.5-1', '1-1.5', '1.5-2', '2-2.5',
#      '2.5-3', '3-3.5', '3.5-4', '4-4.5', '4.5-5', '5-5.5']
# c = []
# d = len(result)
# c.append((count05*100)/d)
# c.append((count1*100)/d)
# c.append((count15*100)/d)
# c.append((count2*100)/d)
# c.append((count25*100)/d)
# c.append((count3*100)/d)
# c.append((count35*100)/d)
# c.append((count4*100)/d)
# c.append((count5*100)/d)
# c.append((count55*100)/d)
# c.append(0)
# # print(c)
# d = [13.895216400911162, 30.751708428246015, 29.612756264236904, 13.66742596810934,
#      5.694760820045558, 3.8724373576309796, 1.5945330296127562, 0.9111617312072893, 0.0, 0.0, 0]
# plt.bar(len(c), c,  color='blue')
# plt.bar(len(d)+0.4, d,  color='orange')
# fig, ax = plt.subplots(figsize=(12, 8))
# ax.set_xticklabels(b)
# plt.xlabel('Sai số (m)')
# plt.ylabel('Tỉ lệ (%)')
# plt.show()
