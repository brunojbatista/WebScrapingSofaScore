from datetime import datetime

from Library_v1.Utils.time import (
    format_date,
)

from Library_v1.Directory.Directory import Directory
from Library_v1.Storage.JsonStorage import JsonStorage

from Automation.Model.Match import Match
from Automation.Model.MatchInformation import MatchInformation
from Automation.Model.Competitions.Competition import Competition

class MatchInformationCache():
    def __init__(self, ):
        self.relativepath: str = None
        self.formattedDate: str = None
        self.filename: str = None
        self.dir: Directory = None
        self.filepath: str = None
        self.json: JsonStorage = None
        self.data: MatchInformation = None

    def init(self, match: Match):
        self.index = match.generateIndex()
        if self.index is None: return
        self.formattedDate = format_date(match.get('date'), "<YYYY>-<MM>-<DD>")
        self.relativepath = f"Caching/MatchInformation/{self.formattedDate}"
        self.filename = f"{self.index}.json"
        self.dir = Directory(self.relativepath)
        self.dir.create()
        self.filepath = Directory.separator(f"{self.dir.get_path()}/{self.filename}")
        self.json = JsonStorage(self.filepath, indent=4)
        self.read()

    def read(self, ) -> list:
        self.data: MatchInformation = self.json.read()
        if self.data is None: self.data: MatchInformation = None

    def save(self, ):
        self.json.write(self.data)
        return self

    def hasData(self, ) -> bool:
        return len(list(self.data.keys()))
    
    def add(self, match: Match, matchInformation: MatchInformation) -> bool:
        if match.generateIndex() is None: return False
        self.init(match)
        # self.data: MatchInformation = matchInformation

        matchInformationReading: MatchInformation = self.get(match)
        print(f"matchInformationReading: {matchInformationReading}")
        if not matchInformationReading is None:
            hasUpdate = False
            if matchInformationReading.updateStats(*matchInformation.get('stats')):
                print("Atualizou o stats....")
                self.data: MatchInformation = matchInformationReading
                hasUpdate = True
            if hasUpdate: self.save()
        else:
            print("Criou....")
            self.data: MatchInformation = matchInformation
            self.save()

        return True
    
    def get(self, match: Match) -> MatchInformation:
        if match.generateIndex() is None: return None
        self.init(match)
        return self.data
    
    def remove(self, match: Match) -> bool:
        if match.generateIndex() is None: return False
        self.init(match)
        self.data: MatchInformation = None
        self.json.delete()
        return True