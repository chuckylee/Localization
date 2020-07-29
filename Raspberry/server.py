from __future__ import print_function

from time import gmtime, strftime, sleep
from bluepy.btle import Scanner, DefaultDelegate, BTLEException
import sys
import datetime
import time 
import math
import json
import xlsxwriter

count = 1
addr = []
rssi = []
sumRSS = []
yRSS = []
oRSS = []
RSS = []
RSSfinal = []
dataJson = []
D = []
DCount = []
S = []
ES = 0
database = []
class ScanDelegate(DefaultDelegate):
    def handleDiscovery(self, dev, isNewDev, isNewData):
        global count, database
        if "24:6f:28:25:f7:5a" == str(dev.addr) or "24:6f:28:27:48:6a" == str(dev.addr) or "24:6f:28:2b:60:32" == str(dev.addr) or "24:6f:28:24:71:d6" == str(dev.addr) or "24:6f:28:25:da:b2" == str(dev.addr) or "24:6f:28:24:81:de" == str(dev.addr) or "24:6f:28:24:d6:26" == str(dev.addr) or "24:6f:28:24:86:2a" == str(dev.addr):
            print(count, datetime.datetime.now(), dev.addr, dev.rssi)
            configData(dev.addr,dev.rssi)
            count += 1
        sys.stdout.flush()

def getDatabase():
    global database
    with open('data.json') as json_file:
        database = json.load(json_file)

def configData(devAddr, devRssi):
    global addr,rssi,count
    if len(addr) == 0:
        addr.append(devAddr)
        rssi.append([])
        rssi[0].append(devRssi)
    else:
        check = True
        for x in range(len(addr)):
            if addr[x] == devAddr:
                rssi[x].append(devRssi)
                check = False
                break
        if check:
            addr.append(devAddr)
            rssi.append([])
            rssi[len(addr)-1].append(devRssi)

def cleanData():
    global addr,rssi, sumRSS, yRSS, oRSS, RSS, RSSfinal, D, DCount, S, ES
    addr = []
    rssi = []
    sumRSS = []
    yRSS = []
    oRSS = []
    RSS = []
    RSSfinal = []
    D = []
    DCount = []
    S = []
    ES = 0

def caculatorRSS():
    global sumRSS, oRSS, yRSS, RSSfinal, RSS, count, rssi, addr, RSSfinalList 
    print(addr)
    print(rssi)
    for x in range(len(addr)):
        if len(sumRSS) < len(addr):
            sumRSS.append(0)
            yRSS.append(0)
        for y in range(len(rssi[x])):
            if sumRSS[x] == 0:
                sumRSS[x] = rssi[x][y]
            else:
                sumRSS[x] = sumRSS[x] + rssi[x][y]
        yRSS[x] = sumRSS[x]/len(rssi[x])

    for x in range(len(addr)):
        if len(oRSS) < len(addr):
            oRSS.append(0)
        for y in range(len(rssi[x])):
            if oRSS[x] == 0:
                oRSS[x] = (rssi[x][y]-yRSS[x])*(rssi[x][y]-yRSS[x])
            else:
                oRSS[x] = oRSS[x]+(rssi[x][y]-yRSS[x]) * \
                    (rssi[x][y]-yRSS[x])
        if len(rssi[x]) != 1:
            oRSS[x] = math.sqrt(oRSS[x]/(len(rssi[x])-1))

    for x in range(len(addr)):
        if len(RSS) < len(addr):
            RSS.append([0])
        for y in range(len(rssi[x])):
            if rssi[x][y] > yRSS[x]-oRSS[x] and rssi[x][y] < yRSS[x]+oRSS[x]:
                if RSS[x][0] == 0:
                    RSS[x][0] = rssi[x][y]
                else:
                    c = False
                    for k in range(len(RSS[x])):
                        if RSS[x][k] == rssi[x][y]:
                            c = True
                            break
                    if c == False:
                        RSS[x].append(rssi[x][y])
    for x in range(len(RSS)):
        if len(RSSfinal) < len(RSS):
            RSSfinal.append(0)
        for y in range(len(RSS[x])):
            if RSSfinal[x] == 0:
                RSSfinal[x] = RSS[x][y]
            else:
                RSSfinal[x] = RSSfinal[x] + RSS[x][y]
        RSSfinal[x] = RSSfinal[x]/len(RSS[x])

    for x in range(len(addr)):
        if oRSS[x] == 0 or len(rssi[x]) == 1:
            RSSfinal[x] = rssi[x][0]

    print("RSSfinal: ",RSSfinal)

