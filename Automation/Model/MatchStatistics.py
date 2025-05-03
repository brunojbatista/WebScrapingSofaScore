from Automation.Model.BaseModel import BaseModel

from Automation.Model.TimeStatistics import TimeStatistics

from Automation.Model.Match import Match

class MatchStatistics(BaseModel):
    def __init__(self, match: Match, halfTimeStats: TimeStatistics, secondTimeStats: TimeStatistics, fullTimeStats: TimeStatistics):
        super().__init__(
            match=match,
            halfTimeStats=halfTimeStats,
            secondTimeStats=secondTimeStats,
            fullTimeStats=fullTimeStats,
        )

    def __eq__(self, other):
        if not isinstance(other, MatchStatistics): return False
        return (
            self.match == other.match and
            self.halfTimeStats == other.halfTimeStats and
            self.secondTimeStats == other.secondTimeStats and
            self.fullTimeStats == other.fullTimeStats
        )