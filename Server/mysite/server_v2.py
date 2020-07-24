import socket
import argparse
import threading 
import json
import xlsxwriter
import math
# define variance
NameESP = []
RSSI = []
checkRSSI = []
distanceValue = []
TriangleValue = []
TriangleChoosen = 0
locationTrila = [0, 0]
count = 0
nameTriangle = [['ESP32-1', 'ESP32-2', 'ESP32-3'],
                ['ESP32-2', 'ESP32-3', 'ESP32-4']]
# ----------------------
parser = argparse.ArgumentParser(description = "This is the server for the multithreaded socket demo!")
parser.add_argument('--host', metavar = 'host', type = str, nargs = '?', default = '192.168.2.16')
parser.add_argument('--port', metavar = 'port', type = int, nargs = '?', default = 8090)
args = parser.parse_args()

print(f"Running the server on: {args.host} and port: {args.port}")

sck = socket.socket()
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
def connect_socket():
    global sck,args
    try: 
        sck.bind((args.host, args.port))
        sck.listen(5)
    except Exception as e:
        raise SystemExit(f"We could not bind the server on host: {args.host} to port: {args.port}, because: {e}")

    while True:
        try: 
            client, ip = sck.accept()
            threading._start_new_thread(on_new_client,(client, ip))
        except KeyboardInterrupt:
            print(f"Gracefully shutting down the server!")
        except Exception as e:
            print(f"Well I did not anticipate this: {e}")


def on_new_client(client, connection):
    ip = connection[0]
    port = connection[1]
    print(f"THe new connection was made from IP: {ip}, and port: {port}!")
    while True:
        msg = client.recv(2000)
        configData(msg)
        # isCalculate()
        # clearData()
        
    print(f"The client from ip: {ip}, and port: {port}, has gracefully diconnected!")
    client.close()

def database():
    global NameESP, RSSI, checkRSSI, nameTriangle, TriangleValue
    with open('data.json') as json_file:
            data = json.load(json_file)
            for y in data:
                NameESP.append(y['name'])
                RSSI.append(0)
                checkRSSI.append([])
                distanceValue.append(0)

    # print(NameESP)
    # print(RSSI)

def configData(string):
    global NameESP, RSSI, checkRSSI
    data = []
    s = string.decode()
    value = ""
    for x in range(len(s)):
        if s[x] != " ":
            value += s[x]
        else:
            data.append(value)
            value = ""

    for x in range(len(NameESP)):
        if data[0] == NameESP[x]:
            RSSI[x] = data[1]
            break

    for x in range(len(RSSI)):
        if RSSI[x] != 0:
            checkRSSI[x].append(RSSI[x])
            #shiftData()

    print(NameESP)
    print(RSSI)
    #print(checkRSSI)
    print("-------------------")

def clearData():
    global RSSI, distanceValue, TriangleValue, TriangleChoosen
    # distanceValue = []
    TriangleValue = []
    # TriangleChoosen = 0
    locationTrila = [0, 0]

def isCalculate():
    global RSSI, NameESP
    isCalculate = True
    for x in range(len(NameESP)):
        if NameESP[x] == "ESP32-1":
            if RSSI[x] == 0:
                isCalculate = False
                break
    if isCalculate:
        caculateDistance()

def caculateDistance():
    global NameESP, RSSI, distanceValue
    for x in range(len(NameESP)):
        if RSSI[x] != 0:
            with open('data.json') as json_file:
                data = json.load(json_file)
                for y in data:
                    if NameESP[x] == y['name']:
                        distanceValue[x] = pow(10, (y['level']-int(RSSI[x]))/40)
        else:
            distanceValue[x] = 0
    print('distanceValue: ' + str(distanceValue))
    defineTriangle()

def defineTriangle():
    global nameTriangle, TriangleValue, TriangleChoosen, NameESP
    TriangleValue = [0,0]
    for i in range(len(nameTriangle)):
        for j in range(len(NameESP)):
            for k in range(len(nameTriangle[i])):
                if NameESP[j] == nameTriangle[i][k]:
                    TriangleValue[i] = TriangleValue[i] + distanceValue[j]
    print('TriangleValue : ' + str(TriangleValue))
    for i in range(len(TriangleValue)):
        if TriangleValue[i] == min(TriangleValue):
            TriangleChoosen = i
    print('TriangleChoosen: ' + str(TriangleChoosen) +
          ' ' + str(nameTriangle[TriangleChoosen]))
    defineLocation()

def defineLocation():
    global nameTriangle, TriangleValue, TriangleChoosen, locationTrila, name, NameESP, count
    A = 0
    B = 0
    C = 0
    D = 0
    E = 0
    F = 0
    location = [[], [], []]
    distance = [0, 0, 0]
    for i in range(len(nameTriangle[TriangleChoosen])):
        with open('data.json') as json_file:
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
    print('Count: ', str(count))
    print('------------------------')
    saveExcel('En2-T1',7,3)

def shiftData():
    global checkRSSI,NameESP
    isDisconnect = True
    for x in range(len(checkRSSI)):
        if len(checkRSSI[x]) > 5:
            checkRSSI[x] = checkRSSI[x][1:]
            for y in range(1,len(checkRSSI[x])):
                temp = checkRSSI[x][0]
                if temp == 0:
                    break
                if temp != checkRSSI[x][y]:
                    isDisconnect = False
                    break
            if isDisconnect:
                checkRSSI[x] = []
                RSSI[x] = 0
                print(f"The client : {NameESP[x]} is diconnected!")

def saveExcel(title,x,y):
    global RSSI, NameESP, locationTrila,count,workbook, worksheet,distanceValue
    if count == 0:
        string = title + str("-(") + str(x) + str("-") + str(y) + str(")") + str(".xlsx")
        workbook = xlsxwriter.Workbook(string)
        worksheet = workbook.add_worksheet()
        worksheet.write('A1', 'ESP1')
        worksheet.write('B1', 'ESP2')
        worksheet.write('C1', 'ESP3')
        worksheet.write('D1', 'ESP4')
        worksheet.write('G1', 'x')
        worksheet.write('H1', 'y')
        worksheet.write('I1', 'Accuracy')
    elif count < 40 and count > 0:
        worksheet.write('A'+str(count), RSSI[0])
        worksheet.write('B'+str(count), RSSI[1])
        worksheet.write('C'+str(count), RSSI[2])
        worksheet.write('D'+str(count), RSSI[3])
        worksheet.write('A'+str(count+1), distanceValue[0])
        worksheet.write('B'+str(count+1), distanceValue[1])
        worksheet.write('C'+str(count+1), distanceValue[2])
        worksheet.write('D'+str(count+1), distanceValue[3])
        worksheet.write('G'+str(count), locationTrila[0])
        worksheet.write('H'+str(count), locationTrila[1])
        worksheet.write('I'+str(count), math.sqrt(pow(locationTrila[0]-x,2)+pow(locationTrila[1]-y,2)))
    elif count == 42:
        workbook.close()
    count += 2



if __name__ == "__main__":
    database()
    connect_socket()
    
