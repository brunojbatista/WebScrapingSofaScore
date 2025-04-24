from Library_v1.Data.BaseData import BaseData
from Library_v1.Utils.time import date_now

class BaseModel(BaseData):
    def __init__(self, **parameters):
        super().__init__(
            **{
                **parameters,
                'created_at': None,
            }
        )
        self.set('created_at', date_now())