import requests, time
from collections import deque
from requests.exceptions import HTTPError
import logging
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
            url += f"?{self.__build_query_params(query_params)}"
            print(url)
        return url

    def __build_query_params(self, params):
        query_params = []
        for key, value in params.items():
            query_params.append(f"{key}={value}")
        return '&'.join(query_params)


class ResponseChecker:
    @staticmethod
    def __log_response(response, result, backoff_time, retries):
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response result: {result}")
        logging.info(f"Response backoff_time: {backoff_time}")
        logging.info(f"Response retries: {retries}")

    @staticmethod
    def check(response, max_retries=5, debug=False):
        handlers = {
            429: ResponseChecker.__handle_429,
            400: ResponseChecker.__handle_error,
            401: ResponseChecker.__handle_error,
            403: ResponseChecker.__handle_error,
            404: ResponseChecker.__handle_error,
            500: ResponseChecker.__handle_error,
            503: ResponseChecker.__handle_error,
        }

        retries = 0
        backoff_time = 60

        while retries < max_retries:
            handler = handlers.get(response.status_code, ResponseChecker.__handle_ok)
            result = handler(response, backoff_time)

            if debug:
                ResponseChecker.__log_response(response, result, backoff_time, retries)
            
            if result is False:
                backoff_time *= 2
                retries += 1
                return False
            elif result is not None:
                backoff_time *= 2
                retries += 1
            else:
                return True

        raise HTTPError(f'Request failed with status {response.status_code} after {max_retries} retries')

    @staticmethod
    def __handle_ok(response, backoff_time):
        return None

    @staticmethod
    def __handle_429(response, backoff_time):
        retry_after = int(response.headers.get('Retry-After', backoff_time))
        ResponseChecker.__wait(retry_after)
        return False

    @staticmethod
    def __wait(seconds):
        for i in range(seconds, 0, -1):
            time.sleep(1)
            print(f"\rToo many requests, retrying in {i-1} seconds...", end='')

    @staticmethod
    def __handle_error(response, backoff_time):
        raise HTTPError(f'Request to {response.url} failed with status code {response.status_code}')


class RequestHandler:
    def __init__(self, api_key, url_builder, endpoints, debug):
        self.api_key = api_key
        self.url_builder = url_builder
        self.endpoints = endpoints
        self.debug = debug
        self.session = requests.Session()

    def make_request(self, endpoint, *args, query_params=None):
        endpoint = self.endpoints[endpoint].format(*args)
        url = self.url_builder.build(endpoint, query_params=query_params)
        headers = {'X-Riot-Token': self.api_key}

        while True:
            response = self.session.get(url, headers=headers)
            check_result = ResponseChecker.check(response, debug=self.debug)

            if check_result:
                return response.json()
            elif check_result is False:
                if self.debug: print(f'\nRetrying after 429 error: {str(response.status_code)}, \nurl : {url}, \nheaders : {headers}, \nresponse : {response.json()}')
                continue
            else:
                raise HTTPError(f"Request to {url} failed with status code {response.status_code}", url, response.status_code)
