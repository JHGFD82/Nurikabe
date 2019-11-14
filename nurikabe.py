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
    id = Column(Integer, primary_key=True)
    catalog_num = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    difficulty = Column(Integer)
    completed = Column(Boolean)


# Set up spaces object
class SpaceDB(Base):
    __tablename__ = 'spaces'
    id = Column(Integer, primary_key=True)
    puzzle_id = Column(Integer)
    x = Column(Integer)
    y = Column(Integer)
    n = Column(Integer)
    answer = Column(Integer)


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
    puzzle_num = 1

    puzzle = session.query(PuzzleDB) \
        .filter(PuzzleDB.id == puzzle_num).first()
    space = session.query(SpaceDB.id, SpaceDB.n, SpaceDB.x, SpaceDB.y, SpaceDB.answer) \
        .filter(SpaceDB.puzzle_id == puzzle_num)
    space_result = space.all()

    # Set up individual box object
    class PuzzleBox:
        def __init__(self, rect):
            self.rect = rect
            self.state = 0
            self.color = WHITE

        def update(self):
            if self.state == 1:
                self.color = BLACK
            elif self.state == 2:
                self.color = WHITE

    # Establish puzzle scale for objects on screen
    puzzle_scale = 0
    for i in range(100, 2000, 100):
        puzzle_scale = i / puzzle.height
        if puzzle_scale > 70:
            break

    # Set position of puzzle on screen
    puzzle_pos_x = screen_width / 2 - puzzle.width * puzzle_scale / 2
    puzzle_pos_y = screen_height / 2 - puzzle.height * puzzle_scale / 2

    border_size = (puzzle_pos_x - 10,
                   puzzle_pos_y - 10,
                   puzzle.width * puzzle_scale + 20,
                   puzzle.height * puzzle_scale + 20)

    # Draw puzzle
    pygame.draw.rect(
        DISPLAY, BLACK, border_size)

    puzzle_grid = [PuzzleBox(Rect(x * puzzle_scale + puzzle_pos_x + 1,
                                  y * puzzle_scale + puzzle_pos_y + 1,
                                  puzzle_scale - 2,
                                  puzzle_scale - 2))
                   for x in range(puzzle.width) for y in range(puzzle.height)]

    for block in puzzle_grid:
        pygame.draw.rect(DISPLAY, block.color, block.rect)

    # Display guide numbers
    space_font = pygame.font.Font('freesansbold.ttf', int(puzzle_scale / 1.5))
    guide_num = [s for s in space_result if s.n is not None]
    for s in guide_num:
        text = space_font.render(str(s.n), True, BLACK)
        textrect = text.get_rect()
        new_x = s.x * puzzle_scale - (puzzle_scale / 2) + puzzle_pos_x
        new_y = s.y * puzzle_scale - (puzzle_scale / 2)  + puzzle_pos_y + (puzzle_scale / 20)
        textrect.center = (new_x, new_y)
        DISPLAY.blit(text, textrect)

    # Actual screen stuff
    while True:
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                try:
                    clk = [s for s in puzzle_grid if s.rect.collidepoint(pos)][0]
                except IndexError:
                    pass
                else:
                    clk.state += 1 if clk.state < 2 else -2
                    clk.update()
                    pygame.draw.rect(DISPLAY, clk.color, clk.rect)
                    pygame.display.update(clk.rect)
                    print('YAAAAAAAY!') if [a.state for a in puzzle_grid] == [b.answer for b in space_result] else ''

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


main()
