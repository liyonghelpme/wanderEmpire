from sqlalchemy import Table, Column
class Caebuy(object):
    def __init__(self,uid,cae,time):
        self.uid=uid
        self.cae=cae
        self.time=time