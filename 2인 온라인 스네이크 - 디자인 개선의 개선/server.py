# https://www.youtube.com/watch?v=G46mkV2tc3E
import socket
from network import Networking
import _thread
from _thread import *
from Player import Player

def client_handler(id, client, player):
    global n, p
    n.send(client, player)

    while True:
        try:
            if id == 0:
                n.send(client, p[1])
                p[0] = n.recv(client)
            elif id == 1:
                n.send(client, p[0])
                p[1] = n.recv(client)
        except:
            quit()

ip = '192.168.0.2'
port = 8080
connected_user = 0

n = Networking(ip, port)
p = [Player(50, 50, (255, 0, 0)), Player(400, 400, (0, 255, 0))]

con = n.host()

con.listen(2)

while True:
    client, _ = con.accept()
    if connected_user != 2:
        start_new_thread(client_handler, (connected_user, client, p[connected_user]))
        connected_user += 1
    else:
        client.close()