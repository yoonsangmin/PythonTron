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

class Player:
    def __init__(self, position, color):
        self.positions = [position]
        self.color = color
        self.prev_direction = None

        self.is_p_en = False

    def draw(self, surface):
        for position in self.positions:
            pygame.draw.rect(surface, self.color, (position[0], position[1], GRID_SIZE, GRID_SIZE))

    def move(self, direction):

        if self.prev_direction != None and (direction[0] * -1, direction[1] * -1) == self.prev_direction:
            return

        x, y = self.positions[0]
        x += direction[0] * GRID_SIZE
        y += direction[1] * GRID_SIZE

        print(x, y)
        self.positions.insert(0, (x, y))

        self.prev_direction = direction

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