# INITIALIZE TOOLS AND BUILD TABLES #

from sqlalchemy import create_engine, MetaData, Table, Column, Integer,\
    Boolean, String, insert, func, orm

engine = create_engine('sqlite:///nurikabe_puzzles.sqlite')
metadata = MetaData()
session = orm.sessionmaker(bind=engine)
session = session()

if not engine.table_names():
    collection_table = Table('collections', metadata,
                             Column('collection_id', Integer(), unique=True, primary_key=True),
                             Column('name', String(50), unique=True),
                             Column('completed', Boolean(), default=False, nullable=False)
                             )

    puzzle_table = Table('puzzles', metadata,
                         Column('collection_id', Integer()),
                         Column('puzzle_id', Integer(), unique=True, primary_key=True),
                         Column('catalog_num', Integer()),
                         Column('width', Integer()),
                         Column('height', Integer()),
                         Column('difficulty', Integer()),
                         Column('completed', Boolean(), default=False, nullable=False)
                         )

    spaces_table = Table('spaces', metadata,
                         Column('puzzle_id', Integer()),
                         Column('space_x', Integer()),
                         Column('space_y', Integer()),
                         Column('space_n', Integer())
                         )

    metadata.create_all(engine)

# TEST TABLE CREATION #

collection = Table('collections', metadata, autoload=True, autoload_with=engine)
puzzle = Table('puzzles', metadata, autoload=True, autoload_with=engine)
space = Table('spaces', metadata, autoload=True, autoload_with=engine)

print(collection.columns.keys())
print(puzzle.columns.keys())
print(space.columns.keys())

# INSERT INITIAL DATA INTO TABLE #
if session.query(puzzle).count() < 1:
    stmt_collection = insert(collection).values(collection_id=0, name='tutorial')
    stmt_puzzle = insert(puzzle).values(collection_id=0, puzzle_id=0, catalog_num=1,
                                        width=4, height=4, difficulty=0)
    stmt_space = insert(space).values(puzzle_id=0, space_x=1, space_y=1, space_n=4)

    connection = engine.connect()

    results1 = connection.execute(stmt_collection)
    results2 = connection.execute(stmt_puzzle)
    results3 = connection.execute(stmt_space)

print(session.query(puzzle).count())