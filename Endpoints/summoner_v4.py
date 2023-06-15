import sys
sys.path.append('/path/to/Endpoints')

#from Endpoint import Endpoint
from RequestHandler import RequestHandler, UrlBuilder, ResponseChecker

class SummonerApi:
    def __init__(self, region, api_key, debug):
        self.region = region
        self.api_key = api_key
        self.url_builder = UrlBuilder(region)
        self.request_handler = RequestHandler(api_key, self.url_builder, ResponseChecker, debug)

    def by_account(self, encrypted_account_id):
        endpoint = f"/lol/summoner/v4/summoners//by-account/{encrypted_account_id}"
        return self.request_handler.make_request(endpoint)

    def by_name(self, summoner_name):
        endpoint = f"/lol/summoner/v4/summoners/by-name/{summoner_name}"
        return self.request_handler.make_request(endpoint)
    
    def by_puuid(self, encrypted_puuid):
        endpoint = f"/lol/summoner/v4/summoners//by-puuid/{encrypted_puuid}"
        return self.request_handler.make_request(endpoint)

    def by_id(self, encrypted_summoner_id):
        endpoint = f"/lol/summoner/v4/summoners/{encrypted_summoner_id}"
        return self.request_handler.make_request(endpoint)

