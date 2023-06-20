from RiotWrapper import RiotWrapper
import logging
import time
import asyncio

#logging.basicConfig(level=logging.DEBUG)

api_key = 'RGAPI-28027390-02a3-4f8f-bfc7-5eb8a65ce2d8'

euw1_api = RiotWrapper(api_key, 'euw1', debug=False)

summoner =  euw1_api.summoner
match = euw1_api.match

puuid = summoner.by_name('randyboii')['puuid']

wins = 0
losses = 0

start_time = time.time()

history = match.by_puuid_matchlist(puuid, count=100)
print(history)

for game in history:
    game = match.by_match_id(game)

    
    position = game['metadata']['participants'].index(puuid)
    infos = game['info']['participants'][position]

    participant_win = infos['win']
    participant_champ = infos['championName']
    participant_win = 'win' if participant_win else 'loss'

    if participant_win == 'win':
        wins += 1
    else:
        losses += 1

    print(participant_win, participant_champ)

print(f'Winrate : {int(wins/(wins+losses)*100)}%')

end_time = time.time()
elapsed_time = end_time - start_time
print(f'Time elapsed: {elapsed_time} seconds')
