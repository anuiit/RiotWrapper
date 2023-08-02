from ..RequestHandler import RequestHandler
from datetime import datetime

class MatchApi:
    ENDPOINTS = {
        'BY_MATCH_ID': '/lol/match/v5/matches/{}',
        'BY_MATCH_ID_TIMELINE': '/lol/match/v5/matches/{}/timeline',
        'BY_PUUID_MATCHLIST': '/lol/match/v5/matches/by-puuid/{}/ids'
    }

    def __init__(self, region, api_key):
        self.request_handler = RequestHandler(api_key, region, True)

    def by_match_id(self, match_id): # Example of match_id : EUW1_6333379226
        return self.request_handler.make_request(self.ENDPOINTS['BY_MATCH_ID'].format(match_id))

    def by_match_id_timeline(self, match_id):
        return self.request_handler.make_request(self.ENDPOINTS['BY_MATCH_ID_TIMELINE'].format(match_id)) 

    def by_puuid_matchlist(
        self, 
        puuid: str,
        startTime: datetime = None,
        endTime: datetime = None,   
        queue: int = None,          # https://static.developer.riotgames.com/docs/lol/queues.json
        typeGame: str = None,       # ranked, normal, tourney, tutorial
        start: int = 0,
        count: int = 20,
    ):

        query_params = {k: v for k, v in locals().items() if v is not None and k != 'self'}

        if startTime:
            startTime = int(datetime.now() - datetime.fromisoformat(startTime.total_seconds()))
        if endTime:
            endTime = int(datetime.now() - datetime.fromisoformat(endTime).total_seconds())

        return self.request_handler.make_request(self.ENDPOINTS['BY_PUUID_MATCHLIST'].format(puuid), query_params=query_params)