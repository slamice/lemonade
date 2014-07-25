from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine("sqlite:///database.db", echo = False)
session = scoped_session(sessionmaker(bind=engine,
                                        autocommit = False,
                                        autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

# Class definitions

class Project(Base):
    __tablename__ = "projects"

    #id, title, description, source text
    id          = Column(Integer, primary_key = True)
    title       = Column(String(50), nullable = False)
    description = Column(String(200), nullable = False)
    source_text = Column(Text, nullable = False)

class Commit(Base):
    __tablename__ = "commits"

    #id, project_id, parent_id, timestamp, message, diffs
    id          = Column(Integer, primary_key = True)
    project_id  = Column(Integer, ForeignKey('projects.id'), nullable = False)
    parent_id   = Column(Integer, nullable = True)
    timestamp   = Column(DateTime, nullable = False)
    message     = Column(String(140), nullable = False)
    diffs       = Column(Text, nullable = False)
    # diffs: a list of dictionaries

    project = relationship("Project", backref=backref("Commit"))

def main():
    pass

if __name__ == "__main___":
    main()