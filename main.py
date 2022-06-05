import random
import pygame
import classes
import os
pygame.init()

with open("./settings.settings", "r") as settings:
    lines = settings.readlines()

if lines[0][0] == "1":
    full = pygame.FULLSCREEN
else:
    full = 0
res = [int(lines[1].split(",")[0]),int(lines[1].split(",")[1])]
FPS = int(lines[2])


start_img = pygame.image.load('./assets/start_btn.png')
settings_img = pygame.image.load('./assets/settings_btn.png')
resolution_img = pygame.image.load('./assets/resolution.png')
FPS_img = pygame.image.load('./assets/FPS.png')
restart_img = pygame.image.load('./assets/restart_btn.png')

res_1920x1080 = pygame.image.load('./assets/resolutions/1920x1080.png')
res_1280x720 = pygame.image.load('./assets/resolutions/1280x720.png')

fps_60 = pygame.image.load('./assets/framerates/60.png')
fps_120 = pygame.image.load('./assets/framerates/120.png')
fps_144 = pygame.image.load('./assets/framerates/144.png')


start_button = classes.Button(res[0]/2-54, res[1]/2-24, start_img, 1)
settings_button = classes.Button(res[0]-26, 0, settings_img, 0.05)
restart_button = classes.Button(res[0]/2-99, res[1]-70, restart_img, 1)

res_1920x1080_button = classes.Button(res[0]*1/5-148, res[1]/2-80 , res_1920x1080, 1)
res_1280_720_button = classes.Button(res[0]*1/5-135, res[1]/2, res_1280x720, 1)

fps_60_button = classes.Button(res[0]*4/5-30, res[1]/2-80, fps_60, 1)
fps_120_button = classes.Button(res[0]*4/5-40, res[1]/2-30, fps_120, 1)
fps_144_button = classes.Button(res[0]*4/5-44, res[1]/2+20, fps_144, 1)

clock = pygame.time.Clock()
screen = pygame.display.set_mode(res, full)
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
            settings=True
            menu=False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    ##########################################################################
    
    if settings:
        screen.fill((150,150,150))
        
        
        
        screen.blit(resolution_img, [res[0]/5-130, res[1]*1/15])
        screen.blit(FPS_img, [res[0]*4/5-50, res[1]*1/15])
        #screen.blit(PlayerImg, PlayerPos)
        #screen.blit(PlayerImg, PlayerPos)
        #screen.blit(PlayerImg, PlayerPos)

        if res_1920x1080_button.draw(screen):
            new_res=[1920,1080]
            res_change=True
        if res_1280_720_button.draw(screen):
            new_res=[1280,720]
            res_change=True
        if fps_60_button.draw(screen):
            new_FPS=60
            FPS_change=True
        if fps_120_button.draw(screen):
            new_FPS=120
            FPS_change=True
        if fps_144_button.draw(screen):
            new_FPS=144
            FPS_change=True

        if restart_button.draw(screen):
            if not res_change:
                new_res = res
            if not FPS_change:
                new_fps = FPS
            
            with open("./settings.settings", "w") as settings_file:
                settings_file.write(str(full)+"\n"+str(new_res[0])+","+str(new_res[1])+"\n"+str(new_FPS))
            pygame.quit()
            os.system("python main.py")

        
        
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    
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
