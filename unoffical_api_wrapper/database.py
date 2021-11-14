from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Leagues, Tournaments, create_table
import dateparser


class DBUtility:
    
    def __init__(self, user: str, password: str, database: str) -> None:
        engine = create_engine(f'postgresql://{user}:{password}@localhost:5432/{database}')
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
    
    def add_league(self, league):
        session = self.Session()
        exist_league = session.query(Leagues).filter_by(
            riot_id=league["id"]
        ).first()
        league_obj = exist_league if exist_league is not None else Leagues()
        if exist_league is None:
            league_obj.riot_id = league["id"]
            league_obj.slug = league["slug"]
        league_obj.name = league["name"]
        league_obj.region = league["region"]
        league_obj.image_url = league["image"]
        league_obj.priority = league["priority"]
        league_obj.priority_position = league["displayPriority"]["position"]
        league_obj.priority_status = league["displayPriority"]["status"]                
    
        session.add(league_obj)
        session.commit()
        session.close()
    
    def add_tournament(self, tournament, league_id):
        session = self.Session()
        league = session.query(Leagues).filter_by(
            riot_id=league_id
        ).first()
        exist_tournament = session.query(Tournaments).filter_by(
            riot_id=tournament["id"]
        ).first()
        tournament_obj = exist_tournament if exist_tournament is not None else Tournaments()
        if exist_tournament is None:
            tournament_obj.riot_id = tournament["id"]
            tournament_obj.slug = tournament["slug"]
        tournament_obj.start_date = dateparser.parse(tournament["startDate"])
        tournament_obj.end_date = dateparser.parse(tournament["endDate"])
        if league:
            tournament_obj.league = league
    
        session.add(tournament_obj)
        session.commit()
        session.close()
