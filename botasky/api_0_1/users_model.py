#! /usr/bin/python2.7
# -*- coding: utf-8 -*-

"""
Created on 2017-7-04


@module: users_model
@used: identify users'model and init it
"""


from sqlalchemy import String, Integer, UniqueConstraint, Index, create_engine
from sqlalchemy import Column
from sqlalchemy.orm import sessionmaker
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

__all__ = ['User', 'Init']
__author__ = 'zhihao'


class User(Base):
    '''users model'''
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    password_hash = Column(String(128))
    __table_args__ = (
        UniqueConstraint('name', 'password_hash', name='uix_name_pwd'),
        Index('ix_name', 'name'),
    )

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Init():
    '''init users model'''
    @staticmethod
    def Engine(usr, pwd, host, port, db):
        dbconn = "mysql+pymysql://{usr}:{pwd}@{host}:{port}/{db}".format(usr=usr, pwd=pwd, host=host,
                                                                         port=port, db=db)
        engine = create_engine(dbconn, echo=True)
        return engine

    @staticmethod
    def Session(engine):
        # init session
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        return session

    @staticmethod
    def Insert_User(session, username, password):
        u = User()
        u.password = password
        new_user = User(name=username, password_hash=u.password_hash)
        session.add(new_user)
        session.commit()
        session.close()
