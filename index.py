# from Automation.Services.LeagueService import LeagueService

from Library_v1.Driver.ChromeDriver import ChromeDriver

from Automation.View.LeaguePage import LeaguePage

from Automation.Model.Match import Match
from Automation.Model.MatchInformation import MatchInformation

from Library_v1.Utils.time import (
    get_date,
    get_time,
)

from Automation.Model.Competitions.Spain.LaLiga import LaLiga
from Automation.Model.Competitions.Spain.LaLiga2 import LaLiga2

from Automation.Model.Competitions.Italy.SerieA import SerieA

from Automation.Model.Cache.MatchCache import MatchCache
from Automation.Model.Cache.MatchInformationCache import MatchInformationCache

from Automation.Model.Time.TimeStatistics import TimeStatistics

from typing import (
    List,
)

d = ChromeDriver()

competition_list = []

# ---------------------------------------------
# Spain
# competition_list.append(LaLiga())
# competition_list.append(LaLiga2())

# Italy
competition_list.append(SerieA())

# # =================================================================

# # Cache de partidas
# from Automation.Model.Cache.MatchCache import MatchCache

# matchCache: MatchCache = MatchCache(get_date(2025, 4, 26))

# print(f"matchCache: {matchCache}")

matchTest = Match(
    id = '11111111111',
    date = get_date(2025, 4, 29),
    time = get_time(8, 58),
    competition = None,
    hometeam = None,
    hometeam_url = None,
    hometeam_emblem_url = None,
    awayteam = None,
    awayteam_url = None,
    awayteam_emblem_url = None,
    home_ft = None,
    away_ft = None,  
)

# matchTest.set_all({
#     "date": get_date(2025, 4, 26),
#     "hour": get_time(16, 0),
#     "country": 'Pais Teste',
#     "league": 'Liga Teste',
#     "hometeam": 'Casa',
#     "awayteam": 'Visitante',
#     "home_ht": None,
#     "away_ht": None,
#     "home_ft": None,
#     "away_ft": None,
# })

# matchCache.add(matchTest)

# =================================================================

# Cache de stats


leaguePage = LeaguePage(d)

for competition in competition_list:
    url = competition.get('url')
    country = competition.get('country').get('name')
    print(f"country: {country}")

    leaguePage.navigate_league_page(url)

    leaguePage.click_per_date()

    events = leaguePage.read_event_cells()

    for e in events:
        print(e.get_all())

    input("Selecione uma partida...")

    match: Match = leaguePage.read_information_match(competition)

    matchCache: MatchCache = MatchCache()

    status = matchCache.add(match)
    print(f"status: {status}")

    stats: List[TimeStatistics] = leaguePage.read_statistics_match()

    matchInformation: MatchInformation = MatchInformation(
        stats=stats
    )

    # print(f"stats: {stats}")
    # print(f"ht: {stats[0].get_all()}")
    # print(f"2t: {stats[1].get_all()}")
    # print(f"ft: {stats[2].get_all()}")


    # stats[2].set('ball_possession', {"home_value": 'bbbbbbbbb', "away_value": 'awdawd'})

    # status = matchInformation.updateStats(stats[-1])
    # print(f"status: {status}")

    # # -------------------------------------------------
    # # Criar a cache de informações do jogo
    matchInformationCache = MatchInformationCache()

    matchInformationCache.add(match, matchInformation)

    # matchInformationReading: MatchInformation = matchInformationCache.get(match)
    # print(f"matchInformationReading: {matchInformationReading}")
    # if not matchInformationReading is None:
    #     if matchInformationReading.updateStats(*stats):
    #         print("Atualizou o stats....")
    #         matchInformationCache.add(match, matchInformationReading)
    # else:
    #     print("Criou....")
    #     matchInformation: MatchInformation = MatchInformation(
    #         stats=stats
    #     )
    #     matchInformationCache.add(match, matchInformation)




print("Finalizou...")
leaguePage.get_actions().sleep(3600)




# leaguePage = LeaguePage(d)

# leaguePage.navigate_league_page('https://www.sofascore.com/pt/torneio/futebol/spain/laliga/8')

# leaguePage.click_per_date()

# events = leaguePage.read_event_cells()

# for e in events:
#     print(e.get_all())

# leaguePage.select_match(events[0])

# # leaguePage.change_tab_in_match('Estatísticas')

# match_information = leaguePage.read_information_match()

# print(match_information.get_all())

# times = leaguePage.read_statistics_match()

# ------------------------------------------------------
# Criar a cache para salvar os dadaos

# print("Finalizou...")
# leaguePage.get_actions().sleep(3600)