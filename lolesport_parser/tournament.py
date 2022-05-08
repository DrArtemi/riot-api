from typing import List
from leaguepedia_parser.site.leaguepedia import leaguepedia
from lolesport_parser.dataclasses.player import Player
from lolesport_parser.dataclasses.tournament import Tournament
from lolesport_parser.transmuters.leaguepedia_to_dto import transmute_lp_tournaments


class TournamentData:
    
    def __init__(self) -> None:
        pass
    
    def get_tournament_for_player(self, player: Player) -> List[Tournament]:
        """Get every tournaments player played in.

        Args:
            player (Player): Player to search for.

        Returns:
            _type_: _description_
        """
        
        if not player or not player.summonerName:
            return []
        result = leaguepedia.query(
            tables="TournamentPlayers, Tournaments",
            join_on="TournamentPlayers.OverviewPage = Tournaments.OverviewPage",
            fields="Tournaments.Name, Tournaments.OverviewPage, Tournaments.TournamentLevel",
            where=f"TournamentPlayers.Player='{player.summonerName}'",
        )
        return transmute_lp_tournaments(result)