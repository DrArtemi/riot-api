from dataclasses import dataclass, field
from typing import List

@dataclass
class Game:
    """
    Game dataclass
    """
    
    gameId:     str = None
    matchId:    str = None
    riotGameId: str = None
    apiVersion: str = None
