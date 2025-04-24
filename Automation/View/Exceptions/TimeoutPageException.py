from Automation.View.Exceptions.ViewException import ViewException

class TimeoutPageException(ViewException):
    def __init__(self, ):
        super().__init__("A página não carregou")