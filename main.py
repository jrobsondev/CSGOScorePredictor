import requests
import json
from datetime import date, timedelta
from team import Team

API_KEY = 'ENTER_API_KEY_HERE'
BASE_URL = 'https://api.pandascore.co/csgo/'

def getTodaysMatches():
    today = date.today().strftime('%Y-%m-%d')
    startDate = f'{today}T00:00:00Z'
    endDate = f'{today}T23:59:59Z'
    todaysMatches = []
    MATCHES_API_URL = f'{BASE_URL}/matches?range[begin_at]={startDate},{endDate}&per_page=3&sort=begin_at&token={API_KEY}' #!!! CHANGE PER PAGE BACK TO 100
    response = requests.get(MATCHES_API_URL)
    matchesJSON = response.json()
    return matchesJSON

def getTeamName(teamId):
    TEAMS_API_URL = f'{BASE_URL}/teams?filter[id]={teamId}&token={API_KEY}'
    response = requests.get(TEAMS_API_URL)
    response = response.json()
    return response[0]["name"]

def getPastMatchResults(teamIds):
    teamResultsDict = {}
    for teamId in teamIds:
        PAST_MATCHES_URL = f'{BASE_URL}/matches/past?filter[opponent_id]={teamId}&per_page=100&token={API_KEY}'
        matches = requests.get(PAST_MATCHES_URL)
        matchesJSON = matches.json()
        teamName = getTeamName(teamId)
        if len(matchesJSON) > 0:
            teamWinsCount = 0
            teamLossesCount = 0
            teamKdDiff = 0
            for matchNum in range(len(matchesJSON)):
                areDetailedStatsAvailable = matchesJSON[matchNum]["detailed_stats"]
                if matchesJSON[matchNum]["winner"] is not None and (teamWinsCount + teamLossesCount) < 3: #!!! CHANGE BACK TO 10
                    matchId = matchesJSON[matchNum]["id"]
                    matchWinnerId = matchesJSON[matchNum]["winner"]["id"]
                    if matchWinnerId == teamId:
                        teamWinsCount += 1
                    else:
                        teamLossesCount += 1
                    if areDetailedStatsAvailable:
                        teamKdDiff += getTeamKdDiff(matchId, teamId)
                    matchNum += 1
            teamResultsDict[teamId] = [teamWinsCount, teamKdDiff]
        else:
            teamResultsDict[teamId] = [0, 0]
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
    teamResults = getPastMatchResults(todaysTeamIds)
    for i in range(len(matchesJSON)):
        team1 = Team()
        team1.id = matchesJSON[i]["opponents"][0]["opponent"]["id"]
        team1.name = matchesJSON[i]["opponents"][0]["opponent"]["name"]
        team1.wins = teamResults[team1.id][0]
        team1.kdDiff = teamResults[team1.id][1]
        team2 = Team()
        team2.id = matchesJSON[i]["opponents"][1]["opponent"]["id"]
        team2.name = matchesJSON[i]["opponents"][1]["opponent"]["name"]
        team2.wins = teamResults[team2.id][0]
        team2.kdDiff = teamResults[team2.id][1]
        predictedWinner = findWinningTeam((team1.name, team1.wins), (team2.name, team2.wins))
        #predictedWinner = max(team1Wins, team2Wins)
        print('------------------------------')
        print(f'{team1.name}({team1.wins}) VS {team2.name}({team2.wins})')
        print(f'Team 1 KDDiff: {team1.kdDiff} || Team 2 KDDiff: {team2.kdDiff}')
        print(f'Predicted Winner: {predictedWinner}')

def findWinningTeam(team1Tuple, team2Tuple):
    if team1Tuple[1] > team2Tuple[1]:
        return team1Tuple[0]
    else:
        return team2Tuple[0]

def getTeamKdDiff(matchId, teamId):
    MATCH_STATS_URL = f'https://api.pandascore.co/csgo/matches/{matchId}/players/stats?token={API_KEY}'
    playersKdDiff = []
    matchStats = requests.get(MATCH_STATS_URL)
    matchStatsJSON = matchStats.json()
    teams = matchStatsJSON["teams"]
    for teamNum in range(len(teams)):
        teamStatsId = teams[teamNum]["id"]
        if teamStatsId == teamId:
            players = teams[teamNum]["players"]
            playerNum = 0
            for playerNum in range(len(players)):
                playerKDDiff = players[playerNum]["stats"]["counts"]["k_d_diff"]
                playersKdDiff.append(playerKDDiff)
                playerNum +=1
            break
        else:
            continue
    playersKdDiffSum = sum(playersKdDiff)
    return playersKdDiffSum

def main():
    getMatchWinnerPredicitions()


if __name__ == '__main__':
    main()

#? How to pretty print JSON
#? response = json.dumps(response, indent=4, sort_keys=True)
#? with open('response.json', 'w+') as f:
#?     f.write(response)