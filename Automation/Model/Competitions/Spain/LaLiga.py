from Automation.Model.Competitions.Competition import Competition
from Automation.Model.Countries.Spain import Spain


class LaLiga(Competition):
    def __init__(self, ):
        super().__init__(
            'La Liga',
            Spain(),
            'https://www.sofascore.com/pt/torneio/futebol/spain/laliga/8',
        )