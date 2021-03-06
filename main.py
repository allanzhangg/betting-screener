
import requests, json, string

base_url = 'https://api.the-odds-api.com/v3/odds/?apiKey='

apiKey = ''  # obtain your own free (albeit limited) API key at https://the-odds-api.com/#get-access
sport = 'soccer'
region = 'us'
mkt = 'h2h'
oddsFormat = 'decimal'

search_url = base_url + apiKey + '&sport=' + sport + '&region=' + region + '&mkt=' + mkt + '&oddsFormat=' + oddsFormat

search_response = requests.get(search_url).json() 

match_list = search_response['data']

matchLeagues = [match['sport_nice'] for match in match_list]
matches = [match['teams'] for match in match_list]
matchBookies = [match['sites'] for match in match_list]

matchOptions = []
matchOdds = []

recommendedTeams = []
recommendedOdds = []
recommendedResults = []

for match in matchBookies:
    bookieOptions = [bookie['site_nice'] for bookie in match]
    bookieOdds = [bookie['odds'] for bookie in match]
    matchOptions.append(bookieOptions)
    matchOdds.append(bookieOdds)

def listBookies (bookieOptions):
    currentBookie = 0
    currentOptions = ""
    while currentBookie < len(bookieOptions):
        if currentBookie != (len(bookieOptions) - 1):
            currentOptions += bookieOptions[currentBookie] + ", "
        else:
            currentOptions += bookieOptions[currentBookie]
        currentBookie += 1
    return currentOptions


def findBookie(bookieInput, bookieOptions):
    currentBookie = 0
    while currentBookie < len(bookieOptions):
        lowerInput = bookieInput.lower()
        lowerComparison = bookieOptions[currentBookie].lower()
        if lowerInput == lowerComparison:
            return currentBookie
        else:
            currentBookie += 1
    return -1  # invalid input condition, expand

        


def convertToOdds(predictedPercentage):
    predictedPercentage = int(predictedPercentage)
    if predictedPercentage == 0:
        predictedPercentage = 0.1
    predictedOdds = (1/predictedPercentage) * 100
    return predictedOdds


def predictionStrength (predictedPercentage, bookieOdds):
    totalStrength = 0.0

    predictedPercentage = float(predictedPercentage)
    predictedOdds = convertToOdds(predictedPercentage)

    bookieOdds = float(bookieOdds)
    improvement = bookieOdds / predictedOdds

    if improvement >= 2:
        totalStrength += 5.0
    elif improvement >= 1.7:
        totalStrength += 4.5
    elif improvement >= 1.5:
        totalStrength += 4.0
    elif improvement >= 1.3:
        totalStrength += 3.5
    elif improvement >= 1.15:
        totalStrength += 3.0
    elif improvement >= 1.05:
        totalStrength += 2.5
    elif improvement >= 1.001:
        totalStrength += 2.0
    else:
        totalStrength += 0.0

    oddsScore = ((predictedPercentage / ((100 + predictedPercentage)/2)) / (10*2)) * 100
    totalStrength += float(oddsScore)

    return totalStrength

def recommend(teams, odds, result):
    recommendedTeams.append(teams)
    recommendedOdds.append(odds)
    recommendedResults.append(result)


def evaluation(strengthScore):
    betLevel = ""
    if strengthScore >= 9.0:
        betLevel = 'very strong'
    elif strengthScore >= 8.0:
        betLevel = 'strong'
    elif strengthScore >= 7.0:
        betLevel = 'decent'
    elif strengthScore >= 5.5:
        betLevel = 'adequate'
    else:
        betLevel = 'weak'
    return betLevel

    
currentMatch = 0

while currentMatch < len(matches):
    print('League: ' + matchLeagues[currentMatch])
    print('Match: ' + matches[currentMatch][0] + ' vs ' + matches[currentMatch][1])

    print("")
    
    currentBookies = listBookies(matchOptions[currentMatch])
    preferredBookie = input("Which company do you prefer? The options are: " + currentBookies + "\n")
    bookieNumber = findBookie(preferredBookie, matchOptions[currentMatch])

    allOdds = matchOdds[currentMatch][bookieNumber]['h2h']
    homeOdds = allOdds[0]
    drawOdds = allOdds[1]
    awayOdds = allOdds[2]
    
    homePrediction = input("What is your predicted percentage of a " + matches[currentMatch][0] + " win?\n")
    homeStrength = predictionStrength(homePrediction, homeOdds)
    if homeStrength >= 8.0:
        recommend(matches[currentMatch], homeOdds, "h")
    homeStrength = round(homeStrength, 2)

    drawPrediction = input("What is your predicted percentage of a draw?\n")
    drawStrength = predictionStrength(drawPrediction, drawOdds)
    if drawStrength >= 8.0:
        recommend(matches[currentMatch], drawOdds, "d")
    drawStrength = round(drawStrength, 2)

    awayPrediction = input("What is your predicted percentage of a " + matches[currentMatch][1] + " win?\n")
    awayStrength = predictionStrength(awayPrediction, awayOdds)
    if awayStrength >= 8.0:
        recommend(matches[currentMatch], awayOdds, "a")
    awayStrength = round(awayStrength, 2)

    print("")
    
    print("Results based on your predictions:")
    print("Betting on a " + matches[currentMatch][0] + " (home) victory @ " + str(allOdds[0]) + " is " + str(evaluation(homeStrength)) + ". (Rating: " + str(homeStrength) + ")")
    print("Betting on a draw @ " + str(allOdds[1]) + " is " + str(evaluation(drawStrength)) + ". (Rating: " + str(drawStrength) + ")")
    print("Betting on a " + matches[currentMatch][1] + " (away) victory @ " + str(allOdds[2]) + " is " + str(evaluation(awayStrength)) + ". (Rating: " + str(awayStrength) + ")")

    currentMatch += 1
    print("")


if len(recommendedResults) > 0:
    print("Based on your predictions, these bets are recommended:")
    currentRecommendation = 0
    while currentRecommendation < len(recommendedResults):
        if recommendedResults[currentRecommendation] == 'h':
            print(recommendedTeams[currentRecommendation][0] + " defeats " + recommendedTeams[currentRecommendation][1] + " @ " + str(recommendedOdds[currentRecommendation]))
        elif recommendedResults[currentRecommendation] == 'a':
            print(recommendedTeams[currentRecommendation][1] + " defeats " + recommendedTeams[currentRecommendation][0] + " @ " + str(recommendedOdds[currentRecommendation]))
        else:
            print(recommendedTeams[currentRecommendation][0] + " draws " + recommendedTeams[currentRecommendation][1] + " @ " + str(recommendedOdds[currentRecommendation]))
        currentRecommendation += 1
else:
    print("Based on your predictions, no bets were recommendable.")







