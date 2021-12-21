from network import Networking
import pygame

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

ip = '192.168.0.2'
port = 8080

pygame.init()

surface = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))

n = Networking(ip, port)
con = n.connect()

p = n.recv(con)
p_en = None
loop = True

is_start = False

fps = pygame.time.Clock()

while loop == True:
    p_en = n.recv(con)
    n.send(con, p)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT]:
        p.change_direction(LEFT)
    elif key[pygame.K_RIGHT]:
        p.change_direction(RIGHT)
    elif key[pygame.K_UP]:
        p.change_direction(UP)
    elif key[pygame.K_DOWN]:
        p.change_direction(DOWN)

    if is_start == True:
        p.move()

    surface.fill(BLACK)
    p.draw(surface)
    p_en.draw(surface)
    pygame.display.flip()

    if p.check_collisions(p_en) or p_en.check_collisions(p):
        n.send(con, p)
        loop = False

    if p_en.is_p_en == True:
        is_start = True


    fps.tick(3)  # fps는 60

pygame.quit()
quit()