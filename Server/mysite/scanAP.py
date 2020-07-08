import socket
import xlsxwriter
import datetime
workbook = xlsxwriter.Workbook('Iphone_31.xlsx')
worksheet = workbook.add_worksheet()
s = socket.socket()
s.bind(('192.168.2.21', 8090))
s.listen(0)
count = 1


while True:
    client, addr = s.accept()
    while True:
        content = client.recv(1000)
        if len(content) == 0:
            print('none')
        else:
            x = datetime.datetime.now()
            print(count)
            if len(content.decode()) <= 4:
                if count <= 20:
                    worksheet.write('B'+str(count), int(content.decode()))
                    worksheet.write('A'+str(count), str(x))
                    print(str(x) + "  "+str(content.decode()))
                    count += 1
                elif count == 21:
                    workbook.close()
    print("closing ")
    client.close()
