import pygame,sys,random
from pygame.locals import *
pygame.init()
clock=pygame.time.Clock()
sw=600
sh=600
screen=pygame.display.set_mode((sw,sh))
pygame.display.set_caption("Dinner")
font=pygame.font.SysFont("Calibri",30)
start=pygame.font.SysFont("Calibri",30)
restart=pygame.font.SysFont("Calibri",30)
score_text=pygame.font.SysFont("Calibri",10)
choice=0

red=(150,4,2)
purple=(73,5,92)
white=(255,255,255)
yellow=(255,255,0)
turquoise=(54,255,255)
gold=(255,185,8)
color_list=[purple,turquoise]
random.shuffle(color_list)

def start():
    while True:
        screen.fill((0,40,10))
        start=font.render("Press space to start",True,(255,255,255))
        screen.blit(start,(150,250))
        if pygame.key.get_pressed()[K_SPACE]:
            reset()
        terminate()
        pygame.display.update()

def terminate():
    for event in pygame.event.get():
        if event.type==QUIT or pygame.key.get_pressed()[K_ESCAPE]:
            pygame.quit()
            sys.exit()

def reset():
    player.size1=50
    player.size2=50
    player.color=color_list[choice]
    player.define()
    food.define()
    monster.define()
    while True:
        terminate()
        screen.fill((0, 20, 40))
        food.feed()
        monster.attack()
        wall1.draw()
        # wall2.draw()
        player.move(wall1)
        # player.move(wall2)
        clock.tick(60)
        pygame.display.update()

class Player:
    def __init__(self):
        self.x=10
        self.y=300
        self.size1=50
        self.size2=50
        self.color=color_list[choice]
        self.movespeed=10

    def define(self):
        self.player=pygame.Rect((self.x,self.y),(self.size1,self.size2))

    def move(self,wall1):
        if pygame.key.get_pressed()[K_UP] and self.player.top>0:
            if self.player.colliderect(wall1.xwall) and abs(wall1.wall.bottom-self.player.top)<10 and abs(wall1.xwall.left-self.player.right)>10 and abs(wall1.xwall.right-self.player.left)>10:
                self.player.y+=0
            else:
                self.player.y-=self.movespeed
        if pygame.key.get_pressed()[K_DOWN] and self.player.bottom<sh:
            if self.player.colliderect(wall1.xwall) and abs(wall1.xwall.top-self.player.bottom)<10 and abs(wall1.xwall.left-self.player.right)>10 and abs(wall1.xwall.right-self.player.left)>10:
                self.player.y+=0
            else:
                self.player.y+=self.movespeed
        if pygame.key.get_pressed()[K_LEFT] and self.player.left>0:
            if self.player.colliderect(wall1.xwall) and abs(wall1.xwall.right-self.player.left)<10 and abs(wall1.xwall.bottom-self.player.top)>9 and abs(wall1.xwall.top-self.player.bottom)>9:
                self.player.x+=0
            else:
                self.player.x-=self.movespeed
        if pygame.key.get_pressed()[K_RIGHT] and self.player.right<sw:
            if self.player.colliderect(wall1.xwall) and abs(wall1.wall.left-self.player.right)<5 and abs(wall1.xwall.bottom-self.player.top)>9 and abs(wall1.xwall.top-self.player.bottom)>9:
                self.player.x+=0
            else:
                self.player.x+=self.movespeed
        pygame.draw.rect(screen,self.color,self.player)



