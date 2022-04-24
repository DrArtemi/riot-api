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
        if tournament_standings.status_code != 200:
            raise tournament_standings.raise_for_status()
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
        if teams.status_code != 200:
            raise teams.raise_for_status()
        return teams.json()['data']['teams']
    
    @staticmethod
    def parse_game(data: dict) -> dict:
        """Clean merged data from game and match frames.

        Args:
            data (dict): Raw data of game and match frames merge.

        Returns:
            dict: Cleaned data.
        """
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
                
        return final_state
        

    def get_match_details(self, match_id: str) -> dict:
        """This endpoint fetches match final state details.

        Args:
            match_id (str): Match id to fetch.

        Raises:
            match_details.raise_for_status: Error if match doesn't exist.
            game_details.raise_for_status: Error if game doesn't exist.

        Returns:
            dict: Cleaned match detailed data.
        """
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
            return None
        match_details = match_details.json()
        match_frames = match_details["frames"]
        
        game_details = requests.get(
            url=f"https://feed.lolesports.com/livestats/v1/window/{int(match_id) + 1}",
            headers=self.headers,
            params=params
        )
        if game_details.status_code != 200:
            return None
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
    
    @staticmethod
    def get_team_stats(team, frames):
        res = dict()
        for key in frames[0][team]:
            if key == "participants":
                res[key] = dict()
                for idx, p in enumerate(frames[0][team]["participants"]):
                    p_id = p.get("participantId")
                    res[key][p_id] = dict()
                    for k in p:
                        if k == "participantId":
                            continue
                        res[key][p_id][k] = [f[team][key][idx][k] for f in frames]
            else:
                res[key] = [f[team][key] for f in frames]
        return res
    
    def get_match_evolution(self, match_id: str, freq: int = 10) -> dict:
        """Fetches metric through the game.

        Args:
            match_id (str): Match id to fetch.
            freq (int, optional): Metrics update frequency in seconds.
            Defaults to 10.

        Returns:
            dict: Final data.
        """
        
        # Gather all game windows
        game_id = int(match_id) + 1
        params = dict()
        frames = requests.get(
            url=f"https://feed.lolesports.com/livestats/v1/window/{game_id}",
            headers=self.headers,
            params=params
        )
        if frames.status_code != 200:
            return None
        frame = frames.json()["frames"][-1]
        time = frame["rfc460Timestamp"]
        frame_list = [frame]
        while frame and frame["gameState"] == "in_game":
            splitted_time = time.split('.')
            full_date = splitted_time[0][:-1] if len(splitted_time) < 2 else splitted_time[0]
            date_time_obj = datetime.datetime.strptime(full_date, "%Y-%m-%dT%H:%M:%S")
            delta_seconds = datetime.timedelta(seconds=freq)
            final_time = (date_time_obj + delta_seconds).strftime("%Y-%m-%dT%H:%M:%S")
            final_time = final_time[:-1] + "0Z"  # Floor seconds + add Z idk why
            params["startingTime"] = final_time
            frames = requests.get(
                url=f"https://feed.lolesports.com/livestats/v1/window/{game_id}",
                headers=self.headers,
                params=params
            )
            if frames.status_code != 200:
                raise frames.raise_for_status()
            frame = frames.json()["frames"][-1]
            time = frame["rfc460Timestamp"]
            frame_list.append(frame)
        
        # Parse data from windows
        final_dict = dict()
        final_dict["timestamps"] = [f["rfc460Timestamp"] for f in frame_list]
        final_dict["blueTeam"] = self.get_team_stats("blueTeam", frame_list)
        final_dict["redTeam"] = self.get_team_stats("redTeam", frame_list)
        
        return final_dict
        


def get_usable_date():
    mydate = datetime.datetime.now()
    minute = datetime.timedelta(minutes=180)
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
    
    # print(api.get_match_details("105568157422015211"))

    print(api.get_match_evolution("105568157422015211"))
