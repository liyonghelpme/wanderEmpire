from sqlalchemy import Table, Column
class Papayafriend(object):
    def __init__(self,uid,papayaid,lev,user_kind):
        self.uid=uid
        self.papayaid=papayaid
        self.lev=self
        self.user_kind=user_kind