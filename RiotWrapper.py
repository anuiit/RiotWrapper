from RequestHandler import RequestHandler
from Endpoints.summoner_v4 import SummonerApi
from Endpoints.match_v5 import MatchApi
from RequestHandler import UrlBuilder
from RequestHandler import ResponseChecker

class RiotWrapper:
    def __init__(self, api_key, region):
        self.api_key = api_key
        self.summoner = SummonerApi(region, api_key)
        self.match = MatchApi(region, api_key)
