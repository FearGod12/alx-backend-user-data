#!/usr/bin/env python3
"""DB module
"""
from typing import TypeVar
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

from user import User

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from user import Base


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> TypeVar("User"):
        """adss a user object to database and return the user
        :param
        email - the email address of the user
        hashed_password- password of the user that has been
        hashed using bcrypt"""
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        self.__session.add(user)
        self.__session.commit()
        return user

    def find_user_by(self, **kwargs):
        """
        retrieves a user based on the provided attributes
        :param kwargs: attributes of the user
        :return: user
        """
        try:
            for key, val in kwargs.items():
                user = self.__session.query(User).filter(key==val).first()
                if user is None:
                    raise NoResultFound
                return user

        except InvalidRequestError as e:
            self.__session.rollback()
            raise e
