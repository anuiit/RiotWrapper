from RiotWrapper import RiotWrapper
from datetime import datetime, date
import logging

#logging.basicConfig(level=logging.DEBUG)

# Create an API instance for the North America region
api_key = 'RGAPI-d502fbf0-f23e-4d41-a963-1b2638cbe04d'

euw1_api = RiotWrapper(api_key, 'euw1', debug=False)

# Get the summoner data for the given summoner name
puuid = euw1_api.summoner.by_name('randyboii')['puuid']

test1 = '2023-01-01'

test2 = date.fromisoformat(test1)



history = euw1_api.match.by_puuid_matchlist(puuid, count=100)
print(history)
test = euw1_api.match.by_match_id(history[0])


game_info = {
                'match_id': test['metadata']['matchId'],
                'game_creation': test,
                'game_mode': test['info']['gameMode'],
                'game_duration': test['info']['gameDuration'],
                #'game_outcome': 'win' if self.get_champion_win(test, puuid) else 'loss'
            }

wins = losses = 0

for game in history:
    game_info = euw1_api.match.by_match_id(game)
    participants = game_info['metadata']['participants']

    if puuid in participants:
        participant_win = test['info']['participants'][participants.index(puuid)]['win']
        participant_win = 'win' if participant_win else 'loss'

        if participant_win == 'win':
            wins += 1
        else:
            losses += 1

print(f'wins: {wins}, losses: {losses}')
print(f'winrate: {wins / (wins + losses)}')

