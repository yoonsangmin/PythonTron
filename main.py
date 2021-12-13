# 참고 영상 출처: https://www.youtube.com/watch?v=bfRwxS5d0SI&list=PLVZH-JVY27dllGu0HgjWw6dKjq-3DYTG5

from tkinter import *
import random

# 상수
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPACE_SIZE = 10

# 초기 값 작을 수록 빠름
SPEED = 10
# 초기 몸 길이
BODY_PARTS = 3
PLAYER_COLOR =  "#00FF00"

FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

# 한 프레임에 키 입력 하나만 받게
CAN_INPUT = True

class Snake:

    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=PLAYER_COLOR, tag="snake")
            self.squares.append(square)

class Food:

    def __init__(self):

        x = random.randint(0, GAME_WIDTH/SPACE_SIZE - 1) * SPACE_SIZE
        y = random.randint(0, GAME_HEIGHT/SPACE_SIZE - 1) * SPACE_SIZE

        self.coordinate = [x, y]

        canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

# 스네이크 업데이트
def next_turn(snake, food):

    global CAN_INPUT

    CAN_INPUT = True

    x, y = snake.coordinates[0]

    if direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE
    elif direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE


    snake.coordinates.insert(0, (x, y))

    # 충돌 처리
    if check_collisions(snake):
        game_over()
        return

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=PLAYER_COLOR)

    snake.squares.insert(0, square)

    # 스네이크가 음식을 먹었는지
    if x == food.coordinate[0] and y == food.coordinate[1]:

        global score

        score += 1

        label.config(text="Score:{}".format(score))

        canvas.delete("food")

        food = Food()

    else:
        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]


    window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):

    global CAN_INPUT

    if CAN_INPUT == False:
        return
    # 이전 방향 - 나중에 스네이크로 옮기기
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

    CAN_INPUT = False

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

def game_over():

    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas', 70), text="Game Over", fill="red", tag="gameover")


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# 나중에 실행 시간에 비례해서 몸 길이, 속도 조정
score = 0
direction = 'down'

label = Label(window, text="Score: {}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack();

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()

# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
