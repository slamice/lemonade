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

class Project(Base):
    __tablename__ = "projects"

    id          = Column(Integer, primary_key = True)
    title       = Column(String(50), nullable = False)
    description = Column(String(200), nullable = False)
    source_text = Column(Text, nullable = False)

    @staticmethod
    def query_all_projects():
        projects = session.query(Project).all()
        return projects

    @staticmethod
    def query_project_by_id(project_id):
        project = session.query(Project).filter_by(id = project_id).one()
        return project

    @staticmethod
    def query_project_by_commit_id(commit_id):
        project = session.query(Project).filter_by(commit_id = commit_id).one()
        return project

class Commit(Base):
    __tablename__ = "commits"

    id          = Column(Integer, primary_key = True)
    project_id  = Column(Integer, ForeignKey('projects.id'), nullable = False)
    parent_id   = Column(Integer, nullable = True)
    timestamp   = Column(DateTime, nullable = False)
    message     = Column(String(140), nullable = False)
    diffs       = Column(Text, nullable = False)
    project = relationship("Project", backref=backref("Commit"))

    @staticmethod
    def query_commit_by_id(commit_id):
        commit = session.query(Commit).filter_by(id = commit_id).one()
        return commit

    @staticmethod
    def query_commits_by_proj_id(project_id):
        commits = session.query(Commit).filter_by(project_id = project_id).all()
        return commits

def main():
    Base.metadata.create_all(engine)

if __name__ == "__main___":
    main()