import socket
import argparse
import threading 
import json
import xlsxwriter
import math
# define variance
NameESP = []
RSSI = []
maxRSSI = []
NameClient = ["client1","client2","client3"]
distanceValue = []
locationNode = []
count = 1
count_ex = 1
#--------------------------------------Excel ----------------------------------
string1 = ["client1", {"Node1": -50, "Node2": -49, "Node3": -60, "Node4": -81}]
string2 = ["client2", {"Node1": -55, "Node2": -79, "Node3": -50, "Node4": -71}]
string3 = ["client3", {"Node1": -60, "Node2": -49, "Node3": -70, "Node4": -80}]
# ----------------------
parser = argparse.ArgumentParser(description = "This is the server for the multithreaded socket demo!")
parser.add_argument('--host', metavar = 'host', type = str, nargs = '?', default = '172.20.10.2')
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
        msg = client.recv(20000)
        print(msg.decode())
        if len(msg) < 100:
            configData(json.loads(msg))
            clear()
    print(f"The client from ip: {ip}, and port: {port}, has gracefully diconnected!")
    client.close()

def database():
    global NameESP, RSSI,  nameTriangle, TriangleValue, maxRSSI, NameClient, locationNode
    with open('data2.json') as json_file:
        data = json.load(json_file)
        for y in data:
            NameESP.append(y['name'])
            RSSI.append(0)
            maxRSSI.append([])
            locationNode.append([])
            locationNode[len(NameESP)-1].append(y['location_x'])
            locationNode[len(NameESP)-1].append(y['location_y'])
            #distanceValue.append(0)
    for x in range(len(maxRSSI)):
        for y in range(len(NameClient)):
            maxRSSI[x].append(-100)
    print("NameESP: ",NameESP)
    print("RSSI: ",RSSI)
    print("maxRSSI: ",maxRSSI)
    print("locationNode: ",locationNode)

def configData(string):
    global NameESP, RSSI, count,maxRSSI
    count += 1
    for name,value in string[1].items():
        for x in range(len(NameESP)):
            if name == NameESP[x]:
                for y in range(len(NameClient)):
                    if string[0] == NameClient[y]:
                        maxRSSI[x][y] = value
                        break
                RSSI[x] = max(maxRSSI[x])
                break
    print(count)
    print(NameESP)
    print(RSSI)
    print(maxRSSI)
    status = True
    for x in range(len(RSSI)):
        if RSSI[x] == -100:
            status = False
            break
    if status:
        caculateDistance()
    print("-------------------")

def caculateDistance():
    global NameESP, RSSI, distanceValue, locationNode
    for x in range(len(NameESP)):
        with open('data2.json') as json_file:
            data = json.load(json_file)
            for y in data:
                if NameESP[x] == y['name']:
                    distanceValue.append(
                        pow(10, (y['level']-int(RSSI[x]))/25))
    print('distanceValue: ' + str(distanceValue))
    for x in range(len(distanceValue)-1):
        for y in range(x+1,len(distanceValue)):
            if distanceValue[x] > distanceValue[y]:
                temp1 = distanceValue[x]
                distanceValue[x] = distanceValue[y]
                distanceValue[y] = temp1
                temp2 = NameESP[x]
                NameESP[x] = NameESP[y]
                NameESP[y] = temp2
                temp3 = locationNode[x]
                locationNode[x] = locationNode[y]
                locationNode[y] = temp3
    print('distanceValue--: ' + str(distanceValue))
    print("NameESP--: ",NameESP)
    print("locationNode--: ",locationNode)
    defineLocation()

def clear():
    global RSSI, distanceValue
    for x in range(len(RSSI)):
        RSSI[x] = -100
    distanceValue = []

def defineLocation():
    global NameESP, distanceValue, locationNode
    A = 0
    B = 0
    C = 0
    D = 0
    E = 0
    F = 0
    locationTrila = [0,0]
    # print('loc: ' + str(location))
    # print('dis: ' + str(distance))

    A = locationNode[0][0] - locationNode[1][0]
    B = locationNode[0][1] - locationNode[1][1]
    D = locationNode[0][0] - locationNode[2][0]
    E = locationNode[0][1] - locationNode[2][1]
    C = pow(distanceValue[1], 2) - pow(distanceValue[0], 2) + pow(locationNode[0][0], 2) - \
        pow(locationNode[1][0], 2) + pow(locationNode[0]
                                     [1], 2) - pow(locationNode[1][1], 2)
    F = pow(distanceValue[2], 2) - pow(distanceValue[0], 2) + pow(locationNode[0][0], 2) -\
        pow(locationNode[2][0], 2) + pow(locationNode[0]
                                     [1], 2) - pow(locationNode[2][1], 2)
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
    saveExcel(locationTrila,5,2.8)

def saveExcel(locationTrila,x,y):
    global NameESP, RSSI, distanceValue, count_ex, workbook, worksheet, locationNode
    if count_ex == 1:
        workbook = xlsxwriter.Workbook("Test-(" + str(x) + "-" + str(y) + ").xlsx") 
        worksheet = workbook.add_worksheet()
        worksheet.write('A'+str(count_ex), "Node1")
        worksheet.write('B'+str(count_ex), "Node2")
        worksheet.write('C'+str(count_ex), "Node3")
        worksheet.write('E'+str(count_ex), "Distance1")
        worksheet.write('F'+str(count_ex), "Distance2")
        worksheet.write('G'+str(count_ex), "Distance3")
        worksheet.write('I'+str(count_ex), "x")
        worksheet.write('J'+str(count_ex), "y")
        worksheet.write('L'+str(count_ex), "Accuracy")
    elif count_ex > 1 and count_ex < 30:
        worksheet.write('A'+str(count_ex), RSSI[0])
        worksheet.write('B'+str(count_ex), RSSI[1])
        worksheet.write('C'+str(count_ex), RSSI[2])
        worksheet.write('E'+str(count_ex), distanceValue[0])
        worksheet.write('F'+str(count_ex), distanceValue[1])
        worksheet.write('G'+str(count_ex), distanceValue[2])
        worksheet.write('I'+str(count_ex), locationTrila[0])
        worksheet.write('J'+str(count_ex), locationTrila[1])
        worksheet.write('L'+str(count_ex), math.sqrt(pow(locationTrila[0]-x,2) + pow(locationTrila[1]-y,2)))
    elif count_ex == 30:
        worksheet.write('E'+str(count_ex + 1), math.sqrt(pow(locationNode[0][0] - x,2)+pow(locationNode[0][1]-y,2)))
        worksheet.write('F'+str(count_ex + 1), math.sqrt(pow(locationNode[1][0] - x,2)+pow(locationNode[1][1]-y,2)))
        worksheet.write('G'+str(count_ex + 1), math.sqrt(pow(locationNode[2][0] - x,2)+pow(locationNode[2][1]-y,2)))
        workbook.close()
    count_ex += 1
if __name__ == "__main__":
    database()
    configData(string1)
    clear()
    configData(string2)
    clear()
    configData(string3)
    #connect_socket()
