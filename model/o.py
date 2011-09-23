from sqlalchemy import Table,Column

class operationalData(object):
    def __init__(self,labor_num,population,exp,corn,cae,nobility,infantry1_num,cavalry1_num,scout1_num,person_god,wealth_god,food_god,war_god,user_kind,otherid,lev,empirename,food, nbattleresult):
        self.labor_num=labor_num
        self.population=population
        self.exp=exp
        self.corn=corn
        self.cae=cae
        self.nobility=nobility
        self.infantry1_num=infantry1_num
        self.cavalry1_num=cavalry1_num
        self.scout1_num=scout1_num
        self.person_god=person_god
        self.wealth_god=wealth_god
        self.food_god=food_god
        self.war_god=war_god
        self.user_kind=user_kind
        self.otherid=otherid
        self.lev=lev
        self.empirename=empirename
        self.food=food
        self.nbattleresult=nbattleresult
