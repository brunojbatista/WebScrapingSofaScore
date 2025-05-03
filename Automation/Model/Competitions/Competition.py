from Automation.Model.BaseModel import BaseModel
from Automation.Model.Countries.Country import Country

class Competition(BaseModel):
    def __init__(self, name: str = None, country: Country = None, url: str = None):
        super().__init__(
            name=name,
            country=country,
            url=url,
        )

    def __str__(self):
        return f"Competition: {self.get('name')}, {self.get('country').get('name')}"
    
    def __eq__(self, other):
        if not isinstance(other, Competition): return False
        return (
            self.name == other.name and
            self.country == other.country and
            self.url == other.url
        )