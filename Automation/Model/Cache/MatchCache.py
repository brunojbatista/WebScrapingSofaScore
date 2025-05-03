from datetime import datetime

from Library_v1.Utils.time import (
    format_date,
)

from Library_v1.Directory.Directory import Directory
from Library_v1.Storage.JsonStorage import JsonStorage

from Automation.Model.Match import Match
from Automation.Model.Competitions.Competition import Competition

class MatchCache():
    def __init__(self, date: datetime = None):
        self.relativepath = "Caching/Matches"
        self.formattedDate: str = None
        self.filename: str = None
        self.dir: Directory = None
        # self.dir.create()
        self.filepath: str = None
        self.json: JsonStorage = None
        self.data: list = []
        
        if not date is None: self.init(date)

    def init(self, date: datetime):
        if not self.formattedDate is None: return
        self.formattedDate = format_date(date, "<YYYY>-<MM>-<DD>")
        self.filename = f"{self.formattedDate}-matches-list.json"
        self.dir = Directory(self.relativepath)
        self.dir.create()
        self.filepath = Directory.separator(f"{self.dir.get_path()}/{self.filename}")
        self.json = JsonStorage(self.filepath, indent=4)
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
        index = match.generateIndex()
        if index is None: return False
        self.init(match.get('date'))
        hasFound = False
        for indexData, m in enumerate(self.data):
            if m['index'] == index:
                if m['match'] != match:
                    self.data[indexData] = {
                        "index": index,
                        "match": match,
                    }
                    hasFound = True
                    break;
                else:
                    return False
        if not hasFound:
            self.data.append({
                "index": index,
                "match": match,
            })
        self.data = sorted(self.data, key=lambda m: m['match'].get('date'))
        self.save()
        return True
    
    def remove(self, match: Match) -> bool:
        index = match.generateIndex()
        if index is None: return False
        self.init(match.get('date'))
        targetIndex = -1
        for index, m in enumerate(self.data):
            if m['index'] == index:
                targetIndex = index;
                break;
        if targetIndex >= 0: 
            del self.data[targetIndex]
            self.save()
            return True
        else:
            return False