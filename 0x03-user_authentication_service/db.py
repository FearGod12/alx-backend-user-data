#!/usr/bin/env python3
"""DB module
"""
from typing import TypeVar, Dict
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
        self._engine = create_engine("sqlite:///a.db", echo=False)
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

    def add_user(self, email: str, hashed_password: str) -> User:
        """adss a user object to database and return the user
        :param
        email - the email address of the user
        hashed_password- password of the user that has been
        hashed using bcrypt"""
        if not email or not hashed_password:
            return
        user = User(email=email, hashed_password=hashed_password)
        self._session
        self.__session.add(user)
        self.__session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        retrieves a user based on the provided attributes
        :param kwargs: attributes of the user
        :return: user
        """
        if not kwargs:
            raise InvalidRequestError
        try:
            return self._session.query(User).filter_by(**kwargs).one()
        except Exception:
            raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        updates the user instance if it has the attribute
        :return: None
        """
        user = self.find_user_by(id=user_id)
        if user is not None:
            try:
                for key, val in kwargs.items():
                    if hasattr(user, key):
                        setattr(user, key, val)
                    else:
                        raise ValueError
                self.__session.commit()
            except AttributeError:
                raise ValueError
