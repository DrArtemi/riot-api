import requests


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



if __name__ == '__main__':
    import pandas as pd
    
    api = RiotUnofficialApi(
        api_key="0TvQnueqKa5mxJntVWt0w4LpLfEkrV1Ta8rQBb9Z",
        lang="en-US"
    )
    
    print(api.get_teams())
