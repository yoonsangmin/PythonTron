# https://www.youtube.com/watch?v=G46mkV2tc3E
import socket
from network import Networking
import _thread
from _thread import *
from Player import Player

# 전역변수 선언
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 최대 좌표
MAX_X = 50
MAX_Y = 50
# 한 칸의 넓이
GRID_SIZE = 10
# 게임 보드 실제 스크린 크기
GAME_WIDTH = MAX_X * GRID_SIZE
GAME_HEIGHT = MAX_Y * GRID_SIZE

# 초기 몸 길이
INITIAL_LENGTH = 3
# 플레이어 간격
PLAYER_GAP = 10

# 방향
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

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
p = [Player((GAME_WIDTH / 2, GAME_HEIGHT / 2 - PLAYER_GAP * GRID_SIZE), BLUE), Player((GAME_WIDTH / 2, GAME_HEIGHT / 2 + PLAYER_GAP * GRID_SIZE), RED)]

con = n.host()

con.listen(2)

while True:
    client, _ = con.accept()
    if connected_user != 2:
        start_new_thread(client_handler, (connected_user, client, p[connected_user]))
        connected_user += 1
        if connected_user == 2:
            p[0].is_p_en = True
            p[1].is_p_en = True
    else:
        client.close()