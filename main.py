import requests
import json

API_KEY = 'ENTER_API_KEY_HERE'
API_URL = f'https://api.pandascore.co/csgo/matches?range[begin_at]=2020-03-22T00:00:00Z,2020-03-22T23:59:59&token={API_KEY}'

def getData():
    response = requests.get(API_URL)
    response = json.dumps(response.json(), indent=4, sort_keys=True)
    print(response)

def main():
    getData()

if __name__ == '__main__':
    main()