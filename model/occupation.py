from sqlalchemy import Table, Column
class Occupation(object):
    def __init__(self,masterid,slaveid):
        self.masterid=masterid
        self.slaveid=slaveid