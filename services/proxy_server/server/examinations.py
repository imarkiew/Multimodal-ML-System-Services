from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Examinations(Base):
    """Class representing 'examinations' entity in database

    """

    __tablename__ = 'examinations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    kind = Column(String)
    title = Column(String, nullable=True)
    date = Column(String)
    results = Column(String)
    path = Column(String)
    username = Column(String)

    def __init__(self, kind, title, date, results, path, username):
        """
        :param kind:
        :param title:
        :param date:
        :param results:
        :param path:
        :param username:
        """
        self.kind = kind
        self.title = title
        self.date = date
        self.results = results
        self.path = path
        self.username = username

    def __repr__(self):
        """Show informations about examination in form of string

        :return: String with information about examination
        """
        return "Examination({}, {}, {}, {}, {}, {}, {})".format(self.id, self.kind, self.title, self.date, self.results, self.path, self.username)
