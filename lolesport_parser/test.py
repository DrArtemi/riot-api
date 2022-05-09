import pandas as pd
from mwrogue.esports_client import EsportsClient
from lolesport_parser.game import GameData
from lolesport_parser.player import PlayerData
from lolesport_parser.tournament import TournamentData

import difflib

if __name__ == "__main__":
    # Get player by string
    player_data = PlayerData(player_name="Saken", esports_client=EsportsClient("lol"))
    tournaments = player_data.tournaments()
    games = player_data.tournament_games(tournament=tournaments[33])
    player_stats = player_data.stats_from_games(games)
