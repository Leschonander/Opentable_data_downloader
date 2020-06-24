import requests
import sys
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
import time
import json
import bs4 as bs
import pandas as pd
import argparse

url = "https://www.opentable.com/state-of-industry"
driver = webdriver.Chrome(ChromeDriverManager().install())
sys.setrecursionlimit(25000)
default_sleep_time = .5


def get_country():
    driver.get(url)
    
    soup = bs.BeautifulSoup(driver.page_source, 'html.parser')

    table = soup.find_all('table', class_='_1qd_QQULShhx1vCPgUJQJv')
    country_data =  pd.read_html(str(table))[0]

    country_data = country_data.set_index('Name').transpose()
    country_data['Date'] = country_data.index

    return country_data

def get_states():
    driver.get(url)
    
    select = Select(driver.find_element_by_xpath('//*[@id="content"]/div/div/main/section[2]/div[4]/div[1]/select'))

    select.select_by_value("states")

    soup = bs.BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find_all('table', class_='_1qd_QQULShhx1vCPgUJQJv')
    state_data =  pd.read_html(str(table))[0]


    state_data = state_data.set_index('Name').transpose()
    state_data['Date'] = state_data.index

    return state_data

def get_cities():
    driver.get(url)
    
    select = Select(driver.find_element_by_xpath('//*[@id="content"]/div/div/main/section[2]/div[4]/div[1]/select'))

    select.select_by_value("cities")

    soup = bs.BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find_all('table', class_='_1qd_QQULShhx1vCPgUJQJv')
    cities_data =  pd.read_html(str(table))[0]
    

    cities_data = cities_data.set_index('Name').transpose()
    cities_data['Date'] = cities_data.index

    return cities_data

def download_country_data():
    data = get_country()
    data.to_csv("Opentable_Country.csv", encoding='utf-8', index=False)

def download_state_data():
    data = get_states()
    data.to_csv("Opentable_States.csv", encoding='utf-8', index=False)

def download_city_data():
    data = get_cities()
    data.to_csv("Opentable_Cities.csv", encoding='utf-8', index=False)

def download_all():
    download_country_data()
    download_state_data()
    download_city_data()

functionMap = {
        'download_all': download_all,
        'download_country': download_country_data,
        'download_state': download_state_data,
        'download_city': download_city_data,
    }

parser = argparse.ArgumentParser(description = 'Download Opentable data')
parser.add_argument('command', choices = functionMap.keys(), help = 'Argument to download different opentable datasets')
args = parser.parse_args()
function = functionMap[args.command]
function()