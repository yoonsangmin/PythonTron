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

# 게임 업데이트 간격
UPDATE_RATE = 50
# 초기 몸 길이
INITIAL_LENGTH = 3
PLAYER_COLOR = "#00FF00"

FOOD_COLOR = "#FF0000"
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
        print(self.position)

# 게임 루프
def next_turn(snake, food):


    snake.can_input = True


    canvas.delete("all")
    snake.move()

    # 스네이크가 음식을 먹었는지
    if snake.check_eat(food):
        global score
        score += 1
        food.create()

    show_info(score)

    snake.draw()
    food.draw()

    # 충돌 처리
    if check_collisions(snake):
        game_over()
        return

    window.after(UPDATE_RATE, next_turn, snake, food)



def check_collisions(player):
    head = player.positions[0]

    if head[0] < 0 or head[0] >= GAME_WIDTH:
        return True
    elif head[1] < 0 or head[1] >= GAME_HEIGHT:
        return True

    # 게임 오버 관련 넣기 - 충돌 처리는 게임 로직으로 빼기
    if head in player.positions[1:]:
        # 게임 종료 관련 컨트롤, 게임 재식작 관련 로직 넣기
        return True

    return False

def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="Game Over", fill="red", tag="gameover")

def draw_object(color, pos, tag = ''):
    canvas.create_rectangle(pos[0], pos[1], pos[0] + GRID_SIZE, pos[1] + GRID_SIZE, fill=color, tag=tag)


def show_info(score):
    label.config(text="Score:{}".format(score))

if __name__ == '__main__':
    window = Tk()
    window.title("Snake Game")
    window.resizable(False, False)

    # 나중에 실행 시간에 비례해서 몸 길이, 속도 조정
    score = 0

    label = Label(window, text="Score: {}".format(score), font=('consolas', 40))
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

    player = Player(PLAYER_COLOR, (GAME_WIDTH / 2, GAME_HEIGHT / 2), UP, 'Player')
    food = Food()

    window.bind('<Left>', lambda event: player.change_direction(LEFT))
    window.bind('<Right>', lambda event: player.change_direction(RIGHT))
    window.bind('<Up>', lambda event: player.change_direction(UP))
    window.bind('<Down>', lambda event: player.change_direction(DOWN))

    next_turn(player, food)

    window.mainloop()
