from sqlalchemy import Table, Column
class Victories(object):
    def __init__(self,uid,won,lost):
        self.won=won
        self.lost=lost