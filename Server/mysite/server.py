import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import socket
import json
import math
s = socket.socket()
data = []
fakeData = ['ESP32-5', '-58', 'ESP32-2', '-67',
            'ESP32-3', '-60', 'ESP32-4', '-57', 'ESP32-1', '-70']
fakeData1 = []
# ------------------------------------------------
name = []
rssi = []
gaussName = []
gaussRssi = []
distanceValue = []
TriangleValue = []
TriangleChoosen = 0
locationTrila = [0, 0]
count = 0
# ------------------------------------------------
nameTriangle = [['ESP32-1', 'ESP32-3', 'ESP32-4'],
                ['ESP32-1', 'ESP32-5', 'ESP32-4']]
# nameTriangle = [['EDISON-36', 'EDISON-44', 'EDISON-45'],
#                 ['EDISON-36', 'EDISON-37', 'EDISON-45'],
#                 ['EDISON-37', 'ESP32-1', 'EDISON-45'],
#                 ['EDISON-46', 'ESP32-1', 'EDISON-45'],
#                 ['ESP32-3', 'ESP32-1', 'EDISON-46'],
#                 ['ESP32-3', 'ESP32-4', 'EDISON-46'],
#                 ['ESP32-5', 'ESP32-4', 'EDISON-46'], ]
# ------------------------------
sumRSS = []
yRSS = []
oRSS = []
RSS = []
RSSfinal = []
name1 = ['esp1', 'esp2', 'esp3']
rssi1 = [-69, -67, -65]
name2 = ['esp3', 'esp1', 'esp2']
rssi2 = [-70, -68, -70]
name3 = ['esp2', 'esp3']
rssi3 = [-57, -52]
name4 = ['esp1', 'esp2', 'esp4']
rssi4 = [-60, -71, -69]
name5 = ['esp1', 'esp5', 'esp3', 'esp4', 'esp2']
rssi5 = [-69, -67, -65, -50, -59]


