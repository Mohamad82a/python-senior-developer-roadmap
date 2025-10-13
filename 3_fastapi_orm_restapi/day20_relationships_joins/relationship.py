from sqlalchemy import ForeignKey, create_engine, Column, String, Integer
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///day20_relationships_joins.db')
SessionLocal = sessionmaker(bind=engine)

class Author(Base):
    __tablename__ = 'author'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship('Book', back_populates='author')


class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('author.id'))
    author = relationship('Author', back_populates='books')

