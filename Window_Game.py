# %%
from pygame.draw import line
from pygame.sprite import groupcollide
from Freecell_Game import CARDS, FreeCellGame
import pygame
import utils

# %%
F = 1

pygame.init()
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 960
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 30
IMAGES = utils.LoadImages()
RECTS = utils.LoadRects()
BLACK = 0, 0, 0
FONT = pygame.font.Font(None, 30):

class WindowGame:
    def __init__(self):
        self.freecell_game = FreeCellGame()
        self.log = []
        pygame.display.set_caption('FreeCell Game')
        self.freecell_game.ParseDataObserve(
            [0, 0, 0, 1, 0, 2, 0, 3, 0, 4, 0, 5, 0, 6, 0, 7, 0, 8, 9, 1, 5, 0, 14, 2, 10, 0, 1, 0, 1, 1, 1, 2, 1, 3,
             1,
             4, 1, 5, 1, 6, 12, 0, 10, 2, 4, 0, 14, 4, 14, 0, 9, 0, 2, 0, 2, 1, 2, 2, 2, 3, 2, 4, 2, 5, 2, 6, 2, 7,
             2,
             8, 2, 9, 2, 10, 2, 11, 14, 3, 3, 0, 3, 1, 3, 2, 3, 3, 3, 4, 3, 5, 3, 6, 3, 7, 3, 8, 3, 9, 3, 10, 10, 1,
             14,
             1, 27])
        self.UpdateScreen()
        self.MainLoop()

    def MainLoop(self):
        print("Main Looping")
        button_down_id = -1
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Quit()
                    return True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print("Mouse Button Down")
                    button_down_id = self.GetButtonArea(event.pos)
                    if button_down_id == -1:
                        # invalid button down
                        self.LogInto('invalid move from.')
                        pass
                elif event.type == pygame.MOUSEBUTTONUP:
                    print("Mouse Button Up")
                    if button_down_id != -1:
                        button_up_id = self.GetButtonArea(event.pos)
                        if button_down_id != -1:
                            if (self.freecell_game.CheckMove(button_down_id, button_up_id)):
                                # move ok
                                self.freecell_game.Move(button_down_id, button_up_id)
                                pass
                            else:
                                # invalid move
                                self.LogInto('invalid move.')
                        else:
                            # invalid button up
                            self.LogInto('invalid move to.')
                    else:
                        pass
                else:  # other type
                    pass
            self.UpdateScreen()
            CLOCK.tick(FPS)

    def GetButtonArea(self, pos):
        for k, v in RECTS.items():
            if v.collidepoint(pos):
                return k
        return -1

    def LogInto(self, s):
        if len(self.log) == 30:
            self.log.pop(0)
        self.log.append(s)

    def Win(self):
        SCREEN.blit(IMAGES['win'], (500, 300))

    def UpdateScreen(self):
        # draw background
        background = IMAGES['background']
        SCREEN.blit(background, (0, 0))
        # draw cards
        for x in range(8):
            heap_list = self.freecell_game.all_cards[x].heap_list
            if len(heap_list) == 0:
                continue
            card = heap_list[-1]
            card_img = IMAGES[card.color + card.point]
            SCREEN.blit(card_img, (20 + 140 * x, 20))
        for x in range(8, 16):
            heap_list = self.freecell_game.all_cards[x].heap_list
            if len(heap_list) == 0:
                continue
            for i in range(len(heap_list)):
                card = heap_list[i]
                card_img = IMAGES[card.color + card.point]
                SCREEN.blit(card_img, (20 + 140 * (x - 8), 200 + 40 * i))
        # draw log
        log_str = ''
        for s in self.log:
            log_str = log_str + s + '\n'
        log_img = FONT.render(log_str, True, BLACK)
        SCREEN.blit(log_img, (1140, 20))
        # update
        pygame.display.update()

    def Quit(self):
        pygame.quit()


# %%
if __name__ == '__main__':
    WindowGame()
