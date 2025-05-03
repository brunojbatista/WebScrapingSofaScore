from Automation.Model.BaseModel import BaseModel

from Automation.Model.Time.TimeStatistics import TimeStatistics
from Automation.Model.Time.HalfTimeStatistics import HalfTimeStatistics
from Automation.Model.Time.SecondTimeStatistics import SecondTimeStatistics
from Automation.Model.Time.FullTimeStatistics import FullTimeStatistics
from typing import (
    List,
)

class MatchInformation(BaseModel):
    def __init__(self,
        details=None,
        stats=[],
    ):
        super().__init__(
            details=details,
            stats=stats,
        )

    def __eq__(self, other):
        if not isinstance(other, MatchInformation): return False
        return (
            self.details == other.details and
            self.stats == other.stats
        )
    
    def hasDetails(self, ) -> bool:
        return not self.get('details') is None
    
    def hasStats(self, ) -> bool:
        return len(self.get('stats')) > 0
    
    def updateDetails(self, ):
        raise NotImplementedError("É preciso implementar a atualização de detalhamento")
    
    def updateStats(self, *newTimeStats: List[TimeStatistics]) -> bool:
        # print(f"newTimeStats: {newTimeStats}")
        currentTimeStats = self.get('stats')
        hasChanged = False
        for newStats in newTimeStats:
            # Buscar pelo index que tem o mesmo time
            # Verificar se o index existir, caso o stat seja diferente substitua-a
            targetIndex = next((index for index, currentStats in enumerate(currentTimeStats) if currentStats.get('time') == newStats.get('time')), -1)
            # print(f"-"*80)
            # print(f"targetIndex: {targetIndex}")
            if targetIndex >= 0:
                targetStats = currentTimeStats[targetIndex]
                # print(targetStats.get_all())
                # print(newStats.get_all())
                if targetStats != newStats:
                    currentTimeStats[targetIndex] = newStats
                    # currentTimeStats[index] = stats
                    self.set('stats', currentTimeStats)
                    hasChanged = True
        return hasChanged