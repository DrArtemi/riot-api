import argparse
from api import RiotUnofficialApi
from database import DBUtility


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
    league_ids = [l["id"] for l in leagues]
    for league in leagues:
        db.add_league(league)
    
    # TODO: ADD TEAMS
    # TODO: ADD PLAYERS (on va re-add les players au niveau des matchs pour les changements d'equipes)

    # TOURNAMENTS
    for league_id in league_ids:
        tournaments = api.get_tournaments(league_id)
                
        # STAGES
        for tournament in tournaments:
            standings = api.get_standings(tournament["id"])
            stages = standings[0]["stages"]
            
            # If no stages in tournament, don't add it
            if len(stages) == 0:
                continue
            
            # Add tournament
            db.add_tournament(tournament, league_id)
            
            # Add stages
            for stage in stages:
                db.add_stage(stage, tournament["id"])            


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