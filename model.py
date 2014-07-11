from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
import datetime
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session

engine = create_engine("sqlite:///translations.db", echo = False)
session = scoped_session(sessionmaker(bind=engine,
                                        autocommit = False,
                                        autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

# Class definitions

class Project(Base):
	__tablename__ = "projects"

	#id, title, description, source text
	id 			= Column(Integer, primary_key = True)
	title 		= Column(String(50), nullable = False)
	description = Column(String(200), nullable = False)
	source_text = Column(String(3000), nullable = False)

class Commit(Base):
	__tablename__ = "commits"

	#id, project_id, new version, time
	id 			= Column(Integer, primary_key = True)
	project_id 	= Column(Integer, ForeignKey('projects.id'), nullable = False)
	timestamp 	= Column(DateTime, nullable = False)
	translation = Column(String(3000), nullable = False)
	message 	= Column(String(140), nullable = False)

	project = relationship("Project", backref=backref("Commit"))

def main():
	pass

if __name__ == "__main___":
	main()