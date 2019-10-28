import socket

import UtilityFunctions

ip = UtilityFunctions.getIP()
s = socket.socket()
sip = ':'.join(''.join([hex(int(i)) for i in ip.split('.')]).split('0x'))
print('code:', sip)
s.bind((ip, 9999))
s.listen(10)  # Accepts up to 10 connections.
while True:
    sc, address = s.accept()
    print('> connected to', address)

    # receive data and write it to file
    filePart = sc.recv(255)
    fileName = str(filePart).lstrip(r"b\'").rstrip('\'').rstrip(' ')
    print('> file name:', fileName)

    filePart = sc.recv(255)
    lent = int(str(filePart).lstrip(r"b\'").rstrip('\'').rstrip(' '))
    print('> length:', lent)

    filePart = sc.recv(2048)
    f = open(fileName, 'wb')  # open in binary
    while filePart:
        f.write(filePart)
        filePart = sc.recv(1024)
    print('successfully received the file')

    f.close()
    print('>', 'file match =', UtilityFunctions.fileSize(fileName) == lent)
    sc.close()
