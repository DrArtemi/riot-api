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
    # Get information from riot api
    leagues = api.get_leagues()
    league_ids = [l["id"] for l in leagues]
            
    # Save leagues to database
    for league in leagues:
        db.add_league(league)

    # Get tournaments for each league
    for league_id in league_ids:
        tournaments = api.get_tournaments(league_id)
        tournament_ids = [t["id"] for t in tournaments]
        
        # Save tournaments to database
        for tournament in tournaments:
            db.add_tournament(tournament, league_id)
        
        # TODO: Building
        # Get matches for each tournament
        # for tournament_id in tournament_ids:
        #     standings = api.get_standings(tournament_id)
        #     stages = standings[0]["stages"]
            
        #     if len(stages) == 0:
        #         continue
            
        #     breakpoint() 
            


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