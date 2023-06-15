import requests

# A class for building URLs based on a given region
class UrlBuilder:
    # A dictionary mapping regions to platforms
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

    # Constructor
    def __init__(self, region, use_platform=False):
        self.region = region
        self.use_platform = use_platform
        self.platform = self.REGION_TO_PLATFORM[region]
        self.REGION_BASE_URL = f"https://{self.region}.api.riotgames.com"
        self.PLATFORM_BASE_URL = f"https://{self.platform}.api.riotgames.com"

    # Method for building a URL based on an endpoint
    def build(self, endpoint):
        base_url = self.PLATFORM_BASE_URL if self.use_platform else self.REGION_BASE_URL
        return base_url + endpoint

    
# A class for checking the response of a request
class ResponseChecker:
    # Static method for checking the response
    @staticmethod
    def check(response):
        if response.status_code != 200:
            raise Exception(f'Request to {response.url} failed with status code {response.status_code}')


# A class for handling requests
class RequestHandler:
    # Constructor
    def __init__(self, api_key, url_builder, response_checker, debug):
        self.api_key = api_key
        self.url_builder = url_builder
        self.response_checker = response_checker
        self.debug = debug

    # Method for making a request to a given endpoint
    def make_request(self, endpoint):
        url = self.url_builder.build(endpoint)
        headers = {'X-Riot-Token': self.api_key}
        response = requests.get(url, headers=headers)
        if self.debug:
            print(f"URL REQUEST : {url}{headers}")

        self.response_checker.check(response)
        return response.json()
