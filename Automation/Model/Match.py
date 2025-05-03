from Automation.Model.BaseModel import BaseModel

from Library_v1.Utils.time import (
    format_date,
)

from Library_v1.Utils.string import (
    slug_name,
)


class Match(BaseModel):
    def __init__(self, 
        id = None,
        date = None,
        time = None,
        # country = None,
        competition = None,
        hometeam = None,
        hometeam_url = None,
        hometeam_emblem_url = None,
        awayteam = None,
        awayteam_url = None,
        awayteam_emblem_url = None,
        home_ft = None,
        away_ft = None,             
    ):
        super().__init__(
            id = id,
            date = date,
            time = time,
            # country = country,
            competition = competition,
            hometeam = hometeam,
            hometeam_url = hometeam_url,
            hometeam_emblem_url = hometeam_emblem_url,
            awayteam = awayteam,
            awayteam_url = awayteam_url,
            awayteam_emblem_url = awayteam_emblem_url,
            home_ft = home_ft,
            away_ft = away_ft,
        )

    def __eq__(self, other):
        if not isinstance(other, Match): return False
        return (
            self.id == other.id and
            self.date == other.date and
            self.time == other.time and
            self.competition == other.competition and
            self.hometeam == other.hometeam and
            self.hometeam_url == other.hometeam_url and
            self.hometeam_emblem_url == other.hometeam_emblem_url and
            self.awayteam == other.awayteam and
            self.awayteam_url == other.awayteam_url and
            self.awayteam_emblem_url == other.awayteam_emblem_url and
            self.home_ft == other.home_ft and
            self.away_ft == other.away_ft
        )

    def generateIndex(self, ):
        if self.get('date') is None or self.get('hometeam') is None or self.get('awayteam') is None: return None
        id = f"{format_date(self.get('date'), "<YYYY>-<MM>-<DD>")}-{slug_name(self.get('hometeam'))}_x_{slug_name(self.get('awayteam'))}"
        return id
