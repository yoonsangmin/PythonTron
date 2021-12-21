import pygame

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, 50, 50))

    def move(self, x_add, y_add):
        self.x += x_add
        self.y += y_add