from typing import List
from leaguepedia_parser.site.leaguepedia import leaguepedia
from lolesport_parser.dataclasses.game import Game
from lolesport_parser.dataclasses.player import Player
from lolesport_parser.dataclasses.tournament import Tournament
from lolesport_parser.transmuters.leaguepedia_to_dto import transmute_lp_games


class GameData:
    
    def __init__(self) -> None:
        pass
    
    def get_tournament_games_for_player(self, tournament: Tournament, player: Player) -> List[Game]:
        """Get tournament games in wich player played.

        Args:
            tournament (Tournament): Tournament to search for
            player (Player): Player to search for

        Returns:
            _type_: _description_
        """
        if (not tournament or not tournament.name or
            not player or not player.summonerName):
            return []
        result = leaguepedia.query(
            tables="Tournaments, ScoreboardGames, ScoreboardPlayers",
            join_on="ScoreboardPlayers.GameId = ScoreboardGames.GameId, ScoreboardPlayers.OverviewPage = Tournaments.OverviewPage", #, ScoreboardGames.OverviewPage = ",
            fields="ScoreboardGames.GameId, ScoreboardGames.MatchId, ScoreboardGames.RiotPlatformGameId",
            where=f"ScoreboardPlayers.Link = '{player.summonerName}' AND Tournaments.name = '{tournament.name}'", # AND 
        )
        return transmute_lp_games(result)