from Automation.Model.BaseModel import BaseModel

class EventCell(BaseModel):
    def __init__(self, ):
        super().__init__(
            id=None,
            url=None,
            date=None,
            hometeam=None,
            awayteam=None,
            home_ft=None,
            away_ft=None,
        )