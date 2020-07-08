import socket
import argparse
import threading 
import xlsxwriter

workbook = xlsxwriter.Workbook('ESP1-8m.xlsx')
worksheet = workbook.add_worksheet()
parser = argparse.ArgumentParser(description = "This is the server for the multithreaded socket demo!")
parser.add_argument('--host', metavar = 'host', type = str, nargs = '?', default = '192.168.2.21')
parser.add_argument('--port', metavar = 'port', type = int, nargs = '?', default = 8090)
args = parser.parse_args()

print(f"Running the server on: {args.host} and port: {args.port}")

sck = socket.socket()
sck.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# define variance
NameESP = []
RSSI = []
data = []
count1 = 1
count2 = 1
count3 = 1
count4 = 1
# ----------------------
worksheet.write('A'+str(count1), "ESP32-1")
# worksheet.write('B'+str(count2), "ESP32-2")
# worksheet.write('C'+str(count3), "ESP32-3")
# worksheet.write('D'+str(count4), "ESP32-4")
count1 += 1
count2 += 1
count3 += 1
count4 += 1
#----------------------
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
    global data
    ip = connection[0]
    port = connection[1]
    print(f"THe new connection was made from IP: {ip}, and port: {port}!")
    while True:
        msg = client.recv(2000)
        if msg.decode() == 'exit':
            break
        # print(f"The client said: {msg.decode()}")
        scanData(msg)
        data = []
    print(f"The client from ip: {ip}, and port: {port}, has gracefully diconnected!")
    client.close()

def scanData(string):
    global data,count1,count2,count3,count4
    s = string.decode()
    value = ""
    for x in range(len(s)):
        if s[x] != " ":
            value += s[x]
        else:
            data.append(value)
            value = ""
    
    if (count1 <= 20):
        #  or (count2 <= 20) or (count3 <= 20) or (count4 <= 20):
        if data[0] == "ESP32-1":
            worksheet.write('A'+str(count1), data[1])
            print(data,count1)
            count1 += 1
        # elif data[0] == "ESP32-2":
        #     worksheet.write('B'+str(count2), data[1])
        #     print(data,count2)
        #     count2 += 1
        # elif data[0] == "ESP32-3":
        #     worksheet.write('C'+str(count3), data[1])
        #     print(data,count3)
        #     count3 += 1
        # elif data[0] == "ESP32-4":
        #     worksheet.write('D'+str(count4), data[1])
        #     print(data,count4)
        #     count4 += 1
    elif (count1 >= 21):
    #  and (count3 >= 21) and (count2 >= 21) and (count4 >= 21):
        workbook.close()

if __name__ == "__main__":
    connect_socket()
