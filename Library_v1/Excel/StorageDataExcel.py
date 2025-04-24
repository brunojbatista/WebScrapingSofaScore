

class StorageDataExcel():
    def __init__(self, columns: list = [], rows: list = []) -> None:
        self.columns = []
        self.rows = []
        self.total_columns = 0;
        self.total_rows = 0;
        self.reset().set_columns(columns).set_rows(rows)

    def get_rows(self, ) -> list:
        return self.rows
    
    def get_columns(self, ) -> list:
        return self.columns

    def update_total_rows(self, ):
        self.total_rows = len(self.get_rows())
    
    def update_total_columns(self, ):
        self.total_columns = len(self.get_columns())

    def set_rows(self, rows: list):
        self.rows = rows
        self.update_total_rows();
        return self;

    def set_columns(self, columns: list):
        self.columns = columns
        self.update_total_columns()
        return self;

    def reset(self, ):
        self.set_rows([])
        self.set_columns([])
        return self;

    def get_total_columns(self, ) -> int:
        return self.total_columns
    
    def get_total_rows(self, ) -> int:
        return self.total_rows