class Location(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def from_dict(source):
        locate = Location(source[u'x'], source[u'y'])
        return locate

    def to_dict(self):
        dest = {
            'x': self.x,
            'y': self.y,
        }
        return dest

    def __repr__(self):
        return(
            f'Location(\
                x={self.x}, \
                y={self.y}, \
            )'
        )


cred = credentials.Certificate(
    "./datatrila-firebase-adminsdk-9q0xv-7e0316a41c.json")
app = firebase_admin.initialize_app(cred)

store = firestore.client()
# doc_ref = store.collection(u'Data')
# data = []
# count=1
# store.collection(u'cities').document().set(data1)
# try:
#     docs = doc_ref.get()

#     for doc in docs:
#         data.append(doc.to_dict())

# except google.cloud.exceptions.NotFound:
#     print(u'Missing data')

# print('Leght:', len(data))

# print(data)


def deleteDatabase():
    global store
    # print('hi')
    doc_ref = store.collection(u'location')
    try:
        docs = doc_ref.get()

        for doc in docs:
            doc.reference.delete()
    except google.cloud.exceptions.NotFound:
        print(u'Missing data')


def configString(string):
    global data
    s = string.decode()
    value = ""
    for x in range(len(s)):
        if s[x] != " ":
            value += s[x]
        else:
            data.append(value)
            value = ""


def arrangeData(arr):
    global name, rssi, count
    x = 0
    count += 1
    while x < len(arr):
        name.append(arr[x])
        rssi.append(arr[x+1])
        x += 2


def averageRSSDatabase(RSS):
    value = 0
    for x in range(len(RSS)):
        value = value + RSS[x]
    value = value/len(RSS)
    return value


def formatData(name, rssi):
    global count, gaussRssi, gaussName
    if (count == 1):
        for x in range(len(name)):
            gaussName.append(name[x])
            gaussRssi.append([])
            gaussRssi[x].append(int(rssi[x]))
    else:
        for x in range(len(name)):
            check = True
            for y in range(len(gaussName)):
                if name[x] == gaussName[y]:
                    gaussRssi[y].append(int(rssi[x]))
                    check = False
                    break
            if check == True:
                gaussName.append(name[x])
                gaussRssi.append([])
                gaussRssi[len(gaussRssi)-1].append(int(rssi[x]))
    print('gaussName: '+str(gaussName))
    print('gaussRSSi: '+str(gaussRssi))


def caculatorRSS():
    global sumRSS, oRSS, yRSS, RSSfinal, RSS, count, gaussRssi, gaussName
    for x in range(len(gaussName)):
        if len(sumRSS) < len(gaussName):
            sumRSS.append(0)
            yRSS.append(0)
        for y in range(len(gaussRssi[x])):
            if sumRSS[x] == 0:
                sumRSS[x] = gaussRssi[x][y]
            else:
                sumRSS[x] = sumRSS[x] + gaussRssi[x][y]
        yRSS[x] = sumRSS[x]/len(gaussRssi[x])

    for x in range(len(gaussName)):
        if len(oRSS) < len(gaussName):
            oRSS.append(0)
        for y in range(len(gaussRssi[x])):
            if oRSS[x] == 0:
                oRSS[x] = (gaussRssi[x][y]-yRSS[x])*(gaussRssi[x][y]-yRSS[x])
            else:
                oRSS[x] = oRSS[x]+(gaussRssi[x][y]-yRSS[x]) * \
                    (gaussRssi[x][y]-yRSS[x])
        if len(gaussRssi[x]) != 1:
            oRSS[x] = math.sqrt(oRSS[x]/(len(gaussRssi[x])-1))

    for x in range(len(gaussName)):
        if len(RSS) < len(gaussName):
            RSS.append([0])
        for y in range(len(gaussRssi[x])):
            if gaussRssi[x][y] > yRSS[x]-oRSS[x] and gaussRssi[x][y] < yRSS[x]+oRSS[x]:
                if RSS[x][0] == 0:
                    RSS[x][0] = gaussRssi[x][y]
                else:
                    c = False
                    for k in range(len(RSS[x])):
                        if RSS[x][k] == gaussRssi[x][y]:
                            c = True
                            break
                    if c == False:
                        RSS[x].append(gaussRssi[x][y])
    for x in range(len(RSS)):
        if len(RSSfinal) < len(RSS):
            RSSfinal.append(0)
        for y in range(len(RSS[x])):
            if RSSfinal[x] == 0:
                RSSfinal[x] = RSS[x][y]
            else:
                RSSfinal[x] = RSSfinal[x] + RSS[x][y]
        RSSfinal[x] = RSSfinal[x]/len(RSS[x])

    for x in range(len(gaussName)):
        if oRSS[x] == 0 or len(gaussRssi[x]) == 1:
            RSSfinal[x] = gaussRssi[x][0]

    print('sum: ' + str(sumRSS))
    print('yRSS: ' + str(yRSS))
    print('oRSS: ' + str(oRSS))
    print('RSS: ' + str(RSS))
    print('RSSfinal: '+str(RSSfinal))


def caculateDistance():
    global name, distanceValue, rssi, RSSfinal, gaussName
    for x in range(len(gaussName)):
        with open('data.json') as json_file:
            data = json.load(json_file)
            for y in data:
                if gaussName[x] == y['name']:
                    distanceValue.append(
                        pow(10, (averageRSSDatabase(y['level'])-int(RSSfinal[x]))/40))
    print('distanceValue: ' + str(distanceValue))


def defineTriangle():
    global nameTriangle, TriangleValue, TriangleChoosen, gaussName
    for i in range(len(nameTriangle)):
        TriangleValue.append(0)

    for i in range(len(nameTriangle)):
        for j in range(len(gaussName)):
            for k in range(len(nameTriangle[i])):
                if gaussName[j] == nameTriangle[i][k]:
                    TriangleValue[i] = TriangleValue[i] + distanceValue[j]
    # print(TriangleValue)
    for i in range(len(TriangleValue)):
        if TriangleValue[i] == min(TriangleValue):
            TriangleChoosen = i
    # print('TriangleChoosen: ' + str(TriangleChoosen) +
    #       ' ' + str(nameTriangle[TriangleChoosen]))


def defineLocation():
    global nameTriangle, TriangleValue, TriangleChoosen, locationTrila, name, gaussName
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
            for j in range(len(gaussName)):
                if nameTriangle[TriangleChoosen][i] == gaussName[j]:
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
    print('------------------------')


def clearData():
    global TriangleValue, locationTrila, TriangleChoosen, distanceValue, name, rssi, data, sumRSS, yRSS, oRSS, RSS, RSSfinal
    TriangleValue = []
    locationTrila = [0, 0]
    TriangleChoosen = 0
    distanceValue = []
    name = []
    rssi = []
    data = []
    sumRSS = []
    yRSS = []
    oRSS = []
    RSS = []
    RSSfinal = []


def addToFirebase(x, y, count):
    store.collection('location').document('locate' + str(count-1)).delete()
    locate = Location(x=x, y=y)
    store.collection(u'location').document(
        'locate' + str(count)).set(locate.to_dict())


def connectSocket():
    global s
    s.bind(('192.168.1.14', 8090))
    s.listen(0)


def shiftData():
    global gaussRssi
    for x in range(len(gaussRssi)):
        if len(gaussRssi[x]) > 10:
            gaussRssi[x] = gaussRssi[x][1:]


def createSocket():
    global locationTrila, s, count
    count_time = 0
    deleteDatabase()
    while True:
        client, addr = s.accept()
        while True:
            content = client.recv(1000)
            if len(content) == 0:
                print('none')
            else:
                print(count_time)
                print(content)
                configString(content)
                arrangeData(data)
                print(data)
                formatData(name, rssi)
                shiftData()
                caculatorRSS()
                caculateDistance()
                defineTriangle()
                defineLocation()
                addToFirebase(locationTrila[0], locationTrila[1], count)
                # print('accuracy: ' + str(math.sqrt((locationTrila[0]-7.6)*(
                #     locationTrila[0]-7.6) + (locationTrila[1]-6.4)*(locationTrila[1]-6.4))))
                clearData()
                # print(data)
                # data = []
            count_time += 1
        print("closing ")
        client.close()


if __name__ == "__main__":
    connectSocket()
    createSocket()
    # formatData(name1, rssi1)
    # caculatorRSS()
    # caculateDistance()
    # defineTriangle()
    # defineLocation()
    # clearData()
    # formatData(name2, rssi2)
    # caculatorRSS()
    # caculateDistance()
    # defineTriangle()
    # defineLocation()
    # clearData()
    # formatData(name3, rssi3)
    # caculatorRSS()
    # caculateDistance()
    # defineTriangle()
    # defineLocation()
    # clearData()
    # formatData(name4, rssi4)
    # caculatorRSS()
    # caculateDistance()
    # defineTriangle()
    # defineLocation()
    # clearData()
    # formatData(name5, rssi5)
    # caculatorRSS()
    # caculateDistance()
    # defineTriangle()
    # defineLocation()
    # clearData()
    # deleteDatabase()
    # locate = Location(x=5, y=6)
    # store.collection(u'location').document(u'locate2').set(locate.to_dict())
    # arrangeData(fakeData)
    # caculateDistance()
    # defineTriangle()
    # defineLocation()
    # clearData()
