from Automation.Model.BaseModel import BaseModel

from Library_v1.Utils.time import (
    format_date,
)

from Library_v1.Utils.string import (
    slug_name,
)


class Match(BaseModel):
    def __init__(self, ):
        super().__init__(
            date = None,
            hour = None,
            country = None,
            league = None,
            hometeam = None,
            awayteam = None,
            home_ht = None,
            away_ht = None,
            home_ft = None,
            away_ft = None,
        )

    def generateId(self, ):
        if self.get('date') is None or self.get('hometeam') is None or self.get('awayteam') is None: return None
        id = f"{format_date(self.get('date'), "<YYYY>-<MM>-<DD>")}__{slug_name(self.get('hometeam'))}__x__{slug_name(self.get('awayteam'))}"
        return id
