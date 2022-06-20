import pygame
import os
from random import randrange

pygame.mixer.init() #sound
pygame.font.init() #text


WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy bird")
FPS = 60 #frame per second

FLAPPY_VEL = 5
TUBE_VEL = 4

WHITE = (255, 255, 255)
GREEN = (104, 211, 0)

FLAPPY_POS = 200

WING_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'wing.mp3'))
POINT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'point.mp3'))
HIT_SOUND =  pygame.mixer.Sound(os.path.join('Assets', 'hit.mp3'))


BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'background.png')), (WIDTH, HEIGHT))

POINT_COUNTER_FONT = pygame.font.SysFont('comicsan', 100)
TEXT_FONT = pygame.font.SysFont('comicsan', 150)

FLAPPY_WIDTH = 55
FLAPPY_HEIGHT = 40

HIT = pygame.USEREVENT + 1

TUBE_WIDTH = 3*FLAPPY_WIDTH//2

DOWNPIPE = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Mario_pipe.png')), (TUBE_WIDTH, HEIGHT))

UPPIPE = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'Mario_pipe.png')), (TUBE_WIDTH, HEIGHT)), 180
)

FLAPPY = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'yellow_flappy.png')), (FLAPPY_WIDTH, FLAPPY_HEIGHT))

FLAPPY_45 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'yellow_flappy.png')), (FLAPPY_WIDTH, FLAPPY_HEIGHT)), 45)
FLAPPY_315 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'yellow_flappy.png')), (FLAPPY_WIDTH, FLAPPY_HEIGHT)), -45)
FLAPPY_270 = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(
    os.path.join('Assets', 'yellow_flappy.png')), (FLAPPY_WIDTH, FLAPPY_HEIGHT)), 90)

def draw_window(flappy, uptube, downtube, score, FLAPPY_ROT):

    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(FLAPPY_ROT[0], (flappy.x, flappy.y))
    for i in range(4):
        WIN.blit(UPPIPE, (uptube[i].x, uptube[i].y))
        WIN.blit(DOWNPIPE, (downtube[i].x, downtube[i].y))
    res = POINT_COUNTER_FONT.render(str(score[0]), 1, WHITE)
    WIN.blit(res, (FLAPPY_POS + FLAPPY_WIDTH, 125))
    pygame.display.update()

def flappy_movement_handler(t1, flappy, FLAPPY_ROT, bool_flappy_rot):
    t2 = pygame.time.get_ticks()

    if t2 - t1 < 200:
        flappy.y -= FLAPPY_VEL
        if not bool_flappy_rot[0]:

            FLAPPY_ROT[0] = FLAPPY_45
            bool_flappy_rot[0] = True
            bool_flappy_rot[1] = False
            bool_flappy_rot[2] = False

    elif 500 > t2 - t1 > 300:
        flappy.y += FLAPPY_VEL
        if not bool_flappy_rot[1]:
            FLAPPY_ROT[0] = FLAPPY
            bool_flappy_rot[0] = False
            bool_flappy_rot[1] = True
            bool_flappy_rot[2] = False

    elif t2 - t1 > 500:
        flappy.y += 3*FLAPPY_VEL//2
        if not bool_flappy_rot[2]:
            FLAPPY_ROT[0] = FLAPPY_315
            bool_flappy_rot[0] = False
            bool_flappy_rot[1] = False
            bool_flappy_rot[2] = True

def tube_movement_handler(uptube, downtube, flappy, colli_uptube, score):
    tmp = 0
    for i in range(4):
        if flappy.colliderect(colli_uptube[i]) or flappy.colliderect(downtube[i]):
            pygame.event.post(pygame.event.Event(HIT))
        else:
            for j in range(TUBE_VEL): #j necerssaire car on a pas toujours l'egalite parfaite i.e j = 0
                if uptube[i].x == FLAPPY_POS - TUBE_WIDTH -j:
                    score[0] += 1
                    POINT_SOUND.play()
            if uptube[i].x + TUBE_WIDTH <= 0:
                tmp = randrange(TUBE_WIDTH, HEIGHT - 3 * TUBE_WIDTH)
                uptube.append(pygame.Rect(13 * TUBE_WIDTH, - HEIGHT + tmp, TUBE_WIDTH, tmp))
                uptube.remove(uptube[i])
                colli_uptube.append(pygame.Rect(13 * TUBE_WIDTH, 0, TUBE_WIDTH, tmp))
                colli_uptube.remove(colli_uptube[i])
            if downtube[i].x + TUBE_WIDTH <= 0:
                downtube.append(pygame.Rect(13 * TUBE_WIDTH, tmp + 4 * FLAPPY_HEIGHT, TUBE_WIDTH, HEIGHT - tmp - (4*FLAPPY_HEIGHT)))
                downtube.remove(downtube[i])
            uptube[i].x -= TUBE_VEL
            colli_uptube[i].x -= TUBE_VEL
            downtube[i].x -= TUBE_VEL

def draw_start():
    WIN.blit(BACKGROUND, (0, 0))
    draw_text = POINT_COUNTER_FONT.render('Press SPACE to start', 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()

def draw_lose(score):
    WIN.blit(BACKGROUND, (0, 0))
    draw_text = POINT_COUNTER_FONT.render('Score : '+str(score[0]), 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)

def main():
    flappy = pygame.Rect(FLAPPY_POS, HEIGHT/2 - FLAPPY_HEIGHT/2, FLAPPY_WIDTH, FLAPPY_HEIGHT)
    uptube = []
    downtube = []
    delta = []
    colli_uptube = []
    #tableau de boolenn qui indique a quelle rotation on est
    bool_flappy_rot = [False, False, False] #-45 degre +45 degree +180 degree
    for i in range(4):

        delta.append(randrange(TUBE_WIDTH, HEIGHT - 3 * TUBE_WIDTH))
        uptube.append(pygame.Rect(500 + i*7*TUBE_WIDTH//2, - HEIGHT + delta[i], TUBE_WIDTH, delta[i]))
        colli_uptube.append(pygame.Rect(500 + i * 7 * TUBE_WIDTH // 2, 0, TUBE_WIDTH, delta[i]))
        downtube.append(pygame.Rect(500 + i * 7 * TUBE_WIDTH // 2, delta[i] + 4 * FLAPPY_HEIGHT, TUBE_WIDTH, HEIGHT - delta[i] - (4*FLAPPY_HEIGHT)))

    clock = pygame.time.Clock()
    run = True
    start = False
    t1 = 0
    score = [0]
    FLAPPY_ROT = [FLAPPY]

    while run:
        clock.tick(FPS)
        while not start:
            draw_start()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        WING_SOUND.play()
                        t1 = pygame.time.get_ticks()
                        start = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    WING_SOUND.play()
                    t1 = pygame.time.get_ticks()
            if event.type == HIT:
                HIT_SOUND.play()
                draw_lose(score)
                main()

        tube_movement_handler(uptube, downtube, flappy, colli_uptube, score)
        flappy_movement_handler(t1, flappy, FLAPPY_ROT, bool_flappy_rot)
        draw_window(flappy, uptube, downtube, score, FLAPPY_ROT)

if __name__ == "__main__":
    main()
