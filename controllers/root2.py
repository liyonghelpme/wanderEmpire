# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController
from repoze.what import predicates
from sqlalchemy.exceptions import InvalidRequestError
from sqlalchemy.exceptions import IntegrityError
from stchong.lib.base import BaseController
from stchong.model import DBSession, metadata,operationalData,businessWrite,businessRead
from stchong import model
from stchong.controllers.secure import SecureController
from datetime import datetime
from stchong.controllers.error import ErrorController
import time
__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the stchong application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    global Building_Price
    global Plant_Price
    global beginTime
    global increasefood
    global increasebuild
    global increaseheishi
    global houses
    global soldie
    global soldiernum
    global production
    global read
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)
    Building_Price=[[1000,0,100,0],[500,10,0,1],[1000,30,0,1],[1500,60,0,1],[1000,60,0,1],[1500,100,0,1],[2000,200,0,1],[2000,200,0,2],[2500,300,0,2],[3000,400,0,2],[3000,400,0,2],[3500,500,0,2],[4000,600,0,2],[4000,600,0,3],[5000,700,0,3],[6000,800,0,3],[-5,0,0,3],[-10,0,0,3],[-20,0,0,3],[5000,150,150,1],[15000,300,20,2],[50000,600,50,3],[100,20,20,1],[300,30,5,1],[500,50,10,1],[600,30,20,1],[750,50,5,1],[900,70,5,1],[1200,50,40,2],[1400,70,5,2],[1600,100,5,2],[1800,100,70,2],[2100,130,5,2],[2400,150,5,2],[2400,130,90,3],[2800,150,5,3],[3200,170,5,3],[7200,150,110,3],[10200,170,5,3],[13200,200,5,3],[-1,0,0,4],[-3,0,0,4],[-5,0,0,4],[-2,0,0,4],[-5,0,0,4],[-10,0,5,4]]#corn,food,labor_num,cae 0:nongtian 1-18:minju 19-21:bingying 22-shangye
    Plant_Price=[[50,0,1],[140,0,1],[255,0,1],[-1,0,1],[504,0,1],[575,0,2],[660,0,2],[-2,0,2],[1265,0,2],[1386,0,3],[1470,0,3],[-5,0,3]]#corn,food,cae
    production=[]#not decided for now
    increasefood=[[1,30],[1,80],[1,160],[5,200],[3,300],[3,370],[3,410],[10,550],[5,520],[5,610],[5,720],[15,1000]]#exp,food
    increasebuild=[[3,0],[1,0],[2,0],[3,0],[2,0],[3,0],[4,0],[3,0],[4,0],[5,0],[4,0],[5,0],[6,0],[7,0],[8,0],[9,0],[10,0],[15,0],[20,0],[5,0],[10,0],[15,0],[1,0],[2,0],[3,0],[2,0],[3,0],[4,0],[3,0],[4,0],[5,0],[4,0],[5,0],[6,0],[5,0],[6,0],[7,0],[6,0],[7,0],[8,0],[10,0],[15,0],[20,0],[15,0],[20,0],[25,0]]#exp,population
    increaseheishi=[[50,10],[100,10],[200,10]]#exp,battlepopulation
    beginTime=(2011,1,1,0,0,0,0,0,0)
    houses=[[20,40,1,1800,1],[40,80,2,1800,1],[60,120,3,1800,1],[75,150,2,7200,2],[95,190,3,7200,2],[115,230,4,7200,2],[105,210,3,10800,2],[125,250,4,10800,2],[150,300,5,10800,2],[135,270,4,14400,2],[155,310,5,14400,3],[180,360,6,14400,3],[190,380,5,18000,3],[210,420,6,18000,3],[230,460,7,18000,3],[280,500,10,3600,4],[400,600,15,3600,4],[500,700,20,3600,4]]#population,food,exp got,caeground_id 1:18 pian yi ground_id-1
    soldie=[[1200,60,20,3],[3100,155,50,3],[6200,310,100,3],[2400,120,20,3],[6200,310,50,3],[12400,620,100,3],[3600,180,20,3],[9300,465,50,3],[18600,930,100,3],[6000,300,20,6],[15100,755,50,6],[30200,1600,100,6],[7500,375,20,6],[18875,943,50,6],[37750,2000,100,6],[9000,450,20,6],[22650,1132,50,6],[45300,2400,100,6],[800,10,2,9],[2100,30,5,9],[4200,60,10,9],[1000,20,2,9],[2700,60,5,9],[5400,120,10,9],[1200,40,2,9],[3300,120,5,9],[6600,240,10,9]]#corn,food,labor_num,cae
    soldiernum=[10,10,10,15,15,15,20,20,20,15,15,15,20,20,20,25,25,25,5,5,5,10,10,10,15,15,15]#soldier exp
    production=[[100,1,1,600],[200,2,1,600],[300,3,1,600],[250,2,1,1800],[500,3,1,1800],[750,4,1,1800],[500,3,1,3600],[1000,4,1,3600],[1500,5,1,3600],[1100,4,2,7200],[2200,5,2,7200],[3300,6,2,7200],[2100,5,2,14400],[4200,6,2,14400],[6300,7,2,14400],[3000,6,3,21600],[6000,7,3,21600],[9000,8,3,21600],[1000,10,2,3600],[2000,15,2,3600],[3000,20,2,3600],[3000,15,3,10800],[6000,20,3,10800],[9000,25,3,10800]]#corn that the plant can produce for a cycle,production,exp,speedup cae ground_id-22
    error = ErrorController()
    def read(city_id):
        try:
            s=' '
            i=0
            cid=int(city_id)
            cset=DBSession.query(businessWrite).filter_by(city_id=cid)
            for c in cset:
                if i==0:
                    s=s+str(c.ground_id)+','+str(c.grid_id)+','+str(c.object_id)+','+str(c.producttime)
                    i=1
                else :
                    s=s+';'+str(c.ground_id)+','+str(c.grid_id)+','+str(c.object_id)+','+str(c.producttime)
            try:
                cc=DBSession.query(businessRead).filter_by(city_id=cid).one()
                #return dict(id=3,s=cc.layout)
                cc.layout=s
                return 1
            except InvalidRequestError:
                newread=businessRead(city_id=cid,layout=s)
                DBSession.add(newread)
                return 2
        except InvalidRequestError:
            return 0
    @expose('json')
    def logsign(self,papayaid):
        try:
            oid=int(papayaid)
            user=DBSession.query(operationalData).filter_by(otherid=oid).one()
        except InvalidRequestError:
            newuser=operationalData(labor_num=0,population=0,exp=0,corn=0,cae=0,nobility=0,infantry_num=0,cavalry_num=0,scout_num=0,person_god=0,wealth_god=0,food_god=0,war_god=0,user_kind=0,otherid=oid,lev=0,empirename='MyEmpire',food=0)
            DBSession.add(newuser)
            c1=DBSession.query('LAST_INSERT_ID()')
           # newaccount=userAccount(userid=c1[0],otherid=oid)
           # DBSession.add(newaccount)
            return dict(id=c1[0])
        return dict(id=user.userid)
    @expose('json')
    def build(self,user_id,city_id,ground_id,grid_id):
        i=0
        try:
            ca=0
            price=Building_Price[int(ground_id)][0]
            pricefood=Building_Price[int(ground_id)][1]
            u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            ptime=p.producttime;
            pop=Building_Price[int(ground_id)][2]+u.labor_num
            if price<0 :
                ca=u.cae+price
                i=1
            if i==1 and ca>=0 and u.food-pricefood>=0 and pop<=u.population and ptime==0:
                sub=u.cae+price
                u.labor_num=pop
                u.cae=sub#to update the datasheet
                u.food=u.food-pricefoods
                ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
                p.ground_id=ground_id
                p.object_id=-1
                p.producttime=ti
                read(city_id)
                return dict(id=1)
            elif ca<0:
                return dict(ca=ca,id=-1)                
            if u.corn-price>=0 and u.food-pricefood>=0 and pop<=u.population and ptime==0:
                sub=u.corn-price
                u.labor_num=pop
                u.corn=sub#to update the datasheet
                u.food=u.food-pricefood
                if(int(ground_id)==0):
                    u.exp=u.exp+increasebuild[int(ground_id)][0]
                    read(int(city_id))
                    p.finish=1
                    return dict(id=11)
                ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
                p.ground_id=int(ground_id)
                p.grid_id=int(grid_id)
                p.producttime=ti
                read(int(city_id))
                return dict(id=1)
            else:
                return dict(price=u.corn-price,food=u.food-pricefood,pop=pop,id=0)
        except InvalidRequestError:
            u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            price=Building_Price[int(ground_id)][0]
            pricefood=Building_Price[int(ground_id)][1]
            pop=(Building_Price[int(ground_id)][2])+u.labor_num
            if price<0:
                ca=u.cae+price
                i=1
            if i==1 and ca>=0 and u.food-pricefood>=0 and pop<=u.population:
                sub=u.cae+price
                u.labor_num=pop
                u.cae=sub#to update the datasheet
                u.food=u.food-pricefood
                ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
                newbuilding=businessWrite(city_id=int(city_id),ground_id=int(ground_id),grid_id=int(grid_id),object_id=-1,producttime=ti,finish=0)
                DBSession.add(newbuilding)
                read(int(city_id))
                return dict(id=1)
            elif i==1 and ca<0:
                return dict(id=0) 
            elif  u.corn-price>=0 and u.food-pricefood>=0 and pop<=u.population:
                sub=u.corn-price
                u.food=u.food-pricefood
                u.labor_num=pop
                u.corn=sub#to update the datasheet
                ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
                
                newbuilding=businessWrite(city_id=int(city_id),ground_id=int(ground_id),grid_id=int(grid_id),object_id=-1,producttime=ti,finish=0)
                DBSession.add(newbuilding)
                read(int(city_id))
                return dict(id=1)
            else:
                return dict(ul=u.labor_num,price=u.corn-price,food=u.food-pricefood,pop=pop,id=-1)

    @expose('json')
    def build2(self,user_id,city_id,ground_id,grid_id):
        i=0
        try:
            
            price=Building_Price[int(ground_id)][0]
            pricefood=Building_Price[int(ground_id)][1]
            u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            return dict(id=0)
        except InvalidRequestError:
            i=0
            u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            price=Building_Price[int(ground_id)][0]
            pricefood=Building_Price[int(ground_id)][1]
            pop=(Building_Price[int(ground_id)][2])+u.labor_num
            ca=1
            if price<0:
                ca=u.cae+price
                i=1
            if i==1 and ca>=0 and u.food-pricefood>=0 and pop<=u.population:
                sub=u.cae+price
                u.labor_num=pop
                u.cae=sub#to update the datasheet
                u.food=u.food-pricefood
                ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
                newbuilding=businessWrite(city_id=int(city_id),ground_id=int(ground_id),grid_id=int(grid_id),object_id=-1,producttime=ti,finish=0)
                DBSession.add(newbuilding)
                read(city_id)
                return dict(id=1)
            elif i==1 and ca<0:
                return dict(ca=ca,i=i,id=0) 
            elif u.corn-price>=0 and u.food-pricefood>=0 and pop<=u.population:
                sub=u.corn-price
                u.food=u.food-pricefood
                u.labor_num=pop
                u.corn=sub#to update the datasheet
                ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
                newbuilding=businessWrite(city_id=int(city_id),ground_id=int(ground_id),grid_id=int(grid_id),object_id=-1,producttime=ti,finish=0)
                DBSession.add(newbuilding)
                read(city_id)
                return dict(id=1)
            else:
                return dict(ul=u.labor_num,price=price,food=pricefood,pop=pop,id=-1)
    @expose('json')
    def planting(self,user_id,city_id,grid_id,object_id):
        try:
            price=Plant_Price[int(object_id)][0]
            pricefood=Plant_Price[int(object_id)][1]
            u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            ptime=p.producttime;
            if price<0:
                sub=u.cae+price
                if sub>=0 and u.food-pricefood>=0 and ptime==0:
                    sub=u.cae
                    u.food=u.food-pricefood
                    u.corn=sub#to update the datasheet
                    ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
                    p.object_id=int(object_id)
                    p.producttime=ti
                    read(city_id)
                    return dict(id=1)
                else:
                    return dict(id=0)
            elif u.corn-price>=0 and u.food-pricefood>=0 and ptime==0:
                sub=u.corn-price
                u.food=u.food-pricefood
                u.corn=sub#to update the datasheet
                ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
                p.object_id=int(object_id)
                p.producttime=ti
                read(city_id)
                return dict(id=1)
            else:
                return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def harvest(self,user_id,city_id,grid_id):
        try:
           p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
           tu=increasefood[p.object_id]
           p.producttime=0
           p.object_id=-1
           u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
           u.exp=u.exp+tu[0]
           u.food=u.food+tu[1]
           return dict(id=1)
        except InvalidRequestError:
           return dict(id=0)
    @expose('json')
    def finish_building(self,user_id,city_id,grid_id):
        try:
           p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
           tu=increasebuild[p.ground_id]
           p.producttime=0
           u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
           u.exp=u.exp+tu[0]
           p.finish=1
           #u.population=u.population+tu[1]
           read(city_id)
           return dict(id=1)
        except InvalidRequestError:
           return dict(id=0)
    @expose('json')
    def speedup(self,user_id,city_id,grid_id):
        try:
            caesars=1
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
            #c=int((p.producttime-ti)/3600.0+0.5)
            c=int((p.producttime+3600-1)/3600)
            
            #if p.ground_id==0:
            #    caesars=Plant_Price[p.object_id][2]
            #if p.ground_id>=1 and p.ground_id<=18:
                #if p.finish==0:
                    #caesars=Building_Price[p.ground_id][3]
                #else:
                    #caesars=houses[p.ground_id-1][4]
            #elif p.ground_id>18 and p.ground_id<=21:
                #if p.finish==0:
                 #   caesars=Building_Price[p.ground_id][3]
                #else:
                 #   if p.object_id>0:
                  #      caesars=soldie[p.object_id][3]
                   # else:
                    #    return dict(id=0)
            #elif p.ground_id>21:
             #   if p.finish==0:
              #      caesars=Building_Price[p.ground_id][3]
               # else:
                #    caesars=production[p.ground_id-22][3]
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            #if u.cae-caesars>=0:
             #   u.cae=u.cae-caesars
              #  p.producttime=1000
               # read(city_id)
                #return dict(id=1)
            #else:
             #  return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)

    @expose('json')
    def population(self,user_id,city_id,grid_id):
        try:
           p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
           num=houses[p.ground_id-1][0]
           food=houses[p.ground_id-1][1]
           ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
           
           u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
           if u.food-food>=0 and ti-p.producttime>houses[p.ground_id-1][3]:
               u.population=u.population+num
               p.producttime=ti
               u.exp=u.exp+houses[p.ground_id-1][2]
               read(city_id)
               return dict(id=1)
           else :
               return dict(f=u.food-food,id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def training(self,user_id,city_id,grid_id,sid):
        try:
           p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
           i=int(sid)
           #three=soldier[i]
           corn=soldie[i][0]
           foo=soldie[i][1]
           pop=soldie[i][2]
           u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
           if u.corn-corn>=0 and u.food-foo>=0 and u.population-pop>=0 and p.producttime==0:
               u.corn=u.corn-corn
               u.food=u.food-foo
               u.population=u.population-pop
               p.object_id=sid
               ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
               p.producttime=ti
               read(city_id)
               return dict(id=1)
           else:
               return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def soldier(self,user_id,city_id,grid_id):
        try:
           p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
           u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
           sid=p.object_id
           if int(sid)>=0 and int(sid)<9:
               u.infantry_num=u.infantry_num+soldie[int(sid)][2]
           if int(sid)>=9 and int(sid)<18:
               u.cavalry_num=u.cavalry_num+soldie[int(sid)][2]
           if int(sid)>=18 :
               u.scout_num=u.scout_num+soldie[int(sid)][2]
           u.exp=u.exp+soldiernum[int(sid)]
           p.producttime=0
           p.object_id=-1
           read(city_id)
           return dict(id=1)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def product(self,user_id,city_id,grid_id):
        try:
           p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
           u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
           ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
           if ti-p.producttime>=production[p.ground_id-22][3]:#time
               u.corn=u.corn+production[p.ground_id-22][0]
               u.exp=u.exp+production[p.ground_id-22][1]
               p.producttime=ti
               read(city_id)
               return dict(id=1)
           else:
               return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)

    @expose('json')
    def retlev(self,rrstring):
        try:
            dict0={}
            list1=rrstring.split(';')
            for string2 in list1 :
                list2=string2.split(',')
                oid=int(list2[0])
                ukind=int(list2[1])
                try:
                    u=DBSession.query(operationalData).filter_by(otherid=oid).filter_by(user_kind=ukind).one()
                    dict0[list2[0]]=dict(level=u.lev)
                except InvalidRequestError:
                    dict0[list2[0]]=dict(level=-1)
            return dict0
        except InvalidRequestError:
            return dict(idd=-1)               
    @expose('stchong.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')

    @expose('stchong.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('stchong.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(environment=request.environ)

    @expose('stchong.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(params=kw)

    @expose('stchong.templates.authentication')
    def auth(self):
        """Display some information about auth* on this application."""
        return dict(page='auth')

    @expose('stchong.templates.index')
    @require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('stchong.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('stchong.templates.login')
    def login(self, came_from=url('/')):
        """Start the user login."""
        login_counter = request.environ['repoze.who.logins']
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from='/'):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ['repoze.who.logins'] + 1
            redirect('/login', came_from=came_from, __logins=login_counter)
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=url('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
