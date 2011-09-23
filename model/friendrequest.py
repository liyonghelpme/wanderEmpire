from sqlalchemy import Table, Column
class FriendRequest(object):
    def __init__(self,sendid,receiveid,message):
        self.sendid=sendid
        self.receiveid=receiveid
        self.message=self.message