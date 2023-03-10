import pygame
from pygame.locals import *
import os
import sys
import math
import random

class saw(object):
    rotate = [pygame.image.load(os.path.join('images', 'SAW0.PNG')),pygame.image.load(os.path.join('images', 'SAW1.PNG')),pygame.image.load(os.path.join('images', 'SAW2.PNG')),pygame.image.load(os.path.join('images', 'SAW3.PNG'))]
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotateCount = 0
        self.vel = 1.4

    def draw(self,win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 20, self.height - 5)  # Defines the accurate hitbox for our character 
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        if self.rotateCount >= 8:  # This is what will allow us to animate the saw
            self.rotateCount = 0
        win.blit(pygame.transform.scale(self.rotate[self.rotateCount//2], (64,64)), (self.x,self.y))  # scales our image down to 64x64 before drawing
        self.rotateCount += 1
    
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] + rect[3] > self.hitbox[1]:
                return True
        return False

class spike(saw):  # We are inheriting from saw
    img = pygame.image.load(os.path.join('images', 'spike.png'))
    def draw(self,win):
        self.hitbox = (self.x + 10, self.y, 28,315)  # defines the hitbox
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        win.blit(self.img, (self.x,self.y))
    def collide(self, rect):
        if rect[0] + rect[2] > self.hitbox[0] and rect[0] < self.hitbox[0] + self.hitbox[2]:
            if rect[1] < self.hitbox[3]:
                return True
        return False

class player(object):
    # skapar listor med run och jump bilderna
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8,10)]
    jump = [pygame.image.load(os.path.join(
        'images', str(x) + '.png')) for x in range(1, 8)]
    print(len(jump), len(run))
    slide = [pygame.image.load(os.path.join('images', 'S1.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(
        os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')), pygame.image.load(os.path.join('images', 'S5.png'))]
    jumpList = [1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-3,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4,-4]
    fall = pygame.image.load(os.path.join('images','0.png'))

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
        self.falling = False

    def draw(self, win):
        if self.falling:
            win.blit(self.fall, (self.x, self.y + 30))
        if self.jumping:
            self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10)
            # 1.2 ??r gravitationskonstant. Vi har 109 delar av v??rat hopp (0 till 108), varje del motsvarar ett index i jumpList
            self.y -= self.jumpList[self.jumpCount] * 1.
            # Vi heltalsdelar med 18 f??r att v??rt hopp ??r 108 stort med 108//18 = 6. Vi laddar in 7 bilder, s?? 0 = 1.png, 18 = 2.png.... o.s.v.
            win.blit(self.jump[self.jumpCount//18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0  # Detta ??r f??r att n?? markniv?? s?? fort vi har n??tt markniv??
                self.jumping = False
                self.runCount = 0
                self.y = 313
        elif self.sliding or self.slideUp:
            if self.slideCount < 17: #N??r karakt??ren slidear ned
                self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10)
                self.y +=4
            elif self.slideCount == 30: #N??r karakt??ren tr??ffar v??ntpunkten och ska resa sig upp
                self.y -= 19
                self.sliding = False
                self.slideUp = True
            elif self.slideCount > 20 and self.slideCount < 80: # NEW
                self.hitbox = (self.x,self.y+3,self.width-8,self.height-35)
            if self.slideCount >= 88: #N??r karakt??ren har rest sig upp
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.y = 313
                self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-10)
            win.blit(self.slide[self.slideCount//8], (self.x, self.y))
            self.slideCount += 2
        else:
            if self.runCount > 19:
                self.runCount = 0
            win.blit(self.run[self.runCount//10], (self.x,self.y))
            self.runCount += 1
            self.hitbox = (self.x+ 4,self.y,self.width-24,self.height-13)
        pygame.draw.rect(win, (255,0,0), self.hitbox, 2)
        
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


def redrawWindow(win, bg, bgX, bgX2, runner, obstacles, score):
    win.blit(bg, (bgX, 0))  # draws our first bg image
    win.blit(bg, (bgX2, 0))  # draws the seconf bg image
    runner.draw(win)
    largeFont = pygame.font.SysFont('comicsans', 30)
    text = largeFont.render('Score: ' + str(score), 1, (255,255,255))
    win.blit(text, (600, 10))
    # Nytt: Loopar genom alla hinder
    for obstacle in obstacles:
        obstacle.draw(win)

    pygame.display.update()

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

def endScreen(runner, score, win, bg, W):                 
    
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN: #Musklick = starta om
                run = False
                main()
        win.blit(bg, (0,0))
        largeFont = pygame.font.SysFont('comicsans', 80)
        lastScore = largeFont.render('Best Score: ' + str(updateFile(score)),1,(255,255,255))
        currentScore = largeFont.render('Score: '+ str(score),1,(255,255,255))
        win.blit(lastScore, (W/2 - lastScore.get_width()/2,150))
        win.blit(currentScore, (W/2 - currentScore.get_width()/2, 240))
        pygame.display.update()
    score = 0

def updateFile(score):
    f = open('scores.txt','r') # Se till att ha skapat en ???score.txt??? i mappen
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        print("!!!!")
        f.close() # st??nger filen
        file = open('scores.txt', 'w') # ??ppnar upp igen och skriver p?? den
        file.write(str(score)) # skriver po??ngen p?? filen
        file.close() # st??nger och avslutar

        return score 
               
    return last

def main():
    W, H = 800, 447
    pygame.init()
    win = pygame.display.set_mode((W, H))
    pygame.display.set_caption('Nimas Side Scroller')

    diff = menu(win)
    pygame.time.set_timer(USEREVENT+1, 500//diff) # Sets the timer for 0.5 seconds
    #Ny
    pygame.time.set_timer(USEREVENT+2, random.randrange(2000, 3500)) # Will trigger every 2 - 3.5 seconds
    bg = pygame.image.load(os.path.join('images', 'bg.png')).convert()
    bgX = 0
    bgX2 = bg.get_width()

    clock = pygame.time.Clock()
    run = True
    speed = 30  # ??ndra hastigheten h??r
    runner = player(200, 313, 64, 64)
    
    score = 0
    obstacles = []
    # ??r ??ver main-loopen
    fallSpeed = 0 #??r till f??r att kolla hastigheten av d??danimationen
    pause = 0 #N??r denna har n??tt ett visst v??rde pausas spelet
    while run:
        redrawWindow(win, bg, bgX, bgX2, runner, obstacles, score)
        keyboardInputs(runner)
        bgX -= 1.4*diff  # Bakgrunden r??r sig bakl??nges
        bgX2 -= 1.4*diff
        if bgX < bg.get_width() * -1:  # Om bakgrunden har blivit "negativ" har vi n??tt kanten och d?? omst??ller vi
            bgX = bg.get_width()
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()
        if pause > 0: # Kollar om vi har f??rlorat, ??kar pause variabeln
            pause += 1
        if pause > fallSpeed * 2:
            endScreen(runner, score, win, bg, W)
        for obstacle in obstacles:
            if obstacle.collide(runner.hitbox):
                runner.falling = True
                if pause == 0: # Kollar om vi redan har f??rlorat eller inte
                    fallSpeed = speed 
                    pause = 1
            obstacle.x -= 1.4*diff
            if obstacle.x < obstacle.width * -1: # Om hindret ??r utanf??r sk??rmen tar vi bort den
                obstacles.pop(obstacles.index(obstacle))

        for event in pygame.event.get():  
            if event.type == pygame.QUIT: 
                run = False    
                pygame.quit() 
                quit()
            
            

            if event.type == USEREVENT+1 and speed < 100: # Checks if timer goes off
                
                if speed < 100:
                    speed += 1 # Increases speed
                    #Spelet ??kar hastighet varje 0.5 sekunder. USEREVENT ??r ett inbyggt allokeringselement i pygame som vi utnyttjar oss av.
            if event.type == USEREVENT+2:
                score += 10
                print(score)
                r = random.randrange(0,2)
                if r == 0:
                    obstacles.append(saw(810, 310, 64, 64))
                elif r == 1:
                    obstacles.append(spike(810, 0, 48, 310))
            # G??r in i: for event in pygame.event.get() loopen
        clock.tick(speed)  # F?? spelet att simuleras genom clock.tick
main()
