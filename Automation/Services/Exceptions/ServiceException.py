class ServiceException(Exception):
    def __init__(self, message: str):
        self.message: str = message
        super().__init__(self.message)