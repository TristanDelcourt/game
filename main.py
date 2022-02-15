import random
import pygame
pygame.init()

full = pygame.FULLSCREEN
win=0
res=[1280,720]

screen = pygame.display.set_mode(res,win)
pygame.display.set_caption("My game")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

#Player parameters
PlayerImg=pygame.image.load("./assets/player.png")
PlayerPos=[res[0]/2-32,4/5*res[1]-32]
player_Xvar, player_Yvar= 0, 0

#Enemy parameters
EnemyImg=pygame.image.load("./assets/enemy.png")
EnemyPos=[random.randint(0,res[0]-32),random.randint(0, res[1]/2-32)]
enemy_Xvar, enemy_Yvar= 0.1, 20

#Bullets parameters
BulletImg=pygame.image.load("./assets/bullet.png")
BulletPos=[0,0]
bullet_Yvar=-0.5
bullet_state=False

def player(PlayerPos):
    screen.blit(PlayerImg, PlayerPos)

def enemy(EnemyPos):
    screen.blit(EnemyImg,EnemyPos)

def bullet_fire(PlayerPos):
    global bullet_state
    bullet_state=True
    screen.blit(BulletImg,[PlayerPos[0]+16,PlayerPos[1]])
    
run=True
while run:
    screen.fill((150,150,150))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q and PlayerPos[0]>0:
                player_Xvar-=0.2
            if event.key == pygame.K_d and PlayerPos[0]<res[0]:
                player_Xvar+=0.2
            if event.key == pygame.K_z and PlayerPos[1]>0:
                player_Yvar-=0.2
            if event.key == pygame.K_s and PlayerPos[1]<res[1]:
                player_Yvar+=0.2
            if event.key == pygame.K_SPACE and bullet_state==False:
                BulletPos[0], BulletPos[1]=PlayerPos[0], PlayerPos[1]
                bullet_fire(BulletPos)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q or pygame.K_d:
                player_Xvar=0
            if event.key == pygame.K_z or pygame.K_s:
                player_Yvar=0
    
    #Player constraints
    PlayerPos[0]+=player_Xvar
    PlayerPos[1]+=player_Yvar
    
    if PlayerPos[0]<0:
        PlayerPos[0]=0
    elif PlayerPos[0]>res[0]-64:
        PlayerPos[0]=res[0]-64
    if PlayerPos[1]<res[1]*3/4:
        PlayerPos[1]=res[1]*3/4
    elif PlayerPos[1]>res[1]-64:
        PlayerPos[1]=res[1]-64
    
    #Enemy mouvement
    EnemyPos[0]+=enemy_Xvar
    
    if EnemyPos[0]<=0:
        EnemyPos[1]+=enemy_Yvar
        enemy_Xvar=0.1
    elif EnemyPos[0]>=res[0]-64:
        EnemyPos[1]+=enemy_Yvar
        enemy_Xvar=-0.1

    #Enemy mouvement
    if bullet_state==True:
        bullet_fire(BulletPos)
        BulletPos[1]+=bullet_Yvar
    if BulletPos[1]<0:
        bullet_state=False

    #collison detection
    if EnemyPos[0]<BulletPos[0]+16<EnemyPos[0]+64 and EnemyPos[1]+64==BulletPos[1]:
        BulletPos[1]=-64
        EnemyPos[0], EnemyPos[1] = random.randint(0,res[0]-32), random.randint(0, res[1]/2-32)

    player(PlayerPos)
    enemy(EnemyPos)
    pygame.display.update()