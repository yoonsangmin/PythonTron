from network import Networking
import pygame

ip = '192.168.0.2'
port = 8080

pygame.init()

size = 500
white = (255, 255, 255)

surface = pygame.display.set_mode((size, size))

n = Networking(ip, port)
con = n.connect()

p = n.recv(con)
p_en = None
loop = True

while loop == True:
    p_en = n.recv(con)
    n.send(con, p)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            loop = False

    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT] and p.x > 0:
        p.move(-1, 0)
    elif key[pygame.K_RIGHT] and p.x < 450:
        p.move(1, 0)
    elif key[pygame.K_UP] and p.y > 0:
        p.move(0, -1)
    elif key[pygame.K_DOWN] and p.y < 450:
        p.move(0, 1)

    surface.fill(white)
    p.draw(surface)
    p_en.draw(surface)
    pygame.display.flip()

pygame.quit()
quit()