from tqdm import tqdm
import argparse
from api import RiotUnofficialApi
from database import DBUtility
from time import sleep


def parse_arguments():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--user", type=str, help="Postgresql username", required=True)
    parser.add_argument("--password", type=str, help="Postgresql password", required=True)
    parser.add_argument("--database", type=str, help="Postgresql databse", default="riot_stats")
    parser.add_argument("--api-key", type=str, help="Riot unofficial api key", required=True)
    
    return parser.parse_args()


def feed_database(api, db):
    # LEAGUES
    leagues = api.get_leagues()
    for league in tqdm(leagues, desc="Leagues"):
        db.add_league(league)
    teams = api.get_teams()
    for team in tqdm(teams, desc="Teams"):
        # (tdb = invalid)
        if team["status"] == "archived" or team["slug"] == 'tbd':
            continue
        players = team.pop("players")
        # Add team
        db.add_team(team)
        
        # Add players
        for player in tqdm(players, desc="Players"):
            db.add_player(player, team["id"])

    # TOURNAMENTS
    for league in tqdm(leagues, desc="Leagues"):
        tournaments = api.get_tournaments(league["id"])
                
        # STAGES
        for tournament in tqdm(tournaments, desc="Tournaments"):
            standings = api.get_standings(tournament["id"])
            stages = standings[0]["stages"]
            
            # If no stages in tournament, don't add it
            if len(stages) == 0:
                continue
            
            # Add tournament
            db.add_tournament(tournament, league["id"])
            
            # Add stages
            for stage in tqdm(stages, desc="Stages"):
                sections = stage.pop("sections", [])
                db.add_stage(stage, tournament["id"])
                
                # Add matches
                matches = []
                for section in sections:
                    for match in section["matches"]:
                        match["section"] = section["name"]
                        matches.append(match.copy())
                
                for match in tqdm(matches, desc="Matches"):
                    # match_final_state = api.get_match_details(match["id"])
                    # match_evolution = api.get_match_evolution(match["id"], freq=60)
                    db.add_match(match, stage, tournament["id"], league["id"])


if __name__ == '__main__':
    args = parse_arguments()
    
    api = RiotUnofficialApi(
        api_key=args.api_key,
        lang="en-US"
    )
    db = DBUtility(
        user=args.user,
        password=args.password,
        database=args.database
    )
    
    feed_database(api, db)