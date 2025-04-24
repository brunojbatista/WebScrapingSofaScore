from Library_v1.Driver.DriverInterface import DriverInterface

from Automation.Services.BaseService import BaseService

"""
    Coleta dos jogos da liga
"""

class LeagueService(BaseService):
    def __init__(self, driver: DriverInterface):
        super().__init__(driver)
    
