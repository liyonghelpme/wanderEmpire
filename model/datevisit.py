from sqlalchemy import Table, Column
class Datevisit(object):
    def __init__(self,uid,visitnum):
        self.uid=uid
        self.visitnum=visitnum