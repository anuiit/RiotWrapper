import requests, time

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
            url += f"?{self.build_query_params(query_params)}"
        return url

    def build_query_params(self, params):
        query_params = []
        for key, value in params.items():
            query_params.append(f"{key}={value}")
        return '&'.join(query_params)


class RequestException(Exception):
    def __init__(self, message, url=None, status_code=None):
        super().__init__(message)
        self.url = url
        self.status_code = status_code

# TODO
# Implement a better rate limiter using the X-App-Rate-Limit-Count header

class ResponseChecker:
    @staticmethod
    def check(response, max_retries=5):
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
            print(f"Response status code : {response.status_code}")
            print(f"Response result : {result}")
            print(f"Response backoff_time : {backoff_time}")
            print(f"Response retries : {retries}")

            if result is not None:
                backoff_time *= 2
                retries += 1
            else:
                return True

        raise RequestException(f'Request failed after {max_retries} retries')

    @staticmethod
    def __handle_ok(response, backoff_time):
        return None

    @staticmethod
    def __handle_429(response, backoff_time):
        retry_after = int(response.headers.get('Retry-After', 60))
        for i in range(retry_after, 0, -1):
            time.sleep(1)
            print(f"\rToo many requests, retrying in {i-1} seconds...", end="")
        print()
        return False


    @staticmethod
    def __handle_error(response, backoff_time):
        raise RequestException(f'Request to {response.url} failed with status code {response.status_code}')


class RequestHandler:
    def __init__(self, api_key, url_builder, endpoints, debug):
        self.api_key = api_key
        self.url_builder = url_builder
        self.endpoints = endpoints
        self.response_checker = ResponseChecker
        self.debug = debug
        self.session = requests.Session()

    def make_request(self, endpoint, *args, query_params=None):
        endpoint = self.endpoints[endpoint].format(*args)
        url = self.url_builder.build(endpoint, query_params=query_params)

        headers = {'X-Riot-Token': self.api_key}
        response = self.session.get(url, headers=headers)

        if self.debug: print(f"URL REQUEST : {url}{headers}")
        
        if self.response_checker.check(response):
            return response.json()
        else:
            return self.make_request(endpoint, *args, query_params=query_params)