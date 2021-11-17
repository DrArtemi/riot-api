from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Leagues, Matches, Players, Stages, Teams, Tournaments, create_table
import dateparser


class DBUtility:
    """This class is used to store league data to database.
    """
    
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

    def add_stage(self, stage, tournament_id):
        session = self.Session()
        tournament = session.query(Tournaments).filter_by(
            riot_id=tournament_id
        ).first()
        exist_stage = session.query(Stages).join(Stages.tournament).\
            filter((Tournaments.riot_id == tournament_id), (Stages.slug == stage["slug"])).first()
        stage_obj = exist_stage if exist_stage is not None else Stages()
        if exist_stage is None:
            stage_obj.slug = stage["slug"]
        stage_obj.name = stage["name"]
        stage_obj.type = stage["type"]
        if tournament:
            stage_obj.tournament = tournament
    
        session.add(stage_obj)
        session.commit()
        session.close()

    def add_team(self, team):
        session = self.Session()
        exist_team = session.query(Teams).filter_by(
            riot_id=team["id"]
        ).first()
        team_obj = exist_team if exist_team is not None else Teams()
        if exist_team is None:
            team_obj.riot_id = team["id"]
        team_obj.slug = team["slug"]
        team_obj.name = team["name"]
        team_obj.code = team["code"]
        team_obj.image = team["image"]
        team_obj.alt_image = team["alternativeImage"]
        team_obj.bg_image = team["backgroundImage"]
        team_obj.status = team["status"]
    
        session.add(team_obj)
        session.commit()
        session.close()
    
    def add_player(self, player, team_id):
        session = self.Session()
        exist_team = session.query(Teams).filter_by(
            riot_id=team_id
        ).first()
        exist_player = session.query(Players).filter_by(
            riot_id=player["id"]
        ).first()
        player_obj = exist_player if exist_player is not None else Players()
        if exist_player is None:
            player_obj.riot_id = player["id"]
            if exist_team:
                player_obj.current_team = exist_team
        player_obj.summoner_name = player["summonerName"]
        player_obj.first_name = player["firstName"]
        player_obj.last_name = player["lastName"]
        player_obj.image = player["image"]
        player_obj.role = player["role"]
        
        if exist_team:
            player_obj.teams.append(exist_team)

        session.add(player_obj)
        session.commit()
        session.close()

    def add_match(self, match, stage, tournament_id, league_id):
        session = self.Session()
        with session.no_autoflush:
            exist_stage = session.query(Stages).join(Stages.tournament).\
                filter((Tournaments.riot_id == tournament_id), (Stages.slug == stage["slug"])).first()
            exist_match = session.query(Matches).filter_by(
                riot_id=match["id"]
            ).first()
            match_obj = exist_match if exist_match is not None else Matches()
            if exist_match is None:
                match_obj.riot_id = match["id"]
            match_obj.state = match["state"]
            if exist_stage:
                match_obj.stage = exist_stage
            
            teams = match.pop("teams")
            for i, team in enumerate(teams):
                exist_team = session.query(Teams).filter_by(
                    riot_id=team["id"]
                ).first()
                if exist_team is None:
                    continue
                if exist_team.league is None:
                    league = session.query(Leagues).filter_by(
                        riot_id=league_id
                    ).first()
                    exist_team.league = league
                if i == 0:
                    match_obj.team_1 = exist_team
                    match_obj.team_1_win = team["result"]["outcome"] == "win"
                elif i == 1:
                    match_obj.team_2 = exist_team
                    match_obj.team_2_win = team["result"]["outcome"] == "win"
            
            session.add(match_obj)
            session.commit()
            session.close()