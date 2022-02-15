import pygame
pygame.init()

full = pygame.FULLSCREEN
win=0

screen = pygame.display.set_mode((1280,720),win)
pygame.display.set_caption("My game")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

def main():
    quit=False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
        screen.fill((100,100,100))
        pygame.display.update()

if __name__=='__main__':
    main()