def calculatorD():
    global addr, RSSfinal, D, DCount
    with open('data.json') as json_file:
        data = json.load(json_file)
        for i in range(len(data)):
            D.append(0)
            DCount.append(i)
            for j in range(len(addr)):
                for k in range(len(data[i]['addr'])) :
                    if data[i]['addr'][k] == addr[j]:
                        # if len(D[i]) == Null:
                        #     D.append(abs(RSSfinal[j]-data[i]['rssi'][k]))
                        #     # print(D)
                        # else:
                            D[i] = D[i] + abs(RSSfinal[j]-data[i]['rssi'][k])
                            # print(D)
    print("D: ",D)

def arrangeD():
    global D, DCount
    for i in range(len(D)-1):
        for j in range(i+1,len(D)):
            if D[i] > D[j]:
                temp1 = D[i]
                D[i] = D[j]
                D[j] = temp1
                temp2 = DCount[i]
                DCount[i] = DCount[j]
                DCount[j] = temp2
    print("DArrange: ",D)
    print("DCount: ",DCount)

def calculatorE():
    global S, ES, D
    S.append(0)
    for i in range(1,len(D)):
        S.append(D[0]-D[i])
        ES = ES + S[i]
        print("1: ", ES)
    ES = ES/(len(D) - 1)
    print("S: ",S)
    print("ES: ",ES)

def calculatorP(kNeareast):
    global D, DCount, database
    Ptx = 0
    Pty = 0
    Pm = 0
    for i in range(kNeareast):
        Ptx += (1/D[i])*database[DCount[i]]['location'][0]
        Pty += (1/D[i])*database[DCount[i]]['location'][1]
        Pm += 1/D[i]
    print("Location: ",Ptx/Pm,Pty/Pm)
    saveExcel(Ptx/Pm,Pty/Pm)

def saveExcel(x,y):
    global count
    if count == 1:
        name = input()
        workbook = xlsxwriter.Workbook(str(name) + ".xlsx") 
        worksheet = workbook.add_worksheet()
        worksheet.write('A'+str(count), x)
        worksheet.write('B'+str(count), y)
    elif count > 1 and count < 21:
        worksheet.write('A'+str(count), x)
        worksheet.write('B'+str(count), y)
    elif count == 21:
        print("Save successful")
        workbook.close()

scanner = Scanner().withDelegate(ScanDelegate())

getDatabase()
check = True
while check:
    scanner.scan(1.5,passive=True)
    print("---------------------------------------"+str(count))
    caculatorRSS()
    calculatorD()
    arrangeD()
    calculatorE()
    calculatorP(2)
    print("Add successful")
    print("Continue or Save file json (y/n)?: ")
    i = input()
    if str(i) == "y":
        check = True
        count = 1
    else:
        print("Saved successful")
        check = False
    cleanData()

# addr = ['0c:61:cf:ab:84:c4','24:6f:28:25:f9:92']
# RSSfinal = [-47,-50]
# calculatorD()
# arrangeD()
# calculatorE()
# calculatorP(2)
# cleanData()
# addr = ['0c:61:cf:ab:84:c4','24:6f:28:25:f9:92']
# RSSfinal = [-47,-50]
# calculatorD()
# arrangeD()
# calculatorE()
# calculatorP(2)
# with open('data.json') as json_file:
#     data = json.load(json_file)
#     for i in range(len(data)):
#         print(data[i]['addr'][0])
