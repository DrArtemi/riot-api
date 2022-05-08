from lolesport_parser.game import GameData
from lolesport_parser.player import PlayerData
from lolesport_parser.tournament import TournamentData
from mwrogue.esports_client import EsportsClient

from lolesport_parser.transmuters.leaguepedia_to_dto import transmute_lp_game_details


if __name__ == "__main__":
    # Get player by string
    player_data = PlayerData()
    player = player_data.search_player("Rekkles")[0]
    
    # Get player tournaments
    tournament_data = TournamentData()
    tournaments = tournament_data.get_tournament_for_player(player)
    tournament = [t for t in tournaments if "LFL 2022 Spring Playoffs" in t.name][0]

    # Get tournament games with player playing
    game_data = GameData()
    games = game_data.get_tournament_games_for_player(tournament, player)
    
    esport_client = EsportsClient("lol")
    res = esport_client.get_data_and_timeline_from_gameid(games[0].gameId)
    res = transmute_lp_game_details(res[0])
    breakpoint()
