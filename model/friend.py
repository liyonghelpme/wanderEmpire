from sqlalchemy import Table, Column
class Friend(object):
    def __init__(self,uid,fotherid):
        self.uid=uid
        self.fotherid=fotherid