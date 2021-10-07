import pygame
from pygame.locals import *
pygame.init()
CLOCK = pygame.time.Clock()

running = True
WINDOWSIZE = (1216, 912)
window = pygame.display.set_mode(WINDOWSIZE, 0, 32)

#BLIT THINGS ON DISPLAY NOT ON WINDOW
DISPLAYSIZE = (304, 208)
display = pygame.Surface((DISPLAYSIZE[0], DISPLAYSIZE[1]))
# The sizes of the window and the display are all mulitples of the blocksize so that the blocks will evenly populate the window
WHITE = 255, 255, 255
BLACK = 0, 0, 0
TEST = pygame.image.load("TestPixel.png")
#TEST = pygame.transform.scale(TEST, (16 * 4, 16*4))
BLOCK_SIZE = 16
RATIO = 4

class Block():
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * BLOCK_SIZE
        self.y = col * BLOCK_SIZE
    

        

    def test_mouse(self):
        self.rect = pygame.rect.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos[0]//RATIO, mouse_pos[1]//RATIO):
            return True

    def draw(self):
        display.blit(TEST, (self.x, self.y))
        


        
    
        

def make_grid():
    grid = []
    for i in range(DISPLAYSIZE[0]//BLOCK_SIZE):
        grid.append([])
        for j in range(DISPLAYSIZE[1]//BLOCK_SIZE):
            grid[i].append(Block(i, j))
    return grid
grid = make_grid()

clicked = False
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == MOUSEBUTTONDOWN:
            clicked = True
        if event.type == MOUSEBUTTONUP:
            clicked = False



    window.blit(pygame.transform.scale(display, WINDOWSIZE), (0, 0))
    for row in grid:
        for block in row:
            if block.test_mouse() and clicked:
                block.draw()


    pygame.display.flip()      
    CLOCK.tick(60)
    
pygame.quit()
