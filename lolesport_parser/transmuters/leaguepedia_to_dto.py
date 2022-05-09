from typing import Dict, List
from lolesport_parser.dataclasses.game import Game

from lolesport_parser.dataclasses.player import Player
from lolesport_parser.dataclasses.tournament import Tournament


def transmute_lp_players(players: List[Dict]) -> List[Player]:
    return [Player(
        summonerName=player.get("ID"),
        leaguepediaPage=player.get("OverviewPage"),
        lolProPage=player.get("Lolpros")
    ) for player in players]


def transmute_lp_tournaments(tournaments: List[Dict]) -> List[Tournament]:
    return [Tournament(
        name=tournament.get("Name"),
        level=tournament.get("TournamentLevel"),
        leaguepediaPage=tournament.get("OverviewPage")
    ) for tournament in tournaments]


def transmute_lp_games(games: List[Dict]) -> List[Game]:
    return [Game(
        gameId=game.get("GameId"),
        matchId=game.get("MatchId"),
        riotGameId=game.get("RiotPlatformGameId"),
        apiVersion=game.get("RiotVersion")
    ) for game in games]
