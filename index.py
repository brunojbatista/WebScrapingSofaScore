# from Automation.Services.LeagueService import LeagueService

from Library_v1.Driver.ChromeDriver import ChromeDriver

from Automation.View.LeaguePage import LeaguePage

d = ChromeDriver()


league = LeaguePage(d)

# from Automation.Model.EventCell import EventCell

# e = EventCell()
# print(e.get_all())

league.navigate_league_page('https://www.sofascore.com/pt/torneio/futebol/spain/laliga/8#id:61643')

league.click_per_date()

events = league.read_event_cells()

for e in events:
    print(e.get_all())

league.select_match(events[0])

# league.change_tab_in_match('Estatísticas')

match_information = league.read_information_match()

print(match_information.get_all())

league.read_statistics_match()

print("Finalizou...")
league.get_actions().sleep(3600)