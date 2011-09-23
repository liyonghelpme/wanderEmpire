from sqlalchemy import Table, Column
class News(object):
    def __init__(self,uid,fpapayaid,kind,time,fuser_kind):
        self.uid=uid
        self.fpapayaid=fpapayaid
        self.kind=kind
        self.time=time
        self.fuser_kind=fuser_kind