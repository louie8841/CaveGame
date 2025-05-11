import sys, pygame, time, os
from random import randint
from pygame.locals import QUIT, Rect, KEYDOWN, K_SPACE, MOUSEBUTTONDOWN

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Cave Game')
FPSCLOCK = pygame.time.Clock()

def runGame():
    global score

    walls = 80
    ship_y = 250
    velocity = 0
    score = 0
    slope = randint(1, 6)
    sysfont = pygame.font.SysFont(None, 36)
    ship_image = pygame.image.load("rocket.png")
    holes = []
    for xpos in range(walls):
        holes.append(Rect(xpos * 10, 100, 10, 400))
    game_over = False

    while True:
        is_space_down = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    is_space_down = True

        if not game_over:
            score += 10
            velocity += -3 if is_space_down else 3
            ship_y += velocity

            edge = holes[-1].copy()
            test = edge.move(0, slope)
            if test.top <= 0 or test.bottom >= 600:
                slope = randint(1, 6) * (-1 if slope > 0 else 1)
                edge.inflate_ip(0, -20)
            edge.move_ip(10, slope)
            holes.append(edge)
            del holes[0]
            holes = [x.move(-10, 0) for x in holes]

            if holes[0].top > ship_y or holes[0].bottom < ship_y + 30:
                game_over = True

        SURFACE.fill((0, 0, 0))
        for hole in holes:
            pygame.draw.rect(SURFACE, (255, 255, 255), hole)
        SURFACE.blit(ship_image, (0, ship_y))
        score_image = sysfont.render("score is {}".format(score),
                                     True, (255, 255, 255))
        SURFACE.blit(score_image, (600, 20))

        if game_over:
            restart()

        pygame.display.update()
        FPSCLOCK.tick(15)

def main():
    font = pygame.font.SysFont(None, 40)
    while True:
        SURFACE.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                time.sleep(1)
                runGame()
        txt = font.render("Click anywhere to start", True, (255, 255, 255))
        SURFACE.blit(txt, (250, 300))
        pygame.display.update()
        FPSCLOCK.tick(15)

def getBest(score):
    global best
    with open('data.dat', 'r') as f:
        if f.read != "":
            bestf = f.read()
            if score > int(bestf):
                best = score
            else:
                best = bestf
        else:
            best = score
    with open('data.dat', 'w') as f:
        f.write(str(best))

def restart():
    global score, best
    font = pygame.font.SysFont(None, 40)
    while True:
        SURFACE.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                time.sleep(1)
                runGame()
        getBest(score)
        txt = font.render("Click anywhere to restart", True, (255, 255, 255))
        txt2 = font.render(f"Your score is {score}", True, (255, 255, 255))
        txt3 = font.render(f"Your best score is {best}", True, (255, 255, 255))
        SURFACE.blit(txt, (250, 300))
        SURFACE.blit(txt2, (300, 250))
        SURFACE.blit(txt3, (260, 200))
        pygame.display.update()
        FPSCLOCK.tick(15)

if __name__ == '__main__':
    main()
