from sqlalchemy import Table,Column

class warMap(object):
    def __init__(self,userid,mapid,gridid,map_kind):
        self.mapid=mapid
        self.gridid=gridid
        self.map_kind=map_kind
        self.userid=userid
