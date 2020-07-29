from __future__ import print_function

from time import gmtime, strftime, sleep
from bluepy.btle import Scanner, DefaultDelegate, BTLEException
import sys
import datetime
import time 
import math
import json
#--------------------------------------------
count = 1
addr = []
rssi = []
sumRSS = []
yRSS = []
oRSS = []
RSS = []
RSSfinal = []
dataJson = []
#--------------------------------------------
class ScanDelegate(DefaultDelegate):
    def handleDiscovery(self, dev, isNewDev, isNewData):
        global count, database
        if "24:6f:28:25:f7:5a" == str(dev.addr) or "24:6f:28:27:48:6a" == str(dev.addr) or "24:6f:28:2b:60:32" == str(dev.addr) or "24:6f:28:24:71:d6" == str(dev.addr) or "24:6f:28:25:da:b2" == str(dev.addr) or "24:6f:28:24:81:de" == str(dev.addr) or "24:6f:28:24:d6:26" == str(dev.addr) or "24:6f:28:24:86:2a" == str(dev.addr):
            print(count, datetime.datetime.now(), dev.addr, dev.rssi)
            configData(dev.addr,dev.rssi)
            count += 1
        sys.stdout.flush()

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
    global addr,rssi, sumRSS, yRSS, oRSS, RSS, RSSfinal
    addr = []
    rssi = []
    sumRSS = []
    yRSS = []
    oRSS = []
    RSS = []
    RSSfinal = []


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

    print(RSSfinal)

def Input():
	print("Enter x: ")
	x = input()
	print("Enter y: ")
	y = input()
	return [int(x),int(y)]

def writeToJson(addr, rssi, location):
	global dataJson
	addrJson = []
	rssiJson = []
	for x in range(len(addr)):
		addrJson.append(addr[x])
		rssiJson.append(RSSfinal[x])
	dataJson.append({'addr': addrJson, 'location': location, 'rssi': rssiJson})

def saveToJson():
	global dataJson
	with open('data.json', 'w') as outfile:
		json.dump(dataJson, outfile)

scanner = Scanner().withDelegate(ScanDelegate())

check = True
while check:
	scanner.scan(10,passive=True)
	print("---------------------------------------"+str(check))
	caculatorRSS()
	writeToJson(addr, RSSfinal, Input())
	print("Add successful")
	print("Continue or Save file json (y/n)?: ")
	i = input()
	if str(i) == "y":
		check = True
	else:
		print("Saved successful")
		saveToJson()
		check = False
	cleanData()
