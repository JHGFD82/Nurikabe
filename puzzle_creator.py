# INITIALIZE TOOLS AND BUILD TABLES #
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy import create_engine, exists
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from os import walk
import numpy as np

engine = create_engine('sqlite:///nurikabe_puzzles.sqlite', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Collection(Base):
    __tablename__ = 'collections'
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    completed = Column(Boolean, default=False, nullable=False)


class Puzzle(Base):
    __tablename__ = 'puzzles'
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    collection_id = Column(Integer, ForeignKey('collections.id'))
    collection = relationship(Collection)
    catalog_num = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    difficulty = Column(Integer)
    completed = Column(Boolean, default=False, nullable=False)


class Space(Base):
    __tablename__ = 'spaces'
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    puzzle_id = Column(Integer, ForeignKey('puzzles.id'))
    puzzle = relationship(Puzzle)
    x = Column(Integer)
    y = Column(Integer)
    n = Column(Integer)


if not engine.table_names():
    Base.metadata.create_all(engine)

    puzzle_folder = 'Puzzles/'
    (_, _, filenames) = next(walk(puzzle_folder))

    for fs in filenames:
        fs_split = fs.split('.')[0].split('-')
        fs = str(puzzle_folder + fs)
        imported = np.genfromtxt(fs, delimiter=",", dtype=int)
        print(imported)
        puzzle_size = (len(imported[0, :]), len(imported[:, 0]))

        collection_exists = session.query(exists().where(Collection.name == fs_split[0])).scalar()
        if collection_exists:
            collection = session.query(Collection).filter(Collection.name == fs_split[0]).first()
        else:
            collection = Collection(name=fs_split[0])
            session.add(collection)
            session.commit()

        puzzle = Puzzle(catalog_num=int(fs_split[1]),
                        width=puzzle_size[0], height=puzzle_size[1],
                        difficulty=int(fs_split[2]))

        puzzle.collection = collection
        session.add(puzzle)
        session.commit()

        for x, y in [(x, y) for y in range(puzzle_size[1]) for x in range(puzzle_size[0])]:
            print(x, y)
            value = imported[y, x]
            space = Space(x=x+1, y=y+1, n=int(value))
            space.puzzle = puzzle
            session.add(space)

        session.commit()
