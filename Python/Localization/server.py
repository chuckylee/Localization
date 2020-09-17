import subprocess
import datetime
import math
import json
import xlsxwriter
import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import time
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
        if S[i] > ES:
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
    print("Location: ", Ptx/Pm, Pty/Pm)
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


# def addToFirebase(position, kNearest):
#     APValue = {}
#     for i in range(len(NameESP)):
#         APValue['AP'+str(NameESP[i][6])] = RSSI[i][len(RSSI[i])-1]
#     locate = Position(Position=position, kNearest=kNearest, APValue=APValue)
#     store.collection(u'Data').document().set(locate.to_dict())


# deleteDatabase()
getDatabase()
# check = True
# while check:
#     print("---------------------------------------")
#     print('Chon nguong gia tri D: ')
#     # x = input()
#     while count < 1000:
#         result = subprocess.check_output(command, shell=True)
#         config(result)
#         print(datetime.datetime.now(), NameESP, RSSI)
#         status = True
#         for i in range(len(RSSI)):
#             if len(RSSI[i]) == 0:
#                 status = False
#                 break
#         if status and len(NameESP) >= 4:
#             calculateRSS()
#             calculatorD()
#             arrangeD(int(40))
#             if len(D) >= 3:
#                 calculatorE()
#                 calculatorP()
#                 count += 1
#             cleanData()
#             print("----------------------------------")
#         # addToFirebase([0, 0], [])
#     check = False
#     print("Save successful")
#     # workbook.close()
#     NameESP = []
#     RSSI = []
NameESP = ["ESP32-9",
           "ESP32-2",
           "ESP32-1",
           "ESP32-8",
           "ESP32-7",
           "ESP32-6",
           "ESP32-3",
           "ESP32-4",
           "ESP32-5"]
RSSI = [[-49.5], [-49], [-52.5], [-66], [-56],
        [-52.5], [-57.666666666666664], [-61], [-60]]
calculateRSS()
calculatorD()
arrangeD(int(50))
calculatorE()
calculatorP()
cleanData()

# NameESP = ["ESP32-9",
#            "ESP32-2",
#            "ESP32-1",
#            "ESP32-8",
#            "ESP32-7",
#            "ESP32-6",
#            "ESP32-3",
#            "ESP32-4",
#            "ESP32-5"]
# RSSI = [[-49.5], [-49, -57], [-52.5], [-66], [-56, -51],
#         [-52.5, -64], [-57.666666666666664, -69], [-61, -76], [-60, -65]]
NameESP = ["ESP32-2", "ESP32-4",
           "ESP32-5", "ESP32-3", "ESP32-6", "ESP32-7"]
RSSI = [[-57], [-76], [-65], [-69], [-64], [-51]]
calculateRSS()
calculatorD()
arrangeD(int(50))
calculatorE()
calculatorP()
cleanData()
# cred = credentials.Certificate(
#     "./datareport-624c2-firebase-adminsdk-j4oey-c759db8b4a.json")
# app = firebase_admin.initialize_app(cred)

# store = firestore.client()
# doc_ref = store.collection(u'Data')
# data = []
# count = 1
# # store.collection(u'cities').document().set(data1)
# try:
#     docs = doc_ref.get()

#     for doc in docs:
#         data.append(doc.to_dict())

# except google.cloud.exceptions.NotFound:
#     print(u'Missing data')

# # print('Leght:', len(data))
# # for i in range(len(data)):
# #     if data[i]['id'] == "Floor8.v2":
# #         for j in range(len(data[i]['data'])):
# #             print(int(data[i]['data'][j]['location'][1])*0.4)
# # print(data)
# reuslt = []
# x = []
# y = []
# for i in range(len(data)):
#     #     # reuslt.append(int(data[i]['Position'][0])*0.4)
#     #     print(int(data[i]['Position'][0])*0.4)
#     # print(reuslt)
#     for j in range(len(data[i]['APValue'])):
#         for name, value in data[i]['APValue'][j].items():
#             NameESP.append(name)
#             RSSI.append([value])
#         # if len(NameESP) == 0:
#         #     for name, value in data[i]['APValue'][j].items():
#         #         NameESP.append(name)
#         #         RSSI.append([value])
#         # else:
#         #     for name, value in data[i]['APValue'][j].items():
#         #         status = True
#         #         for t in range(len(NameESP)):
#         #             if NameESP[t] == name:
#         #                 RSSI[t].append(value)
#         #                 status = False
#         #                 break
#         #         if status:
#         #             NameESP.append(name)
#         #             RSSI.append([value])
#         # print(NameESP)
#         # print(RSSI)
#         calculateRSS()
#         calculatorD()
#         arrangeD(int(40))
#         if len(D) >= 3:
#             calculatorE()
#             a = calculatorP()
#             # print("1: ", a[1])
#             if int(data[i]['Position'][1]) * 0.4 == 1.6:
#                 a[1] = a[1] - 0.4
#                 # print("2: ", a[1])
#             elif int(data[i]['Position'][1]) * 0.4 == (14*0.4):
#                 a[1] = a[1] + 0.8
#                 # print("3: ", a[1])
#             reuslt.append(math.sqrt(pow(a[0]-int(data[i]['Position'][0]) *
#                                         0.4, 2)+pow(a[1]-int(data[i]['Position'][1])*0.4, 2)))
#             x.append(a[0])
#             y.append(0-a[1])
#         cleanData()
#         NameESP = []
#         RSSI = []
#     print("-------------------------------------------------------")
# print(reuslt)
# # print("Len: ", len(reuslt))
# # print("Min: ", min(reuslt))
# # print("Max: ", max(reuslt))
# # print("Mean: ", sum(reuslt)/len(reuslt))
# # a = 0
# # for i in range(len(reuslt)):
# #     a += pow(reuslt[i]-sum(reuslt)/len(reuslt), 2)
# # print("SD: ", a/(len(reuslt)-1))
# print("x= ", x)
# print("y= ", y)
