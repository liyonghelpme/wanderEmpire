from sqlalchemy import Table,Column


class businessRead(object):
    def __init__(self,city_id,layout):
        self.city_id=city_id
        self.layout=layout

