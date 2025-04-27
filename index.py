# from Automation.Services.LeagueService import LeagueService

from Library_v1.Driver.ChromeDriver import ChromeDriver

from Automation.View.LeaguePage import LeaguePage

from Automation.Model.Match import Match

from Library_v1.Utils.time import (
    get_date,
    get_time,
)

from Automation.Model.Leagues.Spain.LaLiga import LaLiga
from Automation.Model.Leagues.Spain.LaLiga2 import LaLiga2



# league = LeaguePage(d)

d = ChromeDriver()

leagues_list = []

# ---------------------------------------------
# Spain
leagues_list.append(LaLiga())
leagues_list.append(LaLiga2())


# =================================================================

# Cache de partidas
from Automation.Model.Cache.MatchCache import MatchCache

matchCache: MatchCache = MatchCache(get_date(2025, 4, 26))

print(f"matchCache: {matchCache}")

matchTest = Match()

matchTest.set_all({
    "date": get_date(2025, 4, 26),
    "hour": get_time(16, 0),
    "country": 'Pais Teste',
    "league": 'Liga Teste',
    "hometeam": 'Casa',
    "awayteam": 'Visitante',
    "home_ht": None,
    "away_ht": None,
    "home_ft": None,
    "away_ft": None,
})

matchCache.add(matchTest)


# league.navigate_league_page('https://www.sofascore.com/pt/torneio/futebol/spain/laliga/8')

# league.click_per_date()

# events = league.read_event_cells()

# for e in events:
#     print(e.get_all())

# league.select_match(events[0])

# # league.change_tab_in_match('Estatísticas')

# match_information = league.read_information_match()

# print(match_information.get_all())

# times = league.read_statistics_match()

# ------------------------------------------------------
# Criar a cache para salvar os dadaos

# print("Finalizou...")
# league.get_actions().sleep(3600)