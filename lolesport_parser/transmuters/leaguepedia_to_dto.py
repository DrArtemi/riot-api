from typing import Dict, List
from lolesport_parser.dataclasses.game import Game, GameDetails, GameDetailsBan, GameDetailsItem, GameDetailsPlayer, GameDetailsTeam

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
        riotGameId=game.get("RiotPlatformGameId")
    ) for game in games]

def transmute_lp_game_details(game_details: Dict) -> GameDetails:
    
    # Retrieve players
    players = list()
    for player in game_details.get("participants", list()):
        items = list()
        for i in range(7):
            items.append(GameDetailsItem(
                itemId=player.get(f"item{i}"),
                slot=i
            ))
        challenges = player.get("challenges")
        players.append(GameDetailsPlayer(
            participantId=player.get("participantId"),
            summonerName=player.get("summonerName"),
            teamId=player.get("teamId"),
            kills=player.get("kills"),
            deaths=player.get("deaths"),
            assists=player.get("assists"),
            cs=player.get("totalMinionsKilled"),  # totalMinionsKilled
            totalGold=player.get("goldEarned"),  # goldEarned
            goldPerMinute=challenges.get("goldPerMinute"),
            firstBloodAssist=player.get("firstBloodAssist"),
            firstBloodKill=player.get("firstBloodKill"),
            killingSprees=player.get("killingSprees"),
            largestKillingSpree=player.get("largestKillingSpree"),
            largestMultiKill=player.get("largestMultiKill"),
            doubleKills=player.get("doubleKills"),
            tripleKills=player.get("tripleKills"),
            quadraKills=player.get("quadraKills"),
            pentaKills=player.get("pentaKills"),
            soloKills=challenges.get("soloKills"),
            killsNearEnemyTurret=challenges.get("killsNearEnemyTurret"),
            killsOnLanersEarlyJungleAsJungler=challenges.get("killsOnLanersEarlyJungleAsJungler"),
            killsOnOtherLanesEarlyJungleAsLaner=challenges.get("killsOnOtherLanesEarlyJungleAsLaner"),
            neutralMinionsKilled=player.get("neutralMinionsKilled"),
            objectivesStolen=challenges.get("objectivesStolen"),
            alliedJungleMonsterKills=challenges.get("alliedJungleMonsterKills"),
            enemyJungleMonsterKills=challenges.get("enemyJungleMonsterKills"),
            level=player.get("champLevel"),  # champLevel
            championId=player.get("championId"),
            championName=player.get("championName"),            
            totalDamageDealt=player.get("totalDamageDealt"),
            magicDamageDealt=player.get("magicDamageDealt"),
            physicalDamageDealt=player.get("physicalDamageDealt"),
            trueDamageDealt=player.get("trueDamageDealt"),
            damagePerMinute=challenges.get("damagePerMinute"),
            teamDamagePercentage=challenges.get("teamDamagePercentage"),
            totalDamageDealtToChampions=player.get("totalDamageDealtToChampions"),
            magicDamageDealtToChampions=player.get("magicDamageDealtToChampions"),
            physicalDamageDealtToChampions=player.get("physicalDamageDealtToChampions"),
            trueDamageDealtToChampions=player.get("trueDamageDealtToChampions"),
            damageDealtToBuildings=player.get("damageDealtToBuildings"),
            damageDealtToObjectives=player.get("damageDealtToObjectives"),
            damageDealtToTurrets=player.get("damageDealtToTurrets"),
            largestCriticalStrike=player.get("largestCriticalStrike"),
            totalDamageShieldedOnTeammates=player.get("totalDamageShieldedOnTeammates"),
            totalDamageTaken=player.get("totalDamageTaken"),
            magicDamageTaken=player.get("magicDamageTaken"),
            physicalDamageTaken=player.get("physicalDamageTaken"),
            trueDamageTaken=player.get("trueDamageTaken"),
            damageTakenOnTeamPercentage=challenges.get("damageTakenOnTeamPercentage"),
            damageSelfMitigated=player.get("damageSelfMitigated"),
            totalHeal=player.get("totalHeal"),
            totalHealsOnTeammates=player.get("totalHealsOnTeammates"),
            timeCCingOthers=player.get("timeCCingOthers"),
            totalTimeCCDealt=player.get("totalTimeCCDealt"),
            visionScore=player.get("visionScore"),
            visionWardsBoughtInGame=player.get("visionWardsBoughtInGame"),
            wardsKilled=player.get("wardsKilled"),
            wardsPlaced=player.get("wardsPlaced"),
            visionScorePerMinute=challenges.get("visionScorePerMinute"),
            wardTakedowns=challenges.get("wardTakedowns"),  # FIXME: Doublon ?
            controlWardsPlaced=challenges.get("controlWardsPlaced"),
            dragonKills=player.get("dragonKills"),  # Personal dragon skills
            firstTowerAssist=player.get("firstTowerAssist"),
            firstTowerKill=player.get("firstTowerKill"),
            turretKills=player.get("turretKills"),  # Personal turrel kills
            turretTakedowns=player.get("turretTakedowns"),  # Total turret kills (maybe team stat is enough)
            turretsLost=player.get("turretsLost"),
            earliestBaron=challenges.get("earliestBaron"),
            firstTurretKilledTime=challenges.get("firstTurretKilledTime"),
            epicMonsterSteals=challenges.get("epicMonsterSteals"),
            kTurretsDestroyedBeforePlatesFall=challenges.get("kTurretsDestroyedBeforePlatesFall"),
            turretPlatesTaken=challenges.get("turretPlatesTaken"),
            spell1Casts=player.get("spell1Casts"),
            spell2Casts=player.get("spell2Casts"),
            spell3Casts=player.get("spell3Casts"),
            spell4Casts=player.get("spell4Casts"),
            summoner1Casts=player.get("summoner1Casts"),
            summoner2Casts=player.get("summoner2Casts"),
            lane=player.get("lane"),
            longestTimeSpentLiving=challenges.get("longestTimeSpentLiving"),
            buffsStolen=challenges.get("buffsStolen"),
            outnumberedKills=challenges.get("outnumberedKills"),
            perfectDragonSoulsTaken=challenges.get("perfectDragonSoulsTaken"),
            perfectGame=challenges.get("perfectGame"),
            elderDragonKillsWithOpposingSoul=challenges.get("elderDragonKillsWithOpposingSoul"),
            epicMonsterKillsNearEnemyJungler=challenges.get("epicMonsterKillsNearEnemyJungler"),
            epicMonsterKillsWithin30SecondsOfSpawn=challenges.get("epicMonsterKillsWithin30SecondsOfSpawn"),
            epicMonsterStolenWithoutSmite=challenges.get("epicMonsterStolenWithoutSmite"),
            flawlessAces=challenges.get("flawlessAces"),
            immobilizeAndKillWithAlly=challenges.get("immobilizeAndKillWithAlly"),
            jungleCsBefore10Minutes=challenges.get("jungleCsBefore10Minutes"),
            junglerKillsEarlyJungle=challenges.get("junglerKillsEarlyJungle"),
            laneMinionsFirst10Minutes=challenges.get("laneMinionsFirst10Minutes"),
            effectiveHealAndShielding=challenges.get("effectiveHealAndShielding"),
            enemyChampionImmobilizations=challenges.get("enemyChampionImmobilizations"),
            items=items
        ))
    
    # Retrieve team information
    teams = list()
    for team in game_details.get("teams", list()):
        # Retrieve bans
        bans = list()
        for ban in team.get("bans", list()):
            bans.append(GameDetailsBan(
                banTurn=ban.get("pickTurn"),
                championId=ban.get("championId")
            ))
        objectives = team.get("objectives", dict())
        baron = objectives.get("baron", dict())
        teamKills = objectives.get("champion", dict())
        dragon = objectives.get("baron", dict())
        inhibitors = objectives.get("inhibitors", dict())
        riftHerald = objectives.get("riftHerald", dict())
        tower = objectives.get("tower", dict())
        teams.append(GameDetailsTeam(
            teamId=team.get("teamId"),
            win=team.get("win"),
            players=[p for p in players if p.teamId == team.get("teamId")],
            bans=bans,
            firstBaron=baron.get("first"),
            baronKills=baron.get("kills"),
            firstBlood=teamKills.get("first"),
            kills=teamKills.get("kills"),
            firstDragon=dragon.get("first"),
            dragonKills=dragon.get("kills"),
            firstInhibitor=inhibitors.get("first"),
            inhibitorKills=inhibitors.get("kills"),
            firstRiftHerald=riftHerald.get("first"),
            riftHeraldKills=riftHerald.get("kills"),
            firstTower=tower.get("first"),
            towerKills=tower.get("kills"),
        ))
    
    return GameDetails(
        gameId=game_details.get("GameId"),
        patch=game_details.get("gameVersion"),
        duration=game_details.get("gameDuration"),
        startTimestamp=game_details.get("gameStartTimestamp"),
        endTimestamp=game_details.get("gameEndTimestamp"),
        teams=teams
    )