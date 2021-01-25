import requests, json

base_url = 'https://api.the-odds-api.com/v3/odds/?apiKey='

apiKey = '3b2afadba2941e02e22e6a85341e05d3'
sport = 'soccer'
region = 'us'
mkt = 'h2h'
oddsFormat = 'decimal'

search_url = base_url + apiKey + '&sport=' + sport + '&region=' + region + '&mkt=' + mkt + '&oddsFormat=' + oddsFormat

data = requests.get(search_url).json()  #works

for match in data:
    # todo: print match, teams
    # ask user for preferred bookie out of possible options
    # ask for user's percentage predictions then provide recommendation on bet
    # if recommended, then store team name + its associated odds on array/list (watch out for draw case)

    # continue until no more matches left to screen, then output all recommendations based on user's predictions
    
    #final step: add a GUI via tkinter



def convertToOdds(predictedPercentage):
    predictedOdds = (1/impliedPercentage) * 100
    return predictedOdds


def predictionStrength (predictedPercentage, bookieOdds):
    totalStrength = 0

    predictedOdds = convertToOdds(predictedPercentage)

    improvement = bookieOdds / predictedOdds

    if improvement >= 2:
        totalStrength += 5
    elif improvement >= 1.7:
        totalStrength += 4.5
    elif improvement >= 1.5:
        totalStrength += 4
    elif improvement >= 1.3:
        totalStrength += 3.5
    elif improvement >= 1.15:
        totalStrength += 3
    elif improvement >= 1.05:
        totalStrength += 2.5
    elif improvement >= 1.001:
        totalStrength += 2
    else:
        totalStrength += 0

    oddsScore = ((predictedPercentage / ((1 + predictedPercentage)/2)) / (10*2))
    totalStrength += oddsScore

    return totalStrength

def recommendation(strengthScore):
    if strengthScore >= 8.5:
        print('Based on your predictions, this bet is very strong.')
    elif strengthScore >= 7:
        print('Based on your predictions, this bet is decent.')
    elif strengthScore >= 5.5:
        print('Based on your predictions, this bet is adequate.')
    else:
        print('Based on your predictions, this bet is weak.')

    


