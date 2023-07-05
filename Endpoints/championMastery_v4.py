from RequestHandler import RequestHandler
from datetime import datetime

class ChampionMasteryApi:
    ENDPOINTS = {
        'BY_SUMMONER': '/lol/champion-mastery/v4/champion-masteries/by-summoner/{}',
        'BY_SUMMONER_CHAMPION': '/lol/champion-mastery/v4/champion-masteries/by-summoner/{}/by-champion/{}',
        'BY_SUMMONER_TOP_CHAMPIONS': '/lol/champion-mastery/v4/champion-masteries/by-summoner/{}/top',
        'BY_SUMMONER_TOTAL_SCORE': '/lol/champion-mastery/v4/scores/by-summoner/{}'
    }

    def __init__(self, region, api_key):
        self.request_handler = RequestHandler(api_key, region, False)

    def champion_rotation(self, summoner_id):
        return self.request_handler.make_request(self.ENDPOINTS['BY_SUMMONER'].format(summoner_id))
    
    def champ_mastery(self, summoner_id, champion_id):
        return self.request_handler.make_request(self.ENDPOINTS['BY_SUMMONER_CHAMPION'].format(summoner_id, champion_id))
    
    def top_champs(self, summoner_id, count=5):
        query_params = {k: v for k, v in locals().items() if v is not None and k != 'self'}

        return self.request_handler.make_request(self.ENDPOINTS['BY_SUMMONER_TOP_CHAMPIONS'].format(summoner_id), query_params=query_params)
    
    def total_score(self, summoner_id):
        return self.request_handler.make_request(self.ENDPOINTS['BY_SUMMONER_TOTAL_SCORE'].format(summoner_id))
