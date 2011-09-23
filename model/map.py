from sqlalchemy import Table, Column

class Map(object):
    def __init__(self,map_kind,num):
        self.map_kind=map_kind
        self.num=num
