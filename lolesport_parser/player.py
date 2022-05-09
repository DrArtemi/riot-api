import difflib
import pandas as pd
from typing import List
from leaguepedia_parser.site.leaguepedia import leaguepedia
from pandas import DataFrame, json_normalize
from mwrogue.esports_client import EsportsClient
from pydantic import ValidationError
from lolesport_parser.dataclasses.game import Game
from lolesport_parser.dataclasses.game_details_v5 import GameDetails as GameDetailsV5
from lolesport_parser.dataclasses.game_details_v4 import GameDetails as GameDetailsV4
from lolesport_parser.dataclasses.tournament import Tournament
from lolesport_parser.transmuters.leaguepedia_to_dto import transmute_lp_games, transmute_lp_players, transmute_lp_tournaments


class PlayerData:
    
    def __init__(self, player_name: str, esports_client: EsportsClient = None) -> None:
        self._esports_client = esports_client
        
        # Parse player from player name
        players_query = leaguepedia.query(
            tables="Players",
            fields="Players.ID, Players.OverviewPage, Players.Lolpros",
            where=f"Players.ID LIKE '%{player_name}%'",
        )
        if not players_query:
            raise KeyError(f"No player found for {player_name} query.")
        potential_players = transmute_lp_players(players_query)
        potential_players_names = [p.summonerName for p in potential_players]
        closest_players_names = difflib.get_close_matches(player_name, potential_players_names, n=1)
        if len(closest_players_names) == 0:
            raise KeyError(f"{player_name} has no close match in {potential_players_names}")
        self.player = [p for p in potential_players if p.summonerName == closest_players_names[0]][0]
    
    @property
    def esports_client(self):
        return self._esports_client
    
    @esports_client.setter
    def esports_client(self, value):
        self._esports_client = value
        
    def tournaments(self, allow_failure=False):
        tournaments_query = leaguepedia.query(
            tables="TournamentPlayers, Tournaments",
            join_on="TournamentPlayers.OverviewPage = Tournaments.OverviewPage",
            fields="Tournaments.Name, Tournaments.OverviewPage, Tournaments.TournamentLevel",
            where=f"TournamentPlayers.Player='{self.player.summonerName}'",
        )
        if not tournaments_query:
            if allow_failure:
                return list()
            else:
                raise KeyError(f"No tournament found for player \"{self.player.summonerName}\".")
        return transmute_lp_tournaments(tournaments_query)

    def tournament_games(self, tournament: Tournament, allow_failure=False):
        if (not tournament or not tournament.name):
            return []
        games_query = leaguepedia.query(
            tables="Tournaments, ScoreboardGames, ScoreboardPlayers",
            join_on="ScoreboardPlayers.GameId = ScoreboardGames.GameId, ScoreboardPlayers.OverviewPage = Tournaments.OverviewPage", #, ScoreboardGames.OverviewPage = ",
            fields="ScoreboardGames.GameId, ScoreboardGames.MatchId, ScoreboardGames.RiotPlatformGameId, ScoreboardGames.RiotVersion",
            where=f"ScoreboardPlayers.Link = '{self.player.summonerName}' AND Tournaments.name = '{tournament.name}'", # AND 
        )
        if not games_query:
            if allow_failure:
                return list()
            else:
                raise KeyError(f"No game found for player \"{self.player.summonerName}\" in tournament \"{tournament.name}\".")
        return transmute_lp_games(games_query)

    def stats_from_games(self, games: List[Game]) -> DataFrame:
        if not self.esports_client:
            raise ValueError("PlayerData esports_client attribute needs to be set. (ex: player_data.esports_client = EsportsClient(\"lol\")")
        dataframes = list()
        for game in games:
            res = self.esports_client.get_data_and_timeline_from_gameid(game.gameId)
            
            # FIXME: I SMELL BULLSHIT HERE, I SHOULD MAKE A CUSTOM PYDANTIC MODEL TO MERGE v4 and v5
            
            # FIXME: This is turbo SUS, some JSONs marked as Riot API v5 seem to be v4 (didn't find any evidence of V4 in fields)
            try:
                gd = GameDetailsV5(**res[0])
                gd_summoner_name = difflib.get_close_matches(self.player.summonerName.upper(), [p.summonerName.upper() for p in gd.participants], n=1)[0]
                player_details = [p for p in gd.participants if p.summonerName.upper() == gd_summoner_name][0]
            except:
                gd = GameDetailsV4(**res[0])
                gd_summoner_name = difflib.get_close_matches(self.player.summonerName.upper(), [p.player.summonerName.upper() for p in gd.participantIdentities], n=1)[0]
                gd_participant_id = [p.participantId for p in gd.participantIdentities if p.player.summonerName.upper() == gd_summoner_name][0]
                player_details = [p for p in gd.participants if p.participantId == gd_participant_id][0]
            
            # FIXME: Exclude perks.styles for the moment
            dataframes.append(json_normalize(data=player_details.dict(exclude={"perks.styles"})))
        return pd.concat(dataframes, axis=0)
