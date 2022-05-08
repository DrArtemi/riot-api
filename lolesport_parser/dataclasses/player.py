from dataclasses import dataclass, field

@dataclass
class Player:
    """
    Player dataclass
    """
    
    summonerName:       str = None
    leaguepediaPage:    str = None
    lolProPage:         str = None
