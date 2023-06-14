import os
import json
import requests
from enum import Enum
from typing import List, Optional
from configparser import ConfigParser
import logging
from datetime import datetime, timezone, date
import pandas as pd

#logging.basicConfig(level=logging.DEBUG)

class LolDataScraper:
    
    def __init__(self, apikey: str, region: Optional[Region] = None) -> None:
        self.apikey = apikey

        if not region:
            self.region = self._get_region_from_user()
        else:
            self.region = region

        self.platform = self._get_platform_from_region(self.region)

        self.region_url = f"https://{self.region.value}.api.riotgames.com"
        self.best_platform_url = f"https://{self._get_best_platform()}.api.riotgames.com"
        self.platform_url = f"https://{self.platform.value}.api.riotgames.com"

    def get_puuid(self, player_name: str) -> str:
        endpoint = f"/lol/summoner/v4/summoners/by-name/{player_name}"
        url = f"{self.region_url}{endpoint}?api_key={self.apikey}"

        response = requests.get(url)
        response.raise_for_status()

        puuid = response.json()["puuid"]

        return puuid

    def get_games_history(self, player_name: str, start_time: date = None, count: str = '20') -> List[dict[str, any]]:

        puuid = self.get_puuid(player_name)

        endpoint = f"/lol/match/v5/matches/by-puuid/{puuid}/ids"
        game_count = f"count={count}"

        if start_time:
            delta = date.today() - start_time
            # convert to seconds
            delta = delta.total_seconds()
            print(delta)

        url = f"{self.platform_url}{endpoint}?{start_time}&start=0&{game_count}&api_key={self.apikey}"
        response = requests.get(url)
        response.raise_for_status()

        games_history = []

        for match_id in response.json():
            endpoint = f"/lol/match/v5/matches/{match_id}"
            url = f"{self.platform_url}{endpoint}?api_key={self.apikey}"
            response = requests.get(url)
            response.raise_for_status()

            game_data = response.json()
            game_creation = datetime.utcfromtimestamp((game_data['info']['gameCreation']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            game_info = {
                'match_id': game_data['metadata']['matchId'],
                'game_creation': game_creation,
                'game_mode': game_data['info']['gameMode'],
                'game_duration': game_data['info']['gameDuration'],
                'game_outcome': 'win' if self.get_champion_win(match_id, puuid) else 'loss'
            }

            games_history.append(game_info)

        return games_history

    def get_champion_win(self, match_id: str, puuid: str) -> dict[str, any]:
        url = f"{self.platform_url}/lol/match/v5/matches/{match_id}?api_key={self.apikey}"

        response = requests.get(url)
        response.raise_for_status()

        participants = response.json()['info']['participants']

        for participant in participants:
            if participant['puuid'] == puuid:
                return participant['win']





    def _get_user_choice(self, choices: List[str], prompt: str) -> str:
        while True:
            print(prompt)
            for idx, choice in enumerate(choices):
                print(f"{idx+1}. {choice}")

            try:
                choice_idx = int(input("> ")) - 1
                if choice_idx < 0 or choice_idx >= len(choices):
                    raise ValueError()
                return choices[choice_idx]
            
            except ValueError:
                print("Invalid choice, please try again")

    def get_summoner_id(self, player_name: str) -> str:
        endpoint = f"/lol/summoner/v4/summoners/by-name/{player_name}"
        url = f"{self.region_url}{endpoint}?api_key={self.apikey}"

        response = requests.get(url)
        response.raise_for_status()

        summoner_id = response.json()["id"]

        return summoner_id

    def get_rank_and_lp(self, player_name: str, queue: str = 'RANKED_SOLO_5x5') -> Optional[tuple[str, int]]:
        endpoint = f"/lol/league/v4/entries/by-summoner/{self.get_summoner_id(player_name)}"
        url = f"{self.region_url}{endpoint}?api_key={self.apikey}"

        response = requests.get(url)
        response.raise_for_status()

        for entry in response.json():
            if entry['queueType'] == queue:
                rank = entry['tier'] + ' ' + entry['rank']
                lp = entry['leaguePoints']
                return (rank, lp)

        return None
    
    def get_masteries(self, player_name: str) -> List[tuple[str, int]]:
        endpoint = f"/lol/champion-mastery/v4/champion-masteries/by-summoner/{self.get_summoner_id(player_name)}"
        url = f"{self.region_url}{endpoint}?api_key={self.apikey}"

        response = requests.get(url)
        response.raise_for_status()

        masteries = []

        for mastery in response.json():
            masteries.append((mastery['championId'], mastery['championPoints']))

        return masteries

def main():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config.json")

    with open(config_path) as f:
        config = json.load(f)

    API_KEY = config['api_key']

    scraper = LolDataScraper(API_KEY)

    print(f"PUUID : {str(scraper.get_puuid('randyboii'))}\n\n")
    print(f"HISTORIQUE : {str(scraper.get_games_history('randyboii', start_time=(date(2023, 1, 1))))}\n\n")
    print(f"RANK & LP : {str(scraper.get_rank_and_lp('randyboii'))}\n\n")

if __name__ == "__main__":
    main()