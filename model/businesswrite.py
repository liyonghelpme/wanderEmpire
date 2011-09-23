from sqlalchemy import Table, Column

class businessWrite(object):
    def __init__(self,city_id,ground_id,grid_id,object_id,producttime,finish):
        self.city_id=city_id
        self.ground_id=ground_id
        self.grid_id=grid_id
        self.object_id=object_id
        self.producttime=producttime
        self.finish=finish
