from Library_v1.Driver.DriverInterface import DriverInterface
from Library_v1.Driver.DriverActions import DriverActions

class BaseView():
    def __init__(self, driver: DriverInterface):
        self.driver: DriverInterface = driver
        self.actions: DriverActions = DriverActions(self.driver)

        self.actions.setZoom(75)

    def get_driver(self, ) -> DriverInterface:
        return self.driver
    
    def get_actions(self, ) -> DriverActions:
        return self.actions