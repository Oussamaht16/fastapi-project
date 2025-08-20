# hada l fichier 9lk ymatal les tables li rah nsha9ohom fl projet ta3na
from ast import Str
from .database import Base
from sqlalchemy.sql import text
from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship

# hada l fichier halinah ba3d database.py bch ndakhlou fih les models ta3na(tables)
from sqlalchemy import Boolean, Column, Integer, String


# hado homa les type t3 les column tawa3na
# hadi laclass lkhassa b table ta3na par exemple post
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)  # nullable maenaha not null
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )
    # now we use one to many method to create a relationship between the Post and User models
    owner_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # relation
    owner = relationship("Users")


# mais remarquna bli tbadal haja lahna marahich ttpliqa f database , lazm nzido library wakhdokhra


# 9alk omba3d troh ll main file ta3k o tkopi meta.Base.metadata.create_all(bind=engine)


#     _______||| ________ pour tableau jdid
class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)  # nullable maenaha not null
    email = Column(
        String, nullable=False, unique=True
    )  # unique bch ma ykounch 3ndna 2 users b nafs l email
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), nullable=False
    )


# ____________|||| votes table for post |||___________
class Vote(Base):
    __tablename__ = "votes"

    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )

    post = relationship("Post")
    user = relationship("Users")
