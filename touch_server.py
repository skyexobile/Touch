# Python program to implement server side of chat room.
import socket
import select
import sys
import thread
import datetime
import time
import math
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# checks whether sufficient arguments have been provided

# takes the first argument from command prompt as IP address
#IP_address = str(sys.argv[1])

# takes second argument from command prompt as port number
#Port = int(sys.argv[2])

"""
binds the server to an entered IP address and at the
specified port number.
The client must be aware of these parameters
"""
server.bind(("127.0.0.1", 5000))

"""
listens for 100 active connections. This number can be
increased as per convenience.
"""
server.listen(100)
start_time = time.time()
list_of_clients = []
clientID = -1

def clientthread(conn, addr):

    while True:
            try:
                message = conn.recv(2048)

                if message:
                    end = time.time()
                    elapsed = (end - start_time)
                    cData = str(message)  + ","+ str(elapsed) + '\n'
                    broadcast(str(addr), conn)
                    message_to_send = cData
                    broadcast(message_to_send, conn)

                else:
                    """message may have no content if the connection
                    is broken, in this case we remove the connection"""
                    remove(conn)

            except:
                continue

"""broadcast the message to all clients who's object is not the same as the one sending
the message """
def broadcast(message, connection):
    for clients in list_of_clients:
        if clients!=connection:
            try:
                clients.send(message.encode())
            except:
                clients.close()

                # if the link is broken
                remove(clients)

""" removes the objectfrom the list that was created at the beginning of
the program"""
def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)
MetaData = False
while True:

    clientID+=1
    conn, addr = server.accept()
    #flag here
    if (MetaData is False):
        list_of_clients.append(conn)
        MetaData = True

    # prints the address of the user that just connected
    #print (str(clientID) + " connected")

    # creates and individual thread for every user that connects
    thread.start_new_thread(clientthread,(conn,clientID))

conn.close()
server.close()
