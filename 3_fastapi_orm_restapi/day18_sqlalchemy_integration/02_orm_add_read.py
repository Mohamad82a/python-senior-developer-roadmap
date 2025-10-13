from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///test.db')
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

Base.metadata.create_all(bind=engine)

db = SessionLocal()
new_user = User(name='John', age=22)
db.add(new_user)
db.commit()

for user in db.query(User).all():
    print(user.name, user.age)


