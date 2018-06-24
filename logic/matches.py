from repository.models import *
import requests


OPEN_FOOTBALL_URL = 'https://raw.githubusercontent.com/openfootball/world-cup.json/master/2018/worldcup.json'
COUNTRIES_BASE_URL = 'https://restcountries.eu/rest/v2/'

COUNTRIES_SPECIAL_CODES = {'KSA': 'SAU', 'URU': 'URY', 'POR': 'PRT', 'DEN': 'DNK', 'CRO': 'HRV', 'SUI': 'CHE',
                           'CRC': 'CRI', 'GER': 'DEU', 'ENG': 'GBR'}

def load_teams():
    try:
        response = requests.get(OPEN_FOOTBALL_URL)
        response.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
        return False, "Couldn't get response"

    try:
        fixture_json = response.json()
    except ValueError:
        return False, "Couldn't decode response"

    try:
        for round_item in fixture_json['rounds']:
            for match in round_item['matches']:
                team1_code = match['team1']['code']
                team2_code = match['team2']['code']

                team1, error = load_team(team1_code)
                if error: return team1, error

                team2, error = load_team(team2_code)
                if error: return team2, error

    except KeyError as key_error:
        return False, "Couldn't get " + key_error + " member from json response"

    return True, None


def load_team(code):
    code_fifa = code
    if code in COUNTRIES_SPECIAL_CODES:
        code = COUNTRIES_SPECIAL_CODES[code]

    team = Team.query.filter_by(code3=code).first()
    
    if team:
        return team, None

    try:
        response = requests.get(COUNTRIES_BASE_URL + 'alpha/' + code)
        response.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
        return False, "Couldn't get response for country code " + code_fifa + " - " + code 

    try:
        country_json = response.json()
    except ValueError:
        return False, "Couldn't decode response"

    try:
        name = country_json['translations']['es']
        flag = country_json['flag']
        population = country_json['population']
    except KeyError as key_error:
        return False, "Couldn't get " + key_error + " member from json response"

    team = Team(code3=code, code_fifa=code_fifa, name=name, flag_picture=flag, population=population)
    db.session.add(team)
    return team, None
