import sys
sys.path.append('/path/to/Endpoints')

#from Endpoint import Endpoint
from RequestHandler import RequestHandler, UrlBuilder, ResponseChecker

'''
class SummonerEndpoint(Endpoint):
    def __init__(self, url, **kwargs):
        new_url = f"/summoner/v4/summoners{url}"
        super().__init__(new_url, **kwargs)


class SummonerApiUrls:
    by_account = SummonerEndpoint("/by-account/{encrypted_account_id}")
    by_name = SummonerEndpoint("/by-name/{summoner_name}")
    by_puuid = SummonerEndpoint("/by-puuid/{encrypted_puuid}")
    by_id = SummonerEndpoint("/{encrypted_summoner_id}")
'''
    

class SummonerApi:
    def __init__(self, region, api_key):
        self.region = region
        self.api_key = api_key
        self.url_builder = UrlBuilder(region)
        self.request_handler = RequestHandler(api_key, self.url_builder, ResponseChecker)

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

