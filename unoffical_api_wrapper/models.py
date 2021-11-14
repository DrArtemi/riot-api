from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)


Base = declarative_base()


def create_table(engine):
    Base.metadata.create_all(engine)


class Leagues(Base):
    __tablename__ = "leagues"

    id = Column(Integer, primary_key=True)
    riot_id = Column('riot_id', String(50), unique=True)
    slug = Column('slug', String(50), unique=True)
    name = Column('name', String(150))
    region = Column('region', String(50))
    image_url = Column('image_url', String(150))
    priority = Column('priority', Integer)
    priority_position = Column('priority_position', Integer)
    priority_status = Column('priority_status', String(50))


class Tournaments(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True)
    riot_id = Column('riot_id', String(50), unique=True) 
    slug = Column('slug', String(50), unique=True)
    start_date = Column('start_date', DateTime)
    end_date = Column('end_date', DateTime)
    # A tournament has one league
    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=False, index=True)
    league = relationship("Leagues", backref="tournaments")
