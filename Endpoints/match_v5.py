from RequestHandler import RequestHandler, UrlBuilder, ResponseChecker
from datetime import date, datetime

class MatchApi:
    def __init__(self, region, api_key):
        self.region = region
        self.api_key = api_key
        self.url_builder = UrlBuilder(region, use_platform=True)
        self.request_handler = RequestHandler(api_key, self.url_builder, ResponseChecker)

    def by_match_id(self, match_id):
        endpoint = f"/lol/match/v5/matches/{match_id}"
        return self.request_handler.make_request(endpoint)

    def by_match_id_timeline(self, match_id):
        endpoint = f"/lol/match/v5/matches/{match_id}/timeline"
        return self.request_handler.make_request(endpoint)
    
    def by_puuid_matchlist(
            self, 
            puuid, 
            startTime: datetime = None, 
            count: int = None, 
            gameType: str='ranked'):
        
        endpoint = f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = []
        
        if startTime is not None:
            startTime = datetime.fromisoformat(startTime).date()
            delta = date.today() - startTime
            # convert to seconds
            delta = int(delta.total_seconds())
            params.append(f"startTime={delta}")

        if count is not None:
            params.append(f"count={count}")

        if gameType is not None:
            params.append(f"type={gameType}")

        if params:
            endpoint += "?" + "&".join(params)

        return self.request_handler.make_request(endpoint)