import pygame
from pygame.locals import *
import json
import random
pygame.init()
CLOCK = pygame.time.Clock()

running = True
WINDOWSIZE = (1200, 800)
window = pygame.display.set_mode(WINDOWSIZE, 0, 32)
MAP_SIZE = [100, 70]


WHITE = 255, 255, 255
BLACK = 0, 0, 0
TEST = pygame.image.load("TestPixel.png")
BLOCK_SIZE = 16 * 2
TEST = pygame.transform.scale(TEST, (BLOCK_SIZE, BLOCK_SIZE))


class Block():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * BLOCK_SIZE
        self.y = col * BLOCK_SIZE
        self.id = 0 # This is what will be written to a text file
        

    def test_mouse(self):
        self.rect = pygame.rect.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos[0], mouse_pos[1]):
            return True

    def draw(self, design):
        window.blit(design, (self.x, self.y))
        
def make_grid():
    grid = []
    for i in range(MAP_SIZE[0]):
        grid.append([])
        for j in range(MAP_SIZE[1]):
            grid[i].append(Block(i, j))
    return grid
grid = make_grid()

def update_grid():
    try:
        with open('leveldata.json', 'r') as f:
                    data = json.load(f)
        i = -1
        j = -1
        for row in grid:
            i += 1
            for block in row:
                j += 1
                if j > len(row) - 1:
                    j = 0
                block.id = data[i][j]
    except FileNotFoundError:
        pass

#update_grid()


left_click = False
right_click = False
clear = False

camera = [0,0]
sens = 10

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        # MOUSE EVENTS
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                left_click = True
            if event.button == 3:
                right_click = True
        if event.type == MOUSEBUTTONUP:
            if event.button == 1:
                left_click = False
            if event.button == 3:
                right_click = False
        if event.type == KEYDOWN:
            if event.key == K_c:
                clear = True
        if event.type == KEYUP:
            if event.key == K_c:
                clear = False
        # NON-MOUSE EVENTS
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                camera[0] = -sens
            if event.key == K_RIGHT:
                camera[0] = sens
            if event.key == K_UP:
                camera[1] = -sens
            if event.key == K_DOWN:
                camera[1] = sens
        if event.type == KEYUP:
            if event.key == K_LEFT:
                camera[0] = 0
            if event.key == K_RIGHT:
                camera[0] = 0
            if event.key == K_UP:
                camera[1] = 0
            if event.key == K_DOWN:
                camera[1] = 0





    window.fill(BLACK)
 
    for row in grid:
        for block in row:
            if block.test_mouse() and left_click:
                block.id = 1
            if block.test_mouse() and right_click:
                block.id = 0
            if clear:
                block.id = 0
            if block.id == 1:
                block.draw(TEST)
            block.x += camera[0]
            block.y += camera[1]

            


    pygame.display.flip()      
    CLOCK.tick(60)

def get_data():
    data = []
    for i in range(WINDOWSIZE[0]//BLOCK_SIZE):
        data.append([])
        for cell in grid[i]:
            data[i].append(cell.id)
    return data

#data = get_data()
#with open('leveldata.json', 'w') as f:
    #json.dump(data, f, indent=2)


pygame.quit()
