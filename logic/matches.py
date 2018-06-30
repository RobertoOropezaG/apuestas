from repository.models import *
import requests


OPEN_FOOTBALL_URL = 'https://raw.githubusercontent.com/openfootball/world-cup.json/master/2018/worldcup.json'
COUNTRIES_BASE_URL = 'https://restcountries.eu/rest/v2/'
FIFA_BASE_URL = 'https://api.fifa.com/api/v1/calendar/matches?idseason=254645&idcompetition=17&language=es-ES'


COUNTRIES_SPECIAL_CODES = {'KSA': 'SAU', 'URU': 'URY', 'POR': 'PRT', 'DEN': 'DNK', 'CRO': 'HRV', 'SUI': 'CHE',
                           'CRC': 'CRI', 'GER': 'DEU', 'ENG': 'GBR'}


def get_json_response(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except (requests.exceptions.RequestException, requests.exceptions.HTTPError):
        return False, "Couldn't get response"

    try:
        response_json = response.json()
    except ValueError:
        return False, "Couldn't decode response as json"

    return response_json, None


def load_teams():
    fixture_json, error = get_json_response(OPEN_FOOTBALL_URL)
    
    if error:
        return False, error

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

    country_json, error = get_json_response(COUNTRIES_BASE_URL + 'alpha/' + code)

    if error:
        return False, error + ' for country code ' + code

    try:
        name = country_json['translations']['es']
        flag = country_json['flag']
        population = country_json['population']
    except KeyError as key_error:
        return False, "Couldn't get '" + key_error + "' field from json response when processing country code " + code

    team = Team(code3=code, code_fifa=code_fifa, name=name, flag_picture=flag, population=population)
    db.session.add(team)
    
    return team, None


def load_matches(date=None):
    matches_json, error = get_json_response(FIFA_BASE_URL)

    if error:
        return False, error + ' getting matches info'

    results = matches_json['Results']

    for result in results:
        team1 = {'code': result['Home']['IdCountry'], 'score': result['Home']['Score']}
        team2 = {'code': result['Away']['IdCountry'], 'score': result['Away']['Score']}
        date = result['Date'].replace('T', ' ').strip('Z')

        print (date, team1, 'vs', team2)
        
        match, error = load_match(date, team1, team2)
        if error: print(error); return None, error

    return True, None


def load_match(date,data1, data2):
    code1 = data1['code'] if data1['code'] not in COUNTRIES_SPECIAL_CODES else COUNTRIES_SPECIAL_CODES[data1['code']]
    code2 = data2['code'] if data2['code'] not in COUNTRIES_SPECIAL_CODES else COUNTRIES_SPECIAL_CODES[data2['code']]
    
    team1 = Team.query.filter_by(code3=code1).first()
    team2 = Team.query.filter_by(code3=code2).first()

    if not team1: return None, 'Couldn\'t load team ' + data1['code']
    if not team2: return None, 'Couldn\'t load team ' + data2['code']

    match = Match.query.filter_by(team1_id=team1.id, team2_id=team2.id, date=date).first()

    if match:
        print('match already existed')
        return match, None


    match = Match(team1=team1, team2=team2, date=date, timezone='UTC',
                    finished=True if data1['score'] is not None else False,
                    score1=data1['score'], score2=data2['score'])

    db.session.add(match)

    print('match created')
    return match, None