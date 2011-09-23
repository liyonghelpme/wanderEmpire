from sqlalchemy import Table, Column
class News(object):
    def __init__(self,uid,fpapayaid,kind,time):
        self.uid=uid
        self.fpapayaid=fpapayaid
        self.kind=kind
        self.time=time