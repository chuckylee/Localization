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
TriangleValue = []
TriangleChoosen = 0
locationTrila = [0, 0]
count = 1
workbook = xlsxwriter.Workbook('6_6.xlsx')
worksheet = workbook.add_worksheet()
worksheet.write('A'+str(count), "client1")
worksheet.write('B'+str(count), "client2")
worksheet.write('C'+str(count), "client3")

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
    global NameESP, RSSI,  nameTriangle, TriangleValue, maxRSSI, NameClient
    with open('data2.json') as json_file:
            data = json.load(json_file)
            for y in data:
                NameESP.append(y['name'])
                RSSI.append(0)
                maxRSSI.append([])
                distanceValue.append(0)
    for x in range(len(maxRSSI)):
        for y in range(len(NameClient)):
            maxRSSI[x].append(-100)
    print(NameESP)
    print(RSSI)
    print(maxRSSI)

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
    saveExcel()
    print("-------------------")

def saveExcel():
    global count, maxRSSI, RSSI,worksheet,workbook
    if count < 20000:
        worksheet.write('A'+str(count), maxRSSI[0][0])
        worksheet.write('B'+str(count), maxRSSI[0][1])
        worksheet.write('C'+str(count), maxRSSI[0][2])
        worksheet.write('E'+str(count), RSSI[0])
    elif count == 20000:
        workbook.close()

def clear():
    global RSSI
    for x in range(len(RSSI)):
        RSSI[x] = -100


if __name__ == "__main__":
    database()
    connect_socket()
