
import socket
import time

host = 'localhost'
port = 5000

clients = []

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host,port))
s.setblocking(0)

quitting = False
print ("Server Started.")

while True:
    try:
        data, addr = s.recvfrom(1024)
        if addr not in clients:
            clients.append(addr)
            print('added new person')
            print('clients ', clients)

        if data:
            print('data received', data)

            for client in clients:
                if addr != client:
                    print(str(addr) + " is sending to ", client)
                    s.sendto(data, client)
    except:
        pass

s.close()
