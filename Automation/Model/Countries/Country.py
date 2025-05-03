from Automation.Model.BaseModel import BaseModel

class Country(BaseModel):
    def __init__(self, name: str = None):
        super().__init__(
            name=name,
        )

    def __str__(self):
        return f"Country: {self.get('name')}"
    
    def __eq__(self, other):
        if not isinstance(other, Country): return False
        return (
            self.name == other.name
        )