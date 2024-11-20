# To saving time, this file is run on Kaggle notebook
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import sys
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

def save_progress(year, team_name):
    with open('/kaggle/working/progress.txt', 'w') as f:
        f.write(f"{year},{team_name}")

def load_progress():
    try:
        with open('/kaggle/working/progress.txt', 'r') as f:
            progress = f.read().strip().split(',')
            return int(progress[0]), progress[1]  # Return last year, last team
    except FileNotFoundError:
        return None, None

def save_data(all_matches):
    df = pd.concat(all_matches)
    matches_path = '/kaggle/working/matches.csv'
    if not os.path.exists(matches_path):
        df.to_csv(matches_path, index=False)
    else:
        df.to_csv(matches_path, mode='a', header=False, index=False)

def save_continuous_progress(year, team_name):
    with open('/kaggle/working/progress.txt', 'a') as f:
        f.write(f"{year},{team_name}")

def get_links(data, cat):
    soup = BeautifulSoup(data.text, 'html.parser')
    links = soup.find_all('a')
    links = [l.get('href') for l in links]
    cat_links = [l for l in links if l and f'all_comps/{cat}/' in l]
    return cat_links

# rename second level columns
def rename_multiindex_col(df):
    columns = df.columns
    new_columns = pd.MultiIndex.from_tuples(
        [(cat, sub) if cat == columns[0][0]
         else (cat, cat + ' ' + sub) for cat, sub in columns]
    )
    df.columns = new_columns
    return df

# shooting
def process_shooting(data):
    shooting_links = get_links(data, 'shooting')
    shooting_data = requests.get(f"https://fbref.com{shooting_links[0]}")
    shooting = pd.read_html(shooting_data.text, match='Shooting')[0]
    shooting = rename_multiindex_col(shooting)
    shooting.columns = shooting.columns.droplevel(0)
    shooting.drop(columns=['Time', 'Comp', 'Round', 'Venue', 'Day', 'Opponent', 'Result', 'GF', 'GA', 'Standard SoT%', 'Standard G/Sh', 'Standard G/SoT',
                        'Expected npxG/Sh', 'Expected G-xG', 'Expected np:G-xG', 'Unnamed: 25_level_0 Match Report'], inplace=True)
    time.sleep(1)
    return shooting

# goalkeeping
def process_gk(data):
    gk_links = get_links(data, 'keeper')
    gk_data = requests.get(f"https://fbref.com{gk_links[0]}")
    gk = pd.read_html(gk_data.text, match='Goalkeeping')[0]
    gk.drop(columns=['Penalty Kicks'], inplace=True)
    columns = gk.columns
    columns = pd.MultiIndex.from_tuples(
        [(cat, 'lauched att' if (cat == 'Launched' and sub == 'Att') else
        'goal kick att' if (cat == 'Goal Kicks' and sub == 'Att') else
        'pass avglen' if (cat == 'Passes' and sub == 'AvgLen') else
                'goal kick avglen' if (cat == 'Goal Kicks' and sub == 'AvgLen') else sub)
        for cat, sub in columns]
    )
    gk.columns = columns
    gk.columns = gk.columns.droplevel(0)
    gk.drop(columns=['Comp', 'Time', 'Round', 'Day', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'Save%', 'PSxG+/-', 'Cmp%', 'Launch%', 'Stp%', 'Match Report'], inplace=True)
    gk.rename(columns={'Cmp' : 'launched cmp', 'Att (GK)' : 'passes att (gk)', 'Opp' : 'crosses faced', 'Stp' : 'crosses stp', 'AvgDist' : 'sweeper avgdist'}, inplace=True)
    time.sleep(1)
    return gk

# passing
def process_passing(data):
    passing_links = get_links(data, 'passing')
    passing_data = requests.get(f"https://fbref.com{passing_links[0]}")
    passing = pd.read_html(passing_data.text, match='Passing')[0]
    passing.drop(columns=['Short', 'Medium', 'Long'], inplace=True)
    passing.columns = passing.columns.droplevel(0)
    passing.drop(columns=['Time', 'Comp', 'Round', 'Day', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'Cmp%', 'Match Report'], inplace=True)
    passing.rename(columns={'Cmp' : 'passes cmp', 'Att' : 'passes att', 'TotDist' : 'total passing dist', 'PrgDist' : 'progressive passing dist'}, inplace=True)
    time.sleep(1)
    return passing

# pass types
def process_pass_types(data):
    pass_types_links = get_links(data, 'passing_types')
    pass_types_data = requests.get(f"https://fbref.com{pass_types_links[0]}")
    pass_types = pd.read_html(pass_types_data.text, match='Pass Types')[0]
    pass_types.columns = pass_types.columns.droplevel(0)
    pass_types.drop(columns=['Time', 'Comp', 'Round', 'Day', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'Att', 'Match Report',
                            'Cmp'], inplace=True)
    pass_types.rename(columns={'In' : 'inswing conrner kicks', 'Out' : 'outswing corner kicks', 'Str' : 'straight corner kicks', 'Off' : 'passes offside',
                                    'Blocks' : 'passes blocked'}, inplace=True)
    time.sleep(1)
    return pass_types

# Goal and Shot Creation
def process_gs(data):
    gs_links = get_links(data, 'gca')
    gs_data = requests.get(f"https://fbref.com{gs_links[0]}")
    gs = pd.read_html(gs_data.text, match='Goal and Shot Creation')[0]
    gs = rename_multiindex_col(gs)
    gs.columns = gs.columns.droplevel(0)
    gs.drop(columns=['Time', 'Comp', 'Round', 'Day', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'SCA Types SCA', 
                     'GCA Types GCA', 'Unnamed: 24_level_0 Match Report'], inplace=True)
    time.sleep(1)
    return gs

