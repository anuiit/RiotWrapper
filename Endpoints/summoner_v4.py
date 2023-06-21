from RequestHandler import RequestHandler, UrlBuilder

# TODO

# Faire une classe API ? 
# Pour la passer en child sur les endpoints de l'api
# ex SummonerApi devient SummonerApi(Api?)
# avec seulement(debug)?
# puisque la région serait choisie par la classe Api? directement
# et du coup il resterait rien ? en __init__? 
# Puisque region, key, url et requestHandler
# serait gérés par la classe Api directement 

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
        self.endpoints = {
            'by_account': '/lol/summoner/v4/summoners/by-account/{}',
            'by_name': '/lol/summoner/v4/summoners/by-name/{}',
            'by_puuid': '/lol/summoner/v4/summoners/by-puuid/{}',
            'by_id': '/lol/summoner/v4/summoners/{}'
        }
        self.request_handler = RequestHandler(api_key, self.url_builder, self.endpoints, debug)

    def by_account(self, encrypted_account_id):
        return self.request_handler.make_request('by_account', encrypted_account_id)

    def by_name(self, summoner_name):
        return self.request_handler.make_request('by_name', summoner_name)
    
    def by_puuid(self, encrypted_puuid):
        return self.request_handler.make_request('by_puuid', encrypted_puuid)

    def by_id(self, encrypted_summoner_id):
        return self.request_handler.make_request('by_id', encrypted_summoner_id)


