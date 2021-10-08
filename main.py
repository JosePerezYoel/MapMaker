import pygame
from pygame.locals import *
import json
pygame.init()
CLOCK = pygame.time.Clock()

running = True
WINDOWSIZE = (1219, 832)
window = pygame.display.set_mode(WINDOWSIZE, 0, 32)



# The sizes of the window and the display are all mulitples of the blocksize so that the blocks will evenly populate the window
WHITE = 255, 255, 255
BLACK = 0, 0, 0
TEST = pygame.image.load("TestPixel.png")
TEST = pygame.transform.scale(TEST, (16 * 4, 16*4))
BLOCK_SIZE = 16 * 4


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
    for i in range(WINDOWSIZE[0]//BLOCK_SIZE):
        grid.append([])
        for j in range(WINDOWSIZE[1]//BLOCK_SIZE):
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
update_grid()


left_click = False
right_click = False
clear = False
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
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
            


    pygame.display.flip()      
    CLOCK.tick(60)

def get_data():
    data = []
    for i in range(WINDOWSIZE[0]//BLOCK_SIZE):
        data.append([])
        for cell in grid[i]:
            data[i].append(cell.id)
    return data

data = get_data()
with open('leveldata.json', 'w') as f:
    json.dump(data, f, indent=2)


pygame.quit()