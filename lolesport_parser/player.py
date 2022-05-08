from typing import List
from leaguepedia_parser.site.leaguepedia import leaguepedia
from lolesport_parser.dataclasses.player import Player
from lolesport_parser.transmuters.leaguepedia_to_dto import transmute_lp_players


class PlayerData:
    
    def __init__(self) -> None:
        pass
    
    def search_player(self, search: str) -> List[Player]:
        """This method returns player ids matching search string.

        Args:
            search (str): player summoner name substring.
        """
        
        if not search:
            return []
        
        result = leaguepedia.query(
            tables="Players",
            fields="Players.ID, Players.OverviewPage, Players.Lolpros",
            where=f"Players.ID LIKE '%{search}%'",
        )
        return transmute_lp_players(result)
