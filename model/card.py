from sqlalchemy import Table, Column
class Card(object):
    def __init__(self,uid):
        self.uid=uid