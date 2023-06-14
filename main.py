from RiotWrapper import RiotWrapper

import logging

logging.basicConfig(level=logging.DEBUG)

# Create an API instance for the North America region
api_key = 'RGAPI-d502fbf0-f23e-4d41-a963-1b2638cbe04d'

euw1_api = RiotWrapper(api_key, 'euw1')

# Get the summoner data for the given summoner name
euw1_summoner = euw1_api.summoner.by_name('randyboii')

print(euw1_summoner)

