import random
import pygame
import classes
pygame.init()

full = pygame.FULLSCREEN
win=0
res=[1280,720]
FPS = 120

start_img = pygame.image.load('./assets/start_btn.png')
exit_img = pygame.image.load('./assets/settings_btn.png')


start_button = classes.Button(res[0]/2-54, res[1]/2-24, start_img, 1)
settings_button = classes.Button(res[0]-26, 0, exit_img, 0.05)


clock = pygame.time.Clock()
screen = pygame.display.set_mode(res,win)
pygame.display.set_caption("My game")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

#Player parameters
PlayerImg=pygame.image.load("./assets/player.png")
PlayerPos=[res[0]/2-32,4/5*res[1]-32]
player_left, player_right, player_up, player_down = False, False, False, False

#Enemy parameters
EnemyImg=pygame.image.load("./assets/enemy.png")
EnemyPos=[0,0]

#Bullets parameters
BulletImg=pygame.image.load("./assets/bullet.png")
BulletPos=[0,0]
bullet_Yvar=-1
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
menu=True
play=False 
settings = False
while run:
    dt = clock.tick(FPS)
    
    ##########################################################################
    
    if menu:
        screen.fill((150,150,150))
        if start_button.draw(screen):
            play=True
            menu=False
        if settings_button.draw(screen):
            settintgs=True
            menu=False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    ##########################################################################
                
    if play:
        screen.fill((150,150,150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player_left=True
                if event.key == pygame.K_d:
                    player_right=True
                if event.key == pygame.K_z:
                    player_down=True
                if event.key == pygame.K_s:
                    player_up=True
                if event.key == pygame.K_SPACE and bullet_state==False:
                    BulletPos[0], BulletPos[1]=PlayerPos[0], PlayerPos[1]
                    bullet_fire(BulletPos)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q or pygame.K_d:
                    player_left=False
                if event.key == pygame.K_d:
                    player_right=False
                if event.key == pygame.K_z:
                    player_down=False
                if event.key == pygame.K_s:
                    player_up=False

        #Player movement    
        if player_left:
            PlayerPos[0]-=0.3*dt
        if player_right:
            PlayerPos[0]+=0.3*dt
        if player_down:
            PlayerPos[1]-=0.3*dt
        if player_up:
            PlayerPos[1]+=0.3*dt
        
        #Player constraints
        if PlayerPos[0]<0:
            PlayerPos[0]=0
        elif PlayerPos[0]>res[0]-64:
            PlayerPos[0]=res[0]-64
        if PlayerPos[1]<res[1]*3/4:
            PlayerPos[1]=res[1]*3/4
        elif PlayerPos[1]>res[1]-64:
            PlayerPos[1]=res[1]-64
        
        #Enemy mouvement
        if EnemyPos[0]<=0:
            EnemyPos[1]+=20
            enemy_Xvar=0.2*dt
        elif EnemyPos[0]>=res[0]-64:
            EnemyPos[1]+=20
            enemy_Xvar=-0.2*dt
        EnemyPos[0]+=enemy_Xvar
        
        #Bullet movement
        if bullet_state==True:
            bullet_fire(BulletPos)
            BulletPos[1]+=bullet_Yvar*dt
        if BulletPos[1]<0:
            bullet_state=False
        #collison detection
        if EnemyPos[0]-5<BulletPos[0]+16<EnemyPos[0]+69 and EnemyPos[1]+59<BulletPos[1]<EnemyPos[1]+69:
            BulletPos[1]=-64
            EnemyPos=[random.randint(0,res[0]-32),random.randint(0, res[1]/2-32)]

        player(PlayerPos)
        enemy(EnemyPos)
        
    ##########################################################################
        
    pygame.display.update()
