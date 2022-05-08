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


@dataclass
class GameDetailsBan:
    banTurn: int = None
    championId: int = None
    

@dataclass
class GameDetailsItem:
    itemId: int = None
    slot: int = None
    

@dataclass
class GameDetailsPlayer:
    """
    Game detail participant
    """
    
    # FIXME: Link Player info ?
    participantId: int = None
    summonerName: str = None
    teamId: int = None
    
    # Basic stats
    kills: int = None
    deaths: int = None
    assists: int = None
    kda: float = None  # FIXME: Not sure about this one
    killParticipation: int = None  # FIXME: Not sure about this one
    cs: int = None  # totalMinionsKilled
    totalGold: int = None  # goldEarned
    goldPerMinute: float = None
    
    # Kills stats
    firstBloodAssist: bool = None
    firstBloodKill: bool = None
    killingSprees: int = None
    largestKillingSpree: int = None
    largestMultiKill: int = None
    doubleKills: int = None
    tripleKills: int = None
    quadraKills: int = None
    pentaKills: int = None
    soloKills: int = None
    killsNearEnemyTurret: int = None
    killsOnLanersEarlyJungleAsJungler: int = None
    killsOnOtherLanesEarlyJungleAsLaner: int = None
    
    # Neutral stats
    neutralMinionsKilled: int = None
    objectivesStolen: int = None
    alliedJungleMonsterKills: int = None
    enemyJungleMonsterKills: int = None
    
    # XP
    level: int = None  # champLevel
    
    # Champion
    championId: int = None  # FIXME Link to Champion object ?
    championName: str = None
    
    # Damage dealt
    #   Total
    totalDamageDealt: int = None
    magicDamageDealt: int = None
    physicalDamageDealt: int = None
    trueDamageDealt: int = None
    damagePerMinute: float = None
    teamDamagePercentage: float = None
    #   Champions
    totalDamageDealtToChampions: int = None
    magicDamageDealtToChampions: int = None
    physicalDamageDealtToChampions: int = None
    trueDamageDealtToChampions: int = None
    #   Objectives
    damageDealtToBuildings: int = None
    damageDealtToObjectives: int = None
    damageDealtToTurrets: int = None
    #   Random
    largestCriticalStrike: int = None
    totalDamageShieldedOnTeammates: int = None
    
    # Damage taken
    totalDamageTaken: int = None
    magicDamageTaken: int = None
    physicalDamageTaken: int= None
    trueDamageTaken: int = None
    damageTakenOnTeamPercentage: float = None
    
    # Damage mitigated
    damageSelfMitigated: int = None
    totalHeal: int = None
    totalHealsOnTeammates: int = None
    
    # Croud control
    timeCCingOthers: int = None
    totalTimeCCDealt: int = None
    
    # Vision
    detectorWardsPlaced: int = None  # Idk what this is
    visionScore: int = None
    visionWardsBoughtInGame: int = None
    wardsKilled: int = None
    wardsPlaced: int = None
    visionScorePerMinute: int = None
    wardTakedowns: int = None  # FIXME: Doublon ?
    controlWardsPlaced: int = None
    
    # Objective kills
    dragonKills: int = None  # Personal dragon skills
    baronTakedowns: int = None  # FIXME: Team stats may be enough
    dragonTakedowns: int = None  # FIXME: Team stats may be enough
    firstTowerAssist: bool = None
    firstTowerKill: bool = None
    turretKills: int = None  # Personal turrel kills
    turretTakedowns: int = None  # Total turret kills (maybe team stat is enough)
    turretsLost: int = None
    earliestBaron: float = None
    firstTurretKilledTime: float = None
    epicMonsterSteals: int = None
    kTurretsDestroyedBeforePlatesFall: int = None
    turretTakedowns: int = None  # FIXME: Team stats may be enough
    turretPlatesTaken: int = None
    
    # Spells casts
    spell1Casts: int = None
    spell2Casts: int = None
    spell3Casts: int = None
    spell4Casts: int = None
    summoner1Casts: int = None
    summoner2Casts: int = None
    
    # Random infos
    lane: str = None
    longestTimeSpentLiving: int = None
    buffsStolen: int = None
    outnumberedKills: int = None
    perfectDragonSoulsTaken: int = None
    perfectGame: int = None
    
    # Turbo random infos
    elderDragonKillsWithOpposingSoul: int = None
    epicMonsterKillsNearEnemyJungler: int = None
    epicMonsterKillsWithin30SecondsOfSpawn: int = None
    epicMonsterStolenWithoutSmite: int = None
    flawlessAces: int = None
    immobilizeAndKillWithAlly: int = None
    jungleCsBefore10Minutes: int = None
    junglerKillsEarlyJungle: int = None
    laneMinionsFirst10Minutes: int = None
    effectiveHealAndShielding: float = None
    enemyChampionImmobilizations: int = None
    
    # Others
    items: List[GameDetailsItem] = field(default_factory=list)
    # FIXME: Add perks


@dataclass
class GameDetailsTeam:
    teamId: int = None
    
    win: bool = None
    
    players: List[GameDetailsPlayer] = field(default_factory=list)
    bans: List[GameDetailsBan] = field(default_factory=list)
    
    firstBaron: bool = None
    baronKills: int = None
    
    firstBlood: bool = None
    kills: int = None
    
    firstDragon: bool = None
    dragonKills: int = None
    
    firstInhibitor: bool = None
    inhibitorKills: int = None
    
    firstRiftHerald: bool = None
    riftHeraldKills: int = None
    
    firstTower: bool = None
    towerKills: int = None


@dataclass
class GameDetails:
    """
    Game details
    """
    
    gameId: str = None
    patch: str = None
    duration: int = None
    startTimestamp: int = None
    endTimestamp: int = None
    teams: List[GameDetailsTeam] = None


@dataclass
class GameTimelineFrame:
    """
    Game timeline frame
    """