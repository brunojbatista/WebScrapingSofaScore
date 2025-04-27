from Automation.Model.BaseModel import BaseModel

class League(BaseModel):
    def __init__(self, name: str = None, country: str = None, url: str = None):
        super().__init__(
            name=name,
            country=country,
            url=url,
        )