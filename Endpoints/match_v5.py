from RequestHandler import RequestHandler, UrlBuilder
from datetime import date, datetime

# TODO

# Move the URLS from the API ex: lol/match/v5/matces...
# to an enum class ?
# En gros le bouger autrement c'est pas très propre là

class MatchApi:
    def __init__(self, region, api_key, debug):
        self.region = region
        self.api_key = api_key
        self.debug = debug
        self.url_builder = UrlBuilder(region, use_platform=True)
        self.endpoints = {
            'by_match_id': '/lol/match/v5/matches/{}',
            'by_match_id_timeline': '/lol/match/v5/matches/{}/timeline',
            'by_puuid_matchlist': '/lol/match/v5/matches/by-puuid/{}/ids'
        }
        self.request_handler = RequestHandler(api_key, self.url_builder, self.endpoints, debug)

    def by_match_id(self, match_id):
        return self.request_handler.make_request('by_match_id', match_id)

    def by_match_id_timeline(self, match_id):
        return self.request_handler.make_request('by_match_id_timeline', match_id)
    

    # TODO 
    # 
    # Change headers parameters like gameType, count etc to be processed w/o
    # using if statements
    def by_puuid_matchlist(
            self, 
            puuid: str,
            startTime: datetime = None,
            endTime: datetime = None,
            queue: int = None,          # https://static.developer.riotgames.com/docs/lol/queues.json
            type: str='ranked',          # ranked, normal, tourney, tutorial
            start: int = None,
            count: int = None,
        ):
        
        params = {}

        for key, value in locals().items():
            if value is not None:
                if key == 'startTime' or key == 'endTime':
                    params[key] = int(date.today() - datetime.fromisoformat(value).date()).total_seconds()
                else:
                    params[key] = value

        return self.request_handler.make_request('by_puuid_matchlist', puuid, query_params=params)
