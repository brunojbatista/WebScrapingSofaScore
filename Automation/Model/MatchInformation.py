from Automation.Model.BaseModel import BaseModel

class MatchInformation(BaseModel):
    def __init__(self, ):
        super().__init__(
            id=None,
            country=None,
            country_url=None,
            name_competition=None,
            competition_url=None,
            hometeam=None,
            hometeam_url=None,
            hometeam_emblem_url=None,
            awayteam=None,
            awayteam_url=None,
            awayteam_emblem_url=None,
        )