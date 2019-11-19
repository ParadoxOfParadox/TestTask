import pygame
import time
import random

pygame.init()
white = (255,255,255)
screen_height = 640
screen_width = 1000
win = pygame.display.set_mode((screen_width,screen_height))

pygame.display.set_caption("Fighter")
class character():
    def __init__(self):
        self.hp=1000
        self.dmg=50
        self.accuracy = 0.95
        self.abilities = ["Fire"]
        self.block = 0.15
        self.speed = 5
        self.x = 50
        self.y = screen_height - 60
        self.width = 40
        self.height = 60
    def kick(self, target):
        y = random.randint(0, 100)
        if self.accuracy * 100 >= y:
            target.hp -= self.dmg
    def regenerate(self):
        if 1.01*self.hp<=1000:
            self.hp+=int(0.01*self.hp)
        else:
            self.hp=1000
    def make_bullet(self):
        bullets.append([50+you.width,you.y-you.height/2])
you = character()

char = pygame.image.load("character.png")
bg = pygame.image.load("background.png")
bullet = pygame.image.load("bullet.png")
enemy = pygame.image.load("enemy.png")

run = True
jump = False
presence = False
enemy_position = screen_width + 60
enemy_speed = 7
enemy_hp = 500
jumpCount = 10
bullet_speed = 10
bullets = []
enemy_bullets = []
flag = time.time()

while run>0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
    keys = pygame.key.get_pressed()
    if keys[pygame.K_TAB]:
        if time.time()-flag>=0.75:
           you.make_bullet()
           flag = time.time()
    if keys[pygame.K_RIGHT]:
        you.x-=you.speed
    if not presence:
        rnd = random.randint(0,100)
        if rnd==0:
            presence = True
            en_flag = time.time()
    else:
        if time.time()-en_flag>0.75:
            enemy_bullets.append([enemy_position,screen_height-90])
            en_flag = time.time()
    if not jump:  
        if keys[pygame.K_SPACE]:
            jump = True
    else:
        if jumpCount >= -10:
            if jumpCount<0:
                you.y+=(jumpCount**2)/3
            else:
                if you.y-(jumpCount**2)/3>=0:
                    you.y-=(jumpCount**2)/3
                else:
                    you.y = 0
            jumpCount-=1
        else:
            jump =False
            jumpCount = 10
    rel_x = you.x % bg.get_rect().width        
    win.blit(bg,(rel_x-bg.get_rect().width,0))
    if rel_x < screen_width:
        win.blit(bg,(rel_x, 0))   
    for i in range(len(enemy_bullets)):
        try:
            if enemy_bullets[i][0]-bullet_speed-10>=0:
                if enemy_bullets[i][0]-bullet_speed<=50+you.width and enemy_bullets[i][1]>=you.y-you.height and enemy_bullets[i][1]<=you.y:
                    you.hp-=you.dmg
                    enemy_bullets.pop(i)
                else:    
                    win.blit(bullet,enemy_bullets[i])
                    enemy_bullets[i][0]-=bullet_speed
            else:
                enemy_bullets.pop(i)
        except:
            pass
    for i in range(len(bullets)):
        try:
            if bullets[i][0]+bullet_speed+10<=screen_width:
                if bullets[i][0]+bullet_speed>=enemy_position and bullets[i][1]>=screen_height-130:
                    enemy_hp-=you.dmg
                    bullets.pop(i)
                else:    
                    win.blit(bullet,bullets[i])
                    bullets[i][0]+=bullet_speed
            else:
                bullets.pop(i)
        except:
            pass
    if you.hp>0:
        pygame.draw.rect(win,(255,0,0),(20,20,you.hp/10,20))
    else:
        run = False
    if presence:
        if enemy_position>=screen_width-100:
            enemy_position-=enemy_speed
        if enemy_hp>0:    
            win.blit(enemy,(enemy_position,screen_height-120))
        else:
            presence = False
            enemy_hp=500
            enemy_position = screen_width + 60
    myfont = pygame.font.SysFont('Comic Sans MS', 25)    
    textsurface = myfont.render('{} hp'.format(str(you.hp)), False, (0, 0, 0))
    win.blit(textsurface,(120,10))
    win.blit(char, (50,you.y-you.height))
    pygame.display.update()
pygame.quit()
