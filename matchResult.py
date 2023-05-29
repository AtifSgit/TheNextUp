import requests, base64
from bs4 import BeautifulSoup
# from .views import addMatchResult

from .models import MatchResult

def findResult(resultLink):

    dbModel = MatchResult()

    url = resultLink

    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    # Find Home and Away Teams
    homeTeamDiv = soup.find('div', {'data-testid': 'match-detail_team-name_home'})
    homeTeam = soup.find('div', {'data-testid': 'match-detail_team-name_home'}).text
    awayTeamDiv = soup.find('div', {'data-testid': 'match-detail_team-name_away'})
    awayTeam = soup.find('div', {'data-testid': 'match-detail_team-name_away'}).text


    sontDiv = soup.find('div', {'id': 'match-detail__statistic__shotsOnTarget'})
    sofftDiv = soup.find('div', {'id': 'match-detail__statistic__shotsOffTarget'})
    posDiv = soup.find('div', {'id': 'match-detail__statistic__possession'}) 
    offDiv = soup.find('div', {'id': 'match-detail__statistic__offsides'}) 
    foulDiv = soup.find('div', {'id': 'match-detail__statistic__fouls'}) 
    catkDiv = soup.find('div', {'id': 'match-detail__statistic__counterAttacks'}) 


    hsont = sontDiv.find('span', {'data-testid': 'match-detail_statistic_home-stat'}).text
    awsont = sontDiv.find('span', {'data-testid': 'match-detail_statistic_away-stat'}).text
    hsofft = sofftDiv.find('span', {'data-testid': 'match-detail_statistic_home-stat'}).text
    awsofft = sofftDiv.find('span', {'data-testid': 'match-detail_statistic_away-stat'}).text
    hpos = posDiv.find('span', {'data-testid': 'match-detail_statistic_home-stat'}).text
    awpos = posDiv.find('span', {'data-testid': 'match-detail_statistic_away-stat'}).text
    hoff = offDiv.find('span', {'data-testid': 'match-detail_statistic_home-stat'}).text
    awoff = offDiv.find('span', {'data-testid': 'match-detail_statistic_away-stat'}).text
    hfoul = foulDiv.find('span', {'data-testid': 'match-detail_statistic_home-stat'}).text
    awfoul = foulDiv.find('span', {'data-testid': 'match-detail_statistic_away-stat'}).text
    hcatk = catkDiv.find('span', {'data-testid': 'match-detail_statistic_home-stat'}).text
    awcatk = catkDiv.find('span', {'data-testid': 'match-detail_statistic_away-stat'}).text


    if homeTeam == "Real Madrid":
        RMSTATS = {
            "Shots on Target" : hsont, 
            "Shots off Target" : hsofft,
            "Possession" : hpos,
            "Offsides" : hoff,
            "Fouls" : hfoul,
            "Counter Attacks" : hcatk,
        }

        RMSTATSLIST = [hsont,hsofft,hpos,hoff,hfoul,hcatk]

        OPPSTATS = {
            "Shots on Target" : awsont, 
            "Shots off Target" : awsofft,
            "Possession" : awpos,
            "Offsides" : awoff,
            "Fouls" : awfoul,
            "Counter Attacks" : awcatk,
        }

        OPPTATSLIST = [awsont,awsofft,awpos,awoff,awfoul,awcatk]

        dbModel.opponent = awayTeam
        dbModel.shootsOnTarget_rm = hsont
        dbModel.shootsOnTarget_opp = awsont
        dbModel.shootsOffTarget_rm = hsofft
        dbModel.shootsOffTarget_opp = awsofft
        dbModel.possession_rm = hpos
        dbModel.possession_opp = awpos
        dbModel.offsides_rm = hoff
        dbModel.offsides_opp = awoff
        dbModel.fouls_rm = hfoul
        dbModel.fouls_opp = awfoul
        dbModel.counterAttack_rm = hcatk
        dbModel.counterAttack_opp = awcatk
        dbModel.save()


    else:

        OPPSTATS = {
            "Shots on Target" : hsont, 
            "Shots off Target" : hsofft,
            "Possession" : hpos,
            "Offsides" : hoff,
            "Fouls" : hfoul,
            "Counter Attacks" : hcatk,
        }
        
        OPPSTATSLIST = [hsont,hsofft,hpos,hoff,hfoul,hcatk]

        RMSTATS = {
            "Shots on Target" : awsont, 
            "Shots off Target" : awsofft,
            "Possession" : awpos,
            "Offsides" : awoff,
            "Fouls" : awfoul,
            "Counter Attacks" : awcatk,
        }

        RMSTATSLIST = [awsont,awsofft,awpos,awoff,awfoul,awcatk]

        dbModel.opponent = homeTeam
        dbModel.shootsOnTarget_opp = hsont
        dbModel.shootsOnTarget_rm = awsont
        dbModel.shootsOffTarget_opp = hsofft
        dbModel.shootsOffTarget_rm = awsofft
        dbModel.possession_opp = hpos
        dbModel.possession_rm = awpos
        dbModel.offsides_opp = hoff
        dbModel.offsides_rm = awoff
        dbModel.fouls_opp = hfoul
        dbModel.fouls_rm = awfoul
        dbModel.counterAttack_opp = hcatk
        dbModel.counterAttack_rm = awcatk
        dbModel.save()

    # print(homeTeam)
    # print(awayTeam)
    # print("\n=======\nReal Madrid")
    # for key, value in RMSTATS.items():
    #     print(key, ' : ', value)


    # print("\n========\n"+homeTeam)
    # for key, value in OPPSTATS.items():
    #     print(key, ' : ', value)


    # # [print("RM:"+i) for i in RMSTATSLIST]

# resultLink = "https://www.livescore.com/en/football/champions-league/group-f/rb-leipzig-vs-real-madrid/798204/stats/"
# findResult(resultLink)