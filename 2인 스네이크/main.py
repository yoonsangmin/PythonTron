# 참고 영상 출처: https://www.youtube.com/watch?v=bfRwxS5d0SI&list=PLVZH-JVY27dllGu0HgjWw6dKjq-3DYTG5

from tkinter import *
import random
import time
from time import *
from enum import Enum

# 상수
# 최대 좌표
MAX_X = 70
MAX_Y = 70
# 한 칸의 넓이
GRID_SIZE = 10
# 게임 보드 실제 스크린 크기
GAME_WIDTH = MAX_X * GRID_SIZE
GAME_HEIGHT = MAX_Y * GRID_SIZE

# 플레이어 간격
PLAYER_GAP = 20

# 게임 업데이트 간격
UPDATE_RATE = 100
# 초기 몸 길이
INITIAL_LENGTH = 3
PLAYER1_COLOR = "#FF0000"
PLAYER2_COLOR = "#0000FF"

FOOD_COLOR = "#00FF00"
BACKGROUND_COLOR = "#000000"

# 방향
LEFT = (-1, 0)
RIGHT = (1, 0)
UP = (0, -1)
DOWN = (0, 1)


class Player(object):

    def __init__(self, color, position, direction, tag):
        self.length = INITIAL_LENGTH
        self.positions = [position]
        # 한 프레임에 키 입력 하나만 받게
        self.can_input = True
        self.color = color
        # 플레이어 태그
        self.tag = tag

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

    def draw(self):
        for position in self.positions:
            draw_object(self.color, position, self.tag)

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
        self.color = FOOD_COLOR
        self.tag = 'food'

        self.create()

    def create(self):
        self.position = (random.randint(0, MAX_X - 1) * GRID_SIZE, random.randint(0, MAX_Y - 1) * GRID_SIZE)
    def draw(self):
        draw_object(self.color, self.position, self.tag)

# 게임 루프
def next_turn(player1, player2, food):


    player1.can_input = True
    player2.can_input = True

    canvas.delete("all")

    player1.move()
    player2.move()

    # 스네이크가 음식을 먹었는지
    if player1.check_eat(food) or player2.check_eat(food):
        food.create()

    show_info(player1.length, player2.length)

    player1.draw()
    player2.draw()
    food.draw()

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

    window.after(UPDATE_RATE, next_turn, player1, player2, food)


def game_over(message):

    canvas.delete('all')
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text=message, fill="red", tag="gameover")

def draw_object(color, pos, tag = ''):
    canvas.create_rectangle(pos[0], pos[1], pos[0] + GRID_SIZE, pos[1] + GRID_SIZE, fill=color, tag=tag)


def show_info(player1_score, player2_score):
    label.config(text="Player 1: {}   Player 2: {}".format(player1_score, player2_score))

if __name__ == '__main__':
    window = Tk()
    window.title("Snake Game")
    window.resizable(False, False)

    # 나중에 실행 시간에 비례해서 몸 길이, 속도 조정
    # score = 0

    label = Label(window, text="Player 1: {}   Player 2: {}".format(0, 0), font=('consolas', 20))
    label.pack()

    canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
    canvas.pack();

    window.update()

    window_width = window.winfo_width()
    window_height = window.winfo_height()
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))

    window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    player1 = Player(PLAYER1_COLOR, (GAME_WIDTH / 2, GAME_HEIGHT / 2 - PLAYER_GAP * GRID_SIZE), DOWN, 'Player1')
    player2 = Player(PLAYER2_COLOR, (GAME_WIDTH / 2, GAME_HEIGHT / 2 + PLAYER_GAP * GRID_SIZE), UP, 'Player2')
    food = Food()

    window.bind('<a>', lambda event: player1.change_direction(LEFT))
    window.bind('<d>', lambda event: player1.change_direction(RIGHT))
    window.bind('<w>', lambda event: player1.change_direction(UP))
    window.bind('<s>', lambda event: player1.change_direction(DOWN))

    window.bind('<Left>', lambda event: player2.change_direction(LEFT))
    window.bind('<Right>', lambda event: player2.change_direction(RIGHT))
    window.bind('<Up>', lambda event: player2.change_direction(UP))
    window.bind('<Down>', lambda event: player2.change_direction(DOWN))

    next_turn(player1, player2, food)

    window.mainloop()
