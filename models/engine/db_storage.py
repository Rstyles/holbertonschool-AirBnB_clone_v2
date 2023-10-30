#!/usr/bin/python3
import os
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State

from models.user import User

"""manages mysql db storage for Holberton ABnB"""


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """initializes the DBStorage"""
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from models.base_model import Base

        user = os.getenv("HBNB_MYSQL_USER")
        password = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine(
            f"mysql+mysqldb://{user}:{password}@{host}/{db}", pool_pre_ping=True
        )
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine)
        self.__session = Session()

    def all(self, cls=None) -> dict:
        """returns a dictionary of all objects of type cls. If None returns all"""
        dictionary = {}
        if cls is None:
            classes = [State, City, User, Place, Review, Amenity]
            for cls in classes:
                for obj in self.__session.query(cls).all():
                    dictionary[type(obj).__name__ + "." + obj.id] = obj
            # for obj in self.__session.query(
            #     User, State, City, Amenity, Place, Review
            # ).all():
            #     dictionary[type(obj).__name__ + "." + obj.id] = obj
        else:
            for obj in self.__session.query(cls).all():
                dictionary[type(obj).__name__ + "." + obj.id] = obj
        return dictionary

    def new(self, obj):
        """adds an object to the db"""
        self.__session.add(obj)

    def save(self):
        """saves the session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes from the current database session obj if not None"""
        if obj:
            self.__session.delete(obj)
        self.__session.commit()

    def reload(self):
        """reloads data from the database"""
        from sqlalchemy.orm import sessionmaker
        from models.base_model import Base
        from sqlalchemy.orm import scoped_session

        Base.metadata.create_all(self.__engine)
        session_facory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_facory)
        self.__session = Session()
