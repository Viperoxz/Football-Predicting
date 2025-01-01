import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

BASE_URL = "https://www.worldfootball.net/{feature}/eng-premier-league-{season}/"
SEASONS = ['2019-2020', '2020-2021', '2021-2022', '2022-2023', '2023-2024', '2024-2025']

def getRound(match_soup):
    round_text = match_soup.find('div', class_='breadcrumb').find('h1').get_text()
    round_info = round_text.split('»')[1].split('.')[0].strip()
    return round_info

def getCoaches(coach_table):
    coaches = [b.get_text() for b in coach_table.find_all('b')]
    home_coach = coaches[0].split(':')[1].strip()
    away_coach = coaches[1].split(':')[1].strip()
    return home_coach, away_coach

def getLineup(team_table):
    players = [a.get_text() for a in team_table.find_all('a')]
    return players

def getTeamName(info_table):
    team_names = [a.get_text() for a in info_table.find_all('a') if 'teams' in a['href']]
    h_name, a_name = team_names[0], team_names[1]
    return h_name, a_name

def writeProgress(url):
    with open('progress.txt', 'a') as f:
        f.write(url + '\n')

def crawl():
    match_data = []
    player_data = []
    
    for season in SEASONS:
        season_url = BASE_URL.format(season=season, feature='all_matches')
        print(f"Crawling season: {season} - URL: {season_url}")
        
        response = requests.get(season_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'class': 'standard_tabelle'})
        
        match_links = [a['href'] for a in table.find_all('a') if 'report' in a['href'] and '(' in a.get_text()]
        match_urls = [BASE_URL.format(season=season, feature='report') + url for url in match_links]
        
        for match_url in match_urls:
            print(f"Crawling match: {match_url}")
            writeProgress(match_url)
            
            match_response = requests.get(match_url)
            match_soup = BeautifulSoup(match_response.text, 'html.parser')
            
            match_round = getRound(match_soup)
            match_tables = match_soup.find_all('table', {'class': 'standard_tabelle'})

            if len(match_tables) == 6:
                info_table, home_table, away_table, coach_table = match_tables[0], match_tables[2], match_tables[3], match_tables[4]
            else:
                info_table, home_table, away_table, coach_table = match_tables[0], match_tables[3], match_tables[4], match_tables[5]

            # Get coach
            home_coach, away_coach = getCoaches(coach_table)

            # Get lineup
            home_lineup = getLineup(home_table)
            away_lineup = getLineup(away_table)
            
            # Get team name
            home_team, away_team = getTeamName(info_table)
            print(home_team, away_team)
            match_id = f"{season}_{len(match_data) + 1}"
            match_data.append({
                "Match ID": match_id,
                "Season": season,
                "Round": match_round,
                "Home Team": home_team,
                "Away Team": away_team,
                "Home Coach": home_coach,
                "Away Coach": away_coach,
            })
            for player in home_lineup:
                player_data.append({
                    "Match ID": match_id,
                    "Team": home_team,
                    "Player Name": player,
                    "Is Home": 1
                })
            for player in away_lineup:
                player_data.append({
                    "Match ID": match_id,
                    "Team": away_team,
                    "Player Name": player,
                    "Is Home": 0
                })
            time.sleep(1)
            print(player_data)
            print(match_data)
            break
    #     print(f"Finished crawling season: {season}")

    matches_df = pd.DataFrame(match_data)
    players_df = pd.DataFrame(player_data)
    matches_df.to_csv('../data/raw/worldfb/worldfb_matches.csv', index=False)
    players_df.to_csv('../data/raw/worldfb/worldfb_players.csv', index=False)
    print("Data saved successfully.")

crawl()