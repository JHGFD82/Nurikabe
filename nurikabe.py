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


# Set up puzzle object
class Puzzle_from_db(Base):
    __tablename__ = 'puzzles'
    puzzle_id = Column(Integer, primary_key=True)
    catalog_num = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    difficulty = Column(Integer)
    completed = Column(Boolean)


# Application settings
screen_width = 1024
screen_height = 768
DISPLAY = pygame.display.set_mode((screen_width,
                                   screen_height))

# Colors
WHITE = (230, 230, 230)
BLACK = (50, 50, 50)
BACKGROUND = (180, 180, 150)


# Begin drawing
def main():
    # Draw initial box
    DISPLAY.fill(BACKGROUND)

    # Set up current puzzle object
    puzzle_num = 0

    puzzle = session.query(Puzzle_from_db)\
        .filter(Puzzle_from_db.puzzle_id == puzzle_num).first()
    print(puzzle.height)

    puzzle_scale = 718 / puzzle.height
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

    for x in range(puzzle.width):
        for y in range(puzzle.height):
            pygame.draw.rect(
                DISPLAY, WHITE, (x * puzzle_scale + puzzle_pos_x + 1,
                                 y * puzzle_scale + puzzle_pos_y + 1,
                                 puzzle_scale - 2,
                                 puzzle_scale - 2)
            )

    font = pygame.font.Font('freesansbold.ttf', int(puzzle_scale))
    text = font.render('4', True, BLACK)
    textrect = text.get_rect()
    textrect.center = (500, 500)
    DISPLAY.blit(text, textrect)

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()


main()
