from Endpoints.summoner_v4 import SummonerApi
from Endpoints.match_v5 import MatchApi

class RiotWrapper:
    def __init__(self, api_key, region):
        self.summoner = SummonerApi(region, api_key)
        self.match = MatchApi(region, api_key)

    # get winrate ?
    # general functions to get stats ?
    # get games played with count ?
    # stats by champion ?
    # stats by role ?
    # average stats ?
    # random games picked ?