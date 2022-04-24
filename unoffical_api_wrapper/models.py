from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)


Base = declarative_base()

player_team_association_table = Table('PlayerTeam', Base.metadata,
    Column('team_id', ForeignKey('teams.id'), primary_key=True),
    Column('player_id', ForeignKey('players.id'), primary_key=True)
)


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
    # League
    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=False, index=True)
    league = relationship("Leagues", backref="tournaments")


class Stages(Base):
    __tablename__ = "stages"

    id = Column(Integer, primary_key=True)
    slug = Column('slug', String(50))
    name = Column('name', String(150))
    type = Column('type', String(50))
    # Tournament
    tournament_id = Column(Integer, ForeignKey('tournaments.id'), nullable=False, index=True)
    tournament = relationship("Tournaments", backref="stages")


class Matches(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    riot_id = Column('riot_id', String(50), unique=True)
    date = Column('date', DateTime)
    state = Column('state', String(50))
    final_state = Column('final_state', String())
    evolution = Column('evolution', String())
    
    # Tournament
    stage_id = Column(Integer, ForeignKey('stages.id'), nullable=False, index=True)
    stage = relationship("Stages", backref="matches")
    # teams
    team_1_id = Column(Integer, ForeignKey('teams.id'), nullable=True, index=True)
    team_2_id = Column(Integer, ForeignKey('teams.id'), nullable=True, index=True)
    team_1 = relationship("Teams", foreign_keys=[team_1_id])
    team_2 = relationship("Teams", foreign_keys=[team_2_id])
    team_1_win = Column(Boolean)
    team_2_win = Column(Boolean)


class Teams(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True)
    riot_id = Column('riot_id', String(50), unique=True)
    slug = Column('slug', String(50))
    code = Column('code', String(50))
    name = Column('name', String(150))
    image = Column('image', String(150))
    alt_image = Column('alt_image', String(150))
    bg_image = Column('bg_image', String(150))
    status = Column('status', String(50))
    # League
    league_id = Column(Integer, ForeignKey('leagues.id'), nullable=True, index=True)
    league = relationship("Leagues", backref="teams")


class Players(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True)
    riot_id = Column('riot_id', String(50), unique=True)
    summoner_name = Column('summoner_name', String(50))
    first_name = Column('first_name', String(50))
    last_name = Column('last_name', String(50))
    image = Column('image', String(150))
    role = Column('role', String(50))
    # Current team
    current_team_id = Column(Integer, ForeignKey('teams.id'), nullable=False, index=True)
    current_team = relationship("Teams", backref="current_players")
    # Teams
    teams = relationship("Teams",
                         secondary=player_team_association_table,
                         backref='players')