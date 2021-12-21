# https://ai-creator.tistory.com/523
import pygame  # 1. pygame 선언
import random
from datetime import datetime
from datetime import timedelta

pygame.init()  # 2. pygame 초기화

# 3. pygame에 사용되는 전역변수 선언
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
size = [400, 400]
screen = pygame.display.set_mode(size)

done = False
clock = pygame.time.Clock()
last_moved_time = datetime.now()

KEY_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}


def draw_block(screen, color, position):
    block = pygame.Rect((position[1] * 20, position[0] * 20),
                        (20, 20))
    pygame.draw.rect(screen, color, block)


class Snake:
    def __init__(self):
        self.positions = [(0, 2), (0, 1), (0, 0)]  # 뱀의 위치
        self.direction = ''

    def draw(self):
        for position in self.positions:
            draw_block(screen, GREEN, position)

    def move(self):
        head_position = self.positions[0]
        y, x = head_position
        if self.direction == 'N':
            self.positions = [(y - 1, x)] + self.positions[:-1]
        elif self.direction == 'S':
            self.positions = [(y + 1, x)] + self.positions[:-1]
        elif self.direction == 'W':
            self.positions = [(y, x - 1)] + self.positions[:-1]
        elif self.direction == 'E':
            self.positions = [(y, x + 1)] + self.positions[:-1]

    def grow(self):
        tail_position = self.positions[-1]
        y, x = tail_position
        if self.direction == 'N':
            self.positions.append((y - 1, x))
        elif self.direction == 'S':
            self.positions.append((y + 1, x))
        elif self.direction == 'W':
            self.positions.append((y, x - 1))
        elif self.direction == 'C':
            self.positions.append((y, x + 1))


class Apple:
    def __init__(self, position=(5, 5)):
        self.position = position

    def draw(self):
        draw_block(screen, RED, self.position)


# 4. pygame 무한루프
def runGame():
    global done, last_moved_time
    # 게임 시작 시, 뱀과 사과를 초기화
    snake = Snake()
    apple = Apple()

    while not done:
        clock.tick(10)
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key in KEY_DIRECTION:
                    snake.direction = KEY_DIRECTION[event.key]

        if timedelta(seconds=0.1) <= datetime.now() - last_moved_time:
            snake.move()
            last_moved_time = datetime.now()

        if snake.positions[0] == apple.position:
            snake.grow()
            apple.position = (random.randint(0, 19), random.randint(0, 19))

        if snake.positions[0] in snake.positions[1:]:
            done = True

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    runGame()
    pygame.quit()



# # https://www.youtube.com/watch?v=rtwtOcfYKqc
#
# import pygame
# import sys
# import time
# import random
#
# from pygame.locals import *
#
# WINDOW_WIDTH = 800
# WINDOW_HEIGHT = 600
# GRID_SIZE = 20
# GRID_WIDTH = WINDOW_WIDTH / GRID_SIZE
# GRID_HEIGHT = WINDOW_HEIGHT / GRID_SIZE
#
#
# # 색상
# WHITE = (255, 255, 255)
# RED = (50, 0, 0)
# BLUE = (0, 0, 50)
# GREEN = (0, 50, 0)
# BLACK = (0, 0, 0)
#
#
# # 방향
# LEFT = (-1, 0)
# RIGHT = (1, 0)
# UP = (0, -1)
# DOWN = (0, 1)
#
# FPS = 20
#
# class Player(object):
#     def __init__(self, color, position):
#         self.create(position)
#         self.color = color
#
#     def create(self, position):
#         self.length = 3
#         self.positions = [(position[0] / 2, position[1] / 2)]
#         # 초기 방향 - 플레이어 두 명이면 레디 할 때 누른 키로 설정하게 바꾸기
#         self.dirction = random.choice([LEFT, RIGHT, UP, DOWN])
#
#     def control(self, new_direction):
#         if (new_direction[0] * -1, new_direction[1] * -1) == self.dirction:
#             print("키안눌림")
#             return
#         else:
#             print("키눌림")
#             self.dirction = new_direction
#
#     def move(self):
#         cur = self.positions[0]
#         x, y = self.dirction
#
#         # 화면 넘어가게 X 충돌 처리에 화면 밖인지 확인하기
#         new_head = (cur[0] + (x * GRID_SIZE), cur[1] + (y * GRID_SIZE))
#
#         # 게임 오버 관련 넣기 - 충돌 처리는 게임 로직으로 빼기
#         if new_head in self.positions[1:]:
#             # 게임 종료 관련 컨트롤, 게임 재식작 관련 로직 넣기
#             self.create()
#         else:
#             self.positions.insert(0, new_head)
#             if len(self.positions) > self.length:
#                 self.positions.pop()
#
#     def check_eat(self, feed):
#         if self.positions[0] == feed.position:
#             self.eat()
#             return True
#         return False
#
#     def eat(self):
#         self.length += 1
#
#     def draw(self, surface):
#         for position in self.positions:
#             draw_object(surface, self.color, position)
#
# class Feed(object):
#     def __init__(self):
#         self.position = (0, 0)
#         self.color = GREEN
#         self.create()
#
#     def create(self):
#         self.position = (random.randint(0, GRID_SIZE - 1) * GRID_SIZE, random.randint(0, GRID_SIZE - 1) * GRID_SIZE)
#
#     def draw(self, surface):
#         draw_object(surface, self.color, self.position)
#
# def draw_object(surface, color, pos):
#     rect = pygame.Rect((pos[0], pos[1]), (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(surface, color, rect)
#
# def show_info(length, speed, surface):
#     font = pygame.font.Font(None, 34)
#     text = font.render("Length: " + str(length) + " Speed: " + str(round(speed, 2)), 1, BLACK)
#     pos = text.get_rect()
#     pos.centerx = 150
#     # pos.centery = 0
#     surface.blit(text, pos)
#
#
# if __name__ == '__main__':
#     # 파이게임 초기화
#     pygame.init()
#     # 윈도우 세팅
#     window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), 0, 32)
#
#     # 창 이름 설정
#     pygame.display.set_caption('Python Game')
#
#     # 게임 화면
#     surface = pygame.Surface(window.get_size())
#     surface = surface.convert()
#     surface.fill(WHITE)
#
#     # 게임 시간
#     clock = pygame.time.Clock()
#     # 리핏 값 설정
#     pygame.key.set_repeat(1, 40)
#     # 적용
#     window.blit(surface, (0, 0))
#
#     # 객체 생성
#     player = Player(RED, (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
#     feed = Feed()
#
#
#     # 게임 루프
#     while True:
#
#         for event in pygame.event.get():
#             if event.type == QUIT:
#                 pygame.quit()
#                 sys.exit()
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_LEFT:
#                     player.control(LEFT)
#                 elif event.type == pygame.K_RIGHT:
#                     player.control(RIGHT)
#                 elif event.key == pygame.K_UP:
#                     player.control(UP)
#                 elif event.type == pygame.K_DOWN:
#                     player.control(DOWN)
#
#             surface.fill(WHITE)
#             player.move()
#             # 먹었으면 재 생성
#             if player.check_eat(feed):
#                 feed.create()
#
#             speed = (FPS + player.length) / 2
#             player.draw(surface)
#             feed.draw(surface)
#
#             show_info(player.length, speed, surface)
#
#             # 윈도우 다시 그리기
#             window.blit(surface, (0, 0))
#             pygame.display.flip()
#             pygame.display.update()
#             clock.tick(speed)