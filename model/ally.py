from sqlalchemy import Table, Column
class Ally(object):
    def __init__(self,uid,fid):
        self.uid=uid
        self.fid=fid