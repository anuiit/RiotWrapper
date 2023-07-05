from Endpoints.summoner_v4 import SummonerApi
from Endpoints.match_v5 import MatchApi
from Endpoints.champion_v3 import ChampionApi
from Endpoints.championMastery_v4 import ChampionMasteryApi
from Endpoints.league_v4 import LeagueApi
from Endpoints.spectator_v4 import SpectatorApi
from Endpoints.leagueExp_v4 import LeagueExpApi
from Endpoints.lolStatus_v4 import LolStatusApi

class RiotWrapper:
    def __init__(self, api_key, region):
        # TODO: add api class
        # self.api = Api(region, api_key)
        # self.summoner = SummonerApi()

        self.summoner = SummonerApi(region, api_key)
        self.match = MatchApi(region, api_key)
        self.champion = ChampionApi(region, api_key)
        self.mastery = ChampionMasteryApi(region, api_key)
        self.league = LeagueApi(region, api_key)
        self.spectator = SpectatorApi(region, api_key)
        self.league_exp = LeagueExpApi(region, api_key)
        self.lol_status = LolStatusApi(region, api_key)
        
    # get winrate ?
    # general functions to get stats ?
    # get games played with count ?
    # stats by champion ?
    # stats by role ?
    # average stats ?
    # random games picked ?
    # change champion id to champion name ?