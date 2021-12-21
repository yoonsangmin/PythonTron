import pygame  # 게임을위한 메인모듈
import pyautogui  # 조작감살짝 늘리기
import sys  # 콘솔창제어
import socket  # 소켓
import threading  # 멀티쓰레딩
import random
from datetime import datetime
from datetime import timedelta

# 전역변수 선언
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# 최대 좌표
MAX_X = 200
MAX_Y = 200
# 한 칸의 넓이
GRID_SIZE = 5
# 게임 보드 실제 스크린 크기
GAME_WIDTH = MAX_X * GRID_SIZE
GAME_HEIGHT = MAX_Y * GRID_SIZE

# 초기 몸 길이
INITIAL_LENGTH = 3
# 플레이어 간격
PLAYER_GAP = 80

# 방향
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)

food_position = (0, 0)

player1_positions = ()
player2_positions = ()

player1_length = INITIAL_LENGTH
player2_length = INITIAL_LENGTH

class Player(object):

    def __init__(self, color, position, direction):
        self.length = INITIAL_LENGTH
        self.positions = [position]
        # 한 프레임에 키 입력 하나만 받게
        self.can_input = True
        self.color = color

        # 초기 방향
        self.direction = direction

        # 그리기 빼기
        # for x, y in self.coordinates:
        #     square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=PLAYER_COLOR, tag="snake")
        #     self.squares.append(square)

    def change_direction(self, new_direction):

        if self.can_input == False:
            return

        if (new_direction[0] * -1, new_direction[1] * -1) == self.direction:
            return
        else:
            self.direction = new_direction

        self.can_input = False

    def move(self):

        cur = self.positions[0]
        x, y = self.direction

        # 화면 넘어가게 X 충돌 처리 추가하기
        new_head = (cur[0] + (x * GRID_SIZE), cur[1] + (y * GRID_SIZE))

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def check_eat(self, food):
        if self.positions[0] == food.position:
            self.eat()
            return True
        return False

    def eat(self):
        self.length += 1

    def draw(self, screen):
        for position in self.positions:
            draw_object(screen, self.color, position)

    def check_collisions(self, other):
        head = self.positions[0]

        if head[0] < 0 or head[0] >= GAME_WIDTH:
            return True
        elif head[1] < 0 or head[1] >= GAME_HEIGHT:
            return True

        # 게임 오버 관련 넣기 - 충돌 처리는 게임 로직으로 빼기
        if head in self.positions[1:]:
            # 게임 종료 관련 컨트롤, 게임 재식작 관련 로직 넣기
            return True

        if head in other.positions:
            return True

        return False

    def set_positions(self, positions):
        self.positions = positions


class Food:

    def __init__(self):
        self.position = (0, 0)
        self.color = GREEN

        # self.create(self.position)

    def set_pos(self, position):
        self.position = position

    def draw(self, screen):
        draw_object(screen, self.color, self.position)

def game_over(message):
    pass

def show_info(player1_score, player2_score):
    pass

def draw_object(screen, color, position):
    block = pygame.Rect((position[0], position[1]),
                        (GRID_SIZE, GRID_SIZE))
    pygame.draw.rect(screen, color, block)


def consoles():
    global food_position
    global player1_positions
    global player2_positions
    global player1_length
    global player2_length
    while True:
        msg = client.recv(1024)
        message = msg.decode()
        command = message.split()[0]

        # if (msg.decode() == 'up'):
        #     eney -= 30
        # elif (msg.decode() == 'down'):
        #     eney += 30
        # elif (msg.decode() == 'right'):
        #     enex += 30
        # elif (msg.decode() == 'left'):
        #     enex -= 30
        if command == 'food':
            food_position = (int(message.split()[1]), int(message.split()[2]))
        elif command == 'player1':
            pass
        elif command == 'player2':
            pass
        elif command == 'length':
            player1_length = int(message.split()[1])
            player2_length = int(message.split()[2])


def acceptC():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.0.2', 8080))

    thr = threading.Thread(target=consoles, args=())
    thr.Daemon = True
    thr.start()


def GameMain():
    # global last_moved_time

    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    fps = pygame.time.Clock()

    # 게임 시작 시, 뱀과 사과를 초기화
    player1 = Player(BLUE, (GAME_WIDTH / 2, GAME_HEIGHT / 2 - PLAYER_GAP * GRID_SIZE), DOWN)
    player2 = Player(RED, (GAME_WIDTH / 2, GAME_HEIGHT / 2 + PLAYER_GAP * GRID_SIZE), UP)
    food = Food()

    while True:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pyautogui.keyUp('left')
                    msg = "client left"
                    client.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송
                    # 명령 전송으로 할 수도 있고 아마도 위치 값 그대로 줄 수도?
                elif event.key == pygame.K_RIGHT:
                    pyautogui.keyUp('right')
                    msg = "client right"
                    client.sendall(msg.encode())
                elif event.key == pygame.K_UP:
                    pyautogui.keyUp('up')
                    msg = "client up"
                    client.sendall(msg.encode())
                elif event.key == pygame.K_DOWN:
                    pyautogui.keyUp('down')
                    msg = "client down"
                    client.sendall(msg.encode())

        # global player1_positions
        # global player2_positions
        #
        # player1.set_positions(player1_positions)
        # player2.set_positions(player2_positions)
        #
        # player1_positions = ()
        # player2_positions = ()

        food.set_pos(food_position)

        # global player1_length, player2_length
        # player1.length = player1_length
        # player2.length = player2_length
        #
        # show_info(player1.length, player2.length)
        #
        # player1.draw(screen)
        # player2.draw(screen)
        food.draw(screen)

        # 충돌 처리 - 클라이언트에서 안 함
        # is_player1_collided = player1.check_collisions(player2)
        # is_player2_collided = player2.check_collisions(player1)

        # 메세지 받아와야 함
        # if is_player1_collided and is_player2_collided:
        #     game_over("Draw")
        #     return
        # elif is_player1_collided:
        #     game_over("Player 2 Win!")
        #     return
        # elif is_player2_collided:
        #     game_over("Player 1 Win!")
        #     return

        pygame.display.update()  # 디스플레이 업데이트
        fps.tick(1000)  # fps는 60


if __name__ == '__main__':
    # pygame 초기화
    pygame.init()  # 시작
    pygame.display.set_caption('Snake')  # 제목

    acceptC()
    GameMain()

    pygame.quit()
    sys.exit()