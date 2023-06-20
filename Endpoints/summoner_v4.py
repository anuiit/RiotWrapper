from RequestHandler import RequestHandler, UrlBuilder, ResponseChecker

# TODO

# Faire une classe API ? 
# Pour la passer en child sur les endpoints de l'api
# ex SummonerApi devient SummonerApi(Api?)
# avec seulement(debug)?
# puisque la région serait choisie par la classe Api? directement
# et du coup il resterait rien ? en __init__? 
# Puisque region, key, url et requestHandler
# serait gérés par la classe Api directement 

class SummonerApi:
    def __init__(self, region, api_key, debug):
        self.region = region
        self.api_key = api_key
        self.url_builder = UrlBuilder(region)
        self.request_handler = RequestHandler(api_key, self.url_builder, ResponseChecker, debug)

    def by_account(self, encrypted_account_id):
        endpoint = f"/lol/summoner/v4/summoners/by-account/{encrypted_account_id}"
        return self.request_handler.make_request(endpoint)

    def by_name(self, summoner_name):
        endpoint = f"/lol/summoner/v4/summoners/by-name/{summoner_name}"
        return self.request_handler.make_request(endpoint)
    
    def by_puuid(self, encrypted_puuid):
        endpoint = f"/lol/summoner/v4/summoners/by-puuid/{encrypted_puuid}"
        return self.request_handler.make_request(endpoint)

    def by_id(self, encrypted_summoner_id):
        endpoint = f"/lol/summoner/v4/summoners/{encrypted_summoner_id}"
        return self.request_handler.make_request(endpoint)


