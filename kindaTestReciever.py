import socket
import sys
s = socket.socket()
s.bind(("localhost",9999))
s.listen(10) # Accepts up to 10 connections.

while True:
    sc, address = s.accept()

    print (address)
    i=1
    f = open('file_'+ str(i)+".pdf",'wb') #open in binary
    i=i+1
    while (True):
    # receive data and write it to file
        l = sc.recv(1024)
        while (l):
                f.write(l)
                l = sc.recv(1024)
    f.close()


    sc.close()

s.close()