class Food:
    def __init__(self,x,y,size1,size2,color,movex,movey):
        self.x=x
        self.y=y
        self.size1=size1
        self.size2=size2
        self.color=color
        self.movex=movex
        self.movey=movey

    def define(self):
        self.food=pygame.Rect((self.x,self.y),(self.size1,self.size2))

    def feed(self):
        global choice
        self.food.x+=self.movex
        self.food.y+=self.movey

        pygame.draw.rect(screen,self.color,self.food)

        if self.food.right>=sw or self.food.left<=0:
            self.movex*=-1
        if self.food.top<=0 or self.food.bottom>=sh:
            self.movey*=-1

        if player.player.colliderect(self.food):
            choice+=1
            if choice==len(color_list):
                choice=0
            player.color=color_list[choice]
            del self.food
            rc1=random.randrange(0,550)
            rc2=random.randrange(0,550)
            self.food=pygame.Rect((rc1,rc2),(self.size1,self.size2))
            player.size1+=4
            player.size2+=4
            player.player=pygame.Rect((player.player.x,player.player.y),(player.size1,player.size2))

        if self.food.colliderect(monster.monster) or self.food.colliderect(wall1.wall):
            tolerance=10
            if abs(monster.monster.right-self.food.left)<tolerance or abs(wall1.wall.right-self.food.left)<tolerance and self.movex<0:
                self.movex*=-1
            if abs(monster.monster.left-self.food.right)<tolerance or abs(wall1.wall.left-self.food.right)<tolerance and self.movex>0:
                self.movex*=-1
            if abs(monster.monster.bottom-self.food.top)<tolerance or abs(wall1.wall.bottom-self.food.top)<tolerance and self.movey<0:
                self.movey*=-1
            if abs(monster.monster.top-self.food.bottom)<tolerance or abs(wall1.wall.top-self.food.bottom)<tolerance and self.movey>0:
                self.movey*=-1


class Monster:
    def __init__(self,x,y,size1,size2,color,movex,movey):
        self.x=x
        self.y=y
        self.size1=size1
        self.size2=size2
        self.color=color
        self.movex=movex
        self.movey=movey

    def define(self):
        self.monster=pygame.Rect((self.x,self.y),(self.size1,self.size2))

    def attack(self):
        tolerance=10
        self.monster.x+=self.movex
        self.monster.y+=self.movey

        pygame.draw.rect(screen,self.color,self.monster)

        if self.monster.right>=sw or self.monster.left<=0:
            self.movex*=-1
        if self.monster.top<=0 or self.monster.bottom>=sh:
            self.movey*=-1

        if self.monster.colliderect(food.food) or self.monster.colliderect(wall1.wall):

            if abs(food.food.left-self.monster.right)<tolerance or abs(wall1.wall.left-self.monster.right)<tolerance and self.movex>0:
                self.movex*=-1
            if abs(food.food.right-self.monster.left)<tolerance or abs(wall1.wall.right-self.monster.left)<tolerance and self.movex<0:
                self.movex*=-1
            if abs(food.food.top-self.monster.bottom)<tolerance or abs(wall1.wall.top-self.monster.bottom)<tolerance and self.movey>0:
                self.movey*=-1
            if abs(food.food.bottom-self.monster.top)<tolerance or abs(wall1.wall.bottom-self.monster.top)<tolerance and self.movey<0:
                self.movey*=-1

        if self.monster.colliderect(player.player):
            while True:
                game_over=font.render("Game Over",True,(255,255,0))
                restart=font.render("Press space to restart",True,(255,255,0))
                screen.fill((0,0,0))
                screen.blit(game_over,(200,250))
                screen.blit(restart,(150,300))
                terminate()
                if pygame.key.get_pressed()[K_SPACE]:
                    return reset()
                pygame.display.update()



class Wall:
    def __init__(self,x,y,size1,size2,color):
        self.x=x
        self.y=y
        self.size1=size1
        self.size2=size2
        self.color=color

    def define(self):
        self.wall=pygame.Rect((self.x,self.y),(self.size1,self.size2))
        self.xwall=pygame.Rect((self.x-10,self.y-5),(self.size1+15,self.size2+10))

    def draw(self):
        #pygame.draw.rect(screen,(255,255,255),self.xwall)
        pygame.draw.rect(screen,self.color,self.wall)









player=Player()
food=Food(300,10,50,50,(255,174,2),5,4)
monster=Monster(300,300,50,50,(0,150,20),7,5)
wall1=Wall(250,250,50,50,(125,0,5))
wall2=Wall(250,350,50,50,(125,0,5))
food.define()
player.define()
monster.define()
wall1.define()
wall2.define()
while True:
    start()
    terminate()
    screen.fill((0,20,40))
    food.feed()
    monster.attack()
    wall1.draw()
    #wall2.draw()
    player.move(wall1)
    #player.move(wall2)
    score_text=font.render("score:")
    clock.tick(60)
    pygame.display.update()