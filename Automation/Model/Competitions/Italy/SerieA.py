from Automation.Model.Competitions.Competition import Competition
from Automation.Model.Countries.Italy import Italy

class SerieA(Competition):
    def __init__(self, ):
        super().__init__(
            'Serie A',
            Italy(),
            'https://www.sofascore.com/pt/torneio/futebol/italy/serie-a/23',
        )