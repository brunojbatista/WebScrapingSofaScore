from datetime import datetime

from Library_v1.Utils.time import (
    format_date,
)

from Library_v1.Directory.Directory import Directory
from Library_v1.Storage.JsonStorage import JsonStorage

from Automation.Model.Match import Match

class MatchCache():
    def __init__(self, date: datetime):
        self.relativepath = "Caching/Matches"
        self.formattedDate = format_date(date, "<YYYY>-<MM>-<DD>")
        self.filename = f"{self.formattedDate}-matches-list.json"
        self.dir = Directory(self.relativepath)
        self.dir.create()
        self.filepath = Directory.separator(f"{self.dir.get_path()}/{self.filename}")
        self.json = JsonStorage(self.filepath, indent=4)

        def match_decoder(obj) -> Match:
            m = Match()
            m.set_all(obj.get('__value'))
            return m

        self.json.add_serialize(
            'match',
            Match,
            lambda obj: obj.get_all(),
            lambda obj: match_decoder(obj),
        )

        self.data: list = []
        self.read()

    def read(self, ) -> list:
        self.data = self.json.read()
        if self.data is None: self.data = []

    def save(self, ):
        self.json.write(self.data)
        return self

    def hasData(self, ) -> bool:
        return len(self.data)
    
    def add(self, match: Match) -> bool:
        id = match.generateId()
        if id is None: return False
        hasFound = False
        for index, m in enumerate(self.data):
            if m['id'] == id:
                self.data[index] = {
                    "id": id,
                    "match": match,
                }
                hasFound = True
                break;
        if not hasFound:
            self.data.append({
                "id": id,
                "match": match,
            })
        self.data = sorted(self.data, key=lambda m: m['match'].get('date'))
        self.save()
        return True
    
    def remove(self, match: Match) -> bool:
        id = match.generateId()
        if id is None: return False
        targetIndex = -1
        for index, m in enumerate(self.data):
            if m['id'] == id:
                targetIndex = index;
                break;
        if targetIndex >= 0: 
            del self.data[targetIndex]
            self.save()
            return True
        else:
            return False