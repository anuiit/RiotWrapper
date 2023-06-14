from RiotWrapper import RiotWrapper
from datetime import datetime, date
import logging

#logging.basicConfig(level=logging.DEBUG)

# Create an API instance for the North America region
api_key = 'RGAPI-d502fbf0-f23e-4d41-a963-1b2638cbe04d'

euw1_api = RiotWrapper(api_key, 'euw1')

# Get the summoner data for the given summoner name
puuid = euw1_api.summoner.by_name('randyboii')['puuid']

test1 = '2023-01-01'

test2 = date.fromisoformat(test1)



history = euw1_api.match.by_puuid_matchlist(puuid, startTime='2023-01-01')
print(history)

print(puuid)

