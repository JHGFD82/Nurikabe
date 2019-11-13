# Import packages
import pygame
from pygame.locals import *
import sys
from sqlalchemy import Column, Integer, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Initialize components
pygame.init()
engine = create_engine('sqlite:///nurikabe_puzzles.sqlite')
Base = declarative_base()
session = sessionmaker(bind=engine)
session = session()

# Colors
WHITE = (230, 230, 230)
BLACK = (50, 50, 50)
RED = (240, 0, 0)
BACKGROUND = (180, 180, 150)


# Set up puzzle object
class PuzzleDB(Base):
    __tablename__ = 'puzzles'
    puzzle_id = Column(Integer, primary_key=True)
    catalog_num = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    difficulty = Column(Integer)
    completed = Column(Boolean)


# Set up spaces object
class SpaceDB(Base):
    __tablename__ = 'spaces'
    puzzle_id = Column(Integer, primary_key=True)
    space_x = Column(Integer)
    space_y = Column(Integer)
    space_n = Column(Integer)


# Application settings
screen_width = 1024
screen_height = 768
DISPLAY = pygame.display.set_mode((screen_width,
                                   screen_height))


# Begin drawing
def main():
    # Draw initial box
    DISPLAY.fill(BACKGROUND)

    # Set up current puzzle object
    puzzle_num = 0

    puzzle = session.query(PuzzleDB) \
        .filter(PuzzleDB.puzzle_id == puzzle_num).first()
    space = session.query(SpaceDB.space_n, SpaceDB.space_x, SpaceDB.space_y) \
        .filter(SpaceDB.puzzle_id == puzzle_num)

    # Set up individual box object
    class PuzzleBox():
        def __init__(self, rect):
            self.rect = rect
            self.state = 0
            self.color = WHITE

        def update(self):
            if self.state == 1:
                self.color = BLACK
            elif self.state == 2:
                self.color = WHITE

    puzzle_scale = 418 / puzzle.height
    puzzle_pos_x = screen_width / 2 - puzzle.width * puzzle_scale / 2
    puzzle_pos_y = screen_height / 2 - puzzle.height * puzzle_scale / 2

    puzzle_size = (puzzle_pos_x,
                   puzzle_pos_y,
                   puzzle.width * puzzle_scale,
                   puzzle.height * puzzle_scale)
    border_size = (puzzle_pos_x - 10,
                   puzzle_pos_y - 10,
                   puzzle.width * puzzle_scale + 20,
                   puzzle.height * puzzle_scale + 20)

    pygame.draw.rect(
        DISPLAY, BLACK, border_size)

    puzzle_grid = [PuzzleBox(Rect(x * puzzle_scale + puzzle_pos_x + 1,
                                  y * puzzle_scale + puzzle_pos_y + 1,
                                  puzzle_scale - 2,
                                  puzzle_scale - 2))
                   for x in range(puzzle.width) for y in range(puzzle.height)]

    for block in puzzle_grid:
        pygame.draw.rect(DISPLAY, block.color, block.rect)

    space_font = pygame.font.Font('freesansbold.ttf', int(puzzle_scale / 1.5))
    space_result = space.all()

    # for s in range(space.count()):
    #     num_placement = puzzle_grid[space_result[s].space_x][space_result[s].space_y]
    #     for t in range(2):
    #         num_placement[t] += puzzle_scale / 2 - 1
    #     current_num = str(space_result[s].space_n)
    #     text = space_font.render(current_num, True, RED)
    #     textrect = text.get_rect()
    #     textrect.center = (num_placement[0], num_placement[1])
    #     DISPLAY.blit(text, textrect)

    while True:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                try:
                    clk = [s for s in puzzle_grid if s.rect.collidepoint(pos)][0]
                except:
                    clk = ''
                else:
                    clk.state += 1 if clk.state < 2 else -2
                    clk.update()
                    pygame.draw.rect(DISPLAY, clk.color, clk.rect)
                    pygame.display.update(clk.rect)

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


main()
