import requests
import json
from datetime import date, timedelta

API_KEY = 'ENTER_API_KEY_HERE'
TEAMS_API_URL = f'https://api.pandascore.co/csgo/teams?filter[id]=3209&token={API_KEY}'

def getData():
    today = date.today().strftime('%Y-%m-%d')
    startDate = f'{today}T00:00:00Z'
    endDate = f'{today}T23:59:59Z'
    MATCHES_API_URL = f'https://api.pandascore.co/csgo/matches?range[begin_at]={startDate},{endDate}&per_page=100&sort=begin_at&token={API_KEY}'
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

def main():
    getData()

if __name__ == '__main__':
    main()