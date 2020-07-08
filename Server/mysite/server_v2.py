import socket
import argparse
import threading 
import json
# define variance
NameESP = []
RSSI = []
distanceValue = []
# ----------------------
parser = argparse.ArgumentParser(description = "This is the server for the multithreaded socket demo!")
parser.add_argument('--host', metavar = 'host', type = str, nargs = '?', default = '192.168.2.21')
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
    print(f"The client from ip: {ip}, and port: {port}, has gracefully diconnected!")
    client.close()

def database():
    global NameESP, RSSI
    with open('data.json') as json_file:
            data = json.load(json_file)
            for y in data:
                NameESP.append(y['name'])
                RSSI.append(0)
    # print(NameESP)
    # print(RSSI)

def configData(string):
    global NameESP, RSSI
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
    print(NameESP)
    print(RSSI)
    print("-------------------")

# def calculateDistance():

if __name__ == "__main__":
    database()
    connect_socket()
    
