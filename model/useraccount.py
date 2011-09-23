from sqlalchemy import Table, Column

class userAccount(object):
    def __init__(self,userid,otherid):
        self.userid=userid
        self.otherid=otherid
