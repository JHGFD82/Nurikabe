import pygame
import sys
import sqlite3

from pygame.locals import *

pygame.init()

class puzzle():

    def __init__(self, **kwargs):
        self.width = kwargs['width']
        self.height = kwargs['height']
        self.difficulty = kwargs['difficulty']

# APPLICATION SIZE
screen_width = 1024
screen_height = 768
DISPLAY = pygame.display.set_mode((screen_width,
                                   screen_height))

# COLORS
WHITE = (230, 230, 230)
BLACK = (50, 50, 50)
BACKGROUND = (180, 180, 150)

def main():

    DISPLAY.fill(BACKGROUND)

    puzzle_width = 4
    puzzle_height = 5
    puzzle_difficulty = 'easy'
    puzzle_parts = {'width':puzzle_width,
                    'height':puzzle_height,
                    'difficulty':puzzle_difficulty}
    current_puzzle = puzzle(**puzzle_parts)

    puzzle_scale = 718 / current_puzzle.height
    puzzle_pos_x = screen_width / 2 - current_puzzle.width * puzzle_scale / 2
    puzzle_pos_y = screen_height / 2 - current_puzzle.height * puzzle_scale / 2

    puzzle_size = (puzzle_pos_x,
                   puzzle_pos_y,
                   current_puzzle.width * puzzle_scale,
                   current_puzzle.height * puzzle_scale)
    border_size = (puzzle_pos_x - 10,
                   puzzle_pos_y - 10,
                   current_puzzle.width * puzzle_scale + 20,
                   current_puzzle.height * puzzle_scale + 20)

    pygame.draw.rect(
        DISPLAY, BLACK, border_size)

    for x in range(current_puzzle.width):
        for y in range(current_puzzle.height):
            pygame.draw.rect(
                DISPLAY, WHITE, (x * puzzle_scale + puzzle_pos_x + 1,
                                 y * puzzle_scale + puzzle_pos_y + 1,
                                 puzzle_scale - 2,
                                 puzzle_scale - 2)
            )

    font = pygame.font.Font('freesansbold.ttf', int(puzzle_scale))
    text = font.render('4', True, BLACK)
    textRect = text.get_rect()
    textRect.center = (500,500)
    DISPLAY.blit(text, textRect)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


main()
