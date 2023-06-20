from RiotWrapper import RiotWrapper
import logging

#logging.basicConfig(level=logging.DEBUG)

api_key = 'RGAPI-557a5c66-be5f-4a92-80ac-5d509825c761'

euw1_api = RiotWrapper(api_key, 'euw1', debug=False)

summoner = euw1_api.summoner
match = euw1_api.match

puuid = summoner.by_name('randyboii')['puuid']


history = match.by_puuid_matchlist(puuid, count=10)
print(history)

for game in history:
    participants = match.by_match_id(game)['metadata']['participants']
    position = participants.index(puuid)

    participant_win = match.by_match_id(game)['info']['participants'][position]['win']
    participant_champ = match.by_match_id(game)['info']['participants'][participants.index(puuid)]['championName']
    participant_win = 'win' if participant_win else 'loss'

    print(participant_win, participant_champ)

