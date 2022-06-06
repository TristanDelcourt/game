import pygame
import os
pygame.init()

NUMBER_OF_MAP_ROWS = 13
NUMBER_OF_MAP_COLUMNS = 25

def get_map():
    with open("./map.map", "r") as map_file:
        map_lines = map_file.readlines()
    
    map_grid=[]
    for line in map_lines:
        if not "-" in line:
            map_grid.append(line[:-1].split("|"))
    
    final_chunks = []
    for k in range(len(map_grid[1])):
        done_chunk = []
        for j in range(int(len(map_grid)/9)):
            current_chunk=[]
            for i in range(9):
                current_chunk.append(map_grid[i+j*9][k])
            done_chunk.append(current_chunk)
        final_chunks.append(done_chunk)
    
    return final_chunks

def initate_assets(res):
    loaded_assets = []
    for i in range(1,NUMBER_OF_MAP_ROWS+1):
        for j in range(1,NUMBER_OF_MAP_COLUMNS+1):
            loaded_assets.append(pygame.transform.scale(pygame.image.load("./map_assets/row-"+str(i)+"-column-"+str(j)+".png"),(res[0]*1/16,res[0]*1/16)))
    return loaded_assets

def render_chunk(chunks , current_chunk, res, screen, tiles):
    """
    Render a chunk
    """
    
    current = chunks[current_chunk[0]][current_chunk[1]]
    
    for line in range(9):
        for column in range(16):
            tile = current[line][column]
            screen.blit(tiles[tile], (column * res[0]*1/16, line * res[0]*1/16))

get_map()