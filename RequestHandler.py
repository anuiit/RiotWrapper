import requests, requests_cache, time
from requests.exceptions import HTTPError
import logging
from urllib.parse import urlencode

logging.basicConfig(level=logging.INFO)

REGION_TO_PLATFORM = {
    'eun1': 'europe',
    'euw1': 'europe',
    'tr1': 'europe',
    'ru': 'europe',
    'jp1': 'asia',
    'kr': 'asia',
    'br1': 'americas',
    'la1': 'americas',
    'la2': 'americas',
    'na1': 'americas',
    'oc1': 'americas'
}

class CustomHTTPError(HTTPError):
    def __init__(self, response):
        super().__init__(f'Request to {response.url} failed with status code {response.status_code}. Details: {response.text}')


class ResponseChecker:
    @staticmethod
    def check(response, max_retries=5):
        handlers = {
            200: ResponseChecker.__handle_ok,
            429: ResponseChecker.__handle_429
        }

        retries = 0
        retry_after = 10

        for retries in range(max_retries):
            handler = handlers.get(response.status_code, CustomHTTPError(response))
            result = handler(response, retry_after)

            if result or not result:
                return result
            else:
                retries += 1
                retry_after *= 2
                ResponseChecker.__wait(retry_after)

        raise CustomHTTPError(response)

    @staticmethod
    def __handle_ok(response, retry_after):
        return True

    @staticmethod
    def __handle_429(response, retry_after):
        retry_after = int(response.headers.get('Retry-After', retry_after))
        ResponseChecker.__wait(retry_after)
        return False

    @staticmethod
    def __wait(retry_after):
        logging.info(f'Retrying in {retry_after} seconds...')
        time.sleep(retry_after + 1) # Just to be safe
        logging.info(f'Waited {retry_after} seconds.\n')
    

class RequestHandler:
    def __init__(self, api_key, region, use_platform, expire_after=3600):
        self.api_key = api_key
        self.region = region
        self.use_platform = use_platform
        self.session = requests.Session()
        self.set_cache(expire_after)
    
    def set_cache(self, expire_after, cache_name='riot_api_cache'):
        requests_cache.install_cache(cache_name, expire_after=expire_after)

    def build(self, region, endpoint, query_params=None):
        platform = REGION_TO_PLATFORM[region]

        if self.use_platform:
            base_url = f"https://{platform}.api.riotgames.com"
        else:
            base_url = f"https://{region}.api.riotgames.com"

        if query_params:
            url = base_url + endpoint + '?' + urlencode(query_params)
        else:
            url = base_url + endpoint

        return url

    def make_request(self, endpoint, query_params=None):
        url = self.build(self.region, endpoint, query_params=query_params)
        headers = {'X-Riot-Token': self.api_key}

        while True:
            response = self.session.get(url, headers=headers)
            check_result = ResponseChecker.check(response)

            if check_result:
                return response.json()
            elif not check_result:
                logging.DEBUG(f'\nRetrying after 429 error: {str(response.status_code)}, \nurl : {url}, \nheaders : {headers}, \nresponse : {response.json()}')
                continue
