import requests
import json
from datetime import date, timedelta

API_KEY = 'ENTER_API_KEY_HERE'
BASE_URL = 'https://api.pandascore.co/csgo/'

def getTodaysMatches():
    today = date.today().strftime('%Y-%m-%d')
    startDate = f'{today}T00:00:00Z'
    endDate = f'{today}T23:59:59Z'
    todaysMatches = []
    MATCHES_API_URL = f'{BASE_URL}/matches?range[begin_at]={startDate},{endDate}&per_page=100&sort=begin_at&token={API_KEY}'
    response = requests.get(MATCHES_API_URL)
    matchesJSON = response.json()
    return matchesJSON

def getTeamName(teamId):
    TEAMS_API_URL = f'{BASE_URL}/teams?filter[id]={teamId}&token={API_KEY}'
    response = requests.get(TEAMS_API_URL)
    response = response.json()
    return response[0]["name"]

def getPastThirtyMatchResults(teamIds):
    teamResultsDict = {}
    for teamId in teamIds:
        PAST_MATCHES_URL = f'{BASE_URL}/matches/past?filter[opponent_id]={teamId}&per_page=100&token={API_KEY}'
        matches = requests.get(PAST_MATCHES_URL)
        matchesJSON = matches.json()
        teamName = getTeamName(teamId)
        if len(matchesJSON) > 0:
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
            teamResultsDict[teamId] = teamWinsCount
            # print('------------------------------')
            # print(f'TEAM: {teamName}')
            # print(f'WINS: {teamWinsCount}')
            # print(f'LOSSES: {teamLossesCount}')
        else:
            teamResultsDict[teamId] = 0
            # print('------------------------------')
            # print(f'TEAM: {teamName}')
            # print(f'No match History')
    return teamResultsDict

def getTodaysTeamIds(matchesJSON):
    todaysTeamIds = []
    for i in range(len(matchesJSON)):
        todaysTeamIds.append(matchesJSON[i]["opponents"][0]["opponent"]["id"])
        todaysTeamIds.append(matchesJSON[i]["opponents"][1]["opponent"]["id"])
        i += 1
    return set(todaysTeamIds)

def getMatchWinnerPredicitions():
    matchesJSON = getTodaysMatches()
    todaysTeamIds = getTodaysTeamIds(matchesJSON)
    teamResults = getPastThirtyMatchResults(todaysTeamIds)
    for i in range(len(matchesJSON)):
        team1Id = matchesJSON[i]["opponents"][0]["opponent"]["id"]
        team1Name = matchesJSON[i]["opponents"][0]["opponent"]["name"]
        team1Wins = teamResults[team1Id]
        team2Id = matchesJSON[i]["opponents"][1]["opponent"]["id"]
        team2Name = matchesJSON[i]["opponents"][1]["opponent"]["name"]
        team2Wins = teamResults[team2Id]
        predictedWinner = findWinningTeam((team1Name, team1Wins), (team2Name, team2Wins))
        #predictedWinner = max(team1Wins, team2Wins)
        print('------------------------------')
        print(f'{team1Name}({team1Wins}) VS {team2Name}({team2Wins})')
        print(f'Predicted Winner: {predictedWinner}')

def findWinningTeam(team1Tuple, team2Tuple):
    if team1Tuple[1] > team2Tuple[1]:
        return team1Tuple[0]
    else:
        return team2Tuple[0]

def main():
    getMatchWinnerPredicitions()


if __name__ == '__main__':
    main()

#? How to pretty print JSON
#? response = json.dumps(response, indent=4, sort_keys=True)
#? with open('response.json', 'w+') as f:
#?     f.write(response)