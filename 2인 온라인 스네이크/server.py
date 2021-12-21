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

enemy_direction = ''

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


class Food:

    def __init__(self):
        self.position = (0, 0)
        self.color = GREEN

        self.create()

    def create(self):
        self.position = (random.randint(0, MAX_X - 1) * GRID_SIZE, random.randint(0, MAX_Y - 1) * GRID_SIZE)

    def send_message(self):
        msg = 'food ' + str(self.position[0]) + ' ' + str(self.position[1])
        client.sendall(msg.encode())

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

# 적 위치 조정
def consoles():
    global eney, enex
    global enemy_direction
    while True:
        msg = client.recv(1024)
        message = msg.decode()
        command = message.split()[0]

        # if (msg.decode() == 'up'):  # 소켓으로부터받은데이터가 up일경우 적y좌표조정
        #     eney -= 30
        # elif (msg.decode() == 'down'):  # 소켓으로부터받은데이터가 down일경우 적y좌표조정
        #     eney += 30
        # elif (msg.decode() == 'right'):  # 소켓으로부터받은데이터가 right일경우 적x좌표조정
        #     enex += 30
        # elif (msg.decode() == 'left'):  # 소켓으로부터받은데이터가 left일경우 적x좌표조정
        #     enex -= 30
        if command == 'player':
            enemy_direction = message.split()[1]


def acceptC():
    global client, server, addr
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('192.168.0.2', 8080))
    server.listen()
    client, addr = server.accept()

    thr = threading.Thread(target=consoles, args=())
    # 클라이언트로부터 받는 데이터를 관리하기위한
    # 멀티쓰레딩(밑에는 데몬스레드라고 선언 -> c++로 따지면 detach와같습니다)
    thr.Daemon = True
    thr.start()


# 게임 루프
def GameMain():
    # global last_moved_time

    screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
    fps = pygame.time.Clock()

    # 게임 시작 시, 뱀과 사과를 초기화
    player1 = Player(BLUE, (GAME_WIDTH / 2, GAME_HEIGHT / 2 - PLAYER_GAP * GRID_SIZE), DOWN)
    player2 = Player(RED, (GAME_WIDTH / 2, GAME_HEIGHT / 2 + PLAYER_GAP * GRID_SIZE), UP)
    food = Food()
    food.send_message()

    while True:
        screen.fill(BLACK)
        player1.can_input = True
        player2.can_input = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pyautogui.keyUp('left')
                    # 이걸하는이유는 키보드를 꾹누르고있으면 원래는 한번가는데
                    # 이걸하면은 쭉누르면 쭉갑니다
                    player1.change_direction(LEFT)
                    msg = "player left"
                    client.sendall(msg.encode())  # 클라이언트에게 내가내린명령전송
                    # 명령 전송으로 할 수도 있고 아마도 위치 값 그대로 줄 수도?
                elif event.key == pygame.K_RIGHT:
                    pyautogui.keyUp('right')
                    player1.change_direction(RIGHT)
                    msg = "player right"
                    client.sendall(msg.encode())
                elif event.key == pygame.K_UP:
                    pyautogui.keyUp('up')
                    player1.change_direction(UP)
                    msg = "player up"
                    client.sendall(msg.encode())
                elif event.key == pygame.K_DOWN:
                    pyautogui.keyUp('down')
                    player1.change_direction(DOWN)
                    msg = "player down"
                    client.sendall(msg.encode())
        # 메세지 보내기
        global enemy_direction
        if enemy_direction == 'left':
            player2.change_direction(LEFT)
        elif enemy_direction == 'right':
            player2.change_direction(RIGHT)
        elif enemy_direction == 'up':
            player2.change_direction(UP)
        elif enemy_direction == 'down':
            player2.change_direction(DOWN)

        player1.move()
        player2.move()

        # 스네이크가 음식을 먹었는지
        if player1.check_eat(food) or player2.check_eat(food):
            food.create()
            food.send_message()

        show_info(player1.length, player2.length)

        player1.draw(screen)
        player2.draw(screen)
        food.draw(screen)

        # 충돌 처리
        is_player1_collided = player1.check_collisions(player2)
        is_player2_collided = player2.check_collisions(player1)

        if is_player1_collided and is_player2_collided:
            game_over("Draw")
            return
        elif is_player1_collided:
            game_over("Player 2 Win!")
            return
        elif is_player2_collided:
            game_over("Player 1 Win!")
            return

        pygame.display.update()  # 디스플레이 업데이트
        fps.tick(10)  # fps는 60


if __name__ == '__main__':
    # pygame 초기화
    pygame.init()  # 시작
    pygame.display.set_caption('Snake')  # 제목

    # last_moved_time = datetime.now()

    acceptC()
    GameMain()
    pygame.quit()
    sys.exit()