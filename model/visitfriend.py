from sqlalchemy import Table, Column
class visitFriend(object):
    def __init__(self,userid,friendid):
        self.userid=userid
        self.friendid=friendid