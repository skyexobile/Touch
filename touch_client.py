# Python program to implement client side of chat room.
import socket
import select
import sys
import datetime
print("starting")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 2:
    print ("Correct usage: script, SubID")
    exit()

subID = str(sys.argv[1])
#IP_address = str(sys.argv[1])
#Port = int(sys.argv[2])
server.connect(("127.0.0.1", 5000))
path = "DataFiles/" + str(subID)+ "/metaData"
counter = 0
while True:

    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server]

    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:

        if socks == server:
            file_version = socks.recv(1)
            if file_version:
                myFile = open(path+str(file_version.decode())+'.csv', 'a')
                #'utf-8-sig'
                message = socks.recv(2048)
                #print("writing to", path+str(file_version.decode()))
                #print ("message is: " + message.decode())
                # write to csv FIle
                myFile.write(message.decode())
                myFile.close()


server.close()
