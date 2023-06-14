from RiotWrapper import RiotAPI

# Create an API instance for the North America region
na_api = RiotAPI('your-api-key', 'na1')
na_summoner = na_api.get_summoner_by_name('some-summoner-name')

# Create another API instance for the Europe region
eu_api = RiotAPI('your-api-key', 'euw1')
eu_summoner = eu_api.get_summoner_by_name('some-summoner-name')
