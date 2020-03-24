import requests
import json
from datetime import date, timedelta

API_KEY = 'ENTER_API_KEY_HERE'
BASE_URL = 'https://api.pandascore.co/csgo/'
TEAMS_API_URL = f'{BASE_URL}/teams?filter[id]=3209&token={API_KEY}'

def getData():
    today = date.today().strftime('%Y-%m-%d')
    startDate = f'{today}T00:00:00Z'
    endDate = f'{today}T23:59:59Z'
    MATCHES_API_URL = f'{BASE_URL}/matches?range[begin_at]={startDate},{endDate}&per_page=100&sort=begin_at&token={API_KEY}'
    response = requests.get(MATCHES_API_URL)
    #print(f'Pages Total: {response.headers["X-Total"]}')
    response = response.json()
    #print(f'Matches: {len(response)}')
    for i in range(len(response)):
        print(response[i]["name"])
        i += 1
    # response = json.dumps(response, indent=4, sort_keys=True)
    # with open('response.json', 'w+') as f:
    #     f.write(response)

def getTeams():
    response = requests.get(TEAMS_API_URL)
    # pages = response.headers['X-Total']
    # print(pages)
    response = response.json()
    print(response)
    # for i in range(len(response)):
    #     team = response[i]['name']
    #     print(team)
    #     i+=1

def getPastThirtyMatchResults(teamId):
    PAST_MATCHES_URL = f'{BASE_URL}/matches/past?filter[opponent_id]={teamId}&per_page=50&token={API_KEY}'
    matches = requests.get(PAST_MATCHES_URL)
    matchesJSON = matches.json()
    teamWinsCount = 0
    teamLossesCount = 0
    for matchNum in range(len(matchesJSON)):
        if matchesJSON[matchNum]["winner"] is not None and (teamWinsCount + teamLossesCount) < 30:
            matchWinnerId = matchesJSON[matchNum]["winner"]["id"]
            if matchWinnerId == teamId:
                teamWinsCount += 1
            else:
                teamLossesCount += 1
            matchNum += 1
    print(f'Wins: {teamWinsCount}')
    print(f'Losses: {teamLossesCount}')

def main():
    getPastThirtyMatchResults(3216)

if __name__ == '__main__':
    main()