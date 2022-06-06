import random
import pygame
from classes import *
import os
import chunk_render
pygame.init()



with open("./settings.settings", "r") as settings:
    lines = settings.readlines()

if lines[0][0] == "1":
    full_on = 1
    full = pygame.FULLSCREEN
else:
    full_on = 0
    full = 0
res = [int(lines[1].split(",")[0]),int(lines[1].split(",")[1])]
FPS = int(lines[2])

def draw_text(text, size, color, font, x, y):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


#image buttons
settings_img = pygame.image.load('./assets/settings_btn.png')
settings_button = Button(res[0]-26, 0, settings_img, 0.05)

#text buttons
start_button = text_Button("PLAY", int(res[0]/16), (99,171,63,255), "Minecraft.ttf", res[0]/2,res[1]/2)
restart_button = text_Button("Restart", int(res[1]/16), (99,171,63,255) ,"Minecraft.ttf", res[0]/2, res[1]*5/6)
full_button = text_Button("Full: O", int(res[0]*5/128), (99,171,63,255), "Minecraft.ttf", res[0]/5, res[1]*5/6)
menu_button = text_Button("MENU", int(res[0]/64), (99,171,63,255) ,"Minecraft.ttf", res[0]/40, res[1]/40)

res_1920x1080_button = text_Button("1920x1080", int(res[0]*5/128), (99,171,63,255),"Minecraft.ttf", res[0]*1/5, res[1]/2-res[1]/18)
res_1280x720_button = text_Button("1280x720", int(res[0]*5/128), (99,171,63,255), "Minecraft.ttf", res[0]*1/5, res[1]/2+res[1]/18)

fps_60_button = text_Button("60", int(res[0]*5/128), (99,171,63,255), "Minecraft.ttf", res[0]*4/5, res[1]/2-res[1]/9)
fps_120_button = text_Button("120", int(res[0]*5/128), (99,171,63,255), "Minecraft.ttf", res[0]*4/5, res[1]/2)
fps_144_button = text_Button("144", int(res[0]*5/128), (99,171,63,255), "Minecraft.ttf", res[0]*4/5, res[1]/2+res[1]/9)

clock = pygame.time.Clock()
screen = pygame.display.set_mode(res, full)
pygame.display.set_caption("My game")
icon = pygame.image.load("./assets/icon.png")
pygame.display.set_icon(icon)

#background
bg_img = pygame.transform.scale(pygame.image.load('./assets/background.png'),res)

#Player psetup
player_front=pygame.transform.scale(pygame.image.load("./assets/player/player_front.png"),[res[0]/16,res[1]/9])
player_back=pygame.transform.scale(pygame.image.load("./assets/player/player_back.png"),[res[0]/16,res[1]/9])
playerImg=player_front
PlayerPos=[res[0]/2-32,4/5*res[1]-32]
player_left, player_right, player_up, player_down = False, False, False, False

#Chunks loading
chunks = chunk_render.get_map()
assets = chunk_render.initate_assets(res)
wall = assets[223]
grass = assets[177]
flower_1 = assets[250]
flower_2 = assets[251]
flower_3 = assets[252]
flower_4 = assets[253]
tiles = {"#": wall, ".": grass, "1": flower_1, "2": flower_2, "3": flower_3, "4": flower_4}
x, y = 0, 0
xmax, ymax = len(chunks)-1, len(chunks[1])-1


menu, run = True, True

settings, play, res_change, FPS_change , full_change = False, False, False, False, False
while run:
    dt = clock.tick(FPS)
    
    
    
    ##########################################################################
    
    if menu:
        
        screen.blit(bg_img,(0,0))
        
        if menu_button.draw(screen):
            settings, play, = False, False
            menu = True
            
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
        screen.blit(bg_img,(0,0))

        if menu_button.draw(screen):
            settings, play, = False, False
            menu = True
        
        draw_text("Resolutions", int(res[0]*5/128) , (99,171,63,255), "Minecraft.ttf" , res[0]/5, res[1]/15+res[1]*80/720)
        draw_text("FPS", int(res[0]*5/128), (99,171,63,255), "Minecraft.ttf", res[0]*4/5, res[1]/15+res[1]*80/720)
        
        if full_button.draw(screen):
            full_on+=1
            if full_on%2==0:
                new_full=0
                full_change=False
            else:
                new_full=1
                full_change=True
        if full_on%2!=0:
            draw_text("X", int(res[0]*5/128), (99,171,63,255), "Minecraft.ttf", res[0]/5+res[0]*11/256, res[1]*5/6)

        if res_1920x1080_button.draw(screen):
            new_res=[1920,1080]
            res_change=True
        if res_1280x720_button.draw(screen):
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
                new_FPS = FPS
            if not full_change:
                new_full = full
            
            with open("./settings.settings", "w") as settings_file:
                settings_file.write(str(new_full)+"\n"+str(new_res[0])+","+str(new_res[1])+"\n"+str(new_FPS))
            pygame.quit()
            os.system("python main.py")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    ##########################################################################
    
    if play:
        
        current_chunk = [x,y]
        chunk_render.render_chunk(chunks, current_chunk, res, screen, tiles)
        
        if menu_button.draw(screen):
            settings, play, = False, False
            menu = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run=False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player_left=True
                if event.key == pygame.K_d:
                    player_right=True
                if event.key == pygame.K_z:
                    playerImg=player_back
                    player_down=True
                if event.key == pygame.K_s:
                    playerImg=player_front
                    player_up=True

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
        current = chunks[current_chunk[0]][current_chunk[1]]

        if PlayerPos[0]<0:
            if current[round(PlayerPos[1]*9/res[1])][0] =='#':
                PlayerPos[0]=80
            elif x>0:
                x-=1
                PlayerPos[0]=res[0]-64
        elif PlayerPos[0]>res[0]-64:
            if current[round(PlayerPos[1]*9/res[1])][-1] =='#':
                PlayerPos[0]=res[0]-144
            elif x<xmax:
                x+=1
                PlayerPos[0]=0
        elif PlayerPos[1]<0:
            if current[0][round(PlayerPos[0]*16/res[0])] == "#":
                PlayerPos[1]=64
            elif y>0:
                y-=1
                PlayerPos[1]=res[1]-64
        elif PlayerPos[1]>res[1]-64:
            if current[-1][round(PlayerPos[0]*16/res[0])] =='#':
                PlayerPos[1]=res[1]-144
            elif y<ymax:
                y+=1
                PlayerPos[1]=0
        
        screen.blit(playerImg, PlayerPos)
        
    ##########################################################################
        
    pygame.display.update()
