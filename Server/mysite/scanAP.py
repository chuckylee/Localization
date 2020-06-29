import socket
import xlsxwriter
import datetime
workbook = xlsxwriter.Workbook('ESP5_3.3m_v21.xlsx')
worksheet = workbook.add_worksheet()
s = socket.socket()
s.bind(('192.168.2.18', 8090))
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
            print(str(x) + "  "+str(content.decode()))
            if len(content.decode()) <= 3:
                if count <= 500:
                    worksheet.write('B'+str(count), int(content.decode()))
                    worksheet.write('A'+str(count), str(x))
                    count += 1
                elif count == 501:
                    workbook.close()
    print("closing ")
    client.close()
