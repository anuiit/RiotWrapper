import requests, requests_cache, time
from requests.exceptions import HTTPError
import logging
from urllib.parse import urlencode

logging.basicConfig(level=logging.INFO)

class UrlBuilder:
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

    def __init__(self, region, use_platform=False):
        self.region = region
        self.use_platform = use_platform
        self.platform = self.REGION_TO_PLATFORM[region]
        self.REGION_BASE_URL = f"https://{self.region}.api.riotgames.com"
        self.PLATFORM_BASE_URL = f"https://{self.platform}.api.riotgames.com"

    def build(self, endpoint, query_params=None):
        base_url = self.PLATFORM_BASE_URL if self.use_platform else self.REGION_BASE_URL
        url = base_url + endpoint

        if query_params:
            url += '?' + urlencode(query_params)
            print(url)
        return url


class CustomHTTPError(HTTPError):
    def __init__(self, response):
        super().__init__(f'Request to {response.url} failed with status code {response.status_code}. Details: {response.text}')


class ResponseChecker:
    @staticmethod
    def __log_response(response, result, retry_after, retries):
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response result: {result}")
        logging.info(f"Response retry_after: {retry_after}")
        logging.info(f"Response retries: {retries}")

    @staticmethod
    def check(response, max_retries=5, debug=False):
        handlers = {
            200: ResponseChecker.__handle_ok,
            429: ResponseChecker.__handle_429
        }

        retries = 0
        retry_after = 10

        for retries in range(max_retries):
            handler = handlers.get(response.status_code, ResponseChecker.__raise_http_error)
            result = handler(response, retry_after)

            if debug:
                ResponseChecker.__log_response(response, result, retry_after, retries)
            
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

    @staticmethod
    def __raise_http_error(response, retry_after):
        raise CustomHTTPError(response)
    

class RequestHandler:
    def __init__(self, api_key, url_builder, endpoints, debug, expire_after=3600):
        self.api_key = api_key
        self.url_builder = url_builder
        self.endpoints = endpoints
        self.debug = debug
        self.session = requests.Session()
        requests_cache.install_cache('riot_api_cache', expire_after=expire_after)
    
    def make_request(self, endpoint, query_params=None):
        url = self.url_builder.build(endpoint, query_params=query_params)
        headers = {'X-Riot-Token': self.api_key}

        while True:
            response = self.session.get(url, headers=headers)
            check_result = ResponseChecker.check(response, debug=self.debug)

            if check_result:
                return response.json()
            elif not check_result:
                if self.debug: print(f'\nRetrying after 429 error: {str(response.status_code)}, \nurl : {url}, \nheaders : {headers}, \nresponse : {response.json()}')
                continue
