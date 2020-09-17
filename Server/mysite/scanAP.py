import socket
import xlsxwriter
import datetime
workbook = xlsxwriter.Workbook('Ihone - 2.xlsx')
worksheet = workbook.add_worksheet()
s = socket.socket()
s.bind(('192.168.2.13', 8090))
s.listen(0)
count = 1
data = ""

while True:
    client, addr = s.accept()
    while True:
        content = client.recv(1000)
        if len(content) == 0:
            print('none')
        else:
            x = datetime.datetime.now()
            print(count)
            print(str(x) + "  "+str(content.decode()))
            # if len(content.decode()) <= 4:
            #     if count <= 2000:
            #         worksheet.write('B'+str(count), int(content.decode()))
            #         worksheet.write('A'+str(count), str(x))
            #         print(str(x) + "  "+str(content.decode()))
            #         data = data + str(content.decode()) + str(",")
            #         count += 1
            #     elif count == 2001:
            #         worksheet.write('C1', str(data))
            #         workbook.close()
    print("closing ")
    client.close()
