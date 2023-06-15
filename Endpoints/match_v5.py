from RequestHandler import RequestHandler, UrlBuilder, ResponseChecker
from datetime import date, datetime

class MatchApi:
    def __init__(self, region, api_key, debug):
        self.region = region
        self.api_key = api_key
        self.debug = debug
        self.url_builder = UrlBuilder(region, use_platform=True)
        self.request_handler = RequestHandler(api_key, self.url_builder, ResponseChecker, debug)

    def by_match_id(self, match_id):
        endpoint = f"/lol/match/v5/matches/{match_id}"
        return self.request_handler.make_request(endpoint)

    def by_match_id_timeline(self, match_id):
        endpoint = f"/lol/match/v5/matches/{match_id}/timeline"
        return self.request_handler.make_request(endpoint)
    
    def by_puuid_matchlist(
            self, 
            puuid, # oui bonjour voilà la def  
            startTime: datetime = None, 
            count: int = None, 
            gameType: str='ranked'):
        
        endpoint = f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {}
        
        if startTime is not None:
            delta = date.today() - datetime.fromisoformat(startTime).date()
            delta = int(delta.total_seconds())
            params['startTime'] = delta

        if count is not None:
            params['count'] = count

        if gameType is not None:
            params['type'] = gameType

        if params:
            query_params = '&'.join([f"{k}={v}" for k, v in params.items()])
            endpoint += f"?{query_params}"

        return self.request_handler.make_request(endpoint)