# defensive actions
def process_def_actions(data):
    def_actions_links = get_links(data, 'defense')
    def_actions_data = requests.get(f"https://fbref.com{def_actions_links[0]}")
    def_actions = pd.read_html(def_actions_data.text, match='Defensive Actions')[0]
    def_actions = rename_multiindex_col(def_actions)
    def_actions.columns = def_actions.columns.droplevel(0)
    def_actions.drop(columns=['Time', 'Comp', 'Round', 'Day', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'Unnamed: 26_level_0 Match Report'], inplace=True)
    def_actions.rename(columns={'Unnamed: 22_level_0 Int' : 'Int', 'Unnamed: 23_level_0 Tkl+Int' : 'Tkl + Int', 'Unnamed: 24_level_0 Clr' : 'Clr',
                                'Unnamed: 25_level_0 Err' : 'Err'}, inplace=True)
    time.sleep(1)
    return def_actions

# Possession
def process_possession(data):
    possession_links = get_links(data, 'possession')
    possession_data = requests.get(f"https://fbref.com{possession_links[0]}")
    possession = pd.read_html(possession_data.text, match='Possession')[0]
    possession = rename_multiindex_col(possession)
    possession.columns = possession.columns.droplevel(0)
    possession.drop(columns=['Time', 'Comp', 'Round', 'Day', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'Unnamed: 33_level_0 Match Report', 'Take-Ons Succ%',
                                    'Take-Ons Tkld%'], inplace=True)
    time.sleep(1)
    return possession

# Miscellaneous Stats
def process_misc_stats(data):
    misc_stats_links = get_links(data, 'misc')
    misc_data = requests.get(f"https://fbref.com{misc_stats_links[0]}")
    misc_stats = pd.read_html(misc_data.text, match='Miscellaneous Stats')[0]
    misc_stats = rename_multiindex_col(misc_stats)
    misc_stats.columns = misc_stats.columns.droplevel(0)
    misc_stats.drop(columns=['Time', 'Comp', 'Round', 'Day', 'Venue', 'Result', 'GF', 'GA', 'Opponent', 'Aerial Duels Won%', 
                             'Unnamed: 26_level_0 Match Report'], inplace=True)
    time.sleep(1)
    return misc_stats

def crawl_data(max_retries = 20):
    years = list(range(2024, 2016, -1))
    # all_matches = [] 
    # standing_url = "https://fbref.com/en/comps/9/Premier-League-Stats"

    # Load progress nếu có
    last_year, last_team = load_progress()

    for year in years:
        if last_year and year > last_year: 
            continue
        try:
            last_year_url = f"https://fbref.com/en/comps/9/{year}-{year+1}/{year}-{year+1}-Premier-League-Stats"
            data = requests.get(last_year_url)
            data.raise_for_status()  # Check for rate limit
        except requests.exceptions.HTTPError as e:
            print(f"Request failed: {e}")
            max_retries -= 1
            if max_retries == 0:
                print("Max retries exceeded")
                sys.exit()
            time.sleep(300)
            
            

        soup = BeautifulSoup(data.text, 'html.parser')
        standings_table = soup.select('table.stats_table')[0]
        links = standings_table.find_all('a')
        links = [l.get('href') for l in links]
        team_links = [l for l in links if '/squads/' in l]
        team_links = [f"https://fbref.com{l}" for l in team_links]
        
        previous_season = soup.select('a.prev')[0].get('href')
        standing_url = f"https://fbref.com{previous_season}"

        for team_link in team_links:
            team_name = team_link.split('/')[-1].replace('-Stats', '').replace('-', ' ')
            
            if last_team and team_name != last_team:
                continue
            last_team = None

            save_progress(year, team_name)  
            save_continuous_progress(year, team_name)

            try:
                data = requests.get(team_link)
                # data.raise_for_status()

                matches = pd.read_html(data.text, match='Scores & Fixtures')[0]
                shooting = process_shooting(data)
                gk = process_gk(data)
                passing = process_passing(data)
                pass_types = process_pass_types(data)
                gs = process_gs(data)
                def_actions = process_def_actions(data)
                possession = process_possession(data)
                misc_stats = process_misc_stats(data)

                team_data = matches.merge(shooting, on='Date')
                team_data = team_data.merge(gk, on='Date')
                team_data = team_data.merge(passing, on='Date')
                team_data = team_data.merge(pass_types, on='Date')
                team_data = team_data.merge(gs, on='Date')
                team_data = team_data.merge(def_actions, on='Date')
                team_data = team_data.merge(possession, on='Date')
                team_data = team_data.merge(misc_stats, on='Date')

                # Lọc ra các trận chỉ thuộc Premier League
                team_data = team_data[team_data['Comp'] == 'Premier League']
                team_data['Season'] = str(year) + '-' + str(year + 1)
                team_data['Team'] = team_name
                # all_matches.append(team_data)
                print(f"Data for {team_name} in {year} season has been scraped.")
                
                # Lưu dữ liệu vào CSV sau khi lấy xong dữ liệu của một đội
                save_data([team_data])
            
            except ValueError:
                continue
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    print("rate limit exceeded")
                    max_retries -= 1
                    if max_retries == 0:
                        print("Max retries exceeded")
                        sys.exit()
                    time.sleep(300)
                else:
                    print(f"Request failed: {e}")
                    sys.exit()

            time.sleep(60) 

if __name__ == "__main__":
    crawl_data()