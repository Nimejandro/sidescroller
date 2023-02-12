import pygame
from pygame.locals import *
import os
import sys
import math


class player():
    # skapar listor med run och jump bilderna. 7 av varje
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8,10)]
    """run = [pygame.image.load(os.path.join('images', str(x) + '.png'))
           for x in range(8, 10)]"""
    jump = [pygame.image.load(os.path.join(
        'images', str(x) + '.png')) for x in range(1, 8)]
    print(len(jump), len(run))
    slide = [pygame.image.load(os.path.join('images', 'S1.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(
        os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')), pygame.image.load(os.path.join('images', 'S5.png'))]
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False

    def draw(self, win):
        if self.jumping:
            # 1.2 är gravitationskonstant. Vi har 109 delar av vårat hopp (0 till 108), varje del motsvarar ett index i jumpList
            self.y -= self.jumpList[self.jumpCount] * 1.2
            # Vi heltalsdelar med 18 för att vårt hopp är 108 stort med 108//18 = 6. Vi laddar in 7 bilder, så 0 = 1.png, 18 = 2.png.... o.s.v.
            win.blit(self.jump[self.jumpCount//18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0  # Detta är för att nå marknivå så fort vi har nått marknivå
                self.jumping = False
                self.runCount = 0
                self.y = 313
        elif self.sliding or self.slideUp:
            if self.slideCount < 10: #När karaktären slidear ned
                self.y += 4
            elif self.slideCount == 40: #När karaktären träffar väntpunkten och ska resa sig upp
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            if self.slideCount >= 55: #När karaktären har rest sig upp
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.y = 313
            win.blit(self.slide[self.slideCount//5], (self.x, self.y))
            self.slideCount += 2
        else:
            if self.runCount > 19:
                self.runCount = 0
            win.blit(self.run[self.runCount//10], (self.x,self.y))
            self.runCount += 1
        """else:
            if self.runCount > 19:
                self.runCount = 0
            # 0 = 8.png, 1 = 9.png ... o.s.v.
            win.blit(self.run[self.runCount//10], (self.x, self.y))
            self.runCount += 1"""


def button(screen, position, text, size, colors="white on blue"):
    fg, bg = colors.split(" on ")
    font = pygame.font.SysFont("Arial", size)
    text_render = font.render(text, 1, fg)
    x, y, w , h = text_render.get_rect()
    x, y = position
    pygame.draw.line(screen, (150, 150, 150), (x, y), (x + w , y), 5)
    pygame.draw.line(screen, (150, 150, 150), (x, y - 2), (x, y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x, y + h), (x + w , y + h), 5)
    pygame.draw.line(screen, (50, 50, 50), (x + w , y+h), [x + w , y], 5)
    pygame.draw.rect(screen, bg, (x, y, w , h))
    print(screen.blit(text_render, (x, y)))
    return screen.blit(text_render, (x, y))


def menu(screen):
    b1 = button(screen, (300, 100), "Easy", 50, "red on green")
    b2 = button(screen, (300, 200), "Medium", 50, "blue on green")
    b3 = button(screen, (300, 300), "Hard", 50, "white on green")
    while True:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # check when you click if the coordinates of the pointer are in the rectangle of the buttons
                if b1.collidepoint(pygame.mouse.get_pos()):
                    return 1
                elif b2.collidepoint(pygame.mouse.get_pos()):
                    return 2
                elif b3.collidepoint(pygame.mouse.get_pos()):
                    return 5
        pygame.display.update()


def redrawWindow(win, bg, bgX, bgX2, runner):
    win.blit(bg, (bgX, 0))  # draws our first bg image
    win.blit(bg, (bgX2, 0))  # draws the seconf bg image
    runner.draw(win) # NEW
    pygame.display.update()  # updates the screen

def keyboardInputs(runner):
    keys = pygame.key.get_pressed() #initiera tangentinputs
    up = keys[pygame.K_SPACE] or keys[pygame.K_UP]
    slide = keys[pygame.K_DOWN]
    if up:
        if not (runner.jumping):
            runner.jumping = True
    if slide:
        if not (runner.sliding):
            runner.sliding = True

def main():
    W, H = 800, 447
    pygame.init()
    win = pygame.display.set_mode((W, H))
    pygame.display.set_caption('Nimas Side Scroller')

    diff = menu(win)
    pygame.time.set_timer(USEREVENT+1, 500//diff) # Sets the timer for 0.5 seconds
    bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
    bgX = 0
    bgX2 = bg.get_width()

    clock = pygame.time.Clock()
    run = True
    speed = 30  # Ändra hastigheten här
    runner = player(200, 313, 64, 64)
    while run:
        redrawWindow(win, bg, bgX, bgX2, runner)
        keyboardInputs(runner)
        bgX -= 1.4*diff  # Bakgrunden rör sig baklänges
        bgX2 -= 1.4*diff

        if bgX < bg.get_width() * -1:  # Om bakgrunden har blivit "negativ" har vi nått kanten och då omställer vi
            bgX = bg.get_width()
        
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()

        for event in pygame.event.get():  
            if event.type == pygame.QUIT: 
                run = False    
                pygame.quit() 
                quit()
            
            if event.type == USEREVENT+1: # Checks if timer goes off
                speed += 1 # Increases speed
                #Spelet ökar hastighet varje 0.5 sekunder. USEREVENT är ett inbyggt allokeringselement i pygame som vi utnyttjar oss av.
        clock.tick(speed)  # Få spelet att simuleras genom clock.tick

main()
