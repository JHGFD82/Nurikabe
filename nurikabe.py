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
WHITE = (230, 230, 210)
BORDER_COLOR = (50, 40, 20)
BLACK = (0, 0, 0)
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


# Application settings
screen_width = 1024
screen_height = 768
DISPLAY = pygame.display.set_mode((screen_width,
                                   screen_height))


# Begin drawing
def main():
    # Set up list of undo moves
    undo_list = []

    # Draw initial box
    DISPLAY.fill(BACKGROUND)

    # Set up current puzzle object
    puzzle_num = 3

    puzzle = session.query(PuzzleDB) \
        .filter(PuzzleDB.id == puzzle_num).first()
    space = session.query(SpaceDB.id, SpaceDB.x, SpaceDB.y, SpaceDB.n) \
        .filter(SpaceDB.puzzle_id == puzzle_num)
    space_result = space.all()

    # Set up individual box object for tools
    class ToolBox:
        def __init__(self, rect):
            self.rect = rect
            self.color = WHITE

    # Set up individual box object within puzzle
    class PuzzleBox:
        def __init__(self, rect):
            self.rect = rect
            self.state = 0
            self.color = WHITE

        def update(self):
            if self.state == 1:
                self.color = BLACK
            else:
                self.color = WHITE

    # Establish puzzle scale for objects on screen
    puzzle_scale = 0
    for i in range(100, 700, 100):
        puzzle_scale = i / puzzle.height
        if puzzle_scale > 70:
            break

    # Set position of puzzle on screen
    puzzle_pos_x = screen_width / 2 - puzzle.width * puzzle_scale / 2
    puzzle_pos_y = screen_height / 2 - puzzle.height * puzzle_scale / 2

    puzzle_border = Rect(puzzle_pos_x - 10,
                         puzzle_pos_y - 10,
                         puzzle.width * puzzle_scale + 20,
                         puzzle.height * puzzle_scale + 20)

    # Draw puzzle
    pygame.draw.rect(
        DISPLAY, BORDER_COLOR, puzzle_border)

    # Set up puzzle tools
    tool_border = Rect(puzzle_border[0] + puzzle_border[2] + 10,
                       puzzle_border[1], 70, 70)
    pygame.draw.rect(
        DISPLAY, BORDER_COLOR, tool_border)

    tool_grid = [ToolBox(Rect((tool_border[0] + 10, tool_border[1] + 10,
                               tool_border[2] - 20, tool_border[3] - 20)))]

    for tool in tool_grid:
        pygame.draw.rect(DISPLAY, WHITE, tool)

    # Set up puzzle box grid
    puzzle_grid = [PuzzleBox(Rect(x * puzzle_scale + puzzle_pos_x + 1,
                                  y * puzzle_scale + puzzle_pos_y + 1,
                                  puzzle_scale - 2,
                                  puzzle_scale - 2))
                   for y in range(puzzle.height) for x in range(puzzle.width)]

    for block in puzzle_grid:
        pygame.draw.rect(DISPLAY, block.color, block.rect)

    def center_draw(shape):
        x = shape.x + puzzle_scale / 2 - 1
        y = shape.y + puzzle_scale / 1.8 - 1
        result = (x, y)
        return result

    # Display guide numbers
    space_font = pygame.font.Font('freesansbold.ttf', int(puzzle_scale / 1.5))
    guide_num = [s for s in space_result if s.n > 0]
    guide_num_in_list = [(s.y - 1) * puzzle.width + s.x - 1 for s in guide_num]
    for a, b in zip(guide_num, guide_num_in_list):
        text = space_font.render(str(a.n), True, BLACK)
        textrect = text.get_rect()
        textrect.center = center_draw(puzzle_grid[b].rect)
        DISPLAY.blit(text, textrect)

    def block_activate(m_pos, state):
        clicked = ''
        try:
            clicked = [s for s in puzzle_grid if
                       s.rect.collidepoint(m_pos) and
                       puzzle_grid.index(s) not in guide_num_in_list][0]
        except IndexError:
            pass
        else:
            # Undo steps
            undo_list.append({'box_num': puzzle_grid.index(clicked),
                              'state': clicked.state})

            if state or state == 0:
                clicked.state = state
            else:
                clicked.state += 1 if clicked.state < 2 else -2

            clicked.update()
            pygame.draw.rect(DISPLAY, clicked.color, clicked.rect)
            if clicked.state == 2:
                pygame.draw.circle(DISPLAY, BLACK, center_draw(clicked.rect), 3)
            pygame.display.update(clicked)

        return clicked

    drag = False
    clk = ''
    held_state = ''
    done = False

    # Actual screen stuff
    while True:

        # On event
        for event in pygame.event.get():

            # On event: click
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # On event: click within puzzle
                if puzzle_border.collidepoint(pos[0], pos[1]):
                    drag = True
                    clk, undo_count = block_activate(pos, '')
                    try:
                        held_state = clk.state
                    except AttributeError:
                        drag = False

                # On event: click within tools
                elif tool_border.collidepoint(pos[0], pos[1]):
                    undo_box = puzzle_grid[undo_list[-1]['box_num']]
                    undo_box.state = undo_list[-1]['state']
                    undo_box.update()
                    pygame.draw.rect(DISPLAY, undo_box.color, undo_box.rect)
                    pygame.display.update(undo_box)
                    undo_list.__delitem__(-1)

            # On event: release
            elif event.type == pygame.MOUSEBUTTONUP:
                drag = False
                done = True if [a.state for a in puzzle_grid] == \
                               [1 if b.n == 0 else 0 for b in space_result] else False

            # On event: quit
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # On drag
        if drag:
            pos = pygame.mouse.get_pos()
            try:
                grabbed = [s for s in puzzle_grid if
                           s.rect.collidepoint(pos) and
                           puzzle_grid.index(s) not in guide_num_in_list][0]
            except IndexError:
                pass
            else:
                if grabbed != clk:
                    clk, undo_count = block_activate(pos, held_state)

        pygame.quit() if done else False

        pygame.display.update()


main()
