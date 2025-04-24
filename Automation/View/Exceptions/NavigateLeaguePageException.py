from Automation.View.Exceptions.ViewException import ViewException

class NavigateLeaguePageException(ViewException):
    def __init__(self, ):
        super().__init__("Erro ao navegar para a página da liga")