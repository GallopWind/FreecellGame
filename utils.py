# %%
import pygame
from Freecell_Game import CARDS
# %%
def LoadImages():
    IMAGES = {}
    IMAGES['background'] = pygame.image.load('images/background.png').convert_alpha()
    IMAGES['win'] = pygame.image.load('images/win.png').convert_alpha()

    for card in CARDS:
        color_icon = pygame.image.load('images/'+card.color+'.png').convert_alpha()
        point_icon = pygame.image.load('images/'+card.point+'-icon.png').convert_alpha()
        blank_card = pygame.image.load('images/blank_card.png').convert_alpha()
        blank_card.blit(color_icon, (1,1))
        blank_card.blit(point_icon, (79,1))
        # pygame.image.save(blank_card, 'tmp/'+card.color+card.point+'.png')
        IMAGES[card.color+card.point] = blank_card
    return IMAGES

def LoadRects():
    RECTS = {}
    for x in range(8):
        RECTS[x] = pygame.Rect(20+140*x,20,120,160)
    for x in range(8,16):
        RECTS[x] = pygame.Rect(20+140*(x-8),200,120,700)
    return RECTS

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1, 1))
    LoadImages()
    pygame.quit()