from sqlalchemy import Table, Column
class Gift(object):
    def __init__(self,uid,fid,askorgive,present,fkind,ukind):
        self.uid=uid
        self.fid=fid
        self.askorgive=askorgive
        self.present=present
        self.fkind=fkind
        self.ukind=ukind