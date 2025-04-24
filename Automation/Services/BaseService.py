from Library_v1.Driver.DriverActions import DriverActions
from Library_v1.Driver.DriverInterface import DriverInterface
# from Library_v1.Driver.ChromeDriver import ChromeDriver

class BaseService():
    def __init__(self, driver: DriverInterface):
        self.driver: DriverInterface = driver
        self.actions: DriverActions = DriverActions(self.driver)

    # def navigate_league_page(self, url: str):
    #     from Automation.Services.Exceptions.NavigateLeaguePageException import NavigateLeaguePageException
    #     self.actions.navigate_url(url)
    #     check_xpath = f"//main/div/div[1]/div/ul/li[last()]/h1[contains(text(), 'Classificações, jogos, resultados e estatísticas')]"
    #     if not self.actions.has_element(check_xpath):
    #         raise ContractException('fail_new_contract_navigate')
    #     return self;
