from map_layout import chunks
import pygame
import os
pygame.init()

NUMBER_OF_MAP_ROWS = 13
NUMBER_OF_MAP_COLUMNS = 25

def initate_assets(res):
    loaded_assets = []
    for i in range(1,NUMBER_OF_MAP_ROWS+1):
        for j in range(1,NUMBER_OF_MAP_COLUMNS+1):
            loaded_assets.append(pygame.transform.scale(pygame.image.load("./map_assets/row-"+str(i)+"-column-"+str(j)+".png"),(res[0]*1/16,res[0]*1/16)))
    return loaded_assets

def render_chunk(chunk, res, screen, tiles):
    """
    Render a chunk
    """
    current = chunks[chunk[0]][chunk[1]]
    
    for line in range(9):
        for column in range(16):
            tile = current[line][column]
            screen.blit(tiles[tile], (column * res[0]*1/16, line * res[0]*1/16))
    return True