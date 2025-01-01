from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

BASE_URL = 'https://sofifa.com/teams?type=all&lg%5B0%5D=13&r={year_key}&set=true'
YEAR_KEYS = {
    '25': '250013',
    '24': '240050',
    '23': '230054',
    '22': '220069',
    '21': '210064',
    '20': '200061'
}

def accept_cookies(driver_object):
    """
    locates and presses the accept cookies button
    """
    time.sleep(15) # wait for the site to fully load
    accept_cookies_button = driver_object.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
    accept_cookies_button.click()

def animate_scroll(driver_object):
    """
    scrolls the web page down. This is just for fun. Animations make my work lively.
    """
    # we are goint to send page down key strokes to the driver
    for i in range(3): # to repeat the key stroke three times
        time.sleep(1)
        driver_object.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN) # sends key stroke PageDown to the driver

def extract_team_names(driver_object):
    """
    extracts the team names from the page
    """
    team_names_elements = driver_object.find_elements(By.XPATH, '//td[@class="s20"]/a[1]')
    team_names = [team_name.text for team_name in team_names_elements]
    return team_names

def extract_overall(driver_object):
    """
    extracts the overall rating of the team
    """
    overall_elements = driver_object.find_elements(By.XPATH, '//td[@data-col="oa"]/em')
    overall_ratings = [overall.text for overall in overall_elements]
    return overall_ratings

def extract_attack(driver_object):
    """
    extracts the attack rating of the team
    """
    attack_elements = driver_object.find_elements(By.XPATH, '//td[@data-col="at"]/em')
    attack_ratings = [attack.text for attack in attack_elements]
    return attack_ratings

def extract_midfield(driver_object):
    """
    extracts the midfield rating of the team
    """
    midfield_elements = driver_object.find_elements(By.XPATH, '//td[@data-col="md"]/em')
    midfield_ratings = [midfield.text for midfield in midfield_elements]
    return midfield_ratings

def extract_defence(driver_object):
    """
    extracts the defence rating of the team
    """
    defence_elements = driver_object.find_elements(By.XPATH, '//td[@data-col="df"]/em')
    defence_ratings = [defence.text for defence in defence_elements]
    return defence_ratings

def extract_avg_age(driver_object):
    """
    extracts the average age of the team
    """
    avg_age_elements = driver_object.find_elements(By.XPATH, '//td[@data-col="sa"]/em')
    avg_ages = [avg_age.text for avg_age in avg_age_elements]
    return avg_ages

def extract_data(driver_object):
    """
    extracts the team data from the page
    """
    team_names = extract_team_names(driver_object)
    overall_ratings = extract_overall(driver_object)
    attack_ratings = extract_attack(driver_object)
    midfield_ratings = extract_midfield(driver_object)
    defence_ratings = extract_defence(driver_object)
    avg_ages = extract_avg_age(driver_object)
    # merge data by each team
    teams_data = pd.DataFrame({
        'team_name': team_names,
        'overall_rating': overall_ratings,
        'attack_rating': attack_ratings,
        'midfield_rating': midfield_ratings,
        'defence_rating': defence_ratings,
        'avg_age': avg_ages
    })
    return teams_data

for year in YEAR_KEYS:
    url = BASE_URL.format(year_key=YEAR_KEYS[year])
    print(url)
    options = Options()
    options.add_experimental_option('detach', True) # Keep the browser open
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    # animate_scroll(driver)
    data = extract_data(driver)
    df_data = pd.DataFrame(data)
    df_data.to_csv(f'../../data/raw/sofifa/teams_data_{year}.csv', index=False)