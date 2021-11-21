from typing import final
import requests
import datetime


class RiotUnofficialApi:
    """This class wraps the unofficial riot API.
    """
    
    def __init__(self, api_key: str, lang: str = "en-US") -> None:
        self.headers = { "x-api-key": api_key }
        self.params = { "hl": lang }
    
    def get_leagues(self) -> list:
        """Gathers every Riot leagues

        Returns:
            list: List of leagues.
        """
        all_leagues = requests.get(
            url="https://esports-api.lolesports.com/persisted/gw/getLeagues",
            headers=self.headers,
            params=self.params
        )
        if all_leagues.status_code != 200:
            raise all_leagues.raise_for_status()
        leagues = all_leagues.json()['data']['leagues']
        return leagues

    def get_tournaments(self, league_id: int) -> list:
        """Gathers all tournaments for a specific league.

        Args:
            league_id (int): League ID.
            
        Returns:
            list: List of tournaments.
        """
        params = dict(
            self.params,
            leagueId=league_id
        )
        league_tournaments = requests.get(
            url="https://esports-api.lolesports.com/persisted/gw/getTournamentsForLeague",
            headers=self.headers,
            params=params
        )
        if league_tournaments.status_code != 200:
            raise league_tournaments.raise_for_status()
        league_tournaments = league_tournaments.json()['data']['leagues'][0]['tournaments']
        return league_tournaments
    
    def get_standings(self, tournament_id: int) -> list:
        """Gathers standings for a specific tounament.
        Returns also matches for the standings.

        Args:
            tournament_id (int): Tournament ID.

        Returns:
            list: List of standings, each containing played matches.
        """
        params = dict(
            self.params,
            tournamentId=tournament_id,
        )
        tournament_standings = requests.get(
            url="https://esports-api.lolesports.com/persisted/gw/getStandings",
            headers=self.headers,
            params=params
        )
        return tournament_standings.json()['data']['standings']
    
    def get_teams(self) -> list:
        """Gathers teams. Returns also current players for each team.

        Returns:
            list: [description]
        """
        teams = requests.get(
            url="https://esports-api.lolesports.com/persisted/gw/getTeams",
            headers=self.headers,
            params=self.params
        )
        return teams.json()['data']['teams']
    
    @staticmethod
    def parse_game(data):
        final_state = {
            "timestamp": data["frames"]["rfc460Timestamp"],
            "blue_team": {
                "players": []
            },
            "red_team": {
                "players": []
            }
        }
        
        # Parse data from game state
        final_state["blue_team"]["players"] += data["blueTeamMetadata"].pop("participantMetadata")
        final_state["blue_team"].update(data["blueTeamMetadata"])
        final_state["red_team"]["players"] += data["redTeamMetadata"].pop("participantMetadata")
        final_state["red_team"].update(data["redTeamMetadata"])
                
        # Parse data from frames
        frames = data.pop("frames")
        tmp_players = frames.pop("participants")
        for player in tmp_players:
            f_blue_player = [p for p in final_state["blue_team"]["players"] if p["participantId"] == player["participantId"]]
            f_red_player = [p for p in final_state["red_team"]["players"] if p["participantId"] == player["participantId"]]
            f_player = f_blue_player + f_red_player
            if len(f_player) > 0:
                f_player[0].update(player)
        # Parse data from teams
        tmp_players = frames["blueTeam"].pop("participants")
        for player in tmp_players:
            f_player = [p for p in final_state["blue_team"]["players"] if p["participantId"] == player["participantId"]]
            if len(f_player) == 0:
                final_state["blue_team"]["players"].append(player)
            else:
                f_player[0].update(player)
        final_state["blue_team"].update(frames["blueTeam"])
        
        tmp_players = frames["redTeam"].pop("participants")
        for player in tmp_players:
            f_player = [p for p in final_state["red_team"]["players"] if p["participantId"] == player["participantId"]]
            if len(f_player) == 0:
                final_state["red_team"]["players"].append(player)
            else:
                f_player[0].update(player)
        final_state["red_team"].update(frames["redTeam"])
        
        breakpoint()
        
        return final_state
        

    def get_match_details(self, match_id) -> dict:
        params = dict(
            self.params,
            startingTime=get_usable_date(),
        )
        # Game ID = Match ID + 1
        match_details = requests.get(
            url=f"https://feed.lolesports.com/livestats/v1/details/{int(match_id) + 1}",
            headers=self.headers,
            params=params
        )
        if match_details.status_code != 200:
            raise match_details.raise_for_status()
        match_details = match_details.json()
        match_frames = match_details["frames"]
        
        game_details = requests.get(
            url=f"https://feed.lolesports.com/livestats/v1/window/{int(match_id) + 1}",
            headers=self.headers,
            params=params
        )
        if game_details.status_code != 200:
            raise game_details.raise_for_status()
        game_details = game_details.json()
        game_metadata = game_details["gameMetadata"]
        game_frames = game_details["frames"]
        
        # Merge last frames from match and game to get final state
        final_state = match_frames[-1]
        final_state.update(game_frames[-1])
        
        game = {
            **game_metadata,
            "frames": final_state
        }
        
        return self.parse_game(game)
        
        
        # blue_team_data = dict()
        # blue_players_data = dict()
        # red_team_data = dict()
        # red_players_data = dict()
        # # extract blue_players_data
        # blue_players_data.update({"participantMetadata": g_data["blueTeamMetadata"].pop("participantMetadata")})
        # blue_team_data.update(g_data["blueTeamMetadata"])

        # print(game["final_state"]["blueTeam"].keys())
        # blue_players_data.update({"final_state_team_participantMetadata": game["final_state"]["blueTeam"].pop("participants")})
        # blue_team_data.update(game["final_state"]["blueTeam"])
        # blue_players_data


def get_usable_date():
    mydate = datetime.datetime.now()
    minute = datetime.timedelta(minutes=120)
    mydate_final = (mydate - minute).strftime("%Y-%m-%dT%H:%M:%S")
    head = mydate_final[:-2]
    tail = round(int(mydate_final[-2:]), -1)
    sec = str(tail)
    if len(sec) < 2:
        sec = '0' + sec
    return head + str(sec) + 'Z'


if __name__ == '__main__':
    import pandas as pd
    
    api = RiotUnofficialApi(
        api_key="0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z",
        lang="en-US"
    )
    
    print(api.get_match_details("105568157422015211"))
