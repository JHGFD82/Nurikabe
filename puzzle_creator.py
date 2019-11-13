# INITIALIZE TOOLS AND BUILD TABLES #
from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///nurikabe_puzzles.sqlite', echo=True)
Base = declarative_base()

Session = sessionmaker(bind=engine)
session = Session()


class Collection(Base):
    __tablename__ = 'collections'
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    completed = Column(Boolean, default=False, nullable=False)
    puzzles = relationship('Puzzle', backref='puzzles')


class Puzzle(Base):
    __tablename__ = 'puzzles'
    collection_id = Column(Integer, ForeignKey('collections.id'))
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    catalog_num = Column(Integer)
    width = Column(Integer)
    height = Column(Integer)
    difficulty = Column(Integer)
    completed = Column(Boolean, default=False, nullable=False)
    spaces = relationship('Space', backref='spaces')


class Space(Base):
    __tablename__ = 'spaces'
    puzzle_id = Column(Integer, ForeignKey('puzzles.id'))
    id = Column(Integer, unique=True, primary_key=True, autoincrement=True)
    x = Column(Integer)
    y = Column(Integer)
    n = Column(Integer)
    answer = Column(Integer)


if not engine.table_names():
    Base.metadata.create_all(engine)

    collection = Collection(name='Tutorial Set')
    collection.puzzles = [Puzzle(catalog_num=1, width=4, height=4, difficulty=0)]
    session.add(collection)
    session.commit()

    test = session.query(Puzzle).filter_by(id=1).one()
    test.spaces = [Space(x=a+1, y=b+1, answer=0) for b in range(4) for a in range(4)]
    session.add(test)
    session.commit()

    test = session.query(Space).filter_by(puzzle_id=1)
    test[0:2].answer = 1
    session.commit()
