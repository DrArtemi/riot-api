from dataclasses import dataclass, field

@dataclass
class Tournament:
    """
    Player dataclass
    """
    
    name:               str = None
    level:              str = None
    leaguepediaPage:    str = None
