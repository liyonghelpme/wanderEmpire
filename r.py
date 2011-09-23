# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, request, redirect,response
from pylons.i18n import ugettext as _, lazy_ugettext as l_
from pylons import response
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController
from repoze.what import predicates
from sqlalchemy.exceptions import InvalidRequestError
from sqlalchemy.exceptions import IntegrityError
from stchong.lib.base import BaseController
from stchong.model import mc,DBSession, taskbonus,metadata,operationalData,businessWrite,businessRead,warMap,Map,visitFriend,Ally,Victories,Gift,Occupation,Battle,News,Friend,Datesurprise,Datevisit,FriendRequest#,logfile
from stchong import model
from stchong.controllers.secure import SecureController
from datetime import datetime
from stchong.controllers.error import ErrorController
import time
import sys
import random
import logging
import StringIO
import hashlib
import copy
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
    
    global Plant_Price#农作物列表
    global beginTime#2011年1月1日0时0分常量
    global houses#民居生产列表
    global soldie#士兵列表
    global soldiernum#士兵经验
    global production#商业列表
    global read#read内部函数
    global mapKind#地图种类对应最大用户数列表
    global makeMap#内部函数，新建地图
    global insert#内部函数，增加warmap中num数
    global getMap#内部函数，获取类型为kind的有空位的地图
    global upd#内部函数，从旧地图升级到新地图
    global housebuild#民居建筑列表
    global resourcebuild#资源建筑物列表
    global milbuild#军事建筑物列表
    global businessbuild#商业建筑物列表
    global godbuild#神像建筑物列表
    global decorationbuild#装饰列表
    global specialgoods#内部函数，判断建筑物特殊物品是否得到满足
    global getGround_id#内部函数,返回建筑物id对应列表
    global stones#石头种类列表
    global woods#木头种类列表
    global expanding#扩地列表
    global EXPANDLEV#扩地最高等级
    global getbonus#内部函数，打怪奖励
    global loginBonus#内部函数，登录奖励
    global alphabet#特殊物品对应字母列表a-l
    global randombuilding#没有被使用，随机一级建筑物列表
    global present#没有被使用，内部函数
    global inornot#内部函数，判断整数是否在列表内
    global allyup#每个爵位等级默认初始拥有最多盟友数
    global NOBILITYUP#爵位最高等级0-6
    global INITIALSTR#没有被使用，初始化字符串
    global INITIALSTR2#正在使用，初始化字符串
    global loginbonuslist#登录奖励列表，连续登录奖励
    global timejudge #内部函数，判断时间是否相差一天function pan duan shifou duguo 0 dian 
    global giftstring #内部函数，返回用户相关礼物字符串 function giftstring
    global sg#内部函数，赠送特殊物品作为礼物
    global minusstateeli#内部函数，消除负面状态function eliminating minusstate
    global completereceive#内部函数，完成礼物赠予或收取
    global checkminusstate#内部函数，查询负面状态是否存在
    global monsterlist#怪物列表
    global returnSoldier#内部函数，返回士兵数量
    global returnsentouryoku#内部函数，返回城内战斗力
    global checkopdata#function,cache
    global deleteopdata#function,cache
    global returnscout#内部函数，返回侦察兵数量function,return scout num of user
    global defencepowerlist#每一级城堡防御力list of defence power of each nobility
    global allyhelp#内部函数返回盟友提供战力function ally help
    global getbonusbattle#内部函数，返回战斗奖励functionspecialgoods bonus for battle
    global warresult#内部函数，返回战争结果function  calculate result of battles
    global functionname#函数名列表list of function name
    global writelog#内部函数，写日志function write to log
    global calev#内部函数，计算爵位等级function castle lev up
    global addnews#内部函数，新闻function add news
    global opentreasurebox#内部函数，计算打开宝箱奖励function
    global nobilitybonuslist#爵位升级奖励
    global tasklist#任务列表
    #global newtask#内部函数，新任务
    global mktaskstr#内部函数，计算任务字符串
    global checkfriend#内部函数，检查是否在好友列表中
    global md5string#计算md5用string
    global judgemd5#内部函数，计算md5
    global CACHEOP#常量，cache调用次数。
    global addcache#内部函数，向cache中写入数据
    global replacecache#内部函数
    global cachewriteback#内部函数
    global callost#内部函数，计算损失
    global getexp#计算经验
    global getresource
    global warresult2
    global getbonusbattle2
    global defenceplist
    global appsecret
    global tasknew
    global tasknew3
    admin = AdminController(model, DBSession, config_type=TGAdminConfig)
    #housebuild：corn,food,resource(+:m -:s),快速升级cae,exp,time，特殊物品，解锁等级
    housebuild=[[500,10,0,0,3,600,None,1],[1400,30,0,5,8,1200,'a,1',1],[2800,0,70,7,15,2400,'a,2;b,3',1],[int(500*1.1),10,0,0,3,600,None,1],[int(1400*1.1),30,0,5,8,1200,'a,1',1],[int(2800*1.1),0,70,7,15,2400,'a,2;b,3',1],[int(500*1.2),10,0,0,3,600,None,1],[int(1400*1.2),30,0,5,8,1200,'a,1',1],[int(2800*1.2),0,70,7,15,2400,'a,2;b,3',1],[int(500*1.3),10,0,0,3,600,None,1],[int(1400*1.3),30,0,5,8,1200,'a,1',1],[int(2800*1.3),0,70,7,15,2400,'a,2;b,3',1],[1500,60,0,0,5,1800,None,5],[4800,120,0,6,13,4800,'b,2;c,2',5],[9000,0,100,8,24,9000,'c,2;d,3',5],[int(1500*1.1),60,0,0,5,1800,None,5],[int(4800*1.1),120,0,6,13,4800,'b,2;c,2',5],[int(9000*1.1),0,100,8,24,9000,'c,2;d,3',5],[int(1500*1.2),60,0,0,5,1800,None,5],[int(4800*1.2),120,0,6,13,4800,'b,2;c,2',5],[int(9000*1.2),0,100,8,24,9000,'c,2;d,3',5],[int(1500*1.3),60,0,0,5,1800,None,5],[int(4800*1.3),120,0,6,13,4800,'b,2;c,2',5],[int(9000*1.3),0,100,8,24,9000,'c,2;d,3',5],[7300,400,0,0,13,15840,None,10],[15000,0,150,8,21,24480,'f,2;g,2',10],[19000,0,-150,11,30,30600,'g,2;h,3',10],[int(7300*1.1),400,0,0,13,15840,None,10],[int(15000*1.1),0,150,8,21,24480,'f,2;g,2',10],[int(19000*1.1),0,-150,11,30,30600,'g,2;h,3',10],[int(7300*1.2),400,0,0,13,15840,None,10],[int(15000*1.2),0,150,8,21,24480,'f,2;g,2',10],[int(19000*1.2),0,-150,11,30,30600,'g,2;h,3',10],[int(7300*1.3),400,0,0,13,15840,None,10],[int(15000*1.3),0,150,8,21,24480,'f,2;g,2',10],[int(19000*1.3),0,-150,11,30,30600,'g,2;h,3',10],[3500,200,0,0,11,5400,None,15],[6600,0,120,7,25,18000,'d,2;e,2',15],[11000,0,-120,9,39,21240,'e,2;f,3',15],[int(3500*1.1),200,0,0,11,5400,None,15],[int(6600*1.1),0,120,7,25,18000,'d,2;e,2',15],[int(11000*1.1),0,-120,9,39,21240,'e,2;f,3',15],[int(3500*1.2),200,0,0,11,5400,None,15],[int(6600*1.2),0,120,7,25,18000,'d,2;e,2',15],[int(11000*1.2),0,-120,9,39,21240,'e,2;f,3',15],[int(3500*1.3),200,0,0,11,5400,None,15],[int(6600*1.3),0,120,7,25,18000,'d,2;e,2',15],[int(11000*1.3),0,-120,9,39,21240,'e,2;f,3',15],[10500,600,0,0,20,25200,None,20],[15500,0,200,9,32,36720,'h,2;i,2',20],[19500,0,-200,13,43,71640,'i,2;j,2',20],[int(10500*1.1),600,0,0,20,25200,None,20],[int(15500*1.1),0,200,9,32,36720,'h,2;i,2',20],[int(19500*1.1),0,-200,13,43,71640,'i,2;j,2',20],[int(10500*1.2),600,0,0,20,25200,None,20],[int(15500*1.2),0,200,9,32,36720,'h,2;i,2',20],[int(19500*1.2),0,-200,13,43,71640,'i,2;j,2',20],[int(10500*1.3),600,0,0,20,25200,None,20],[int(15500*1.3),0,200,9,32,36720,'h,2;i,2',20],[int(19500*1.3),0,-200,13,43,71640,'i,2;j,2',20],[-10,0,0,0,15,7560,None,5],[20000,0,300,20,25,15480,'b,2;c,2',5],[25000,0,-300,35,40,30600,'c,2;d,3',5],[int(-10*1.1),0,0,0,15,7560,None,5],[int(20000*1.1),0,300,20,25,15480,'b,2;c,2',5],[int(25000*1.1),0,-300,35,40,30600,'c,2;d,3',5],[int(-10*1.2),0,0,0,15,7560,None,5],[int(20000*1.2),0,300,20,25,15480,'b,2;c,2',5],[int(25000*1.2),0,-300,35,40,30600,'c,2;d,3',5],[int(-10*1.3),0,0,0,15,7560,None,5],[int(20000*1.3),0,300,20,25,15480,'b,2;c,2',5],[int(25000*1.3),0,-300,35,40,30600,'c,2;d,3',5]]#corn,food,resource(+:m -:s),cae,exp,time
    #resourcebuild：corn,food,labor_num,wood,exps，解锁等级
    resourcebuild=[[1000,0,80,0,5,0],[-10,0,0,0,15,10],[-20,0,0,0,40,20],[-30,0,0,0,70,30],[10000,600,120,0,20,10],[28500,1000,250,0,30,18]]#corn,food,labor_num,wood,exps
    #milbuild：corn,food,labor_num,resource,update(cae),exp,time，特殊物品，解锁等级
    milbuild=[[4000,130,100,0,0,5,3600,None,1],[9000,0,20,200,15,10,11520,'a,3',1],[20000,0,50,-200,22,20,22680,'b,3;c,4',1],[12000,320,130,0,0,15,7200,None,5],[25000,0,20,500,21,20,14760,'b,3',5],[50000,0,50,-500,30,35,28440,'c,3;d,4',5],[6000,300,150,0,0,7,10800,None,5],[12000,0,20,300,13,15,21600,'c,3',5],[25000,0,50,-300,19,30,32400,'d,3;e,4',5]]#corn,food,labor_num,resource,update(cae),exp,time
    #businessbuild：corn,food,labor,resource,update(cae),exp,time，特殊物品，解锁等级
    businessbuild=[[300,20,20,0,0,3,600,None,1],[500,30,5,0,6,7,1800,'a,1',1],[1100,0,0,70,8,11,3600,'a,2;b,3',1],[1200,45,40,0,0,5,3600,None,4],[1800,50,10,100,7,9,10740,'b,2;c,2',4],[3000,70,15,-100,9,14,15120,'c,2;d,3',4],[-5,0,0,0,0,15,5400,None,6],[5000,0,0,120,10,20,14400,'b,2;c,2',6],[7000,0,0,-120,15,25,23400,'c,2;d,3',6],[2000,80,50,0,0,7,19800,None,8],[3300,0,15,150,8,9,35270,'d,2;e,2',8],[4500,0,20,-150,10,11,46800,'e,2;f,3',8],[5000,100,70,0,0,9,8280,None,15],[7000,0,20,170,9,11,22320,'f,2;g,2',15],[13500,0,25,-170,11,13,28800,'g,2;h,3',15],[-10,0,0,0,0,25,20520,None,14],[9000,130,0,200,15,30,25200,'d,2;e,2',14],[11000,0,25,-200,20,35,33120,'e,2;f,3',14],[7200,130,90,0,0,20,21600,None,21],[11000,0,25,210,10,33,28800,'h,2;i,2',21],[19900,0,30,-210,12,45,36720,'i,2;j,3',21],[8000,170,110,0,0,29,30600,None,29],[13000,0,30,230,11,45,34200,'j,2;k,2',29],[21000,0,35,-230,13,61,46800,'k,2;l,3',29],[-15,0,0,0,0,35,25200,None,24],[13000,0,250,20,45,30240,'h,2;i,2',24],[17000,200,0,-250,25,60,46800,'i,2;j,3',24]]#corn,food,labor,resource,update(cae),exp,time
    #godbuild corn,food,升级cae,exp,人口上限populationupbound，时间
    godbuild=[[10000,500,0,50,250,7200],[10000,500,0,50,250,7200],[10000,500,0,50,250,7200],[10000,500,0,50,250,7200],[20000,1000,10,100,250,21600],[20000,1000,10,100,250,21600],[20000,1000,10,100,250,21600],[20000,1000,10,100,250,21600],[50000,1500,20,300,250,43200],[50000,1500,20,300,250,43200],[50000,1500,20,300,250,43200],[50000,1500,20,300,250,43200],[100000,2000,50,500,250,64800],[100000,2000,50,500,250,64800],[100000,2000,50,250,1000,64800],[100000,2000,50,250,1000,64800],[100000,2000,50,500,250,64800],[500000,2500,100,1000,250,86400],[500000,2500,100,1000,250,86400],[500000,2500,100,1000,250,86400],[500000,2500,100,1000,250,86400]]# corn,food,cae,exp,populationupbound
    #decorationbuild：cornorcae，人口上限，解锁等级
    decorationbuild=[[10,5,1],[20,5,1],[30,5,1],[50,5,4],[-1,50,5],[100,6,6],[100,6,6],[100,6,6],[100,6,6],[100,6,6],[100,6,6],[200,8,7],[-3,170,8],[400,15,9],[600,20,10],[800,25,11],[1000,30,12],[900,35,13],[8000,40,14],[2000,50,15],[-5,300,10],[1500,60,16],[1500,60,16],[1500,60,16],[1600,65,18],[1600,65,18],[1600,65,18],[1600,65,18],[-3,150,15],[-3,150,15],[-3,150,15],[-3,150,15],[1800,70,20],[1800,70,20],[1800,70,20],[2000,80,25],[2000,80,25],[2000,80,25],[-10,300,20]]#corn(or cae),populationupbound
    #农作物list：#corn,exp,food,time，解锁等级
    Plant_Price=[[50,1,20,600,1],[165,3,50,2700,1],[-1,10,120,3600,5],[700,7,150,9360,5],[1440,12,300,22680,7],[-10,30,430,14400,7],[203,5,45,1200,10],[400,9,70,2700,15],[-4,33,280,9000,10],[1210,15,200,11520,20],[3000,25,410,29160,25],[-15,60,650,25200,15]]#corn,food,cae
    beginTime=(2011,1,1,0,0,0,0,0,0)
    #人口招募 招募人口数population,消耗food,exp got,cae（不用） 
    houses=[[10,20,1,1800,1],[15,30,5,1800,1],[20,40,9,1800,1],[10,20,1,1800,1],[15,30,5,1800,1],[20,40,9,1800,1],[10,20,1,1800,1],[15,30,5,1800,1],[20,40,9,1800,1],[10,20,1,1800,1],[15,30,5,1800,1],[20,40,9,1800,1],[32,64,3,7560,1],[43,86,7,7560,1],[55,110,11,7560,1],[32,64,3,7560,1],[43,86,7,7560,1],[55,110,11,7560,1],[32,64,3,7560,1],[43,86,7,7560,1],[55,110,11,7560,1],[32,64,3,7560,1],[43,86,7,7560,1],[55,110,11,7560,1],[70,140,7,18720,2],[83,174,14,18720,2],[100,200,21,18720,2],[70,140,7,18720,2],[83,174,14,18720,2],[100,200,21,18720,2],[70,140,7,18720,2],[83,174,14,18720,2],[100,200,21,18720,2],[70,140,7,18720,2],[83,174,14,18720,2],[100,200,21,18720,2],[50,90,6,12600,2],[62,116,15,12600,3],[75,142,23,12600,3],[50,90,6,12600,2],[62,116,15,12600,3],[75,142,23,12600,3],[50,90,6,12600,2],[62,116,15,12600,3],[75,142,23,12600,3],[50,90,6,12600,2],[62,116,15,12600,3],[75,142,23,12600,3],[95,190,12,29880,3],[115,230,24,29800,3],[135,270,36,29800,3],[95,190,12,29880,3],[115,230,24,29800,3],[135,270,36,29800,3],[95,190,12,29880,3],[115,230,24,29800,3],[135,270,36,29800,3],[95,190,12,29880,3],[115,230,24,29800,3],[135,270,36,29800,3],[100,150,15,21600,4],[150,225,25,21600,4],[200,300,35,21600,4],[100,150,15,21600,4],[150,225,25,21600,4],[200,300,35,21600,4],[100,150,15,21600,4],[150,225,25,21600,4],[200,300,35,21600,4],[100,150,15,21600,4],[150,225,25,21600,4],[200,300,35,21600,4]]#population,food,exp got,cae 
    #士兵：corn,food,labor_num,cae（不要），时间
    soldie=[[750,90,30,3,7200],[2400,270,90,3,21600],[4800,540,180,3,43200],[1600,180,30,3,7200],[5000,540,30,3,21600],[10000,1080,180,3,43200],[2400,270,30,3,7200],[7500,810,90,3,21600],[15000,1620,180,3,43200],[2000,150,10,6,7200],[6300,450,30,6,21600],[12600,900,60,6,43200],[2600,300,10,6,7200],[7900,900,30,6,21600],[15800,1800,60,6,43200],[3300,450,10,6,7200],[10000,1350,30,6,21600],[20000,2700,60,6,43200],[150,10,2,9,7200],[500,30,6,9,21600],[1000,60,12,9,43200],[310,20,2,9,7200],[990,60,6,9,21600],[1980,120,12,9,43200],[480,30,2,9,7200],[1500,90,6,9,21600],[3000,180,12,9,43200]]#corn,food,labor_num,cae
    #士兵经验
    soldiernum=[5,10,15,15,25,35,30,45,60,10,15,20,30,40,50,60,75,90,3,6,9,9,14,19,18,28,38]#soldier exp
    #商业生产 产量，经验，cae（不要），时间
    production=[[100,1,1,600],[300,5,1,600],[500,9,1,600],[600,3,1,5400],[900,9,1,5400],[1200,16,1,5400],[800,10,2,1800],[1400,20,2,1800],[2100,30,2,1800],[1200,7,1,10440],[1800,11,1,10440],[2600,19,1,10440],[2300,12,2,21600],[3200,20,2,21600],[4500,29,2,21600],[2500,18,3,7200],[4400,28,3,7200],[6800,40,3,7200],[1400,15,2,14760],[2100,24,2,14760],[3100,34,2,14760],[3500,23,3,30600],[4400,34,3,30600],[5600,45,3,30600],[5000,30,12,26200],[7000,50,12,26200],[9000,70,12,26200]]#corn that the plant can produce for a cycle,production,exp,speedup cae 
    #扩地list 金钱，cae币
    expanding=[[10000,5,10],[50000,10,20],[100000,20,50],[500000,35,90],[1000000,55,140],[1500000,80,200],[2000000,110,330],[2500000,145,580],[3000000,185,740],[5000000,230,920]]#ing land corn,cae
    error = ErrorController()
    EXPANDLEV=10#最高等级 ，从0开始
    #不使用randombuilding
    randombuilding=[[1,1],[100,1],[103,5],[106,10],[109,15],[112,20],[300,1],[303,5],[309,10],[312,15],[318,20],[321,25],[500,1],[501,1],[502,1],[503,1],[505,1],[508,5],[509,5],[510,5],[511,5],[512,5],[513,5],[514,7],[515,8],[516,9],[519,13],[520,14],[521,15],[522,16],[523,17],[525,19],[526,19],[527,19],[528,19],[529,20],[530,20],[531,20],[536,22],[537,22],[538,22],[539,23],[541,24]]#building id, lev
    #各爵位地图用户数
    mapKind=[8,32,72,128,200,512,800]
    #woods product cost(corn or cae),exp,gain,time，解锁等级
    woods=[[600,5,20,4320,7],[3600,15,50,21600,10],[-4,20,70,6480,7],[1000,10,40,5400,15],[6000,20,80,25200,20],[-8,50,120,9000,7]]#woods product cost(corn or cae),exp,gain,time
    #stones product cost(corn or cae),exp,gain,time，解锁等级
    stones=[[1200,10,20,4320,10],[7200,20,50,21600,15],[-5,30,70,6480,10],[2000,15,40,5400,20],[12000,25,80,25200,25],[-10,65,120,9000,10]]#stones product cost(corn or cae),exp,gain,time
    alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n']
    allyup=[1,2,3,4,5,6,7]
    loginbonuslist=[3000,5000,8000,12000,-2]#loginbonus
    #怪兽list 战斗力，经验，corn，随机物品数量，损失战斗力
    monsterlist=[20,30,41,25,37,49,28,42,56,33,49,65,40,58,77,50,75,100,42,65,90,51,74,104,60,90,120,73,109,145,80,120,160,100,150,200]#50,60,90,100,40,50,100,110,180,200]
    #monsterlist=[[50,10,1700,1,28],[100,30,3100,1,55],[150,50,4600,2,83],[200,80,6000,2,110],[300,110,8900,2,165],[500,150,15000,3,275],[1000,200,30000,3,550]]
    INITIALSTR="0,782,0,0,1;501,818,-1,0,1;516,824,-1,0,1;525,825,-1,0,1;501,858,-1,0,1;534,859,-1,0,1;100,863,-1,0,1;517,864,-1,0,1;526,865,-1,0,1;501,895,-1,0,1;501,896,-1,0,1;501,897,-1,0,1;501,898,-1,0,1;501,899,-1,0,1;501,900,-1,0,1;501,901,-1,0,1;501,902,-1,0,1;501,903,-1,0,1;501,904,-1,0,1;501,905,-1,0,1;501,906,-1,0,1;501,938,-1,0,1;501,978,-1,0,1;300,980,-1,1,1;1,983,-1,0,1;1,985,1,1,1;200,857,-1,"
    INITIALSTR2="0,455,0,0,1;503,491,-1,0,1;503,527,-1,0,1;503,531,-1,0,1;503,528,-1,0,1;503,567,-1,0,1;520,568,-1,0,1;503,571,-1,0,1;503,606,-1,0,1;503,607,-1,0,1;503,608,-1,0,1;503,609,-1,0,1;503,610,-1,0,1;503,611,-1,0,1;503,612,-1,0,1;503,613,-1,0,1;503,614,-1,0,1;503,615,-1,0,1;503,616,-1,0,1;530,646,-1,0,1;503,651,-1,0,1;1,688,-1,0,1;503,691,-1,0,1;503,731,-1,0,1;503,771,-1,0,1;200,566,-1,"
    NOBILITYUP=6 
    #defencepower,corn,food,wood,stone,cae
    defencepowerlist=[[50,10000,500,0,0,5],[100,20000,1000,0,0,5],[200,50000,0,500,0,20],[500,150000,0,500,500,50],[700,200000,0,1000,1000,70],[1000,250000,0,1500,1500,100],[5000,1000000,0,5000,5000,500]]#defencepower,corn,food,wood,stone,cae
    #defencepower,cae,food,stone,wood
    defenceplist=[[100,5,10,0,0],[300,13,10,0,0],[500,21,0,0,5],[700,29,0,0,5],[1000,42,0,5,0],[3000,110,0,5,0],[5000,188,0,5,0]]
    functionname=['logsign','retlev','build','planting','harvest']
    #corn,food,wood,stone
    nobilitybonuslist=[[1000,100,10,0],[5000,500,50,0],[10000,1000,100,0],[50000,5000,0,500],[100000,10000,0,1000],[500000,50000,0,5000]]
    md5string='0800717193'
    log=logging.getLogger('root')
    CACHEOP=10#调用10次checkopdata
    appsecret='FA6AMZKT77L4e4bc0a6'
    #任务列表
    tasklist=[[['查看帮助文档','不耻下问是良好美德，点击Menu键（或设置图标）查看帮助文档~','查看帮助文档 0/1',100,5,'0,0'],['种植粮食','地主家也没有余粮了，伤不起呀！快去种点啥吧，，','开垦农田 0/1;种植胡萝卜 0/6',300,10,'1,1!0$1','2,1!0$6'],['店铺收税','咱也是地主啦！快去店铺收税吧','普通面包房收税 0/250',100,5,'2,100!0$250']]]
    @expose('json')
    def share(self,uid):
        u=checkopdata(uid)
        u.corn=u.corn+100
        replacecache(uid,u)
        return dict(id=1)
    def judgemd5(string,md5s):
        src=string+md5string
        md5=(hashlib.md5(src).hexdigest().upper())
        if md5==md5s:
            return True
        else:
            return False
    @expose('json')
    def completepay(self,uid,tid,papapas,signature):
        u=checkopdata(uid)
        if u.tid=='-1':
            s=hashlib.md5(u.otherid+'-'+tid+'-'+appsecret).hexdigest()
            if s==signature:
                u.paytime=-1
                if int(papapas)==300:
                    u.cae=u.cae+int(int(papapas)/100)
                elif int(papapas)==1000:
                    u.cae=u.cae+11
                elif int(papapas)==2500:
                    u.cae=u.cae+30
                elif int(papapas)==5000:
                    u.cae=u.cae+65
                elif int(papapas)==10000:
                    u.cae=u.cae+140
                else:
                    u.cae=u.cae+int(int(papapas)/100)
                replacecache(uid,u) 
                return dict(id=1)
            else:
                return dict(id=0)
        else:
            if tid!=u.tid:
                return dict(id=0)
            u.tid='-1'
            u.paytime=-1
            u.cae=u.cae+int(int(papapas)/100)
            replacecache(uid,u)
            return dict(id=1)
    #######payment
    @expose()
    def payment(self,tid,uid,papapas,signature,time):
        try:
            uu=DBSession.query(operationalData).filter_by(otherid=uid).filter_by(user_kind=0).one()
            DBSession.commit()
            u=checkopdata(uu.userid)
            s=hashlib.md5(tid+'-'+uid+'-'+papapas+'-'+appsecret).hexdigest() 
            if s==signature:
                #u.tid=tid
                #u.paytime=time
                #u.cae=u.cae+int(int(papapas)/100)
                replacecache(u.userid,u)
                return '1'
            else:
                return '0'
        except:
            return '0'
    ###########iphone 邀请好友相关
    @expose('json')
    def sethead(self,hid,uid):
        u=checkopdata(uid)
        u.hid=int(hid)
        replacecache(uid,u)
        return dict(id=1)
    @expose('json')
    def sendinvite(self,uid,invitestring):
        try:
            uu=DBSession.query(operationalData).filter_by(userid=int(invitestring)).one()
            DBSession.commit()
            u=checkopdata(uu.userid)
            ub=checkopdata(uid)
            if u.invite==1 or ub.invited==1:
                return dict(id=0)
            ub.invited=1
            u.invite=1
            u.inviteid=ub.userid
            u.cae=u.cae+3
            try:
                f=DBSession.query(Friend).filter_by(uid=uid).filter_by(fotherid=fotherid).one()            
                DBSession.commit()
            except:
                nf=Friend(uid=uid,fotherid=u.otherid)
                DBSession.add(nf)
                DBSession.commit()
                nf2=Friend(uid=u.userid,fotherid=ub.otherid)
                DBSession.add(nf2)
                DBSession.commit()
            replacecache(u.userid,u)
            replacecache(uid,ub)
            return dict(id=1)
        except:
            return dict(id=0)
    @expose('json')
    def invitefriend(self,uid,fid):
        uid=int(uid)
        fid=int(fid)
        try:
            #uf=DBSession.query(operationalData).filter_by(userid=fid).one()
            #u=DBSession.query(operationalData).filter_by(userid=uid).one()
            uf=checkopdata(fid)#cache
            u=checkopdata(uid)#cache
            istring=''
            istring=u.empirename+','+str(u.lev)+','+str(u.nobility)
            if uf.invitestring=='' or uf.invitestring==None:
                uf.invitestring=istring
            else:
                uf.invitestring=uf.invitestring+';'+istring
            replacecache(fid,uf)#cache
            #replacecache(uid,u)
            return 2
        except:
            return dict(id=0)
    @expose('json')
    def acceptfriend(self,uid,fotherid,user_kind):
        uid=int(uid)
        user_kind=int(user_kind)
        try:
            f=DBSession.query(Friend).filter_by(uid=uid).filter_by(fotherid=fotherid).one()
            return dict(id=0)
        except InvalidRequestError:
            nf=Friend(uid=uid,fotherid=fotherid)
            DBSession.add(nf)
            uf1=DBSession.query(operationalData).filter_by(otherid=fotherid).filter_by(user_kind=1).one()
            uf=checkopdata(uf1.userid)#cache
            u=checkopdata(uid)#cache
            #u=DBSession.query(operationalData).filter_by(userid=uid).one()
            nf2=Friend(uid=uf.userid,fotherid=u.otherid)
            try:
                fr=DBSession.query(FriendRequest).filter_by(sendid=fotherid).filter_by(receiveid=u.otherid).one()
                fr.delete()
            except:
                x=1
            DBSession.add(nf2)
            return dict(id=1) 
    @expose('json')
    def refusefriend(self,uid,fotherid,user_kind):
        uid=int(uid)
        user_kind=int(user_kind)
        try:
            fr=DBSession.query(FriendRequest).filter_by(sendid=fotherid).filter_by(receiveid=u.otherid).one()
            fr.delete()
            return dict(id=1)
        except:
            x=1
            return dict(id=1)            
    @expose('json')
    def makefriend(self,uid,fotherid,user_kind,message):
        uid=int(uid)
        user_kind=int(user_kind)
        u=checkopdata(uid)
        nfr=RequestFriend(sendid=u.otherid,receiveid=fotherid,message=message)
        DBSession.add(nfr)
        return dict(id=1)
    @expose('json')
    def returnrequest(self,uid):
        u=checkopdata(uid)
        rlist=[]
        d=DBSession.query(FriendRequest).filter_by(receiveid=u.otherid)
        
        for x in d:
            u=DBSession.query(operationalData).filter_by(otherid=x.otherid).filter_by(user_kind=1).one()
            rlist.append([x.sendid,x.message,x.hid,x.empirename])
        return dict(requestlist=rlist)
    @expose('json')
    def returnfriendlist(self,uid):
        uid=int(uid)
        friendlist=[]
        try:
            fset=DBSession.query(Friend).filter_by(uid=uid)
            for n in fset:
                u=DBSession.query(operationalData).filter_by(otherid=n.fotherid).filter_by(user_kind=1).one()
                friendlist.append([n.fotherid,u.empirename,u.hid])
                
            return dict(friendlist=friendlist)
        except:
            return dict(id=0)
    def checkfriend(uid,fotherid):
        uid=int(uid)
        try:
            fs=DBSession.query(Friend).filter_by(uid=uid)
            for f in fs:
                if f.fotherid==fotherid:
                    return False
            return True
        except:
            return True
    @expose('json')
    def refreshfriend(self,uid,page):
        uid=int(uid)
        userlist=[]
        nl=[]
        num=5
        x=0 
        page=int(page)  
        friendlist=[]     
        try:
            userset=DBSession.query(operationalData).filter_by(user_kind=1).order_by(operationalData.userid)#是否只能要求iphone版好友？
            for nn in userset:
                n=checkopdata(nn.userid)#cache
                if checkfriend(uid,n.otherid)==True:
                    if n.userid!=uid:
                        ntemp=[n.otherid,n.userid,n.empirename,n.lev,n.nobility,n.hid]
                        nl.append(ntemp)    
            if len(nl)==0 or nl==None :
                return dict(id=0)
            if len(nl)-1<page*num:
                return dict(id=0)
            l1=0
            if len(nl)>(page+1)*num:
                l1=(page+1)*num+1
            else:
                l1=len(nl)
            i=page*num
            while i<l1:               
                friendlist.append(znl[i])
                i=i+1
            #return dict(id=1)
            return dict(refreshfriend=friendlist)
                
        except InvalidRequestError:
            return dict(id=0)         
    ###########任务相关
    @expose('json')
    def newtasktest(self,uid):#测试用，创建新任务
        u=None
        tl=None
        try:
            #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            u=checkopdata(uid)#cache
            #tl=newtask(u)
            replacecache(uid,u)#cache
            return dict(tasklist=tl)
        except:
            return dict(id=tl)
    @expose('json')
    def taskgivenup(self,uid):#放弃任务
        uid=int(uid)
        #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        u=checkopdata(uid)#cache
        #tasklist=newtask(u) 
        
        
        u.taskstring=''     
        u.tasknum=u.tasknum+1
        task=tasknew(uid)
        u.currenttask=task[1]
        u.taskstring='0'
        replacecache(uid,u)#cache
        if task[0]<0:
            return dict(task=-1)
        return dict(task=task[0])
    @expose('json')
    def taskaccomplished(self,uid):#任务完成
        uid=int(uid)
        #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        u=checkopdata(uid)#cache
        if u.currenttask==None or u.currenttask=='' or int(u.currenttask)<0 or int(u.currenttask)>len(taskbonus)-1:
            return dict(id=0)
        u.corn=u.corn+taskbonus[int(u.currenttask)][1][0]
        u.exp=u.exp+taskbonus[int(u.currenttask)][1][1]  
        t=tasknew(uid)   
        task=t[0]
        t2=t[1]
        u.taskstring='' 
        u.currenttask=t2   
        u.taskstring='0'
        #tasklist1=newtask(u)
        replacecache(uid,u)#cache
        if task<0:
            task=-1
        return dict(task=task,tid=t2) 
    @expose('json')
    def taskstep(self,uid,taskstring):#任务中间步骤完成保存
        uid=int(uid)
        #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        u=checkopdata(uid)#cache
        u.taskstring=taskstring
        replacecache(uid,u)#cache
        return dict(id=1)
    @expose('json')
    def tasknew2(self,uid):
        u=checkopdata(uid)
        if u.currenttask=='-1' or u.currenttask=='':
            u.currenttask=str(0)
            u.taskstring='0'
            replacecache(uid,u)
            return [taskbonus[0][0],0]
        else:
            if int(u.currenttask)>=len(taskbonus):
                return -1
            else:
                if int(u.currenttask)<0:
                    u.currenttask=str(-int(u.currenttask))
                ct=int(u.currenttask)
                if taskbonus[ct+1][2]>u.lev:
                    u.currenttask=str(-int(u.currenttask))
                    return dict(id=u.currenttask)
                u.currenttask=str(ct+1)
                u.taskstring='0'
                replacecache(uid,u)
                return dict(ct=ct,t=u.currenttask,tid=taskbonus[ct+1][0])    
    def tasknew(uid):
        u=checkopdata(uid)
        if u.currenttask=='-1' or u.currenttask=='':
            u.currenttask=str(0)
            u.taskstring='0'
            replacecache(uid,u)
            return [taskbonus[0][0],0]
        else:
            if int(u.currenttask)>=len(taskbonus)-1 or int(u.currenttask)<=(-len(taskbonus)+1):
                u.currenttask=str(-int(u.currenttask))
                u.taskstring=''
                replacecache(uid,u)
                return [-1,u.currenttask]
            else:
                if int(u.currenttask)<0:
                    u.currenttask=str(-int(u.currenttask))
                ct=int(u.currenttask)
                if taskbonus[ct+1][2]>u.lev:
                    u.currenttask=str(-int(u.currenttask))
                    replacecache(uid,u)
                    return [-1,u.currenttask]
                u.currenttask=str(int(u.currenttask)+1)
                u.taskstring='0'
                replacecache(uid,u)
                return [taskbonus[ct+1][0],u.currenttask]
    def tasknew3(u):
        #u=checkopdata(uid)
        if u.currenttask=='-1' or u.currenttask=='':
            u.currenttask=str(0)
            u.taskstring='0'
            replacecache(uid,u)
            return [taskbonus[0][0],0]
        else:
            if int(u.currenttask)>=len(taskbonus)-1 or int(u.currenttask)<=(-len(taskbonus)+1):
                u.currenttask=str(-int(u.currenttask))
                u.taskstring=''
                replacecache(u.userid,u)
                return [-1,u.currenttask]
            else:
                if int(u.currenttask)<0:
                    u.currenttask=str(-int(u.currenttask))
                ct=int(u.currenttask)
                if taskbonus[ct+1][2]>u.lev:
                    u.currenttask=str(-int(u.currenttask))
                    replacecache(u.userid,u)
                    return [-1,u.currenttask]
                u.currenttask=str(int(u.currenttask)+1)
                u.taskstring='0'
                replacecache(u.userid,u)
                return [taskbonus[ct+1][0],u.currenttask]
    @expose('json')
    def newtask(self,uid,taskid):
        u=checkopdata(uid)
        u.currenttask=taskid#差taskstring
        return dict(id=1)  
    #def newtask(u):#内部函数，创建新任务
        #tl=[]
        #if u.tasknum==0:
        #    u.currenttask='3,0'
        #    taskstring=mktaskstr(3,0)
        #    if taskstring=='':
        #        return dict(id=tl)
         #   u.taskstring=taskstring
         #   u.tasknum=1
         #   return tasklist[0][0]
       # else:
         #   taskl=u.currenttask.split(',')
         #   tasklev=int(taskl[0])
          #  tasknum=int(taskl[1])
         #   if tasknum==len(tasklist[tasklev-3])-1:
         #       if u.lev<tasklev+1:#当用户的级数小于当前将要选择的用户的级数，返回空list
          #          return tl
           #     if tasklev-2==len(tasklist):
           #         return tl                
           #     taskstring=mktaskstr(tasklev+1,0)
           #     if taskstring=='':
            #        return tl
           #     u.taskstring=taskstring
           #     u.currenttask=str(tasklev+1)+','+'0'                
           #     return tasklist[tasklev-2][0]#-3+1
           # else:
            #    taskstring=mktaskstr(tasklev,tasknum+1)
            #    if taskstring=='':
            #        return tl
            #    u.taskstring=taskstring
            #    u.currenttask=str(tasklev)+','+str(tasknum+1)
             #   return tasklist[tasklev-3][tasknum+1]         
    def mktaskstr(lev,num):#内部函数，任务字符串
        if lev-3>=len(tasklist)or num>=len(tasklist[lev-3]):
            return ''
        taskstring=tasklist[lev-3][num][0]+';'+str(tasklist[lev-3][num][3])+';'+str(tasklist[lev-3][num][4])
        i=5
        k=len(tasklist[lev-3][num])
        while i<k:
            taskstring=taskstring+';'+tasklist[lev-3][num][i]
            i=i+1
        return taskstring
    ###########################
    @expose(content_type="image/png")
    def returnfile(self,name):#客户端下载请求函数，图片名称不能含有‘.'字符，返回图片名称为输入参数name值
        try:
            openfile=open(name,'r')
            rd=openfile.read()
            openfile.close()
            theFile = StringIO.StringIO(rd)       
            response.headers['Content-Type']  = 'image/png'
            response.headers['Content-Disposition'] = 'attachment; filename=name'
            tmp=theFile.getvalue()
            theFile.close()
            return tmp
        except:
            openfile=open('a','r')#如果没有查到图片，返回图片'a'
            rd=openfile.read()
            openfile.close()
            theFile = StringIO.StringIO(rd)       
            response.headers['Content-Type']  = 'image/png'
            response.headers['Content-Disposition'] = 'attachment; filename='+name
            tmp=theFile.getvalue()
            theFile.close()
            return tmp
    @expose(content_type="text/plain")
    def updatescript(self,name):
        try:
            name1='script/'+name
            openfile=open(name1,'r')
            rd=openfile.read()
            openfile.close()
            theFile = StringIO.StringIO(rd)       
            response.headers['Content-Type']  = 'text/plain'
            response.headers['Content-Disposition'] = 'attachment; filename='+name
            tmp=theFile.getvalue()
            theFile.close()
            return tmp
        except:
            openfile=open('a','r')#如果没有查到图片，返回图片'a'
            rd=openfile.read()
            openfile.close()
            theFile = StringIO.StringIO(rd)       
            response.headers['Content-Type']  = 'image/png'
            response.headers['Content-Disposition'] = 'attachment; filename='+name
            tmp=theFile.getvalue()
            theFile.close()
            return tmp
            


    def writelog(beginend,num,state):#beginend=0：#调用开始，beginend=1，调用结束 num：函数名称list,functionname下标，state：状态字符串
        strl=''
        timestr=str(int(time.mktime(time.localtime())-time.mktime(beginTime)))
        if beginend==0:
            strl=timestr+',begin,'+functionname[num]+state+'\n'
            logfile.write(strl)
            logfile.flush()
        else:
            strl=timestr+',end,'+functionname[num]+state+'\n'
            logfile.write(strl)
            logfile.flush()            
            
    #cache related 与缓存相关测试函数
    @expose('json')
    def gameexit(self,uid):
        cachewriteback(uid)
        deletecache(uid)
    @expose('json')
    def deletecache(self,uid):
        deleteopdata(uid)
    @expose('json')
    def testwriteback(self,uid):
        ucache=mc.get(str(uid))
        if ucache!=None:
            uc=ucache[0]
            um=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            um=copy.deepcopy(uc)
            return dict(id=uc.invitestring,u=um.invitestring)
        else:
            return dict(id=0)
    @expose('json')
    def testcache(self,uid):
        u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        addcache(uid,u)
    @expose('json')
    def getcache(self,uid):
        uc=mc.get(str(uid))
        if uc!=None:
            return dict(id=uc[0].userid,call=uc[1])
        else:
            return dict(id=0)
    @expose('json')
    def testwritecache(self,uid):
        u=checkopdata(uid)#cache
        u.invitestring='testcache'
        replacecache(uid,u)#重要
        
        return dict(string=u.invitestring)
    @expose('json')
    def writeback(self,uid):
        ucache=mc.get(str(uid))
        
        
        if ucache!=None:
            uc=ucache[0]
            um=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            um.userid=uc.userid
            um.labor_num=uc.labor_num
            um.population=uc.population
            um.exp=uc.exp
            um.corn=uc.corn
            um.cae=uc.cae
            um.nobility=uc.nobility
            um.subno=uc.subno
            um.infantry1_num=uc.infantry1_num
            um.cavalry1_num=uc.cavalry1_num
            um.scout1_num=uc.scout1_num
            um.person_god=uc.person_god
            um.person_god_lev=uc.person_god_lev
            um.wealth_god=uc.wealth_god
            um.wealth_god_lev=uc.wealth_god_lev
            um.food_god=uc.food_god
            um.food_god_lev=uc.food_god_lev
            um.war_god=uc.war_god
            um.war_god_lev=uc.war_god_lev
            um.user_kind=uc.user_kind
            um.otherid=uc.otherid
            um.lev=uc.lev
            um.empirename=uc.empirename
            um.food=uc.food
            um.populationupbound=uc.populationupbound
            um.wood=uc.wood
            um.stone=uc.stone
            um.specialgoods=uc.specialgoods
            um.treasurebox=uc.treasurebox
            um.treasurenum=uc.treasurenum
            um.landkind=uc.landkind
            um.visitnum=uc.visitnum
            um.allyupbound=uc.allyupbound
            um.allynum=uc.allynum
            um.infantry2_num=uc.infantry2_num
            um.cavalry2_num=uc.cavalry2_num
            um.scout3_num=uc.scout3_num
            um.scout2_num=uc.scout2_num
            um.infantry3_num=uc.infantry3_num
            um.cavalry3_num=uc.cavalry3_num
            um.loginnum=uc.loginnum
            um.minusstate=uc.minusstate
            um.monsterlist=uc.monsterlist
            um.monsterdefeat=uc.monsterdefeat
            um.rate=uc.rate
            um.allycancel=uc.allycancel
            um.defencepower=uc.defencepower
            um.battleresult=uc.battleresult
            um.nbattleresult=uc.nbattleresult
            um.wealthgodtime=uc.wealthgodtime
            um.foodgodtime=uc.foodgodtime
            um.wargodtime=uc.wargodtime
            um.popgodtime=uc.popgodtime
            um.newcomer=uc.newcomer
            um.castlelev=uc.castlelev
            um.infantrypower=uc.infantrypower
            um.cavalrypower=uc.cavalrypower
            um.currenttask=uc.currenttask
            um.taskstring=uc.taskstring
            um.tasknum=uc.tasknum
            um.invitestring=uc.invitestring
            um.signtime=uc.signtime
            um.tid=uc.tid
            um.paytime=uc.paytime
            um.hid=uc.hid
            um.monstertime=uc.monstertime
            um.invite=uc.invite
            um.invited=uc.invited
            um.inviteid=uc.inviteid
            um.monster=uc.monster
            um.monlost=uc.monlost
            um.monfood=um.monfood
            return dict(id=1)
        else:
            return dict(id=0)
    def addcache(uid,u):
        uli=[u,0]
        mc.add(str(uid),uli)
    def checkopdata(uid):
        ul=mc.get(str(uid))
        #if ul!=None and ul[1]>=CACHEOP:
        #    cachewriteback(uid)#将cache中内容写回数据库
        #    deleteopdata(uid)#删除cache中对应对象
        #    u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        #    uli=[u,0]
        #    mc.add(str(uid),uli)
        #    return uli[0]            
        if ul==None:
            u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            uli=[u,0]
            mc.add(str(uid),uli)
            return uli[0]
        ul[1]=ul[1]+1
        mc.replace(str(uid),ul)
        return ul[0]
    def replacecache(uid,u):#将新值写入cache，与checkopdata成对使用
        ul=mc.get(str(uid))
        if ul!=None:
            ul[0]=u
            mc.replace(str(uid),ul)
            cachewriteback(uid)
            return 1
        else:
            return 0
    def deleteopdata(uid):
        return mc.delete(str(uid),time=0) 
    def cachewriteback(uid):
        ucache=mc.get(str(uid))        
        if ucache!=None:
            uc=ucache[0]
            um=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            um.userid=uc.userid
            um.labor_num=uc.labor_num
            um.population=uc.population
            um.exp=uc.exp
            um.corn=uc.corn
            um.cae=uc.cae
            um.nobility=uc.nobility
            um.subno=uc.subno
            um.infantry1_num=uc.infantry1_num
            um.cavalry1_num=uc.cavalry1_num
            um.scout1_num=uc.scout1_num
            um.person_god=uc.person_god
            um.person_god_lev=uc.person_god_lev
            um.wealth_god=uc.wealth_god
            um.wealth_god_lev=uc.wealth_god_lev
            um.food_god=uc.food_god
            um.food_god_lev=uc.food_god_lev
            um.war_god=uc.war_god
            um.war_god_lev=uc.war_god_lev
            um.user_kind=uc.user_kind
            um.otherid=uc.otherid
            um.lev=uc.lev
            um.empirename=uc.empirename
            um.food=uc.food
            um.populationupbound=uc.populationupbound
            um.wood=uc.wood
            um.stone=uc.stone
            um.specialgoods=uc.specialgoods
            um.treasurebox=uc.treasurebox
            um.treasurenum=uc.treasurenum
            um.landkind=uc.landkind
            um.visitnum=uc.visitnum
            um.allyupbound=uc.allyupbound
            um.allynum=uc.allynum
            um.infantry2_num=uc.infantry2_num
            um.cavalry2_num=uc.cavalry2_num
            um.scout3_num=uc.scout3_num
            um.scout2_num=uc.scout2_num
            um.infantry3_num=uc.infantry3_num
            um.cavalry3_num=uc.cavalry3_num
            um.loginnum=uc.loginnum
            um.minusstate=uc.minusstate
            um.monsterlist=uc.monsterlist
            um.monsterdefeat=uc.monsterdefeat
            um.rate=uc.rate
            um.allycancel=uc.allycancel
            um.defencepower=uc.defencepower
            um.battleresult=uc.battleresult
            um.nbattleresult=uc.nbattleresult
            um.wealthgodtime=uc.wealthgodtime
            um.foodgodtime=uc.foodgodtime
            um.wargodtime=uc.wargodtime
            um.popgodtime=uc.popgodtime
            um.newcomer=uc.newcomer
            um.castlelev=uc.castlelev
            um.infantrypower=uc.infantrypower
            um.cavalrypower=uc.cavalrypower
            um.currenttask=uc.currenttask
            um.taskstring=uc.taskstring
            um.tasknum=uc.tasknum
            um.invitestring=uc.invitestring
            um.paytime=uc.paytime
            um.tid=uc.tid
            um.hid=uc.hid
            um.monstertime=uc.monstertime
            um.invite=uc.invite
            uc.invited=uc.invited
            um.inviteid=uc.inviteid
            um.monster=uc.monster
            um.monlost=uc.monlost
            um.monfood=uc.monfood
            return 1
        else:
            return 0
    @expose('json')
    def memm(self):
        mc.add('a','b')
        value=mc.get('a')
        return dict(id=value)           
    #cache related
    
    @expose('json')#打分函数，在用户达到5级时调用，若用户没有评分，则在用户10级时再次调用，奖励5cae
    def rate(self,uid):
        #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        u=checkopdata(uid)#cache
        u.rate=1
        u.cae=u.cae+5
        replacecache(uid,u)#cache
        return dict(id=1)
    @expose('json')
    def levup(self,uid,lev):#operationalData:update,modify 用户升级时调用，uid为用户userid，lev为目标等级，10，30,60,100级时增加人口上限
        #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        u=checkopdata(uid)#cache
        u.corn=u.corn+(int(lev))*200#奖励corn 用户等级*20 
        u.lev=int(lev)
        tasklist=[]
        task=[-1,-1]
        #if u.currenttask=='' or u.currenttask==None:
        #    tasklist=newtask(u)
        #if u.lev==10:#等级为10时，人口上相增长1000
        #    u.populationupbound=u.populationupbound+1000
        #elif u.lev==30 or u.lev==60 or u.lev==100:#30,60，100级时增长2000
        #    u.populationupbound=u.populationupbound+2000
        if u.lev%10==0:
            u.populationupbound=u.populationupbound+250
            u.cae=u.cae+u.lev/10
        if u.currenttask!='-1' and int(u.currenttask)<0:
            task=tasknew3(u)
            #u.currenttask=task[0]
            u.taskstring='0'
        replacecache(uid,u)#cache
        task1=task[0]
        if task[0]<0:
            task1=-1
        if u.lev==10 and u.rate==0:#当用户到达10级且没有评分，则返回rate=0告知客户端。
            return dict(task=task1,tasklist=tasklist,rate=0,id=1)
        return dict(task=task1,id=1,tasklist=tasklist)        
    def timejudge(t):#判断当前时间和传入时间t相隔时间是否超过1天。在selectgift函数中被调用
        t2=int(time.mktime(time.localtime())-time.mktime(beginTime))
        s=t2/86400-t/86400
        if s<1 :#如果没有超过一天，返回false
            return False
        else:
            return True
    def loginBonus(u):#called when login;u is the user;operationalData:query->update 用户u的每日登录奖励
            time1=int(time.mktime(time.localtime())-time.mktime(beginTime))
            ds=DBSession.query(Datesurprise).filter_by(uid=u.userid).one()
            s=time1/86400-u.logintime/86400
            if u.newcomer<3:#当处在新手任务时，不给登录奖励
                return 0
            if s>1:#重新计算登录奖励
                u.loginnum=0
            if ds.datesurprise==0 :
                
                bonus=loginbonuslist[u.loginnum]#根据连续登录次数决定登录奖励
                if bonus>0 :
                    u.corn=u.corn+bonus
                else:
                    u.cae=u.cae-bonus
                if u.loginnum<4:
                    u.loginnum=u.loginnum+1
                else:
                    u.loginnum=0
                ds.datesurprise=1
                return bonus
            else:
                return 0 
    def inornot(num,li):#辅助函数，判断整数num是否在整数列表li中 in or not
        if len(li)==0:
            return False
        for i in li:
            if num==i :
                return True
        return False
    def present(u):#没有被使用，返回4中随机建筑
        index=random.randint(0,len(randombuilding)-1)
        i=0
        li=[]
        while i<4 :
            while randombuilding[index][1]>u.lev or inornot(index,li)==True:
                index=random.randint(0,len(randombuilding)-1)
            i=i+1
            li.append(randombuilding[index][0])
            index=random.randint(0,len(randombuilding)-1)
        return li

    def getbonus(u):#计算打败怪兽后的奖励，返回特殊物品字符串，在对外接口defeatmonster中被调用
        num1=[]
        restr=''
        num2=[]
        j=0
        nobility=u.nobility
        k=0
        if nobility>=0 and nobility<=1:
            k=1
        elif nobility>=2 and nobility<=4:
            k=2
        else:
            k=3
        while j<k:
            index=random.randint(0,11)
            if inornot(index,num2)==False:
                num2.append(index)
                j=j+1
        j=0
        strr=u.specialgoods.split(';')
        for x in strr:#添加特殊物品
            strx=x.split(',')
            x1=strx[0]
            y1=int(strx[1])
            while j<k:
                a1=alphabet[num2[j]]
                if a1==x1:
                    y1=y1+1
                    break
                j=j+1
            j=0
            num1.append([x1,y1])
        i=0
        s=''
        for n in num1:#拼接string
            if i==0:
                s=s+str(n[0])+','+str(n[1])
                i=1
            else:
                s=s+';'+str(n[0])+','+str(n[1])
        u.specialgoods=s        
        return s
    def getbonusbattle(u,k):#战斗胜利后的奖励，在warresult中被调用 type=1,got type=0,lost
        num1=[]
        restr=''
        num2=[]
        j=0
        nobility=u.nobility
        while j<k:
            index=random.randint(0,11)
            if inornot(index,num2)==False:
                num2.append(index)
                j=j+1
        j=0
        a1=random.choice(alphabet)
        strr=u.specialgoods.split(';')
        for x in strr:
            strx=x.split(',')
            x1=strx[0]
            y1=int(strx[1])
            while j<k:
                a1=alphabet[num2[j]]
                if a1==x1:
                    #if type==1:#got
                    y1=y1+1
                    #else:#lost
                    #    y1=y1-1
                    #    if y1<0:
                    #        y1=0
                    break
                j=j+1
            num1.append([x1,y1])
        i=0
        s=''
        for n in num1:
            if i==0:
                s=s+str(n[0])+','+str(n[1])
                i=1
            else:
                s=s+';'+str(n[0])+','+str(n[1])
        u.specialgoods=s
        i=0
        s=''
        for x in num2:
            if i==0:
                s=s+str(x)
                i=1
            else:
                s=s+'!'+str(x)
        return s        
    def getbonusbattle2(u,k,type):#战斗胜利后的奖励，在warresult中被调用 type=1,got type=0,lost
        num1=[]
        restr=''
        num2=[]
        j=0
        nobility=u.nobility
        while j<k:
            index=random.randint(0,11)
            if inornot(index,num2)==False:
                num2.append(index)
                j=j+1
        j=0
        a1=random.choice(alphabet)
        strr=u.specialgoods.split(';')
        for x in strr:
            strx=x.split(',')
            x1=strx[0]
            y1=int(strx[1])
            while j<k:
                a1=alphabet[num2[j]]
                if a1==x1:
                    if type==1:#got
                        y1=y1+1
                    else:#lost
                        y1=y1-1
                        if y1<0:
                            y1=0
                    break
                j=j+1
            num1.append([x1,y1])
        i=0
        s=''
        for n in num1:
            if i==0:
                s=s+str(n[0])+','+str(n[1])
                i=1
            else:
                s=s+';'+str(n[0])+','+str(n[1])
        u.specialgoods=s
        i=0
        s=''
        for x in num2:
            if i==0:
                s=s+str(x)
                i=1
            else:
                s=s+'!'+str(x)
        return s

    def returnSoldier(u):#不再使用，返回用户u各种士兵列表
        soldier=[]
        soldier.append(u.infantry1_num)
        soldier.append(u.infantry2_num)
        soldier.append(u.infantry3_num)
        soldier.append(u.cavalry1_num)
        soldier.append(u.cavalry2_num)
        soldier.append(u.cavalry3_num)
        return soldier
    def returnsentouryoku(u):#返回用户u总战斗力
        sentouryoku=[]
        power=u.infantrypower+u.cavalrypower
        return power     
    ##################怪兽相关    
    @expose('json')
    def monsterrefresh(self,userid,monsterstr):#对外接口，客户端刷新怪兽字符串，monsterstr
        #u=DBSession.query(operationalData).filter_by(userid=int(userid)).one()
        midlist=[]
        u=checkopdata(userid)#cache
        u.monsterlist=monsterstr
        #u.monsterdefeat=0
        u.monstertime=0
        if monsterstr=='' or monsterstr==None:
            return dict(id=0)
        monsterlist=monsterstr.split(';')
        for monster in monsterlist:
            mm=monster.split(',')
            midlist.append(int(mm[0]))
        i=0
        #max=midlist[0]
        #while i<len(midlist):
        #    if max<midlist[i]:
        #        max=midlist[i]
        #    i=i+1
        u.monster=u.monster+1 
        replacecache(userid,u)#cache
        
        return dict(id=1) 
    @expose('json')
    def delaymonster(self,uid):
        u=checkopdata(uid)#cache
        if u.cae-10<0:
            return dict(id=0)
        u.cae=u.cae-10
        u.monstertime=u.monstertime+86400
        replacecache(uid,u)
        return dict(id=1)
    @expose('json')
    def speedupmonster(self,uid,monsterstr): 
        
        u=checkopdata(uid)#cache
        if u.cae-10<0:
            
            return dict(id=0)
        u.cae=u.cae-10
        u.monsterlist=monsterstr
        #u.monsterdefeat=0
        u.monstertime=0
        u.monster=u.monster+1
        replacecache(uid,u)#cache
        
        return dict(id=1)     
    @expose('json')   
    def monstercomplete(self,uid):
        u=checkopdata(uid)
        refreshtime=random.randint(24,48)
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        u.monstertime=t+refreshtime*3600
        u.monsterlist=''
        u.exp=u.exp+int(u.monlost/2)
        u.corn=u.corn+u.monlost*30
        u.monlost=0
        #u.monster=-1
        replacecache(uid,u)
        return dict(monstertime=u.monstertime)
    @expose('json')
    def foodlost(self,uid):
        try:
            user=checkopdata(uid)
            foodlost=0
            if user.monfood==0 or user.monfood==None:
                fo=user.food
                foodlost=random.randint(int(fo/20),int(fo/10))
                user.food=user.food-foodlost
                user.monfood=1
                replacecache(uid,user)
            return dict(foodlost=foodlost)
        except :
            return dict(foodlost=0)
    @expose('json')
    def defeatmonster(self,uid,gridid):#对外接口，与怪兽进行战斗
        listsoldier=[]
        l2=[]
        mlist=[]
        mmlist=[]
        monsterid=-1
        mstr=''
        nobility=0
        yuzhi=3#随机值
        powerlost=0
        i=0
        s=''
        muu=0
        try:
            #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            u=checkopdata(uid)#cache
            monsterstr=u.monsterlist
            nobility=u.nobility
            if monsterstr=='' or monsterstr==None:
                return dict(id=0)
            mlist=monsterstr.split(';')
            for m in mlist:                
                ml=m.split(',')
                if len(ml)<2:
                    continue
                if gridid==ml[1]:
                    monsterid=int(ml[0])
                    break
            if monsterid==-1:
                return dict(id=0)
            listsoldier=returnSoldier(u)
            up=returnsentouryoku(u)#user power to defeat monster
            k=monsterlist[monsterid]
            #k=monsterlist[monsterid/3]
            #if monsterid%3==1:
            #    k=int(k*1.5)
            #elif monsterid%3==2:
            #    k=int(k*2)
            if up-k<0:
                return dict(id=0)
            else:
                #k1=k+5
                #k2=k-5
                #k=random.randint(k2,k1)
                #muu=int(k/2)
                
                #mu=random.randint(muu-3,muu+3)
                if u.lev<=8:
                    mu=int((k+2-1)/2)
                    u.exp=u.exp+(int(k+4-1)/4)
                elif u.lev>8 and u.lev<=15:
                    mu=int((3*k+2)/5)
                    u.exp=u.exp+int((k+2.5-1)/2.5)
                else:
                    mu=int((13*k-7)/20)
                    u.exp=u.exp+int((k+2-1)/2)
                powerlost=mu
                
                #u.exp=u.exp+int(mu/2)
                u.corn=u.corn+mu*30
                if monsterid%3==0:
                    t=1
                elif monsterid%3==1:
                    t=2
                else:
                    t=3
                s=getbonusbattle(u,t)
                mu=u.infantrypower-mu
                if mu>=0:
                    u.infantrypower=mu
                else:
                    u.infantrypower=0
                    u.cavalrypower=u.cavalrypower+mu
            i=0
            for m in mlist:
                ml=m.split(',')
                if ml[1]!=gridid:
                    if i==0:
                        mstr=mstr+m
                        i=1
                    else:
                        mstr=mstr+';'+m
            u.monsterlist=mstr
            #u.monsterdefeat=u.monsterdefeat+1
            card=0
            u.monlost=powerlost
            ##计算荣誉
            count=u.monsterdefeat.split(';')
            ct=[]
            if count!=None and len(count)>0:
                for c in count:
                    ct.append(int(c))
                if monsterid!=-1:
                    ct[int(monsterid/3)]=ct[int(monsterid/3)]+1
                if ct[int(monsterid/3)]==10:
                    card=1
                elif ct[int(monsterid/3)]==25:
                    card=2
                elif ct[int(monsterid/3)]==50:
                    card=3
                elif ct[int(monsterid/3)]==100:
                    card=4
                elif ct[int(monsterid/3)]==500:
                    card=5
                i=0
                ss=''
                for cc in ct:
                    if i==0:
                        ss=ss+str(cc)
                        i=1
                    else:
                        ss=ss+';'+str(cc)
                u.monsterdefeat=ss
             ##计算荣誉
            #u.monsterdefeat=ss       
            replacecache(uid,u)#cache
            return dict(id=1,cardid=card,powerlost=powerlost,infantrypower=u.infantrypower,cavalrypower=u.cavalrypower,specialgoods=s)  
        except InvalidRequestError:
            return dict(id=0)
    ##################
    ##################负面状态相关
    def checkminusstate(u,mstr):#str为表示负面状态的字符串，函数用于检查此城市的负面状态中是否含有str状态，在对外接口addminusstate中使用
        mlist=mstr.split(mstr)
        i=0
        s=''
        for m in mlist:
            if u.minusstate.find(m)!=-1:
                if i==0:
                    s=m
                    i=1
                else:
                    s=s+';'+m
        return s   
    def checkminusstate2(u,str):#str为表示负面状态的字符串，函数用于检查此城市的负面状态中是否含有str状态，在对外接口addminusstate中使用
        if u.minusstate.find(str)!=-1:
            return True
        else:
            return False
    @expose('json')
    def addminusstate(self,city_id,minusstr):#对外接口，在城市city_id的grid_id处，增加类型为type的异常状态，异常状态字符串在warmap数据库中
        #t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        war=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
        str2=minusstr
        strminus=minusstr#异常状态字符串，最后加', '是为了使用checkminusstate的方便
        #strminus=checkminusstate(war,minusstr)        
        if war.minusstate=='':
            war.minusstate=strminus
            return dict(id=1)
        else:
            if strminus!='':
                war.minusstate=war.minusstate+';'+strminus
                return dict(id=1)    
            else:
                return dict(id=0)
    @expose('json')
    def addminusstate2(self,city_id,type,grid_id):#对外接口，在城市city_id的grid_id处，增加类型为type的异常状态，异常状态字符串在warmap数据库中
        #t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        war=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
        str2=type+','+grid_id+', '
        strminus=type+','+grid_id#异常状态字符串，最后加', '是为了使用checkminusstate的方便        
        if war.minusstate=='':
            war.minusstate=strminus
            return dict(id=1)
        else:
            war.minusstate=war.minusstate+';'+strminus
            return dict(id=1)            
    @expose('json')
    def eliminusstate(self,uid,city_id,grid_id):#对外接口，用户uid对城市city_id grid_id处的负面状态进行消除操作
        stri=''
        i=0
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        try:
            #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            u=checkopdata(uid)
            war=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
            strminus=war.minusstate
            minuslist=strminus.split(';')
            if minuslist==None or len(minuslist)==0:
                return dict(id=10)
            else:
                for ml in minuslist :
                    if ml=='' or ml==None:
                        continue
                    mle=ml.split(',')
                    if len(mle)>=2:
                        if mle[1]==grid_id :
                            if mle[0]=='3':
                                return dict(id=0)
                            mle[0]='3'
                        stri=stri+mle[0]+','+mle[1]+';'
                war.minusstate=stri
                
                lev=int((u.lev-1)/10)
                u.corn=u.corn+50+lev*20
                u.exp=u.exp+1+lev*1
                #u.corn=u.corn+50
                if u.userid!=war.userid:#当不是打理自己的城堡时，记录新闻
                    addnews(war.userid,u.otherid,1,t,u.user_kind) 
                replacecache(uid,u)  
                return dict(id=1)
        except InvalidRequestError:
            return dict(id=20)         
    def minusstateeli(user,war,stri,t1):#自动消除负面状态，返回值mark，当mark=1时，只给经验。在harvest，finipop，production接口中使用
        mark=0
        if war.minusstate=='' or war.minusstate==None:
            return 0
        msl=war.minusstate.split(';')
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        ss=''
        sss=''
        day1=0
        i=0
        if msl==None:
            return 0
        for msle in msl :
            if msle=='' or msle==None:
                continue
            mslee=msle.split(',')
            if len(mslee)<2:
                continue
            day=t/86400-t1/86400
            if stri==mslee[1] and user.lev<10:

                if day>=3:
                    mark=1
                           
            elif stri==mslee[1] and user.lev>=10 and user.lev<20:
                if day>=5:
                    mark=1
                        
            elif stri==mslee[1]:
                if day>=7:
                    mark=1
            else:
                sss=sss+mslee[0]+','+mslee[1]+';'
                ss=ss+msle+';'            
        war.minusstate=ss
        return mark
    ################
    ################结盟相关                       
    @expose('json')
    def makeally(self,uid,fid):#对外接口，用户uid向fid结盟
        uid=int(uid)
        fid=int(fid)
        #u=DBSession.query(operationalData).filter_by(userid=uid).one()
        #f=DBSession.query(operationalData).filter_by(userid=fid).one()
        u=checkopdata(uid)#cache
        f=checkopdata(fid)#cache
        try:
            a1=DBSession.query(Ally).filter_by(uid=uid).filter_by(fid=fid).one()
            return dict(id=0)
        except InvalidRequestError:   
            if u.allynum < u.allyupbound:
                u.allynum=u.allynum+1
                newally=Ally(uid=uid,fid=fid)
                DBSession.add(newally)  
                replacecache(uid,u)#cache
                return dict(id=1)
            else:
                return dict(id=0) 
                            
    @expose('json')
    def cancelally(self,uid,fid):#对外接口，用户uid取消与fid用户的结盟关系
        uid=int(uid)
        fid=int(fid)
        #u=DBSession.query(operationalData).filter_by(userid=uid).one()
        u=checkopdata(uid)#cache
        try:
            u.allynum=u.allynum-1
            if u.allynum<0:
                u.allynum=0
            a1=DBSession.query(Ally).filter_by(uid=uid).filter_by(fid=fid).one()            
            u.corn=u.corn-5000*(u.nobility+1)
            if u.corn<0:
                u.corn=0
            DBSession.delete(a1)      
            replacecache(uid,u)#cache  
            return dict(id=1)
        except InvalidRequestError:
            return dict(id=0)                                  
    @expose('json')
    def addallyupbound(self,userid):#增加可结盟数上限
        try:
            userid=int(userid)
            #u=DBSession.query(operationalData).filter_by(userid=userid).one()
            u=checkopdata(userid)#cache
            if u.nobility>NOBILITYUP :
                return dict(id=0)
            sub=u.allyupbound-allyup[u.nobility]
            cae=5*(sub+1)+5
            if u.cae-cae>=0:
                u.cae=u.cae-cae
                u.allyupbound=u.allyupbound+1
                replacecache(userid,u)#cache
                return dict(id=1)
            else:
                return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    ################
    ################宝箱相关
    @expose('json')
    def newtbox(self,user_id,num):#对外接口，用户user_id,生成新宝箱，num为宝箱座位数
        try:
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            u.treasurenum=int(num)
            u.treasurebox=''
            replacecache(user_id,u)#cache
            return dict(id=1)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')#operationalData:query->update
    def helpopen(self,user_id,fuser_id):#对外接口，用户user_id帮助 用户fuser_id 打开宝箱
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        #u1=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
        #u2=DBSession.query(operationalData).filter_by(userid=int(fuser_id)).one()
        u1=checkopdata(user_id)#cache
        u2=checkopdata(fuser_id)#cache
        papayaid1=u1.otherid
        blist=[]
        if u2.treasurebox!='':
            s=(u2.treasurebox).split(';')
            length=len(s)
            if length<u2.treasurenum:
                u2.treasurebox=u2.treasurebox+';'+str(papayaid1)
                u1.corn=u1.corn+1000#user who helped his or her friend opening the treasurebox will get a 1000 corn bonus
                addnews(int(fuser_id),u1.otherid,4,t,u1.user_kind)
                replacecache(user_id,u1)#cache
                replacecache(fuser_id,u2)#cache
                return dict(id=1)
            else:
                return dict(id=0)
        else:
            u2.treasurebox=str(papayaid1)
            u1.corn=u1.corn+1000#user who helped his or her friend opening the treasurebox will get a 1000 corn bonus
            addnews(int(fuser_id),u1.otherid,4,t,u1.user_kind)
            replacecache(user_id,u1)#cache
            replacecache(fuser_id,u2)#cache            
            return dict(id=1)
    @expose('json')
    def selfopen(self,user_id):#用户使用cae币打开宝箱
        #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
        u=checkopdata(user_id)#cache
        if u.cae-1>=0:
            if u.treasurebox!='':
                s=(u.treasurebox).split(';')
                length=len(s)
                if length<u.treasurenum:
                    u.treasurebox=u.treasurebox+';'+str(-1)
                    u.cae=u.cae-1
                    replacecache(user_id,u)#cache
                    return dict(id=1)
                else:
                    return dict(id=0)
            else:
                u.treasurebox='-1'
                u.cae=u.cae-1
                replacecache(user_id,u)#cache
                return dict(id=1)
        else:
            return dict(id=0)
    @expose('json')
    def completeopen(self,user_id):#对外接口，完成打开宝箱，num为特殊物品列表
        #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
        try:
            u=checkopdata(user_id)#cache
            u.treasurenum=0
            u.treasurebox=''
            num=opentreasurebox(u)
            replacecache(user_id,u)#cache
            return dict(id=1,specialgoods=num)
        except:
            return dict(id=0)
    def opentreasurebox(u):#宝箱礼物 在对外接口completeopen中被调用，返回两种特殊物品
        num1=[]
        restr=''
        num2=[]
        j=0
        nobility=u.nobility
        k=2
        while j<k:
            index=random.randint(0,11)
            if inornot(index,num2)==False:
                num2.append(index)
                j=j+1
        j=0
        #a1=random.choice(alphabet)
        strr=u.specialgoods.split(';')
        for x in strr:
            strx=x.split(',')
            x1=strx[0]
            y1=int(strx[1])
            while j<k:
                a1=alphabet[num2[j]]
                #num2.append(x1)
                if a1==x1:
                    y1=y1+1
                    #num2.append(y1)
                    break
                j=j+1
            j=0
            num1.append([x1,y1])
        i=0
        s=''
        for n in num1:
            if i==0:
                s=s+str(n[0])+','+str(n[1])
                i=1
            else:
                s=s+';'+str(n[0])+','+str(n[1])
        u.specialgoods=s
        cornbonus=2000+u.lev*50
        u.corn=u.corn+cornbonus
        u.exp=u.exp+5+u.lev
        return num2        
    ###############
        
    def specialgoods(ground_id,stri,u):#判断建筑物的特殊物品要求是否得到满足 return true if special goods enough;operationalData:query->update
        stri='111'
        stru=u.specialgoods
        num1=[]
        num2=[]
        if stru==None:
            return True
        struset=stru.split(';')
        if struset!=None:
            for su in struset:
                suset=su.split(',')
                
                type=suset[0]
                ac=suset[1]
                num1.append([type,ac])
            if ground_id>=100 and ground_id<=199:
                stri=housebuild[ground_id-100][6]
            elif ground_id>=200 and ground_id<=299:
                stri=milbuild[ground_id-200][7]
            elif ground_id>=300 and ground_id<=399:
                stri=businessbuild[ground_id-300][7]
            else:
                return True
            if stri=='111':
                return True
            else:
                if stri==None:
                    return True
                strset=stri.split(';')
                for ss in strset:
                    ssset=ss.split(',')
                    num2.append([ssset[0],ssset[1]])
                for x in num2:
                    for y in num1:
                        if y[0]==x[0]:
                            if int(y[1])-int(x[1])>=0:
                                y[1]=str(int(y[1])-int(x[1]))
                            else:
                                return False
                strre=''
                mark=0
                for y in num1:
                    tempstr=y[0]+','+y[1]
                    if mark==0:
                        strre=strre+tempstr
                        mark=1
                    else:
                        strre=strre+';'+tempstr
                u.specialgoods=strre
                return True
        else:
            return True
    def getGround_id(ground_id):# return lis[]
        castle=[[-1,-1]]
        error=[[-2,-2]]
        if ground_id==0:
            return None#castle
        elif ground_id>=1 and ground_id<=99:#resource
            return resourcebuild[ground_id-1]
        elif ground_id>=100 and ground_id<=199:#house
            return housebuild[ground_id-100]
        elif ground_id>=200 and ground_id<=299:#military
            return milbuild[ground_id-200]
        elif ground_id>=300 and ground_id<=399:#business
            return businessbuild[ground_id-300]
        elif ground_id>=400 and ground_id<=499:#god
            return godbuild[ground_id-400]
        elif ground_id>=500 and ground_id<=699:#decoration
            return decorationbuild[ground_id-500]
        else:
            return None
    ###############赠送礼物相关        
    def sg(otherid,user_kind,sp):#赠送特殊物品作为礼物
        stri='111'        
        uu=DBSession.query(operationalData).filter_by(otherid=otherid).filter_by(user_kind=user_kind).one()#7.29 otherid改为varchar类型
        u=checkopdata(uu.userid)#cache
        stru=u.specialgoods
        num1=[]
        num2=[]
        sp1=alphabet[sp]
        if stru==None:
            return True
        struset=stru.split(';')
        if struset!=None:
            for su in struset:
                suset=su.split(',')
                
                type=suset[0]
                ac=suset[1]
                num1.append([type,ac])
            for y in num1:
                if y[0]==sp1:
                    y[1]=str(int(y[1])+1)
            strre=''
            mark=0
            for y in num1:
                tempstr=y[0]+','+y[1]
                if mark==0:
                    strre=strre+tempstr
                    mark=1
                else:
                    strre=strre+';'+tempstr
            u.specialgoods=strre
            replacecache(u.userid,u)#cache
            return strre
        else:
            return ''            
    @expose('json')
    def selectgift(self,uid,fid,specialgoods,askorgive):#对外接口，选择一种特殊物品作为礼物，0：赠送，1索要 operationalData:query;Gift:insert->update
        uid=int(uid)
        #u=DBSession.query(operationalData).filter_by(userid=uid).one()
        u=checkopdata(uid)#cache
        fid=int(fid)
        #f=DBSession.query(operationalData).filter_by(userid=fid).one()
        f=checkopdata(fid)
        upapayaid=u.otherid
        fpapayaid=f.otherid
        specialgoods=int(specialgoods)
        askorgive=int(askorgive)
        try:
            sgift=DBSession.query(Gift).filter_by(uid=upapayaid).filter_by(fid=fpapayaid).filter_by(ukind=u.user_kind).filter_by(fkind=f.user_kind).filter_by(askorgive=askorgive).one()
            #tt=sgift.time
            #return dict(id=timejudge(sgift.time))
            if timejudge(sgift.time)==True:
                
                t1=sgift.time
                sgift.time=int(time.mktime(time.localtime())-time.mktime(beginTime))
                sgift.present=specialgoods
                if askorgive==0:#2011.7.13 addnews
                    addnews(fid,u.otherid,2,sgift.time,u.user_kind)
                sgift.received=0
                return dict(id=1)
            else:
                #x=int(time.mktime(time.localtime())-time.mktime(beginTime))/86400-tt/86400
                return dict(id=0)
        except InvalidRequestError:
            ng=Gift(uid=upapayaid,fid=fpapayaid,askorgive=askorgive,present=specialgoods,fkind=f.user_kind,ukind=u.user_kind)
            DBSession.add(ng)
            c1=DBSession.query('LAST_INSERT_ID()')
            sgift=DBSession.query(Gift).filter_by(uid=upapayaid).filter_by(fid=fpapayaid).filter_by(askorgive=askorgive).one()
            sgift.time=int(time.mktime(time.localtime())-time.mktime(beginTime))
            if askorgive==0:#2011.7.13 addnews
                addnews(fid,u.otherid,2,sgift.time,u.user_kind)            
            return dict(id=1)
    def giftstring(uid):#从gift数据表中查到用户uid相关的礼物信息logsign中使用...fid,present,askorgive;Gift:query
        #uid=int(uid)
        s=''
        mark=0
        try:
            sgift=DBSession.query(Gift).filter_by(fid=uid)
            if sgift!=None:
                for sg in sgift:
                    if sg.received==0 :
                        if mark==0:
                            s=s+str(sg.uid)+','+str(sg.present)+','+str(sg.askorgive)
                            #sg.received=1
                            mark=1
                        else:
                            s=s+';'+str(sg.uid)+','+str(sg.present)+','+str(sg.askorgive)
                            #sg.received=1
            return s
        except InvalidRequestError:
            return '' 
    
    def completereceive(sg,gii):#Gift:update
        #for sg in sgift :
        if sg.uid==gii[0] and sg.present==int(gii[1]) and sg.askorgive==int(gii[2]) and sg.received==0:
            sg.received=1
            return 1
        return sg.uid
    @expose('json')
    def receivegift(self,uid,giftstr):#对外接口，接受礼物giftstr
        three=[]
        uid=int(uid)
        mark=0
        #u=DBSession.query(operationalData).filter_by(userid=uid).one()
        u=checkopdata(uid)#cache
        sgift=DBSession.query(Gift).filter_by(fid=u.otherid).all()
        s1=[]
        if giftstr!='' and giftstr!=None:
            gifts=giftstr.split(';')
            for gi in gifts :
                gii=gi.split(',')
                three.append(gii)
            for ss in sgift:
                for gii in three:
                    if int(gii[2])==0 :
                        if int(gii[1])>=0 and int(gii[1])<12 :                        
                            c=completereceive(ss,gii)
                            if c==1:
                                specialg=int(gii[1])
                                s1.append(sg(u.otherid,u.user_kind,specialg))
                                
                            else:
                                mark=c
                                
                                continue
                    else:
                        fid=int(gii[0])
                        if int(gii[1])>=0 and int(gii[1])<12 :
                            c=completereceive(ss,gii)
                            if c==1:
                                specialg=int(gii[1])
                                s1.append(sg(fid,u.user_kind,specialg))
                            else:
                                mark=c
                                continue
            replacecache(uid,u)
            return dict(id=1,mark=mark)
        else:
            return dict(id=0)  
    #################
    #################访问好友                  
    @expose('json')
    def getfriend(self,userid,otherid,user_kind):#对外接口，用户userid 访问由otherid+user_kind确定的好友 get friends page;operationalData:query->updatewarMap:query;businessRead:query;visitFriend:query->update
        userid=int(userid)
        friendid=-1
        u=None
        uu=None
        readstr=''
        lis=[]
        lis2=[]
        i=1
        city_id=0
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        city=None
        uw=None
        dv=None
        try:
            dv=DBSession.query(Datevisit).filter_by(uid=int(userid)).one()
            bonus=0
            #uu=DBSession.query(operationalData).filter_by(userid=userid).one()
            uu=checkopdata(userid)#cache
            u=DBSession.query(operationalData).filter_by(otherid=otherid).filter_by(user_kind=int(user_kind)).one()#7.29,otherid 
            uw=DBSession.query(warMap).filter_by(userid=u.userid).one()
            friendid=u.userid
            city=DBSession.query(warMap).filter_by(userid=u.userid).one()
            read=DBSession.query(businessRead).filter_by(city_id=city.city_id).one()
            readstr=read.layout
            #lis=present(u)
            #lis2=present(uu)
            visit=DBSession.query(visitFriend).filter_by(userid=userid).filter_by(friendid=friendid).one()
            
            if visit.visited==0:
                bonus=85+15*(dv.visitnum+1)
                uu.corn=uu.corn+85+15*(dv.visitnum+1)
                dv.visitnum=dv.visitnum+1
                uu.visitnum=dv.visitnum
                
                visit.visited=1
                i=0
            addnews(u.userid,uu.otherid,0,t,uu.user_kind)#2011.7.13:add news
            replacecache(userid,uu)#cache
            return dict(monsterdefeat=u.monsterdefeat,hid=u.hid,power=u.infantrypower+u.cavalrypower,casubno=u.subno,empirename=u.empirename,minusstr=uw.minusstate,allyupbound=u.allyupbound,frienduserid=u.userid,city_id=city.city_id,visited=i,corn=bonus,stri=readstr,friends=u.treasurebox,lev=u.lev,nobility=u.nobility,treasurenum=u.treasurenum,time=int(time.mktime(time.localtime())-time.mktime(beginTime)))
        except InvalidRequestError:
            newvisit=visitFriend(userid=userid,friendid=friendid)
            DBSession.add(newvisit)
            uu.corn=uu.corn+85+15*(dv.visitnum+1)
            dv.visitnum=dv.visitnum+1
            uu.visitnum=dv.visitnum+1
            
            addnews(u.userid,uu.otherid,0,t,uu.user_kind)#2011.7.13:add news
            replacecache(userid,uu)#cache
            return dict(monsterdefeat=u.monsterdefeat,hid=u.hid,power=u.infantrypower+u.cavalrypower,subno=u.subno,empirename=u.empirename,minusstr=uw.minusstate,frienduserid=u.userid,city_id=city.city_id,visited=0,corn=85+15*(dv.visitnum),stri=readstr,friends=u.treasurebox,lev=u.lev,nobility=u.nobility,treasurenum=u.treasurenum,time=int(time.mktime(time.localtime())-time.mktime(beginTime)))
    @expose('json')
    def sell(self,user_id,city_id,grid_id):#对外接口，卖建筑物sell building#operationalData:update;businessWrite:query->update
        try:
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            lis=getGround_id(p.ground_id)
            if lis==None:
                return dict(id=0)
            else:
                if p.ground_id>=1 and p.ground_id<=99:
                    u.labor_num=u.labor_num-lis[2]
                elif p.ground_id>=200 and p.ground_id<=299:
                    if p.ground_id%3==0:
                        u.labor_num=u.labor_num-lis[2]
                    elif p.ground_id%3==1:
                        lisx=getGround_id(p.ground_id-1)
                        u.labor_num=u.labor_num-lis[2]-lisx[2]
                    elif p.ground_id%==2:
                        lisx=getGround_id(p.ground_id-1)
                        lisy==getGround_id(p.ground_id-2)
                        u.labor_num=u.labor_num-lis[2]-lisx[2]-lisy[2]
                elif p.ground_id>=300 and p.ground_id<399:
                    if p.ground_id%3==0:
                        u.labor_num=u.labor_num-lis[2]
                    elif p.ground_id%3==1:
                        lisx=getGround_id(p.ground_id-1)
                        u.labor_num=u.labor_num-lis[2]-lisx[2]
                    elif p.ground_id%==2:
                        lisx=getGround_id(p.ground_id-1)
                        lisy==getGround_id(p.ground_id-2)
                        u.labor_num=u.labor_num-lis[2]-lisx[2]-lisy[2]
                elif p.ground_id>=400 and p.ground_id<499:
                    if p.ground_id==400 or p.ground_id==404 or p.ground_id==408 or p.ground_id==412 or p.ground_id==416:
                        u.food_god_lev=0
                    elif p.ground_id==401 or p.ground_id==405 or p.ground_id==409 or p.ground_id==413 or p.ground_id==417:
                        u.person_god_lev=0

                    elif p.ground_id==402 or p.ground_id==406 or p.ground_id==410 or p.ground_id==414 or p.ground_id==418:
                        u.wealth_god_lev=0
                    else:
                        u.war_god_lev=0
                else:
                    x=0     
                if p.ground_id>=400 and p.ground_id<=499 and int((p.ground_id-400)/4)==0:
                    u.populationupbound=u.populationupbound-250
                elif p.ground_id>=400 and p.ground_id<=499 and int((p.ground_id-400)/4)==1:
                    #if p.finish==0:
                    #    u.populationupbound=u.populationupbound-250
                    #else:
                    u.populationupbound=u.populationupbound-500
                elif p.ground_id>=400 and p.ground_id<=499 and int((p.ground_id-400)/4)==2:
                    #if p.finish==0:
                    #    u.populationupbound=u.populationupbound-500
                    #else:
                    u.populationupbound=u.populationupbound-750
                elif p.ground_id>=400 and p.ground_id<=499 and int((p.ground_id-400)/4)==3:
                    #if p.finish==0:
                    #    u.populationupbound=u.populationupbound-750
                    #else:
                    u.populationupbound=u.populationupbound-1000   
                elif p.ground_id>=400 and p.ground_id<=499 and int((p.ground_id-400)/4)==4:
                    #if p.finisht==0:
                    #    u.populationupbound=u.populationupbound-1000
                    #else:
                    u.populationupbound=u.populationupbound-1250    
                lis1=[]                 
                if lis[0]>0:
                    if p.ground_id>=1 and p.ground_id<=99:
                        u.corn=u.corn+lis[0]/4
                    elif p.ground_id>=500 and p.ground_id<=599:
                        u.corn=u.corn+lis[0]/4
                    elif p.ground_id>=400 and p.ground_id<=499:
                        if p.ground_id<=404:
                            u.corn=u.corn+2500
                        elif p.ground_id<=408:
                            u.corn=u.corn+5000
                        elif p.ground_id<=412:
                            u.corn=u.corn+10000
                        elif p.ground_id<=416:
                            u.corn=u.corn+20000
                        else:
                            u.corn=u.corn+40000
                    elif p.ground_id>=100 and p.ground_id<=199:    
                        if (p.ground_id-100)%3==0:
                        #x=x+lis[0]
                            u.corn=u.corn+lis[0]/4
                        elif (p.ground_id-100)%3==1:
                            lis1=getGround_id(p.ground_id-1)
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]/2
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*2
                        elif (p.ground_id-100)%3==2:
                            lis1=getGround_id(p.ground_id-2)  
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*4
                    elif p.ground_id>=200 and p.ground_id<=299:
                        if (p.ground_id-200)%3==0:
                        #x=x+lis[0]
                            u.corn=u.corn+lis[0]/4
                        elif (p.ground_id-200)%3==1:
                            lis1=getGround_id(p.ground_id-1)
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]/2
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*2
                        elif (p.ground_id-200)%3==2:
                            lis1=getGround_id(p.ground_id-2)  
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*4
                    elif p.ground_id>=300 and p.ground_id<=399:
                        if (p.ground_id-300)%3==0:
                        #x=x+lis[0]
                            u.corn=u.corn+lis[0]/4
                        elif (p.ground_id-300)%3==1:
                            lis1=getGround_id(p.ground_id-1)
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]/2
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*2
                        elif (p.ground_id-300)%3==2:
                            lis1=getGround_id(p.ground_id-2)  
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*4                                                                                          
                else:
                    if p.ground_id>=1 and p.ground_id<=99:
                        u.corn=u.corn+500*(-1*lis[0])
                    elif p.ground_id>=500 and p.ground_id<=599:
                        u.corn=u.corn+500*(-1*lis[0])                        
                    elif p.ground_id>=400 and p.ground_id<=499:
                        if p.ground_id<=404:
                            u.corn=u.corn+2500
                        elif p.ground_id<=408:
                            u.corn=u.corn+5000
                        elif p.ground_id<=412:
                            u.corn=u.corn+10000
                        elif p.ground_id<=416:
                            u.corn=u.corn+20000
                        else:
                            u.corn=u.corn+40000
                    elif p.ground_id>=100 and p.ground_id<=199:    
                        if (p.ground_id-100)%3==0:
                        #x=x+lis[0]
                            u.corn=u.corn+500*(-1*lis1[0])
                        elif (p.ground_id-100)%3==1:
                            lis1=getGround_id(p.ground_id-1)
                            if lis1[0]>0:
                                #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]/2
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*2
                        elif (p.ground_id-100)%3==2:
                            lis1=getGround_id(p.ground_id-2)
                            if lis1[0]>0:
                                #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*4
                    elif p.ground_id>=200 and p.ground_id<=299:
                        if (p.ground_id-200)%3==0:
                        #x=x+lis[0]
                            u.corn=u.corn+500*(-1*lis1[0])
                        elif (p.ground_id-200)%3==1:
                            lis1=getGround_id(p.ground_id-1)
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]/2
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*2
                        elif (p.ground_id-200)%3==2:
                            lis1=getGround_id(p.ground_id-2)  
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*4
                    elif p.ground_id>=300 and p.ground_id<=399:
                        if (p.ground_id-300)%3==0:
                        #x=x+lis[0]
                            u.corn=u.corn+500*(-1*lis1[0])
                        elif (p.ground_id-300)%3==1:
                            lis1=getGround_id(p.ground_id-1)
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]/2
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*2
                        elif (p.ground_id-300)%3==2:
                            lis1=getGround_id(p.ground_id-2)  
                            if lis1[0]>0:
                            #x=x+lis1[0]
                                u.corn=u.corn+lis1[0]
                            else:
                                u.corn=u.corn+500*(-1*lis1[0])*4                                                                  
                if u.labor_num<0:
                    u.labor_num=0
                if p.ground_id>=500:
                    u.populationupbound=u.populationupbound-decorationbuild[p.ground_id-500][1]
                #if u.population>u.populationupbound:
                #    u.population=u.populationupbound      
                p.ground_id=-1
                p.producttime=0
                p.object_id=-1
                p.finish=0
                read(city_id)
                replacecache(user_id,u)#cache
                return  dict(id=1,lis1=lis1[0])
        except InvalidRequestError:
            return dict(id=0)   
    ###############地图相关
    def makeMap(kind):#Map:insert
        newMap=Map(map_kind=kind,num=0)
        DBSession.add(newMap)
        c1=DBSession.query('LAST_INSERT_ID()')
        return c1[0]
    def insert(mapid):#Map:update
        try:
            c=DBSession.query(Map).filter_by(mapid=mapid).one()
            c.num=c.num+1
            return c.num
        except InvalidRequestError:
            return -1
    def getMap(kind):#Map:update
        try:
            c=DBSession.query(Map).filter_by(map_kind=kind)
            if c!=None :
                for m in c:
                    if m.num<mapKind[kind]:
                        cm=[insert(m.mapid),m.mapid]
                        return cm
            return [0,0]
        except InvalidRequestError:
            return [0,0]       
    def upd(oldmapid,kind):#Map:update
        try:
            c=DBSession.query(Map).filter_by(mapid=oldmapid).one()
            c.num=c.num-1
            i=getMap(kind)
            if i[0]>0:
                return i
            else:
                cid=makeMap(kind)
                i=insert(cid[0])
                return [i,cid[0]]
        except:
            return [0,0]
    ###############
    def read(city_id):# 向businessread表中写入数据
        try:
            s=''
            i=0
            cid=int(city_id)
            cset=DBSession.query(businessWrite).filter_by(city_id=cid)
            for c in cset:
                if i==0:
                    s=s+str(c.ground_id)+','+str(c.grid_id)+','+str(c.object_id)+','+str(c.producttime)+','+str(c.finish)
                    i=1
                else :
                    s=s+';'+str(c.ground_id)+','+str(c.grid_id)+','+str(c.object_id)+','+str(c.producttime)+','+str(c.finish)
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
    def changename(self,userid,newname):#对外接口，更改领地名
        #u=DBSession.query(operationalData).filter_by(userid=int(userid)).one()
        u=checkopdata(userid)#cache
        u.empirename=newname
        replacecache(userid,u)#cache
        return dict(id=1,newname=newname)
    @expose('json')
    def newcomplete(self,uid,level):#对外接口，新手任务
        try:
            level=int(level)
            #user=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            user=checkopdata(uid)#cache
            t=int(time.mktime(time.localtime())-time.mktime(beginTime))
            war=DBSession.query(warMap).filter_by(userid=int(uid)).one()
            if level==1:        
                user.newcomer=level
                user.corn=950
                user.exp=5
                user.cae=1
                user.food=120
                user.population=380
                user.labor_num=280
                replacecache(uid,user)#cache
                return dict(id=user.newcomer)
            elif level==2:
                user.newcomer=level
                user.corn=2950
                user.food=90
                user.cae=3
                user.exp=20
                user.lev=user.lev+1
                user.population=user.population+10
                try:
                    n=DBSession.query(businessWrite).filter_by(city_id=war.city_id).filter_by(grid_id=573).one()
                    n.ground_id=100
                    n.producttime=t
                    n.finish=0
                except InvalidRequestError:
                
                    newbuilding=businessWrite(city_id=war.city_id,ground_id=100,grid_id=573,object_id=-1,producttime=t,finish=0)
                    DBSession.add(newbuilding)
                read(war.city_id)
            
            else:
                user.newcomer=level
                user.exp=50#50+
                user.lev=user.lev+1
                user.corn=5550
                user.cae=6
                task=tasknew(user.userid)
                user.monstertime=t+1800
                user.monsterlist=''
                #user.food=190
                #user.infantrypower=60
                #user.labor_num=0
                #user.population=160
                user.corn=user.corn+3000
                user.currenttask=task[1]
                user.taskstring='0'
                ds=DBSession.query(Datesurprise).filter_by(uid=user.userid).one()
                ds.datesurprise=1
                
            replacecache(uid,user)#cache
            return dict(task=task[0],id=user.newcomer)
        except :
            return dict(id=0)
    ###############
    ###############新闻相关
    def addnews(uid,fpapayaid,kind,time,fuser_kind):#添加新闻函数
        news=News(uid=uid,fpapayaid=fpapayaid,kind=kind,time=time,fuser_kind=fuser_kind)
        DBSession.add(news)
    @expose('json')
    def getnewsnum(self,uid):#获取新闻总数
        try:
            nlist=[]
            uid=int(uid)
            newsset=DBSession.query(News).filter_by(uid=uid)
            for n in newsset:
                nlist.append(n.uid)
            i=len(nlist) 
            return dict(id=i)    
        except:
            return dict(id=0)
    @expose('json')
    def getnews(self,uid,off,size):#对外接口，获取新闻
        uid=int(uid)
        newslist=[]
        nl=[]
        num=11
        x=0 
        off=int(off)
        size=int(size)       
        try:
            newsset=DBSession.query(News).filter_by(uid=uid).order_by(News.id)
            for n in newsset:
                ntemp=[n.fpapayaid,n.kind,n.time]
                nl.append(ntemp)    
            if len(nl)==0 or nl==None :
                return dict(id=0)
            #u=DBSession.query(operationalData).filter_by(userid=uid).one()
            u=checkopdata(uid)#cache
            i=off
            l1=size+off
            if l1>len(nl):
                l1=len(nl)
            while i<l1:
                n1=[nl[i][0],nl[i][1],nl[i][2]]
                i=i+1
                newslist.append(n1)
            #return dict(id=1)
            return dict(time=u.logintime,news=newslist)
                
        except InvalidRequestError:
            return dict(id=0) 
    ###############  
  
         
   
    @expose('json')
    def logsign(self,papayaid,user_kind):# 对外接口，登陆注册login if signed or sign;operationalData:query
        user=None
        oid=papayaid#papayaid改为string类型
        user_kind=int(user_kind)
        logintime=int(time.mktime(time.localtime())-time.mktime(beginTime))
        lbonus=-1
        wargodtime=-1
        wealthgodtime=-1
        popgodtime=-1
        wealthgodtim=-1
        foodlost=0
        try:
            #writelog(0,0,'begin')
            ruser=DBSession.query(operationalData).filter_by(otherid=oid).filter_by(user_kind=user_kind).one()
            user=checkopdata(ruser.userid)
            ds=DBSession.query(Datesurprise).filter_by(uid=user.userid).one()
            #if ds.datesurprise==0:#计算怪物抢走的粮食
            #    if user.monsterlist!='0,7' and user.monsterlist!=None and user.monsterlist!='' and user.monstertime==0:
            #        fo=user.food
            #        foodlost=random.randint(int(fo/20),int(fo/10))
            #        user.food=user.food-foodlost
            bonus=loginBonus(user)#获取登录奖励
            lbonus=bonus
            s=DBSession.query(warMap).filter_by(userid=user.userid).one()#获取city_id
            st=DBSession.query(businessRead).filter_by(city_id=s.city_id).one()#获取经营页面整体信息
            stt=st.layout
            corn=user.corn
            cae=user.cae
            population=user.population
            labor_num=user.labor_num
            exp=user.exp
            fo=user.food
            tasklist=[]
            #if user.currenttask=='' or user.currenttask==None:
            #    tasklist=newtask(user)
            user.logintime=logintime
            lisa=[]
            try:
                ally=DBSession.query(Ally).filter_by(uid=user.userid)
                for a in ally :
                    #papaya=DBSession.query(operationalData).filter_by(userid=a.fid).one()
                    papaya=checkopdata(a.fid)#cache
                    lisa.append(papaya.otherid)
            except InvalidRequestError:
                lisa=[]
            giftstr=giftstring(user.otherid)
            minusstr=s.minusstate
            #writelog(1,0,'loginover')
            replacecache(user.userid,user)
            #logging.info(str(user.userid)+'is login')
            #if user.signtime>0:
             #   user.monstertime=user.monstertime+3600  
            if user.war_god==1:
                wargodtime=3600-(logintime-user.wargodtime)
            elif user.war_god==2:
                wargodtime=21600-(logintime-user.wargodtime)
            elif user.war_god==3:
                wargodtime=86400-(logintime-user.wargodtime)
            else:
                wargodtime=user.wargodtime
            if wargodtime<=0:
                user.war_god=0
                user.wargodtime=0
                wargodtime=0
            if user.person_god==1:
                popgodtime=3600-(logintime-user.popgodtime)
            elif user.person_god==2:
                popgodtime=21600-(logintime-user.popgodtime)
            elif user.person_god==3:
                popgodtime=86400-(logintime-user.popgodtime)
            else:
                popgodtime=user.popgodtime
            if popgodtime<=0:
                user.pop_god=0
                user.popgodtime=0 
                popgodtime=0
            if user.food_god==1:
                foodgodtime=3600-(logintime-user.foodgodtime)
            elif user.food_god==2:
                foodgodtime=21600-(logintime-user.foodgodtime)
            elif user.food_god==3:
                foodgodtime=86400-(logintime-user.foodgodtime)
            else:
                foodgodtime=user.foodgodtime
            if foodgodtime<=0:
                user.food_god=0
                user.foodgodtime=0 
                foodgodtime=0
            if user.wealth_god==1:
                wealthgodtime=3600-(logintime-user.wealthgodtime)
            elif user.wealth_god==2:
                wealthgodtime=21600-(logintime-user.wealthgodtime)
            elif user.wealth_god==3:
                wealthgodtime=86400-(logintime-user.wealthgodtime)
            else:
                wealthgodtime=user.wealthgodtime
            if wealthgodtime<=0:
                user.wealth_god=0
                user.wealthgodtime=0 
                wealthgodtime=0 
            task=-1
            if user.currenttask=='' or user.currenttask==None or user.currenttask=='-1' or int(user.currenttask)<0:
                task=-1
            else:
                task=taskbonus[int(user.currenttask)][0]   
             
            if user.newcomer<3:
                return dict(monsterdefeat=user.monsterdefeat,monsterid=user.monster,foodlost=user.monfood,monsterstr=user.monsterlist,task=task,monstertime=user.monstertime,citydefence=user.defencepower,wargod=user.war_god,wargodtime=wargodtime,populationgod=user.person_god,populationgodtime=popgodtime,foodgod=user.food_god,foodgodtime=foodgodtime,wealthgod=user.wealth_god,wealthgodtime=wealthgodtime,scout1_num=user.scout1_num,scout2_num=user.scout2_num,scout3_num=user.scout3_num,nobility=user.nobility,subno=user.subno,infantrypower=user.infantrypower,cavalrypower=user.cavalrypower,castlelev=user.castlelev,empirename=user.empirename,newstate=user.newcomer,lev=user.lev,labor_num=user.labor_num,allyupbound=user.allyupbound,minusstr=minusstr,giftstr=giftstr,bonus=bonus,allylis=lisa,id=user.userid,stri=stt,food=user.food,wood=user.wood,stone=user.stone,specialgoods=user.specialgoods,population=user.population,popupbound=user.populationupbound,time=logintime,exp=user.exp,corn=user.corn,cae=user.cae,map_id=s.mapid,city_id=s.city_id,landkind=user.landkind,treasurebox=user.treasurebox,treasurenum=user.treasurenum)    
            if user_kind==0:
                return dict(monsterdefeat=user.monsterdefeat,monsterid=user.monster,foodlost=user.monfood,monsterstr=user.monsterlist,task=task,monstertime=user.monstertime,citydefence=user.defencepower,wargod=user.war_god,wargodtime=wargodtime,populationgod=user.person_god,populationgodtime=popgodtime,foodgod=user.food_god,foodgodtime=foodgodtime,wealthgod=user.wealth_god,wealthgodtime=wealthgodtime,scout1_num=user.scout1_num,scout2_num=user.scout2_num,scout3_num=user.scout3_num,nobility=user.nobility,subno=user.subno,tasklist=tasklist,taskstring=user.taskstring,infantrypower=user.infantrypower,cavalrypower=user.cavalrypower,castlelev=user.castlelev,empirename=user.empirename,lev=user.lev,labor_num=user.labor_num,allyupbound=user.allyupbound,minusstr=minusstr,giftstr=giftstr,bonus=bonus,allylis=lisa,id=user.userid,stri=stt,food=user.food,wood=user.wood,stone=user.stone,specialgoods=user.specialgoods,population=user.population,popupbound=user.populationupbound,time=logintime,exp=user.exp,corn=user.corn,cae=user.cae,map_id=s.mapid,city_id=s.city_id,landkind=user.landkind,treasurebox=user.treasurebox,treasurenum=user.treasurenum)
            else:
                return dict(monsterdefeat=user.monsterdefeat,monsterid=user.monster,hid=user.hid,foodlost=user.monfood,monsterstr=user.monsterlist,task=task,monstertime=user.monstertime,headid=user.hid,citydefence=user.defencepower,wargod=user.war_god,wargodtime=wargodtime,populationgod=user.person_god,populationgodtime=popgodtime,foodgod=user.food_god,foodgodtime=foodgodtime,wealthgod=user.wealth_god,wealthgodtime=wealthgodtime,scout1_num=user.scout1_num,scout2_num=user.scout2_num,scout3_num=user.scout3_num,nobility=user.nobility,subno=user.subno,invitestring=user.invitestring,tasklist=tasklist,taskstring=user.taskstring,infantrypower=user.infantrypower,cavalrypower=user.cavalrypower,castlelev=user.castlelev,empirename=user.empirename,lev=user.lev,labor_num=user.labor_num,allyupbound=user.allyupbound,minusstr=minusstr,giftstr=giftstr,bonus=bonus,allylis=lisa,id=user.userid,stri=stt,food=user.food,wood=user.wood,stone=user.stone,specialgoods=user.specialgoods,population=user.population,popupbound=user.populationupbound,time=logintime,exp=user.exp,corn=user.corn,cae=user.cae,map_id=s.mapid,city_id=s.city_id,landkind=user.landkind,treasurebox=user.treasurebox,treasurenum=user.treasurenum)
                    
        except InvalidRequestError:
            newuser=operationalData(labor_num=280,population=380,exp=0,corn=1000,cae=1,nobility=0,infantry1_num=30,cavalry1_num=0,scout1_num=0,person_god=0,wealth_god=0,food_god=0,war_god=0,user_kind=user_kind,otherid=oid,lev=1,empirename='我的领地',food=100)
            DBSession.add(newuser)
            c1=DBSession.query('LAST_INSERT_ID()')
            c1=c1[0]
            gi=0
            mi=0
            mid=getMap(0)
            nuid=c1[0]
            
            nu=DBSession.query(operationalData).filter_by(userid=nuid).one()
            #mc.add(str(nuid),nu)
            #nu=mc.get(str(nuid))
            nu.logintime=logintime
            nu.signtime=logintime
            newvictories=Victories(uid=c1[0],won=0,lost=0)
            DBSession.add(newvictories)
            nu.infantrypower=60
            nu.infantrypower=30
            nu.monsterlist='0,7'
            if mid[0]!=0:
                nwMap=warMap(c1[0],mid[1],mid[0]-1,0)
                DBSession.add(nwMap)
                gi=mid[0]-1
                mi=mid[1]
            else:
                mid=makeMap(0)
                num=insert(mid[0])
                #return dict(id=num[0],mid=mid,num=num[1])
                i=num-1
             #   return dict(c1=c1[0],mid=mid,i=i)
                nwMap=warMap(c1[0],mid[0],i,0)
                gi=i
                mi=mid[0]
                DBSession.add(nwMap)
            cid=DBSession.query('LAST_INSERT_ID()')
            inistr=''
            inistr=inistr+INITIALSTR2+str(logintime)+',0;'+'100,575,-1,'+str(logintime-86400)+',1;300,570,-1,'+str(logintime-86400)+',1;1,690,0,'+str(logintime-86400)+',1';
            
            nbr=businessRead(city_id=cid[0][0],layout=inistr)
            DBSession.add(nbr)
            nbw=businessWrite(city_id=cid[0][0],ground_id=0,grid_id=455,object_id=0,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=491,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=527,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)            
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=528,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=200,grid_id=566,object_id=-1,producttime=logintime,finish=0)#bingying
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=567,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=531,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)            
            nbw=businessWrite(city_id=cid[0][0],ground_id=520,grid_id=568,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=100,grid_id=575,object_id=-1,producttime=logintime-86400,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=571,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=515,grid_id=493,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=606,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=607,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=608,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=609,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=610,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=611,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=612,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=613,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=614,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=615,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=616,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw) 
            nbw=businessWrite(city_id=cid[0][0],ground_id=530,grid_id=646,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=651,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw) 
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=691,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=731,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=503,grid_id=771,object_id=-1,producttime=0,finish=1)
            DBSession.add(nbw)                                    
            nbw=businessWrite(city_id=cid[0][0],ground_id=1,grid_id=688,object_id=-1,producttime=0,finish=1) 
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=1,grid_id=690,object_id=0,producttime=logintime-86400,finish=1)
            DBSession.add(nbw)
            nbw=businessWrite(city_id=cid[0][0],ground_id=300,grid_id=570,object_id=-1,producttime=logintime-86400,finish=1)  
            DBSession.add(nbw)       
            ds=Datesurprise(uid=nu.userid,datesurprise=0)
            DBSession.add(ds)
            dv=Datevisit(uid=nu.userid,visitnum=0)
            DBSession.add(dv)
            #writelog(1,0,'signover')
            #return dict(userid=nuid,id=0)
            addcache(c1[0],nu)#cache,新用户注册时，添加到cache中
            return dict(infantrypower=nu.infantrypower,cavalrypower=nu.cavalrypower,castlelev=nu.castlelev,newstate=0,popupbound=nu.populationupbound,wood=nu.wood,stone=nu.stone,specialgoods=nu.specialgoods,time=nu.logintime,labor_num=280,nobility=0,population=380,food=100,corn=1000,cae=nu.cae,exp=0,stri=inistr,id=c1[0],city_id=cid[0][0],mapid=mi,gridid=gi)
       
    @expose('json')
    def upgrademap(self,userid):#对外接口，爵位升级，进入新地图 user update and go to new map#OccupationData:query operationalData:query->update;warMap:update;Victories:update
        try:
            userid=int(userid)
            #u=DBSession.query(operationalData).filter_by(userid=userid).one()
            u=checkopdata(userid)#cache
            o=DBSession.query(Occupation).filter_by(masterid=userid)
            p=DBSession.query(warMap).filter_by(userid=userid).one()
            v=DBSession.query(Victories).filter_by(uid=userid).one()
            
            if u.nobility==NOBILITYUP:
                return dict(id=0)
            for oo in o:
                DBSession.delete(oo)
            c=upd(p.mapid,u.nobility+1)
            u.corn=u.corn+nobilitybonuslist[u.nobility][0]
            u.food=u.food+nobilitybonuslist[u.nobility][1]
            u.wood=u.wood+nobilitybonuslist[u.nobility][2]
            u.stone=u.stone+nobilitybonuslist[u.nobility][3]
            p.gridid=c[0]-1
            p.mapid=c[1]
            p.map_kind=p.map_kind+1
            no=u.nobility
            u.allyupbound=u.allyupbound+allyup[no+1]-allyup[no]
            u.nobility=u.nobility+1
            v.lostinmap=0
            v.woninmap=0
            v.delostinmap=0
            v.dewoninmap=0
            u.battleresult=''
            u.subno=0
            replacecache(userid,u)#cache
            return dict(mapid=p.mapid,gridid=p.gridid)
        except InvalidRequestError:
            return dict(id=0)
    
    @expose('json')
    def adddefence(self,uid,type):#对外接口，增加城池防御力
        type=int(type)
        uid=int(uid)
        food=0
        wood=0
        stone=0
        cae=0
        nobility=0
        
        try:
            #u=DBSession.query(operationalData).filter_by(userid=uid).one()
            u=checkopdata(uid)#cache
            nobility=u.nobility
            x=defenceplist[nobility][1]
            if type==0:
                cae=x
                if u.cae-cae>=0:
                    u.defencepower=u.defencepower+defenceplist[nobility][0]
                    u.cae=u.cae-cae
                    replacecache(uid,u)#cache
                    return dict(id=1)
                else:
                    return dict(id=0)
            else:
                corn=150*defenceplist[nobility][0]
                food=10*defenceplist[nobility][2]
                stone=5*defenceplist[nobility][3]
                wood=5*defenceplist[nobility][4]
                if u.corn-corn>=0 and u.food-food>=0 and u.stone-stone>=0 and u.wood-wood>=0:
                    u.corn=u.corn-corn
                    u.food=u.food-food
                    u.stone=u.stone-stone
                    u.wood=u.wood-wood
                    u.defencepower=u.defencepower+defenceplist[nobility][0]
                    replacecache(uid,u)#cache
                    return dict(id=1)
                else:
                    return dict(id=0) 
        except InvalidRequestError:
            return dict(id=0)
    def allyhelp(uid,type,poweru):#计算盟友战斗力
        uid=int(uid)
        fullpower=0
        #enemy_id=int(enemy_id)
        type=int(type)#0:attack,1:defence
        poweru=int(poweru)
        try:
            #u=DBSession.query(operationalData).filter_by(userid=uid).one()
            u=checkopdata(uid)#cache
            #ba=DBSession.query(Battle).filter_by(uid=uid).filter_by(enemy_id=enemy_id).one()
            allyset=DBSession.query(Ally).filter_by(uid=uid)

            for a in allyset :
                fid=a.fid
                #f=DBSession.query(operationalData).filter_by(userid=fid).one()
                f=checkopdata(fid)#cache
                if int((returnsentouryoku(f)+20-1)/20)>int((poweru+10-1)/10):
                    fullpower=fullpower+int((poweru+10-1)/10)
                else:
                    fullpower=fullpower+int((returnsentouryoku(f)+20-1)/20)
            return fullpower
        except InvalidRequestError:
            return 0 
    @expose('json')
    def attack(self,uid,enemy_id,timeneed,infantry,cavalry):#对外接口，进攻
        uid=int(uid)
        enemy_id=int(enemy_id)
        timeneed=int(timeneed)
        infantry=int(infantry)
        cavalry=int(cavalry)
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        try:
            ub=DBSession.query(Battle).filter_by(uid=uid).filter_by(enemy_id=enemy_id).one()
            #u=DBSession.query(operationalData).filter_by(userid=uid).one()
            u=checkopdata(uid)#cache
            u.infantrypower=u.infantrypower-infantry
            u.cavalrypower=u.cavalrypower-cavalry  
            ub.timeneed=timeneed
            ub.finish=0
            ub.left_time=t
            ub.powerin=infantry
            ub.powerca=cavalry
            ub.power=infantry+cavalry
            allypower=allyhelp(uid,0,infantry+cavalry)
            ub.allypower=allypower
            u.signtime=0
            replacecache(uid,u)#cache
            return dict(id=1)   
        except InvalidRequestError:
            u=DBSession.query(operationalData).filter_by(userid=uid).one()
            u.infantrypower=u.infantrypower-infantry
            u.cavalrypower=u.cavalrypower-cavalry   
            allypower=allyhelp(uid,0,infantry+cavalry)    
            nb=Battle(uid=uid,enemy_id=enemy_id,left_time=t,timeneed=timeneed,powerin=infantry,powerca=cavalry,power=infantry+cavalry,allypower=allypower)
            DBSession.add(nb)
            replacecache(uid,u)#cache
            return dict(id=1)                                     
    def returnscout(u):#返回侦察兵数量
        scout=[]
        scout.append(u.scout1_num)
        scout.append(u.scout2_num)
        scout.append(u.scout3_num)
        return scout
    @expose('json')
    def detect(self,uid,enemy_id,type):#对外接口，侦察
        type=int(type)
        scout=[]
        num=[2,6,12,0]
        i=0
        k=3
        mark=0
        enemy_id=int(enemy_id)
        try:
            #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            u=checkopdata(uid)#cache
            scout=returnscout(u)
            m=random.randint(1,10)
            if type<=2 and scout[type]-6<0:
                return dict(id=0)
            if type==3 and u.cae-2*(u.nobility+1)<0:
                return dict(id=0)
            if type==4 and u.cae-1<0:
                return dict(id=0)
            if type==0:
                if m<=7:
                    u.scout_num1=u.scout1_num-6
                    mark=1
                v=DBSession.query(Victories).filter_by(uid=enemy_id).one()
                replacecache(uid,u)#cache
                return dict(dead=mark,won=v.won,lost=v.lost)
            elif type==1:
                if m<=8:
                    u.scout_num2=u.scout2_num-6
                    mark=1
                #uv=DBSession.query(operationalData).filter_by(userid=enemy_id).one()
                uv=checkopdata(enemy_id)#cache
                v=DBSession.query(Victories).filter_by(uid=enemy_id).one()
                replacecache(uid,u)#cache
                return dict(dead=mark,won=v.won,lost=v.lost,power=uv.infantrypower+uv.cavalrypower)
            elif type==2:
                if m<=9:
                    u.scout_num3=u.scout3_num-6
                    mark=1
                #uv=DBSession.query(operationalData).filter_by(userid=enemy_id).one()
                uv=checkopdata(enemy_id)#cache
                v=DBSession.query(Victories).filter_by(uid=enemy_id).one()    
                replacecache(uid,u)#cache            
                return dict(dead=mark,won=v.won,lost=v.lost,power=uv.infantrypower+uv.cavalrypower,allynum=uv.allynum)
            elif type==3:
                u.cae=u.cae-2*(u.nobility+1)
                #uv=DBSession.query(operationalData).filter_by(userid=enemy_id).one()
                uv=checkopdata(enemy_id)#cache
                v=DBSession.query(Victories).filter_by(uid=enemy_id).one()      
                replacecache(uid,u)#cache        
                return dict(won=v.won,lost=v.lost,power=uv.infantrypower+uv.cavalrypower,allynum=uv.allynum,citydefence=u.defencepower)
            else:
                u.cae=u.cae-1
                ba=DBSession.query(Battle).filter_by(uid=enemy_id).filter_by(enemy_id=u.userid).one()
                power=ba.allypower
                replacecache(uid,u)#cache
                return dict(power=power)       
        except InvalidRequestError:
            return dict(id=0)                 
    @expose('json')
    def war2(self,uid):   
        if uid==None:
            return dict(id=0)
        uid=int(uid)
        battleresult=warresult2(uid) 
        #u=DBSession.query(operationalData).filter_by(userid=uid).one()
        u=checkopdata(uid)#cache
        nobility=u.nobility*3+u.subno
        subno=u.subno
        return dict(nobility=nobility,battleresult=battleresult,subno=u.subno)             
    @expose('json')
    def war(self,uid):#对外接口，战争结果
        if uid==None:
            return dict(id=0)
        uid=int(uid)
        battleresult=warresult(uid) 
        #u=DBSession.query(operationalData).filter_by(userid=uid).one()
        u=checkopdata(uid)#cache
        nobility=u.nobility*3+u.subno
        subno=u.subno
        return dict(nobility=nobility,battleresult=battleresult,subno=u.subno) 
    def callost(poweru,powere,type):
        lost=[0,0]
        constu=0
        conste=0
        if type==1:#poweru为进攻兵力
            if poweru>powere:
                if poweru>powere and poweru<=2*powere:
                    conste=0.4
                elif poweru>2*powere and poweru<=5*powere:
                    conste=0.5
                elif poweru>5*powere and poweru<=10*powere:
                    conste=0.6
                elif poweru>10*powere and poweru<=100*powere:
                    conste=0.7
                else:
                    conste=1
                lost[1]=int(powere*conste)
                lost[0]=int(lost[1]*0.75)
            else:
                if powere<=2*poweru:
                    constu=0.4
                elif powere>2*poweru and powere<=5*poweru:
                    constu=0.5
                elif powere>5*poweru and powere<=10*poweru:
                    constu=0.6
                elif powere>10*poweru and powere<=100*poweru:
                    constu=0.7
                else:
                    constu=1
                lost[0]=int(poweru*constu)
                lost[1]=int(lost[0]*0.6)
        else:
            if poweru>powere:
                if poweru>powere and poweru<=2*powere:
                    conste=0.4
                elif poweru>2*powere and poweru<=5*powere:
                    conste=0.5
                elif poweru>5*powere and poweru<=10*powere:
                    conste=0.6
                elif poweru>10*powere and poweru<=100*powere:
                    conste=0.7
                else:
                    conste=1
                lost[1]=int(powere*conste)
                lost[0]=int(lost[1]*0.6)
            else:
                if powere<=2*poweru:
                    constu=0.4
                elif powere>2*poweru and powere<=5*poweru:
                    constu=0.5
                elif powere>5*poweru and powere<=10*poweru:
                    constu=0.6
                elif powere>10*poweru and powere<=100*poweru:
                    constu=0.7
                else:
                    constu=1
                lost[0]=int(poweru*constu)
                lost[1]=int(lost[0]*0.75)
        return lost        
    def getexp(kill):#
        exp=0
        if kill<=1000:
            exp=kill 
        elif kill>=1000 and kill<=5000:
            exp=1000+int(0.5*(kill-1000))
        elif kill>5000 and kill<=10000:
            exp=3000+int(0.1*(kill-5000))
        else:
            exp=3500+int(0.05*(kill-10000))
        return exp
    def getresource(kill,u):
        bonusstring=''
        k=random.randint(1,100)
        if kill<=1000:
            if k>=1 and k<=24:#corn
                u.corn=u.corn+kill
                bonusstring='0,'+str(kill)#0,金钱
            elif k>24 and k<=48:#food
                u.food=u.food+kill
                bonusstring='1,'+str(kill)#1,food
            elif k>48 and k<=72:#wood
                u.wood=u.wood+int(0.3*kill)
                bonusstring='2,'+str(int(0.3*kill))#3,wood
            elif k>73 and k<=96:#stone
                u.stone=u.stone+int(0.5*kill)
                bonusstring='3,'+str(int(0.5*kill))#4,stone
            else:#cae
                u.cae=u.cae+1
                bonusstring='4,'+str(1)#5,cae
        elif kill>1000 and kill<=5000:
            if k>=1 and k<=24:#corn
                u.corn=u.corn+1000+int(0.5*(kill-1000))
                bonusstring='0,'+str(1000+int(0.5*(kill-1000)))#0,金钱
            elif k>24 and k<=48:#food
                u.food=u.food+1000+int(0.5*(kill-1000))
                bonusstring='1,'+str(1000+int(0.5*(kill-1000)))#1,food
            elif k>48 and k<=72:#wood
                u.wood=u.wood+300+int(0.15*(kill-1000))
                bonusstring='2,'+str(300+int(0.15*(kill-1000)))#3,wood
            elif k>73 and k<=96:#stone
                u.stone=u.stone+500+int(0.25*(kill-1000))
                bonusstring='3,'+str(500+int(0.25*(kill-1000)))#4,stone
            else:#cae
                u.cae=u.cae+3
                bonusstring='4,'+str(3)#5,cae  
        elif kill>5000 and kill<=10000:
            if k>=1 and k<=24:#corn
                u.corn=u.corn+3000+int(0.1*(kill-5000))
                bonusstring='0,'+str(3000+int(0.1*(kill-5000)))#0,金钱
            elif k>24 and k<=48:#food
                u.food=u.food+3000+int(0.1*(kill-5000))
                bonusstring='1,'+str(3000+int(0.1*(kill-5000)))#1,food
            elif k>48 and k<=72:#wood
                u.wood=u.wood+900+int(0.03*(kill-5000))
                bonusstring='2,'+str(900+int(0.03*(kill-5000)))#3,wood
            elif k>73 and k<=96:#stone
                u.stone=u.stone+1500+int(0.05*(kill-5000))
                bonusstring='3,'+str(1500+int(0.05*(kill-1000)))#4,stone
            else:#cae
                u.cae=u.cae+5
                bonusstring='4,'+str(5)#5,cae    
        else:
            if k>=1 and k<=24:#corn
                u.corn=u.corn+3500+int(0.05*(kill-10000))
                bonusstring='0,'+str(3500+int(0.05*(kill-10000)))#0,金钱
            elif k>24 and k<=48:#food
                u.food=u.food+3500+int(0.05*(kill-10000))
                bonusstring='1,'+str(3500+int(0.05*(kill-10000)))#1,food
            elif k>48 and k<=72:#wood
                u.wood=u.wood+1050+int(0.015*(kill-10000))
                bonusstring='2,'+str(1050+int(0.015*(kill-10000)))#3,wood
            elif k>73 and k<=96:#stone
                u.stone=u.stone+1750+int(0.025*(kill-10000))
                bonusstring='3,'+str(1750+int(0.025*(kill-10000)))#4,stone
            else:#cae
                u.cae=u.cae+10
                bonusstring='4,'+str(10)#5,cae    
        return bonusstring                  
    def warresult2(uid):
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        battleset=[]
        battleset3=[]
        battleset1=DBSession.query(Battle).filter_by(uid=int(uid))
        battleset2=DBSession.query(Battle).filter_by(enemy_id=int(uid)) 
        powerplus=0
        powerminus=0
        stru=''
        s=''
        returnstring=''
        uid=int(uid)
        for b1 in battleset1:
            if t-b1.left_time>b1.timeneed and b1.finish==0:
                battleset.append(b1)
        for b2 in battleset2:
            if t-b2.left_time>b2.timeneed and b2.finish==0:
                battleset.append(b2)
        if len(battleset)==0 or battleset==None:
            #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            u=checkopdata(uid)#cache
            returnstring=u.nbattleresult
            u.nbattleresult=''
            replacecache(uid,u)#cache
            return returnstring
        max=0
        i=0
        k=0
        while k<len(battleset):
            while i<len(battleset):
                if t-battleset[i].left_time>t-battleset[max].left_time : 
                    max=i
                i=i+1
            tmp=battleset[k]
            battleset[k]=battleset[max]
            battleset[max]=tmp
            k=k+1
            i=k
            max=k
        i=0
        battleset3=battleset
        #u=DBSession.query(operationalData).filter_by(userid=uid).one()
        u=checkopdata(uid)#cache
        ii=0  
        listattack=[]
        for b in battleset3:#按战斗开始时间排序
            powerplus=-1
            if b.uid==int(uid):#查询用户为攻击方
                listattack.append(0)
                if ii==0:
                    s=str(b.enemy_id)+',1'
                    ii=1
                else:
                    s=s+';'+str(b.enemy_id)+',1'
                war_godb=0
                try:
                    #f=DBSession.query(operationalData).filter_by(userid=b.enemy_id).one()
                    f=checkopdata(b.enemy_id)#cache
                    
                except:
                    return dict(id=b.enemy_id)
                poweru=b.power
                poweruu=poweru
                
                if u.war_god==1 and t-u.wargodtime<3600:
                    if u.war_god_lev==1:
                        poweru=int(poweru*(1.02))
                    elif u.war_god_lev==2:
                        poweru=int(poweru*(1.04))
                    elif u.war_god_lev==3:
                        poweru=int(poweru*(1.06))
                    elif u.war_god_lev==4:
                        poweru=int(poweru*(1.08))
                    elif u.war_god_lev==5:
                        poweru=int(poweru*(1.10))
                elif u.war_god==2 and t-u.wargodtime<21600:
                    if u.war_god_lev==1:
                        poweru=int(poweru*(1.02))
                    elif u.war_god_lev==2:
                        poweru=int(poweru*(1.04))
                    elif u.war_god_lev==3:
                        poweru=int(poweru*(1.06))
                    elif u.war_god_lev==4:
                        poweru=int(poweru*(1.08))
                    elif u.war_god_lev==5:
                        poweru=int(poweru*(1.10))
                elif u.war_god==3 and t-u.wargodtime<86400:
                    if u.war_god_lev==1:
                        poweru=int(poweru*(1.02))
                    elif u.war_god_lev==2:
                        poweru=int(poweru*(1.04))
                    elif u.war_god_lev==3:
                        poweru=int(poweru*(1.06))
                    elif u.war_god_lev==4:
                        poweru=int(poweru*(1.08))
                    elif u.war_god_lev==5:
                        poweru=int(poweru*(1.10))
                else:
                    u.war_god=0
                    u.wargodtime=-1
                godplusu=poweru-poweruu
                poweru=poweru+b.allypower
                powere=returnsentouryoku(f)
                poweree=powere
                if f.war_god==1 and t-f.wargodtime<3600:
                    if f.war_god_lev==1:
                        powere=int(powere*(1.02))
                    elif f.war_god_lev==2:
                        powere=int(powere*(1.04))
                    elif f.war_god_lev==3:
                        powere=int(powere*(1.06))
                    elif f.war_god_lev==4:
                        powere=int(powere*(1.08))
                    elif f.war_god_lev==5:
                        powere=int(powere*(1.10))
                elif f.war_god==2 and t-f.wargodtime<21600:
                    if f.war_god_lev==1:
                        powere=int(powere*(1.02))
                    elif f.war_god_lev==2:
                        powere=int(powere*(1.04))
                    elif f.war_god_lev==3:
                        powere=int(powere*(1.06))
                    elif f.war_god_lev==4:
                        powere=int(powere*(1.08))
                    elif f.war_god_lev==5:
                        powere=int(powere*(1.10))
                elif f.war_god==3 and t-f.wargodtime<86400:
                    if f.war_god_lev==1:
                        powere=int(powere*(1.02))
                    elif f.war_god_lev==2:
                        powere=int(powere*(1.04))
                    elif f.war_god_lev==3:
                        powere=int(powere*(1.06))
                    elif f.war_god_lev==4:
                        powere=int(powere*(1.08))
                    elif f.war_god_lev==5:
                        powere=int(powere*(1.10))
                else:
                    f.war_god=0
                    f.wargodtime=-1
                godpluse=powere-poweree
                powere=powere+f.defencepower+allyhelp(b.enemy_id,1,powere)
                lostcal=callost(poweru,powere,1)
                if poweru>powere:#jingongfang shengli
                    #fanhui sunshi bingli 
                    lostu=lostcal[0]
                    loste=lostcal[1]
                    powerplus=b.power-lostu                      
                    expgotu=getexp(loste)#用户计算获得经验值
                    expgote=getexp(lostu)#敌人计算经验值
                    u.exp=u.exp+expgotu#用户获得经验
                    s1=getbonusbattle2(u,4,1)
                    resourcegetu=getresource(loste,u)#huoquziyuan function
                    s=s+',1,'+str(lostu)+','+str(expgotu)+','+str(poweru)+','+str(powere)+','+s1+','+resourcegetu#'enemy_id,attackordefence,wonorlost,powerlost,corn,exp,specialgoods
                    fpower=loste
                    f.exp=f.exp+expgote#敌人获得经验
                    powerplus=b.power-lostu
                    ss='-'+getbonusbattle2(f,2,0)#损失2个物品
                    sss=str(b.uid)+',0,0,'+str(fpower)+','+str(expgote)+','+str(powere)+','+str(poweru)+','+ss+','+str(-int((f.corn+100-5)/100))#防御失败损失特殊物品及%5金币
                    f.corn=int((f.corn+100/95-1)/(100/95))
                    if f.corn<0:
                        f.corn=0
                    vu=DBSession.query(Victories).filter_by(uid=b.uid).one()
                    vf=DBSession.query(Victories).filter_by(uid=b.enemy_id).one()
                    vu.won=vu.won+1
                    vu.woninmap=vu.woninmap+1
                    vf.delostinmap=vf.delostinmap+1
                    vf.delost=vf.delost+1
                    calev(u,vu)
                    #vf.lost=vf.lost+1
                    try:
                        no=DBSession.query(Occupation).filter_by(masterid=b.uid).filter_by(slaveid=b.enemy_id).one()
                    except:   
                        no=Occupation(masterid=b.uid,slaveid=b.enemy_id)
                        DBSession.add(no)
                    addnews(u.userid,f.otherid,3,t,f.user_kind)
                    addnews(f.userid,u.otherid,4,t,u.user_kind)
                else:
                    lostu=lostcal[0]
                    loste=lostcal[1]
                    powerplus=b.power-lostu
                    expgotu=getexp(loste)##############
                    expgote=getexp(lostu)
                    u.exp=u.exp+expgotu
                    s1=getbonusbattle2(u,1,1)
                    s=s+',0,'+str(lostu)+',0,'+str(expgotu)+','+str(poweru)+','+str(powere)+','+s1+','+'null'
                    fpower=loste
                    f.exp=f.exp+expgote
                    ss=getbonusbattle2(f,3,1)
                    resourcegete=getresource(lostu,f)#huoquziyuan function
                    sss=str(b.uid)+',0,1,'+str(fpower)+','+str(expgote)+','+str(powere)+','+str(poweru)+','+ss+','+resourcegete
                    vu=DBSession.query(Victories).filter_by(uid=b.uid).one()
                    vf=DBSession.query(Victories).filter_by(uid=b.enemy_id).one()
                    vu.lost=vu.lost+1
                    vu.lostinmap=vu.lostinmap+1
                    vf.dewon=vf.dewon+1 
                    vf.dewoninmap=vf.dewoninmap+1
                mu=b.powerin-lostu
                if mu>=0:
                    uinlost=mu
                    ucalost=b.powerca
                else:
                    uinlost=0
                    ucalost=b.powerca+mu
                u.infantrypower=u.infantrypower+uinlost
                u.cavalrypower=u.cavalrypower+ucalost
                mu=f.infantrypower-loste
                if mu>=0:
                    f.infantrypower=mu
                else:
                    f.infantrypower=0
                    f.cavalrypower=f.cavalrypower+mu  
                if f.cavalrypower<0:
                    f.defencepower=f.defencepower+mu
                if f.defencepower<0:
                    f.defencepower=0
                s=s+','+f.otherid+','+str(uinlost)+','+str(ucalost)+','+f.empirename+','+str(f.nobility)+','+str(f.infantrypower)+','+str(f.cavalrypower)+','+str(godplusu)+','+str(godpluse)
                sss=sss+','+u.otherid+','+str(f.infantrypower)+','+str(f.cavalrypower)+','+u.empirename+','+str(u.nobility)+','+str(uinlost)+','+str(ucalost)+','+str(godpluse)+','+str(godplusu)
                if f.battleresult=='' or f.battleresult==None:
                    f.battleresult=sss
                else:
                    f.battleresult=f.battleresult+';'+sss
                if f.nbattleresult=='' or f.nbattleresult==None:
                    f.nbattleresult=sss
                else:
                    f.nbattleresult=f.nbattleresult+';'+sss                           
                b.power=0
                b.powerin=0
                b.powerca=0
                b.finish=1                
                replacecache(u.userid,u)
                replacecache(f.userid,f)                           
            elif b.enemy_id==int(uid):#查询用户为防守方
                listattack.append(1)
                if ii==0:
                    s=str(b.uid)+',0'  
                    ii=1
                else:
                    s=s+';'+str(b.uid)+',0'                  
                #f=DBSession.query(operationalData).filter_by(userid=b.uid).one()
                f=checkopdata(b.uid)#cache
                poweru=returnsentouryoku(u)
                poweruu=poweru
                if u.war_god==1 and t-u.wargodtime<3600:
                    if u.war_god_lev==1:
                        poweru=int(poweru*(1.02))
                    elif u.war_god_lev==2:
                        poweru=int(poweru*(1.04))
                    elif u.war_god_lev==3:
                        poweru=int(poweru*(1.06))
                    elif u.war_god_lev==4:
                        poweru=int(poweru*(1.08))
                    elif u.war_god_lev==5:
                        poweru=int(poweru*(1.10))
                elif u.war_god==2 and t-u.wargodtime<21600:
                    if u.war_god_lev==1:
                        poweru=int(poweru*(1.02))
                    elif u.war_god_lev==2:
                        poweru=int(poweru*(1.04))
                    elif u.war_god_lev==3:
                        poweru=int(poweru*(1.06))
                    elif u.war_god_lev==4:
                        poweru=int(poweru*(1.08))
                    elif u.war_god_lev==5:
                        poweru=int(poweru*(1.10))
                elif u.war_god==3 and t-u.wargodtime<86400:
                    if u.war_god_lev==1:
                        poweru=int(poweru*(1.02))
                    elif u.war_god_lev==2:
                        poweru=int(poweru*(1.04))
                    elif u.war_god_lev==3:
                        poweru=int(poweru*(1.06))
                    elif u.war_god_lev==4:
                        poweru=int(poweru*(1.08))
                    elif u.war_god_lev==5:
                        poweru=int(poweru*(1.10))
                else:
                    u.war_god=0
                    u.wargodtime=-1
                godplusu=poweru-poweruu
                poweru=poweru+u.defencepower+allyhelp(int(uid),1,poweru)
                powere=b.power
                poweree=powere
                if f.war_god==1 and t-f.wargodtime<1800:
                    if f.war_god_lev==1:
                        powere=int(powere*(1.02))
                    elif f.war_god_lev==2:
                        powere=int(powere*(1.04))
                    elif f.war_god_lev==3:
                        powere=int(powere*(1.06))
                    elif f.war_god_lev==4:
                        powere=int(powere*(1.08))
                    elif f.war_god_lev==5:
                        powere=int(powere*(1.10))
                elif f.war_god==2 and f-u.wargodtime<10800:
                    if f.war_god_lev==1:
                        powere=int(powere*(1.02))
                    elif f.war_god_lev==2:
                        powere=int(powere*(1.04))
                    elif f.war_god_lev==3:
                        powere=int(powere*(1.06))
                    elif f.war_god_lev==4:
                        powere=int(powere*(1.08))
                    elif f.war_god_lev==5:
                        powere=int(powere*(1.10))
                elif f.war_god==3 and t-f.wargodtime<43200:
                    if f.war_god_lev==1:
                        powere=int(powere*(1.02))
                    elif f.war_god_lev==2:
                        powere=int(powere*(1.04))
                    elif f.war_god_lev==3:
                        powere=int(powere*(1.06))
                    elif f.war_god_lev==4:
                        powere=int(powere*(1.08))
                    elif f.war_god_lev==5:
                        powere=int(powere*(1.10))
                else:
                    f.war_god=0
                    f.wargodtime=-1
                godpluse=powere-poweree
                powere=powere+b.allypower
                lostcal=callost(poweru,powere,0)#防守
                if poweru>powere:
                    lostu=lostcal[0]
                    powerminus=lostu
                    expgotu=getexp(loste)#用户计算获得经验值
                    expgote=getexp(lostu)#敌人计算经验值
                    s1=getbonusbattle2(u,3,1)
                    u.exp=u.exp+expgotu
                    resourcegetu=getresource(loste,u)#huoquziyuan function
                    s=s+',1,'+str(lostu)+','+str(expgotu)+','+str(poweru)+','+str(powere)+','+s1+','+resourcegetu
                    loste=int((powere+100/15-1)/(100/15))
                    fpower=loste
                    f.exp=f.exp+expgote
                    ss=getbonusbattle2(f,1,1)
                    sss=str(b.enemy_id)+',1,0,'+str(fpower)+','+str(expgote)+','+str(powere)+','+str(poweru)+','+ss+','+'null'
                    b.power=0
                    b.finish=1
                    vu=DBSession.query(Victories).filter_by(uid=b.uid).one()
                    vf=DBSession.query(Victories).filter_by(uid=b.enemy_id).one()
                    vu.dewon=vu.dewon+1
                    vu.dewoninmap=vu.dewoninmap+1
                    vf.lost=vf.lost+1 
                    vf.lostinmap=vf.lostinmap+1                   
                else:
                    lostu=lostcal[0]
                    powerminus=lostu
                    #u.exp=u.exp+1*powerminus
                    expgotu=getexp(loste)#用户计算获得经验值
                    expgote=getexp(lostu)#敌人计算经验值
                    u.exp=u.exp+expgotu
                    s1=getbonusbattle2(u,2,0)#损失2个特殊物品
                    s=s+',0,'+str(powerminus)+','+str(expgotu)+','+str(poweru)+','+str(powere)+',-'+s1+','+str(-int((u.corn+100-1)/100))
                    u.corn=int((u.corn+100/99-1)/(100/99))
                    loste=lostcal[1]
                    fpower=loste#敌方损失战斗力
                    f.exp=f.exp+expgote
                    ss=getbonusbattle2(f,4,1)
                    resourcegete=getresource(lostu,f)#huoquziyuan function
                    sss=str(b.enemy_id)+',1,1,'+str(fpower)+','+str(expgote)+','+str(powere)+','+str(poweru)+','+ss+','+resourcegete
                    vu=DBSession.query(Victories).filter_by(uid=b.uid).one()
                    vf=DBSession.query(Victories).filter_by(uid=b.enemy_id).one()
                    vu.delost=vu.delost+1
                    vu.delostinmap=vu.delostinmap+1
                    vf.won=vf.won+1
                    vf.woninmap=vf.woninmap+1
                    calev(f,vf)
                    try:
                        no=DBSession.query(Occupation).filter_by(masterid=b.enemy_id).filter_by(slaveid=b.uid).one()
                    except:   
                        no=Occupation(masterid=b.enemy_id,slaveid=b.uid)
                        DBSession.add(no)                    
                    addnews(u.userid,f.otherid,4,t,f.user_kind)
                    addnews(f.userid,u.otherid,3,t,u.user_kind)
                mu=b.powerin-loste
                if mu>=0:
                    finlost=mu
                    fcalost=b.powerca
                else:
                    finlost=0
                    fcalost=b.powerca+mu                    
                mu=u.infantrypower-powerminus
                if mu>=0:
                    u.infantrypower=mu
                else:
                    u.infantrypower=0
                    u.cavalrypower=u.cavalrypower+mu
                if u.cavalrypower<0:
                    u.defencepower=u.defencepower+mu
                if u.defencepower<0:
                    u.defencepower=0
                f.infantrypower=f.infantrypower+finlost
                f.cavalrypower=f.cavalrypower+fcalost
                s=s+','+f.otherid+','+str(u.infantrypower)+','+str(u.cavalrypower)+','+f.empirename+','+str(f.nobility)+','+str(finlost)+','+str(fcalost)+','+str(godplusu)+','+str(godpluse)
                sss=sss+','+u.otherid+','+str(finlost)+','+str(fcalost)+','+u.empirename+','+str(u.nobility)+','+str(u.infantrypower)+','+str(u.cavalrypower)+','+str(godpluse)+','+str(godplusu)
                if f.battleresult=='' or f.battleresult==None:
                    f.battleresult=sss
                else:
                    f.battleresult=f.battleresult+';'+sss
                if f.nbattleresult=='' or f.nbattleresult==None:
                    f.nbattleresult=sss
                else:
                    f.nbattleresult=f.nbattleresult+';'+sss                                     
                b.power=0
                b.powerin=0
                b.powerca=0
                b.finish=1 
                replacecache(f.userid,f)#cache
                replacecache(u.userid,u)#cache
            b.left_time=-1
            b.timeneed=-1
        if u.battleresult=='' or u.battleresult==None:
            u.battleresult=s  
        else:
            u.battleresult=u.battleresult+';'+s
        if s=='':
            returnstring=u.nbattleresult
        else:
            if u.nbattleresult!=None and u.nbattleresult!='':
                returnstring=u.nbattleresult+';'+s
            else:
                returnstring=s
        replacecache(u.userid,u)#cache        
        #u.nbattleresult=''
        return returnstring                          
    def warresult(uid):#计算战争结果，war中使用
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        battleset=[]
        battleset3=[]
        battleset1=DBSession.query(Battle).filter_by(uid=int(uid))
        battleset2=DBSession.query(Battle).filter_by(enemy_id=int(uid)) 
        powerplus=0
        powerminus=0
        stru=''
        s=''
        returnstring=''
        uid=int(uid)
        for b1 in battleset1:
            if t-b1.left_time>b1.timeneed and b1.finish==0:
                battleset.append(b1)
        for b2 in battleset2:
            if t-b2.left_time>b2.timeneed and b2.finish==0:
                battleset.append(b2)
        if len(battleset)==0 or battleset==None:
            #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
            u=checkopdata(uid)#cache
            returnstring=u.nbattleresult
            u.nbattleresult=''
            replacecache(uid,u)#cache
            return returnstring
        max=0
        i=0
        k=0
        while k<len(battleset):
            while i<len(battleset):
                if t-battleset[i].left_time>t-battleset[max].left_time : 
                    max=i
                i=i+1
            tmp=battleset[k]
            battleset[k]=battleset[max]
            battleset[max]=tmp
            k=k+1
            i=k
            max=k
        i=0
        battleset3=battleset
        #u=DBSession.query(operationalData).filter_by(userid=uid).one()
        u=checkopdata(uid)#cache
        ii=0  
        listattack=[]      
        for b in battleset3:#按战斗开始时间排序
            powerplus=-1
            if b.uid==int(uid):#查询用户为攻击方
                listattack.append(0)
                if ii==0:
                    s=str(b.enemy_id)+',1'
                    ii=1
                else:
                    s=s+';'+str(b.enemy_id)+',1'
                war_godb=0
                try:
                    #f=DBSession.query(operationalData).filter_by(userid=b.enemy_id).one()
                    f=checkopdata(b.enemy_id)#cache
                    
                except:
                    return dict(id=b.enemy_id)
                poweru=b.power
                poweruu=poweru
                
                if u.war_god==1 and t-u.wargodtime<3600:
                    if u.war_god_lev==1:
                        poweru=int(poweru*(1.05))
                    elif u.war_god_lev==2:
                        poweru=int(poweru*(1.1))
                    elif u.war_god_lev==3:
                        poweru=int(poweru*(1.15))
                elif u.war_god==2 and t-u.wargodtime<21600:
                    if u.war_god_lev==1:
                        poweru=int(poweru*(1.05))
                    elif u.war_god_lev==2:
                        poweru=int(poweru*(1.1))
                    elif u.war_god_lev==3:
                        poweru=int(poweru*(1.15))
                elif u.war_god==3 and t-u.wargodtime<86400:
                    if u.war_god_lev==1:
                        poweru=int(poweru*(1.05))
                    elif u.war_god_lev==2:
                        poweru=int(poweru*(1.1))
                    elif u.war_god_lev==3:
                        poweru=int(poweru*(1.15))
                else:
                    u.war_god=0
                    u.wargodtime=-1
                godplusu=poweru-poweruu
                poweru=poweru+b.allypower
                powere=returnsentouryoku(f)
                poweree=powere
                if f.war_god==1 and t-f.wargodtime<3600:
                    if f.war_god_lev==1:
                        powere=int(powere*(1.05))
                    elif f.war_god_lev==2:
                        powere=int(powere*(1.1))
                    elif f.war_god_lev==3:
                        powere=int(powere*(1.15))
                elif f.war_god==2 and t-f.wargodtime<21600:
                    if f.war_god_lev==1:
                        powere=int(powere*(1.05))
                    elif f.war_god_lev==2:
                        powere=int(powere*(1.1))
                    elif f.war_god_lev==3:
                        powere=int(powere*(1.15))
                elif f.war_god==3 and t-f.wargodtime<86400:
                    if f.war_god_lev==1:
                        powere=int(powere*(1.05))
                    elif f.war_god_lev==2:
                        powere=int(powere*(1.1))
                    elif f.war_god_lev==3:
                        powere=int(powere*(1.15))
                else:
                    f.war_god=0
                    f.wargodtime=-1
                godpluse=powere-poweree
                powere=powere+f.defencepower+allyhelp(b.enemy_id,1,powere)
                if poweru>powere:#jingongfang shengli
                    lostu=int((powere+20-1)/20)
                    powerplus=b.power-lostu                      
                    u.corn=u.corn+120*lostu
                    u.exp=u.exp+2*lostu
                    s1=getbonusbattle(u,4)
                    s=s+',1,'+str(lostu)+','+str(120*lostu)+','+str(2*lostu)+','+str(poweru)+','+str(powere)+','+s1#'enemy_id,attackordefence,wonorlost,powerlost,corn,exp,specialgoods
                    loste=int((powere+100/3-1)/(100/3))
                    fpower=loste
                    #f.exp=f.exp+1*fpower
                    powerplus=b.power-lostu
                    ss=getbonusbattle(f,1)
                    sss=str(b.uid)+',0,0,'+str(fpower)+','+str(-int((f.corn+100-1)/100))+',0,'+str(powere)+','+str(poweru)+','+ss
                    f.corn=int((f.corn+100/99-1)/(100/99))
                    #if f.battleresult=='' or f.battleresult==None:
                    #    f.battleresult=sss
                    #else:
                    #    f.battleresult=f.battleresult+';'+sss 
                    #if f.nbattleresult=='' or f.nbattleresult==None:
                    #    f.nbattleresult=sss
                    #else:
                    #    f.nbattleresult=f.nbattleresult+';'+sss
                    vu=DBSession.query(Victories).filter_by(uid=b.uid).one()
                    vf=DBSession.query(Victories).filter_by(uid=b.enemy_id).one()
                    vu.won=vu.won+1
                    vu.woninmap=vu.woninmap+1
                    vf.delostinmap=vf.delostinmap+1
                    vf.delost=vf.delost+1
                    calev(u,vu)
                    #vf.lost=vf.lost+1
                    try:
                        no=DBSession.query(Occupation).filter_by(masterid=b.uid).filter_by(slaveid=b.enemy_id).one()
                    except:   
                        no=Occupation(masterid=b.uid,slaveid=b.enemy_id)
                        DBSession.add(no)
                    addnews(u.userid,f.otherid,3,t,f.user_kind)
                    addnews(f.userid,u.otherid,4,t,u.user_kind)
                else:
                    lostu=int((poweru+100/15-1)/(100/15))
                    powerplus=b.power-lostu
                    u.exp=u.exp+1*lostu
                    s1=getbonusbattle(u,2)
                    s=s+',0,'+str(lostu)+',0,'+str(1*lostu)+','+str(poweru)+','+str(powere)+','+s1
                    loste=int((powere+100-1)/100)
                    fpower=loste
                    #f.exp=f.exp+2*fpower
                    f.corn=f.corn+100*fpower
                    ss=getbonusbattle(f,2)
                    sss=str(b.uid)+',0,1,'+str(fpower)+','+str(100*fpower)+',0,'+str(powere)+','+str(poweru)+','+ss
                    #if f.battleresult=='' or f.battleresult==None:
                    #    f.battleresult=sss
                    #else:
                    #    f.battleresult=f.battleresult+';'+ss
                    #if f.nbattleresult=='' or f.nbattleresult==None:
                    #    f.nbattleresult=sss
                    #else:
                    #    f.nbattleresult=f.nbattleresult+';'+sss
                    vu=DBSession.query(Victories).filter_by(uid=b.uid).one()
                    vf=DBSession.query(Victories).filter_by(uid=b.enemy_id).one()
                    vu.lost=vu.lost+1
                    vu.lostinmap=vu.lostinmap+1
                    vf.dewon=vf.dewon+1 
                    vf.dewoninmap=vf.dewoninmap+1
                mu=b.powerin-lostu
                if mu>=0:
                    uinlost=mu
                    ucalost=b.powerca
                else:
                    uinlost=0
                    ucalost=b.powerca+mu
                u.infantrypower=u.infantrypower+uinlost
                u.cavalrypower=u.cavalrypower+ucalost
                mu=f.infantrypower-loste
                if mu>=0:
                    f.infantrypower=mu
                else:
                    f.infantrypower=0
                    f.cavalrypower=f.cavalrypower+mu  
                if f.cavalrypower<0:
                    f.defencepower=f.defencepower+mu
                if f.defencepower<0:
                    f.defencepower=0
                s=s+','+f.otherid+','+str(uinlost)+','+str(ucalost)+','+f.empirename+','+str(f.nobility)+','+str(f.infantrypower)+','+str(f.cavalrypower)+','+str(godplusu)+','+str(godpluse)
                sss=sss+','+u.otherid+','+str(f.infantrypower)+','+str(f.cavalrypower)+','+u.empirename+','+str(u.nobility)+','+str(uinlost)+','+str(ucalost)+','+str(godpluse)+','+str(godplusu)
                if f.battleresult=='' or f.battleresult==None:
                    f.battleresult=sss
                else:
                    f.battleresult=f.battleresult+';'+sss
                if f.nbattleresult=='' or f.nbattleresult==None:
                    f.nbattleresult=sss
                else:
                    f.nbattleresult=f.nbattleresult+';'+sss                           
                b.power=0
                b.powerin=0
                b.powerca=0
                b.finish=1                
                replacecache(u.userid,u)
                replacecache(f.userid,f)                           
            elif b.enemy_id==int(uid):#查询用户为防守方
                listattack.append(1)
                if ii==0:
                    s=str(b.uid)+',0'  
                    ii=1
                else:
                    s=s+';'+str(b.uid)+',0'                  
                #f=DBSession.query(operationalData).filter_by(userid=b.uid).one()
                f=checkopdata(b.uid)#cache
                poweru=returnsentouryoku(u)
                poweruu=poweru
                if u.war_god==1 and t-u.wargodtime<3600:
                    if u.war_god_lev==1:
                        poweru=int(poweru*(1.05))
                    elif u.war_god_lev==2:
                        poweru=int(poweru*(1.1))
                    elif u.war_god_lev==3:
                        poweru=int(poweru*(1.15))
                elif u.war_god==2 and t-u.wargodtime<21600:
                    if u.war_god_lev==1:
                        poweru=int(poweru*(1.05))
                    elif u.war_god_lev==2:
                        poweru=int(poweru*(1.1))
                    elif u.war_god_lev==3:
                        poweru=int(poweru*(1.15))
                elif u.war_god==3 and t-u.wargodtime<86400:
                    if u.war_god_lev==1:
                        poweru=int(poweru*(1.05))
                    elif u.war_god_lev==2:
                        poweru=int(poweru*(1.1))
                    elif u.war_god_lev==3:
                        poweru=int(poweru*(1.15))
                else:
                    u.war_god=0
                    u.wargodtime=-1
                godplusu=poweru-poweruu
                poweru=poweru+u.defencepower+allyhelp(int(uid),1,poweru)
                powere=b.power
                poweree=powere
                if f.war_god==1 and t-f.wargodtime<3600:
                    if f.war_god_lev==1:
                        powere=int(powere*(1.05))
                    elif f.war_god_lev==2:
                        powere=int(powere*(1.1))
                    elif f.war_god_lev==3:
                        powere=int(powere*(1.15))
                elif f.war_god==2 and f-u.wargodtime<21600:
                    if f.war_god_lev==1:
                        powere=int(powere*(1.05))
                    elif f.war_god_lev==2:
                        powere=int(powere*(1.1))
                    elif f.war_god_lev==3:
                        powere=int(powere*(1.15))
                elif f.war_god==3 and t-f.wargodtime<86400:
                    if f.war_god_lev==1:
                        powere=int(powere*(1.05))
                    elif f.war_god_lev==2:
                        powere=int(powere*(1.1))
                    elif f.war_god_lev==3:
                        powere=int(powere*(1.15))
                else:
                    f.war_god=0
                    f.wargodtime=-1
                godpluse=powere-poweree
                powere=powere+b.allypower
                if poweru>powere:
                    lostu=int((poweru+100-1)/100)
                    powerminus=lostu
                    #u.exp=u.exp+2*int(poweru*0.01)
                    u.corn=u.corn+100*powerminus
                    s1=getbonusbattle(u,2)
                    s=s+',1,'+str(lostu)+','+str(100*lostu)+',0,'+str(poweru)+','+str(powere)+','+s1
                    loste=int((powere+100/15-1)/(100/15))
                    fpower=loste
                    f.exp=f.exp+1*fpower
                    ss=getbonusbattle(f,2)
                    sss=str(b.enemy_id)+',1,0,'+str(fpower)+',0,'+str(1*fpower)+','+str(powere)+','+str(poweru)+','+ss
                    b.power=0
                    b.finish=1
                    vu=DBSession.query(Victories).filter_by(uid=b.uid).one()
                    vf=DBSession.query(Victories).filter_by(uid=b.enemy_id).one()
                    vu.dewon=vu.dewon+1
                    vu.dewoninmap=vu.dewoninmap+1
                    vf.lost=vf.lost+1 
                    vf.lostinmap=vf.lostinmap+1                   
                else:
                    lostu=int((poweru+100/3-1)/(100/3))
                    powerminus=lostu
                    #u.exp=u.exp+1*powerminus
                    
                    s1=getbonusbattle(u,1)
                    s=s+',0,'+str(powerminus)+','+str(-int((u.corn+100-1)/100))+',0,'+str(poweru)+','+str(powere)+','+s1
                    u.corn=int((u.corn+100/99-1)/(100/99))
                    loste=int((poweru+20-1)/20)
                    fpower=loste#敌方损失战斗力
                    f.corn=f.corn+120*fpower
                    u.exp=u.exp+2*fpower
                    ss=getbonusbattle(f,4)
                    sss=str(b.enemy_id)+',1,1,'+str(fpower)+','+str(120*fpower)+','+str(2*fpower)+','+str(powere)+','+str(poweru)+','+ss
                    vu=DBSession.query(Victories).filter_by(uid=b.uid).one()
                    vf=DBSession.query(Victories).filter_by(uid=b.enemy_id).one()
                    vu.delost=vu.delost+1
                    vu.delostinmap=vu.delostinmap+1
                    vf.won=vf.won+1
                    vf.woninmap=vf.woninmap+1
                    calev(f,vf)
                    try:
                        no=DBSession.query(Occupation).filter_by(masterid=b.enemy_id).filter_by(slaveid=b.uid).one()
                    except:   
                        no=Occupation(masterid=b.enemy_id,slaveid=b.uid)
                        DBSession.add(no)                    
                    addnews(u.userid,f.otherid,4,t,f.user_kind)
                    addnews(f.userid,u.otherid,3,t,u.user_kind)
                mu=b.powerin-loste
                if mu>=0:
                    finlost=mu
                    fcalost=b.powerca
                else:
                    finlost=0
                    fcalost=b.powerca+mu                    
                mu=u.infantrypower-powerminus
                if mu>=0:
                    u.infantrypower=mu
                else:
                    u.infantrypower=0
                    u.cavalrypower=u.cavalrypower+mu
                if u.cavalrypower<0:
                    u.defencepower=u.defencepower+mu
                if u.defencepower<0:
                    u.defencepower=0
                f.infantrypower=f.infantrypower+finlost
                f.cavalrypower=f.cavalrypower+fcalost
                #mu=f.infantrypower-fpower
                #if mu>=0:
                #    f.infantrypower=mu
                #else:
                #   f.infantrypower=0
                #   f.cavalrypower=f.cavalrypower+mu 
                s=s+','+f.otherid+','+str(u.infantrypower)+','+str(u.cavalrypower)+','+f.empirename+','+str(f.nobility)+','+str(finlost)+','+str(fcalost)+','+str(godplusu)+','+str(godpluse)
                sss=sss+','+u.otherid+','+str(finlost)+','+str(fcalost)+','+u.empirename+','+str(u.nobility)+','+str(u.infantrypower)+','+str(u.cavalrypower)+','+str(godpluse)+','+str(godplusu)
                if f.battleresult=='' or f.battleresult==None:
                    f.battleresult=sss
                else:
                    f.battleresult=f.battleresult+';'+sss
                if f.nbattleresult=='' or f.nbattleresult==None:
                    f.nbattleresult=sss
                else:
                    f.nbattleresult=f.nbattleresult+';'+sss                                     
                b.power=0
                b.powerin=0
                b.powerca=0
                b.finish=1 
                replacecache(f.userid,f)#cache
                replacecache(u.userid,u)#cache
            b.left_time=-1
            b.timeneed=-1
        if u.battleresult=='' or u.battleresult==None:
            u.battleresult=s  
        else:
            u.battleresult=u.battleresult+';'+s
        if s=='':
            returnstring=u.nbattleresult
        else:
            if u.nbattleresult!=None and u.nbattleresult!='':
                returnstring=u.nbattleresult+';'+s
            else:
                returnstring=s
        replacecache(u.userid,u)#cache        
        #u.nbattleresult=''
        return returnstring
    def calev(u,v):#计算爵位等级，在warresult中调用
        nobility1=u.nobility
        subno=0
        if nobility1>=0 and nobility1<=1:
            bili=0.5
        elif nobility1>=2 and nobility1<=4:
            bili=0.6
        elif nobility1==5:
            bili=0.8
        else:
            bili=0.9
        enemynum=int(((mapKind[nobility1]-1)*bili)/3.0)
        if v.woninmap>=enemynum and v.woninmap<enemynum*2:
            u.subno=1
            #u.castlelev=u.castlelev+1  
        elif v.woninmap>=enemynum*2 and v.woninmap<enemynum*3:
            u.subno=2
        elif v.woninmap>=enemynum*3:
            u.subno=3
        return u.subno

    @expose('json')
    def battlelist(self,uid):
        alist=[]
        dlist=[]
        attacklist=[]
        defencelist=[]
        uid=int(uid)
        alist=DBSession.query(Battle).filter_by(uid=uid) 
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        for x in alist:
            if x.finish==0:
                #ue=DBSession.query(operationalData).filter_by(userid=x.enemy_id).one()
                ue=checkopdata(x.enemy_id)#cache
                atemp=[ue.otherid,x.timeneed-(t-x.left_time),x.powerin,x.powerca,ue.user_kind]
                attacklist.append(atemp)
        dlist=DBSession.query(Battle).filter_by(enemy_id=uid)
        for x in dlist:
            if x.finish==0 and t-x.left_time>x.timeneed/2 :
                #ue=DBSession.query(operationalData).filter_by(userid=x.uid).one()
                ue=checkopdata(x.uid)#cache
                dtemp=[ue.otherid,x.timeneed-(t-x.left_time),x.powerin,x.powerca,ue.user_kind]
                defencelist.append(dtemp)    
        return dict(attacklist=attacklist,defencelist=defencelist)
    
    @expose('json')
    def warrecord(self,uid):#对外接口，战绩
        #u=DBSession.query(operationalData).filter_by(userid=int(uid)).one()
        u=checkopdata(uid)#cache
        uv=DBSession.query(Victories).filter_by(uid=int(uid)).one()
        return dict(warrecord=u.battleresult,won=uv.won,attack=uv.won+uv.lost,woninmap=uv.woninmap,lostinmap=uv.lostinmap,dewoninmap=uv.dewoninmap,delostinmap=uv.delostinmap)                                                        
    @expose('json')
    def warinfo(self,userid):#对外接口，战报
        userid=int(userid)
        u=None
        v=None
        m=None
        u1=None
        bili=0
        attacklist=[]
        defencelist=[]
        u1=None
        l1=[]
        list1=[]
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        try:
            
            #u=DBSession.query(operationalData).filter_by(userid=userid).one()
            u=checkopdata(userid)#cache
            v=DBSession.query(Victories).filter_by(uid=userid).one()
            m=DBSession.query(warMap).filter_by(userid=userid).one()
            #battleresult=warresult(u.userid)
            newstr=u.signtime
            nobility1=u.nobility
            subno=u.subno
            won=v.won
            lost=v.lost
            list1=DBSession.query(warMap).filter_by(mapid=m.mapid)
            listuser=[]
            alist=DBSession.query(Battle).filter_by(uid=userid)  
            for x in alist:
                if x.finish==0:
                    #ue=DBSession.query(operationalData).filter_by(userid=x.enemy_id).one()
                    ue=checkopdata(x.enemy_id)#cache
                    atemp=[ue.otherid,x.timeneed-(t-x.left_time),x.powerin,x.powerca,ue.user_kind]
                    attacklist.append(atemp)
            dlist=DBSession.query(Battle).filter_by(enemy_id=userid)
            for x in dlist:
                if x.finish==0 and t-x.left_time>x.timeneed/2 :
                    #ue=DBSession.query(operationalData).filter_by(userid=x.uid).one()
                    ue=checkopdata(x.uid)#cache
                    dtemp=[ue.otherid,x.timeneed-(t-x.left_time),x.powerin,x.powerca,ue.user_kind]
                    defencelist.append(dtemp)
            for l in list1 :
                l1=[]
                try:
                    #u1=DBSession.query(operationalData).filter_by(userid=l.userid).one()
                    u1=checkopdata(l.userid)#cache
                    l1.append(u1.otherid)
                    l1.append(u1.user_kind)
                    l1.append(u1.nobility)
                    l1.append(l.gridid)
                    l1.append(u1.empirename)
                    l1.append(u1.userid)
                    l1.append(u1.subno)
                    newstr=u1.signtime
                    l1.append(newstr)
                    try:
                        occ=DBSession.query(Occupation).filter_by(masterid=userid).filter_by(slaveid=l.userid).one()
                        l1.append(1)
                    except InvalidRequestError:
                        l1.append(0)
                    if l.userid != userid:
                        listuser.append(l1)
                        
                except: 
                    continue               
            #ca=calev(u,v)
            
            return dict(newstr=newstr,infantrypower=u.infantrypower,cavalrypower=u.cavalrypower,citydefence=u.defencepower,attacklist=attacklist,defencelist=defencelist,time=t,gridid=m.gridid,monsterstr=u.monsterlist,nobility=nobility1,subno=subno,won=won,lost=lost,list=listuser)
        except InvalidRequestError:
            return dict(list=list1[0].userid,u=u.userid,v=v.uid,m=m.userid,map=m.mapid)
            
           

    @expose('json')
    def move(self,movestring):#对外接口，经营页面移动建筑物
        src=[]
        dst=[]
        strset2=''
        try:
            strset=movestring.split(':')
            city_id=strset[0]
            move=strset[1]
            strset2=move.split(';')
            
            
            i=0
            for s in strset2 :
                strset3=s.split(',')
                former=int(strset3[0])
                latter=int(strset3[1])
              
                p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=former).one()
                p.grid_id=-1-p.grid_id
                src.append(p)
                try:
                    p1=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=latter).one()
                    if p1.ground_id==-1:
                        DBSession.delete(p1)
                     
                    dst.append(p1.grid_id)
               
                except InvalidRequestError:
                    dst.append(latter)
                i=i+1
            k=0
            while k<i:
                try:
                    p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=latter).one()
                except:
                    src[k].grid_id=dst[k]
                k=k+1    
            read(city_id)
            return dict(id=1)
        except:
            k=len(src)-1
            former=-1
            while k>=0 :
               strset3=strset2[k].split(',')
               former=int(strset3[0])
               src[k].grid_id=former
               k=k-1 
            return dict(k=k,id=0,city_id=city_id,former=former,latter=latter,i=i)
    @expose('json')
    def godbless(self,uid,godtype,caetype):#对外接口，施加神迹
        uid=int(uid)
        #u=DBSession.query(operationalData).filter_by(userid=uid).one()
        u=checkopdata(uid)#cache
        t=int(time.mktime(time.localtime())-time.mktime(beginTime))
        godtype=int(godtype)
        caetype=int(caetype)
        mark=0
        if caetype==0:
            if u.cae-10>=0:
                u.cae=u.cae-10
                if godtype==0:

                    u.food_god=1
                    u.foodgodtime=t                    
                elif godtype==1:
                    u.person_god=1
                    u.popgodtime=t
                elif godtype==2:
                    u.wealth_god=1
                    u.wealthgodtime=t
                else:
                    u.war_god=1
                    u.wargodtime=t
                replacecache(uid,u)#cache
                return dict(id=1)
            else:
                return dict(id=0)
        elif caetype==1:
            if u.cae-20>=0:
                u.cae=u.cae-20
                if godtype==0:
                    u.food_god=2
                    u.foodgodtime=t                

                elif godtype==1:
                    u.person_god=2
                    u.popgodtime=t
                elif godtype==2:
                    u.wealth_god=2
                    u.wealthgodtime=t
                else:
                    u.war_god=2
                    u.wargodtime=t
                replacecache(uid,u)#cache
                return dict(id=1)
            else:
                return dict(id=0)  
        else:
            if u.cae-30>=0:
                u.cae=u.cae-30
                if godtype==0:
                    u.food_god=3
                    u.foodgodtime=t                

                elif godtype==1:
                    u.person_god=3
                    u.popgodtime=t
                elif godtype==2:
                    u.wealth_god=3
                    u.wealthgodtime=t
                else:
                    u.war_god=3
                    u.wargodtime=t
                replacecache(uid,u)#cache
                return dict(id=1)
            else:
                return dict(id=0)
                             
                 

    @expose('json')
    def updatebuilding(self,user_id,city_id,ground_id,grid_id,type):# 对外接口，升级建筑物update building operationalData:query->update; businessWrite:query->update
        ground_id=int(ground_id)
        try:
            ca=0
            cae=0
            price=0
            pricefood=0
            pop=0
            ground_id=int(ground_id)
            stone=0
            wood=0
            lis=getGround_id(int(ground_id))
            if lis==None:
                return dict(id=-int(ground_id))
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
            price=lis[0]
            if p.ground_id<=0 or p.grid_id<=0:
                return dict(id=0)
            if int(type)==0:
                if ground_id>=100 and ground_id<=199:
                    cae=lis[3]
                    
                elif ground_id>=200 and ground_id<=299:
                    cae=lis[4]
                    pop=lis[2]
                elif ground_id>=300 and ground_id<=399:
                    cae=lis[4]
                    pop=lis[2]
                elif ground_id>=400 and ground_id<=499:
                    cae=lis[2]
                #if u.cae-cae>=0:    
                if u.cae-cae>=0 and u.labor_num+pop<=u.population:
                    p.producttime=ti
                    p.finish=0
                    p.ground_id=ground_id
                    p.object_id=-1
                    u.cae=u.cae-cae
                    u.labor_num=u.labor_num+pop
                    if p.ground_id>=1 and p.ground_id<=99:
                        u.exp=u.exp+lis[4]
                    elif p.ground_id>=100 and p.ground_id<=199:
                        u.exp=u.exp+lis[4]
                    elif p.ground_id >=200 and p.ground_id<=299:
                        u.exp=u.exp+lis[5]
                    elif p.ground_id>=300 and p.ground_id<=399:
                        u.exp=u.exp+lis[5]
                    elif p.ground_id>=400 and p.ground_id<=499:
                        u.exp=u.exp+lis[3]
                    if ground_id>=400 and ground_id<=499:
                        u.populationupbound=u.populationupbound+lis[4]
                    read(city_id)
                    replacecache(u.userid,u)#cache
                    return dict(id=1)
                else:
                    return dict(id=0)
            else:
                if ground_id>=1 and ground_id<=499:
                    pricefood=lis[1]
                if ground_id >=1 and ground_id<=99:
                    pop=lis[2]
                elif ground_id>=200 and ground_id<399:
                    pop=lis[2]
                if ground_id>=1 and ground_id<=99:
                    wood=lis[3]
                elif ground_id>=100 and ground_id<=199:
                    if lis[2]>0:
                        wood=lis[2]
                    else:
                        stone=-lis[2]
                elif ground_id>=200 and ground_id<=299:
                    if lis[3]>0:
                        wood=lis[3]
                    else:
                        stone=-lis[3]
                elif ground_id>=300 and ground_id<=399:
                    if lis[3]>0:
                        wood=lis[3]
                    else:
                        stone=-lis[3]
                elif ground_id>=400 and ground_id<=499:
                    pricefood=lis[1]
                if price>=0:
                    if u.corn-price>=0 and u.food-pricefood>=0 and u.labor_num+pop<=u.population and u.wood-wood>=0 and u.stone-stone>=0 and p.finish==1 and specialgoods(int(ground_id),u.specialgoods,u)==True:
                        u.corn=u.corn-price
                        u.stone=u.stone-stone
                        u.wood=u.wood-wood
                        u.food=u.food-pricefood
                        u.labor_num=u.labor_num+pop
                        p.finish=0
                        p.producttime=ti
                        p.ground_id=int(ground_id)
                        if p.ground_id>=1 and p.ground_id<=99:
                            u.exp=u.exp+lis[4]
                        elif p.ground_id>=100 and p.ground_id<=199:
                            u.exp=u.exp+lis[4]
                        elif p.ground_id >=200 and p.ground_id<=299:
                            u.exp=u.exp+lis[5]
                        elif p.ground_id>=300 and p.ground_id<=399:
                            u.exp=u.exp+lis[5]
                        elif p.ground_id>=400 and p.ground_id<=499:
                            u.exp=u.exp+lis[3]                        
                        if int(ground_id)>=400 and int(ground_id)<=499:
                            u.populationupbound=u.populationupbound+lis[4]
                        read(city_id)
                        replacecache(u.userid,u)#cache
                        return dict(id=1)
                    else:
                        return dict(id=0)
                else:
                    if u.cae+price>=0 and u.food-pricefood>=0 and u.labor_num+pop<=u.population and u.wood-wood>=0 and u.stone-stone>=0 and  p.finish==1 and specialgoods(int(ground_id),u.specialgoods,u)==True:
                        u.cae=u.cae+price
                        u.food=u.food-pricefood
                        u.labor_num=u.labor_num+pop
                        u.wood=u.wood-wood
                        u.stone=u.stone-stone
                        p.finish=0
                        p.producttime=ti
                        if p.ground_id>=1 and p.ground_id<=99:
                            u.exp=u.exp+lis[4]
                        elif p.ground_id>=100 and p.ground_id<=199:
                            u.exp=u.exp+lis[4]
                        elif p.ground_id >=200 and p.ground_id<=299:
                            u.exp=u.exp+lis[5]
                        elif p.ground_id>=300 and p.ground_id<=399:
                            u.exp=u.exp+lis[5]
                        elif p.ground_id>=400 and p.ground_id<=499:
                            u.exp=u.exp+lis[3]                        
                        #p.producttime=ti
                        p.ground_id=int(ground_id)
                        if int(ground_id)>=400 and int(ground_id)<=499:
                            u.populationupbound=u.populationupbound+lis[4]
                        read(city_id)
                        replacecache(u.userid,u)#cache
                        return dict(id=1)
                    else:
                        return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def build(self,user_id,city_id,ground_id,grid_id):# 对外接口，建造建筑物build operationalData:query->update; businessWrite:query->update
        i=0
        price=0
        pricefood=0
        pop=0
        stone=0
        wood=0
        try:
            ca=0
            price=0
            pricefood=0
            pop=0
            ground_id=int(ground_id)
            stone=0
            wood=0
            lis=getGround_id(int(ground_id))
            if lis==None:
                return dict(id=int(ground_id))
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            ptime=p.producttime
            price=lis[0]
            ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
           #if p.ground_id>=1 and p.ground_id<=99:
           #    u.exp=u.exp+lis[4]
           #elif p.ground_id>=100 and p.ground_id<=199:
           #    u.exp=u.exp+lis[4]
           #elif p.ground_id >=200 and p.ground_id<=299:
           #    u.exp=u.exp+lis[5]
           #elif p.ground_id>=300 and p.ground_id<=399:
           #    u.exp=u.exp+lis[5]
           #elif p.ground_id>=400 and p.ground_id<=499:
           #    u.exp=u.exp+lis[3]
            if ground_id>=1 and ground_id<=499:
                pricefood=lis[1]
            if ground_id >=1 and ground_id<=99:
                pop=lis[2]
            elif ground_id>=200 and ground_id<399:
                pop=lis[2]
            if ground_id>=1 and ground_id<=99:
                wood=lis[3]
            elif ground_id>=100 and ground_id<=199:
                if lis[2]>0:
                    wood=lis[2]
                else:
                    stone=-lis[2]
            elif ground_id>=200 and ground_id<=299:
                if lis[3]>0:
                    wood=lis[3]
                else:
                    stone=-lis[3]
            elif ground_id>=300 and ground_id<=399:
                if lis[3]>0:
                    wood=lis[3]
                else:
                    stone=-lis[3]        
            if price>=0:
                if u.corn-price>=0 and u.food-pricefood>=0 and u.labor_num+pop<=u.population and u.wood-wood>=0 and u.stone-stone>=0 and ptime==0 and specialgoods(int(ground_id),u.specialgoods,u)==True:
                    u.corn=u.corn-price
                    u.stone=u.stone-stone
                    u.wood=u.wood-wood
                    u.food=u.food-pricefood
                    u.labor_num=u.labor_num+pop
                    
                    p.finish=0
                    if ground_id>=1 and ground_id<=99:
                        p.finish=1
                        p.producttime=0
                        u.exp=u.exp+lis[4]
                    elif ground_id>=100 and ground_id<=199:
                        u.exp=u.exp+lis[4]
                    elif ground_id>=200 and ground_id<=399:
                        u.exp=u.exp+lis[5]
                    elif ground_id>=500 and ground_id<=699:
                        p.finish=1
                        p.producttime=0
                        u.populationupbound=u.populationupbound+lis[1]
                        
                    elif ground_id>=400 and ground_id<=499:
                        u.populationupbound=u.populationupbound+lis[3]  
                        u.exp=u.exp+lis[3] 
                        p.producttime=ti                     
                    else:
                        p.producttime=ti
                        
                    p.ground_id=int(ground_id)
                    #if p.ground_id==400 or p.ground_id==404 or p.ground_id==408 or p.ground_id==412:
                    #    u.food_god_lev=u.food_god_lev+1
                    #elif p.ground_id==401 or p.ground_id==405 or p.ground_id==409 or p.ground_id==413:
                    #    u.person_god_lev=u.person_god_lev+1
                    #elif p.ground_id==402 or p.ground_id==406 or p.ground_id==410 or p.ground_id==414:
                    #    u.wealth_god_lev=u.wealth_god_lev+1
                    #elif p.ground_id==403 or p.ground_id==407 or p.ground_id==411 or p.ground_id==415:
                    #    u.war_god_lev=u.war.god_lev+1                   
                    read(city_id)
                    replacecache(u.userid,u)#cache
                    return dict(id=1)
                else:
                    return dict(id=0)
            else:
                if u.cae+price>=0 and u.food-pricefood>=0 and u.labor_num+pop<=u.population and u.wood-wood>=0 and u.stone-stone>=0 and ptime==0 and specialgoods(int(ground_id),u.specialgoods,u)==True:
                    u.cae=u.cae+price
                    u.food=u.food-pricefood
                    u.labor_num=u.labor_num+pop
                    u.wood=u.wood-wood
                    u.stone=u.stone-stone
                    p.finish=0
                    if ground_id>=1 and ground_id<=99:
                        p.finish=1
                        p.producttime=0
                        u.exp=u.exp+lis[4]
                    elif ground_id>=100 and ground_id<=199:
                        u.exp=u.exp+lis[4]
                    elif ground_id>=200 and ground_id<=399:
                        u.exp=u.exp+lis[5]
                    
                    elif ground_id>=500 and ground_id<=699:
                        p.finish=1
                        p.producttime=0
                        u.populationupbound=u.populationupbound+lis[1]
                    elif ground_id>=400 and ground_id<=499:
                        u.populationupbound=u.populationupbound+lis[4]
                        u.exp=u.exp+lis[3]
                        p.producttime=ti
                    else:
                        p.producttime=ti
                    #p.producttime=ti
                    p.ground_id=int(ground_id)
                    read(city_id)
                    replacecache(u.userid,u)#cache
                    return dict(id=1)
                else:
                    return dict(id=0)
        except InvalidRequestError:
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            ground_id=int(ground_id)
            lis=getGround_id(int(ground_id))
            if lis[0]==None:
                return dict(id=-3)
            ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
            price=lis[0]
            if ground_id>=1 and ground_id<=499:
                pricefood=lis[1]
            if ground_id >=1 and ground_id<=99:
                pop=lis[2]
            elif ground_id>=200 and ground_id<399:
                pop=lis[2]
            if ground_id>=1 and ground_id<=99:
                wood=lis[3]
            elif ground_id>=100 and ground_id<=199:
                if lis[3]!=0:
                    return dict(id='can not update')
                if lis[2]>0:
                    wood=lis[2]
                else:
                    stone=-lis[2]
            elif ground_id>=200 and ground_id<=299:
                if lis[4]!=0:
                    return dict(id='can not  update')
                if lis[3]>0:
                    wood=lis[3]
                else:
                    stone=-lis[3]
            elif ground_id>=300 and ground_id<=399:
                if lis[4]!=0:
                    return dict(id='can not update')
                if lis[3]>0:
                    wood=lis[3]
                else:
                    stone=-lis[3]
                    
            newbuilding=None
            if ground_id>=1 and ground_id<=99:
                newbuilding=businessWrite(city_id=int(city_id),ground_id=int(ground_id),grid_id=int(grid_id),object_id=-1,producttime=0,finish=1)
            elif ground_id>=500 and ground_id<=699:
                newbuilding=businessWrite(city_id=int(city_id),ground_id=int(ground_id),grid_id=int(grid_id),object_id=-1,producttime=0,finish=1)
            else:
                newbuilding=businessWrite(city_id=int(city_id),ground_id=int(ground_id),grid_id=int(grid_id),object_id=-1,producttime=ti,finish=0)
            if price>=0:
                if u.corn-price>=0 and u.food-pricefood>=0 and u.labor_num+pop<=u.population and u.wood-wood>=0 and u.stone-stone>=0 and specialgoods(int(ground_id),u.specialgoods,u)==True:
                    u.corn=u.corn-price
                    u.food=u.food-pricefood
                    u.labor_num=u.labor_num+pop
                    u.wood=u.wood-wood
                    u.stone=u.stone-stone
                    if ground_id>=1 and ground_id<=99:
                        u.exp=u.exp+lis[4]
                    elif ground_id>=100 and ground_id<=199:
                        u.exp=u.exp+lis[4]
                    elif ground_id>=200 and ground_id<=399:
                        u.exp=u.exp+lis[5]
                    elif ground_id>=500 and ground_id<=699:
                        u.populationupbound=u.populationupbound+lis[1]
                    elif ground_id>=400 and ground_id<=499:
                        u.populationupbound=u.populationupbound+lis[4]
                        u.exp=u.exp+lis[3]                        
                    DBSession.add(newbuilding)
                    c1=DBSession.query('LAST_INSERT_ID()')
                    #if ground_id==400 or ground_id==404 or ground_id==408 or ground_id==412:
                    #    u.food_god_lev=u.food_god_lev+1
                    #elif ground_id==401 or ground_id==405 or ground_id==409 or ground_id==413:
                    #    u.person_god_lev=u.person_god_lev+1
                    #elif ground_id==402 or ground_id==406 or ground_id==410 or ground_id==414:
                    #    u.wealth_god_lev=u.wealth_god_lev+1
                    #elif ground_id==403 or ground_id==407 or ground_id==411 or ground_id==415:
                    #    u.war_god_lev=u.war.god_lev+1
                    read(city_id)
                    replacecache(u.userid,u)#cache
                    return dict(id=1,gid=ground_id)
                else:
                    return dict(id=0)
            else:
                if u.cae+price>=0 and u.food-pricefood>=0 and u.labor_num+pop<=u.population and u.wood-wood>=0 and u.stone-stone>=0 and specialgoods(int(ground_id),u.specialgoods,u)==True:
                    u.cae=u.cae+price
                    u.wood=u.wood-wood
                    u.stone=u.stone-stone
                    u.food=u.food-pricefood
                    u.labor_num=u.labor_num+pop
                    if ground_id>=1 and ground_id<=99:
                        u.exp=u.exp+lis[4]
                    elif ground_id>=100 and ground_id<=199:
                        u.exp=u.exp+lis[4]
                    elif ground_id>=200 and ground_id<=399:
                        u.exp=u.exp+lis[5]
                    elif ground_id>=400 and ground_id<=499:
                        u.populationupbound=u.populationupbound+lis[4]    
                        u.exp=u.exp+lis[3]                    
                    elif ground_id>=500 and ground_id<=699:
                        u.populationupbound=u.populationupbound+lis[1]
                    DBSession.add(newbuilding)
                    read(city_id)
                    replacecache(u.userid,u)#cache
                    return dict(id=1)
                else:
                    return dict(id=0)

    @expose('json')
    def planting(self,user_id,city_id,grid_id,object_id,type):#对外接口，种植，资源获取operationalData:query->update; businessWrite:query->update
        try:
            if int(type)==0:
                price=Plant_Price[int(object_id)][0]
            elif int(type)==1:
                price=stones[int(object_id)][0]
            else:
                price=woods[int(object_id)][0]
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            ptime=p.producttime;
            if price<0:
                sub=u.cae+price
                if sub>=0 and ptime==0:
                    #sub=u.cae
                    
                    u.cae=sub#to update the datasheet
                    ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
                    p.object_id=int(object_id)
                    p.producttime=ti
                    read(city_id)
                    replacecache(u.userid,u)#cache
                    return dict(id=1)
                else:
                    return dict(id=0)
            elif u.corn-price>=0  and ptime==0:
                sub=u.corn-price
                
                u.corn=sub#to update the datasheet
                ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
                p.object_id=int(object_id)
                p.producttime=ti
                read(city_id)
                replacecache(u.userid,u)#cache
                return dict(id=1)
            else:
                return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def harvest(self,user_id,city_id,grid_id,type):#对外接口，种植，资源收获warMap:query;operationalData:query->update; businessWrite:query->update
        try:
            type=int(type)
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            war=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
            
            mark=minusstateeli(u,war,grid_id,p.producttime)
            mark=0
            t=int(time.mktime(time.localtime())-time.mktime(beginTime))
            factor=1
            factor2=1.0
            if u.food_god==1 and t-u.foodgodtime<3600:
                if u.food_god_lev==1:
                    factor=1.2
                elif u.food_god_lev==2:
                    factor=1.4
                elif u.food_god_lev==3:
                    factor=1.6
                elif u.food_god_lev==4:
                    factor=1.8
                elif u.food_god_lev==5:
                    factor=2
            elif u.food_god==2 and t-u.foodgodtime<21600:
                if u.food_god_lev==1:
                    factor=1.2
                elif u.food_god_lev==2:
                    factor=1.4
                elif u.food_god_lev==3:
                    factor=1.6
                elif u.food_god_lev==4:
                    factor=1.8
                elif u.food_god_lev==5:
                    factor=2
            elif u.food_god==3 and t-u.foodgodtime<86400:
                if u.food_god_lev==1:
                    factor=1.2
                elif u.food_god_lev==2:
                    factor=1.4
                elif u.food_god_lev==3:
                    factor=1.6
                elif u.food_god_lev==4:
                    factor=1.8
                elif u.food_god_lev==5:
                    factor=2
            else:
                u.food_god=0
                u.foodgodtime=-1                                
            tu=[]
            if p.ground_id==2:#水晶农田
                factor2=1.2
            elif p.ground_id==3:#宝石农田
                factor2=1.4
            elif p.ground_id==4:#精灵农田
                factor2=1.6
            if type==0:
                tu=Plant_Price[p.object_id]
            elif type==1:
                tu=stones[p.object_id]
            else:
                tu=woods[p.object_id]
            
                           
            if p.producttime!=1 and t-p.producttime>86400*3:
                p.producttime=0
                u.exp=u.exp+tu[1]
                p.object_id=-1 
                read(city_id)
                replacecache(u.userid,u)
                return dict(id=1)
            if type==0 and mark==0:
                tu=Plant_Price[p.object_id]
                u.food=u.food+int(tu[2]*factor*factor2)
            elif type==1 and mark==0:
                tu=stones[p.object_id]
                u.stone=u.stone+int(tu[2]*factor)
            elif type==2 and mark==0:
                tu=woods[p.object_id]
                u.wood=u.wood+int(tu[2]*factor)
            p.producttime=0
            p.object_id=-1
            u.exp=u.exp+tu[1]
            read(city_id)
            replacecache(u.userid,u)#cache
            return dict(id=1)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def finish_building(self,user_id,city_id,grid_id):#对外接口，完成建筑物建造operationalData:query->update; businessWrite:query->update
        try:
           p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
           lis=getGround_id(p.ground_id)
           #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
           u=checkopdata(user_id)#cache
           #if p.ground_id>=1 and p.ground_id<=99:
           #    u.exp=u.exp+lis[4]
           #elif p.ground_id>=100 and p.ground_id<=199:
           #    u.exp=u.exp+lis[4]
           #elif p.ground_id >=200 and p.ground_id<=299:
           #    u.exp=u.exp+lis[5]
           #elif p.ground_id>=300 and p.ground_id<=399:
           #    u.exp=u.exp+lis[5]
           #elif p.ground_id>=400 and p.ground_id<=499:
           #    u.exp=u.exp+lis[3]
               #u.populationupbound=u.populationupbound+lis[4]
           if p.ground_id==400 or p.ground_id==404 or p.ground_id==408 or p.ground_id==412 or p.ground_id==416:
               if p.ground_id==400:
                   u.food_god_lev=1
               elif p.ground_id==404:
                   u.food_god_lev=2
               elif p.ground_id==408:
                   u.food_god_lev=3
               elif p.ground_id==412:
                   u.food_god_lev=4
               elif p.ground_id==416:
                   u.food_god_lev=5
           elif p.ground_id==401 or p.ground_id==405 or p.ground_id==409 or p.ground_id==413 or p.ground_id==417:
               if p.ground_id==401:
                   u.person_god_lev=1
               elif p.ground_id==405:
                   u.persn_god_lev=2
               elif p.ground_id==409:
                   u.person_god_lev=3
               elif p.ground_id==413:
                   u.person_god_lev=4
               elif p.ground_id==417:
                   u.person_god_lev=5
           elif p.ground_id==402 or p.ground_id==406 or p.ground_id==410 or p.ground_id==414 or p.ground_id==418:
               if p.ground_id==402:
                   u.wealth_god_lev=1
               elif p.ground_id==406:
                   u.wealth_god_lev=2
               elif p.ground_id==410:
                   u.wealth_god_lev=3
               elif p.ground_id==414:
                   u.wealth_god_lev=4
               elif p.ground_id==418:
                   u.wealth_god_lev=5
           else:
               if p.ground_id==403:
                   u.war_god_lev=1
               elif p.ground_id==407:
                   u.war_god_lev=2
               elif p.ground_id==411:
                   u.war_god_lev=3
               elif p.ground_id==415:
                   u.war_god_lev=4
               elif p.ground_id==419:
                   u.war_god_lev=5
           #if p.ground_id>=500 and p.ground_id<=699:
           #    u.populationupbound=u.populationupbound+lis[1]
           p.producttime=0        
           p.finish=1
           read(city_id)
           replacecache(u.userid,u)#cache
           return dict(id=1)
        except InvalidRequestError:
           return dict(id=0)
    @expose('json')
    def speedup(self,user_id,city_id,grid_id):#对外接口，加速operationalData:query->update; businessWrite:query->update
        try:
            caesars=1
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
            t=ti-p.producttime
            
            if p.ground_id==0:
                return dict(id=0)
            elif  p.ground_id>=1 and p.ground_id<=99:
                if p.finish==0:
                    return dict(id=0)                        
                else:
                    caesars=(Plant_Price[p.object_id][3]-t+3600-1)/3600
                    if u.cae-caesars>=0:
                        u.cae=u.cae-caesars
                        
                        p.producttime=1
                        read(city_id)
                        replacecache(u.userid,u)#cache
                        return dict(id=1)
                    else:
                        return dict(id=0)
            elif p.ground_id>=100 and p.ground_id<=199:
                if p.finish==0:
                    caesars=(housebuild[p.ground_id-100][5]-t+3600-1)/3600
                    if u.cae-caesars>=0:
                        u.cae=u.cae-caesars
                        p.producttime=0
                        #u.exp=u.exp+housebuild[p.ground_id-100][4]
                        p.finish=1
                        read(city_id)
                        replacecache(u.userid,u)#cache
                        return dict(id=1)
                    else:
                        return dict(id=1)
                else:
                    caesars=(houses[p.ground_id-100][3]-t+3600-1)/3600
                    if u.cae-caesars>=0:
                        u.cae=u.cae-caesars
                        p.producttime=1
                        #u.exp=u.exp+houses[p.ground_id-100][2]
                        #if u.population+houses[p.ground_id-100][0]>u.populationupbound:
                            #u.population=u.populationupbound
                        #else:
                            #u.population=u.population+houses[p.ground_id-100][0]
                        read(city_id)
                        replacecache(u.userid,u)#cache
                        return dict(id=1)
                    else:
                        return dict(id=0)
  
            elif p.ground_id>=200 and p.ground_id<=299:
                if p.finish==0:
                    caesars=(milbuild[p.ground_id-200][6]-t+3600-1)/3600
                    if u.cae-caesars>=0:
                        u.cae=u.cae-caesars
                        
                        p.producttime=0
                        #u.exp=u.exp+milbuild[p.ground_id-200][5]
                        p.finish=1
                        read(city_id)
                        replacecache(u.userid,u)#cache
                        return dict(id=1)
                    else:
                        return dict(id=0)
                else:
                    if p.object_id>=0:
                        caesars=(soldie[p.object_id][4]-t+3600-1)/3600
                        if u.cae-caesars>=0:
                            u.cae=u.cae-caesars
                            #sid=p.object_id
                            #if int(sid)>=0 and int(sid)<9:
                                #u.infantry_num=u.infantry_num+soldie[int(sid)][2]
                            #if int(sid)>=9 and int(sid)<18:
                                #u.cavalry_num=u.cavalry_num+soldie[int(sid)][2]
                            #if int(sid)>=18 :
                                #u.scout_num=u.scout_num+soldie[int(sid)][2]
                            #u.exp=u.exp+soldiernum[int(sid)]
                            p.producttime=1
                            
                            read(city_id)
                            replacecache(u.userid,u)#cache
                            return dict(id=1)
                        else:
                            return dict(id=0)
                    else:
                        return dict(id=0) 
            elif p.ground_id>=300 and p.ground_id<=399:
                if p.finish==0:
                    caesars=(businessbuild[p.ground_id-300][6]-t+3600-1)/3600
                    if u.cae-caesars>=0:
                        u.cae=u.cae-caesars
                        p.producttime=ti
                        #u.exp=u.exp+businessbuild[p.ground_id-300][5]
                        p.finish=1
                        read(city_id)
                        replacecache(u.userid,u)#cache
                        return dict(id=1)
                    else:
                        return dict(id=0)
                else:
                    caesars=(production[p.ground_id-300][3]-t+3600-1)/3600
                    if u.cae-caesars>=0:
                        u.cae=u.cae-caesars
                        p.producttime=1
                        read(city_id)
                        replacecache(u.userid,u)#cache
                        #u.exp=u.exp+production[p.ground_id-300][1]
                        #u.corn=u.corn+production[p.ground_id-300][0]
                    return dict(id=1)     
            elif p.ground_id>=400 and p.ground_id<499:
                if p.finish==0:
                    caesars=(godbuild[p.ground_id-400][5]-t+3600-1)/3600
                    if u.cae-caesars>=0:
                        u.cae=u.cae-caesars
                        p.producttime=0
                        #u.exp=u.exp+godbuild[p.ground_id-400][3]
                        #u.populationupbound=u.populationupbound+godbuild[p.ground_id-400][4]
                        p.finish=1
                        read(city_id)
                        replacecache(u.userid,u)#cache
                        return dict(id=1)
                    else:
                        return dict(id=0) 
                else:
                    return dict(id=0)                  
        except InvalidRequestError:
            return dict(id=0)

    @expose('json')
    def population(self,user_id,city_id,grid_id):#对外接口，招募人口recruit population;operationalData:query->update; businessWrite:query->update
        try:
                
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            num=houses[p.ground_id-100][0]
            food=houses[p.ground_id-100][1]
            ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
            
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            if u.food-food>=0 and ti-p.producttime>houses[p.ground_id-100][3]:
                u.food=u.food-food
                p.producttime=ti
                #u.exp=u.exp+houses[p.ground_id-100][2]
                read(city_id)
                replacecache(u.userid,u)#cache
                return dict(id=1)
            else :
                return dict(f=u.food-food,id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def finipop(self,user_id,city_id,grid_id):#对外接口，完成人口招募 finish population;warMap:query; operationalData,businessWrite:query->update
        try:
            p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            war=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
            num=houses[p.ground_id-100][0]
            mark=minusstateeli(u,war,grid_id,p.producttime)
            mark=0
            t=int(time.mktime(time.localtime())-time.mktime(beginTime))
            factor=1
            if u.person_god==1 and t-u.popgodtime<3600 :
                if u.person_god_lev==1:
                    factor=1.2
                elif u.person_god_lev==2:
                    factor=1.4
                elif u.person_god_lev==3:
                    factor=1.6
                elif u.person_god_lev==4:
                    factor=1.8
                elif u.person_god_lev==5:
                    factor=2
            elif u.person_god==2 and t-u.popgodtime<21600 :
                if u.person_god_lev==1:
                    factor=1.2
                elif u.person_god_lev==2:
                    factor=1.4
                elif u.person_god_lev==3:
                    factor=1.6
                elif u.person_god_lev==4:
                    factor=1.8
                elif u.person_god_lev==5:
                    factor=2
            elif u.person_god==3 and t-u.popgodtime<86400 :
                if u.person_god_lev==1:
                    factor=1.2
                elif u.person_god_lev==2:
                    factor=1.4
                elif u.person_god_lev==3:
                    factor=1.6
                elif u.person_god_lev==4:
                    factor=1.8
                elif u.person_god_lev==5:
                    factor=2
            else:
                u.person_god=0
                u.popgodtime=-1                                
            if mark==0 and u.population+int(num*factor)>u.populationupbound:
                u.population=u.populationupbound
            elif mark==0:
                u.population=u.population+int(num*factor)
            p.producttime=0
            u.exp=u.exp+houses[p.ground_id-100][2]
            read(city_id)
            replacecache(u.userid,u)#cache
            return dict(id=1)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def training(self,user_id,city_id,grid_id,sid):# 对外接口，训练士兵training soldiers; operationalData:query->update; businessWrite:query->update
        try:
           p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
           i=int(sid)
           #three=soldier[i]
           corn=soldie[i][0]
           foo=soldie[i][1]
           pop=soldie[i][2]
           #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
           u=checkopdata(user_id)#cache
           if u.corn-corn>=0 and u.food-foo>=0 and u.population-pop>=0 and p.producttime==0 and p.finish==1:
               u.corn=u.corn-corn
               u.food=u.food-foo
               u.population=u.population-pop
               p.object_id=sid
               ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
               p.producttime=ti
               read(city_id)
               replacecache(u.userid,u)#cache
               return dict(id=1)
           else:
               return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def soldier(self,user_id,city_id,grid_id):#对外接口，完成士兵训练 finish training warMap:query;businessWrite,operationalData:query->update
        try:
           p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
           war=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
           #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
           u=checkopdata(user_id)#cache
           sid=p.object_id
           mark=-1
           mark=minusstateeli(u,war,grid_id,p.producttime)
           mark=0
           if mark==0 and int(sid)>=0 and int(sid)<9:
               if int(sid)>=0 and int(sid)<=2:
                   u.infantry1_num=u.infantry1_num+soldie[int(sid)][2]
                   u.infantrypower=u.infantrypower+soldie[int(sid)][2]
               elif int(sid)>=3 and int(sid)<=5:
                   u.infantry2_num=u.infantry2_num+soldie[int(sid)][2]
                   u.infantrypower=u.infantrypower+soldie[int(sid)][2]*2
               elif int(sid)>=6 and int(sid)<=8:
                   u.infantry2_num=u.infantry2_num+soldie[int(sid)][2]
                   u.infantrypower=u.infantrypower+soldie[int(sid)][2]*3
           if mark==0 and int(sid)>=9 and int(sid)<18:
               if int(sid)>=9 and int(sid)<=11:
                   u.cavalry1_num=u.cavalry1_num+soldie[int(sid)][2]
                   u.cavalrypower=u.cavalrypower+soldie[int(sid)][2]*4
               elif int(sid)>=12 and int(sid)<=14:
                   u.cavalrypower=u.cavalrypower+soldie[int(sid)][2]*5
                   u.cavalry2_num=u.cavalry2_num+soldie[int(sid)][2]
               elif int(sid)>=15 and int(sid)<=17:
                   u.cavalrypower=u.cavalrypower+soldie[int(sid)][2]*6
                   u.cavalry3_num=u.cavalry3_num+soldie[int(sid)][2]
           if mark==0 and int(sid)>=18 :
               if int(sid)>=18 and int(sid)<=20:
                   u.scout1_num=u.scout1_num+soldie[int(sid)][2]
               elif int(sid)>=21 and int(sid)<=23:
                   u.scout2_num=u.scout2_num+soldie[int(sid)][2]
               else:
                   u.scout3_num=u.scout3_num+soldie[int(sid)][2]
           u.exp=u.exp+soldiernum[int(sid)]
           p.producttime=0
           p.object_id=-1
           read(city_id)
           replacecache(u.userid,u)#cache
           return dict(id=1)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def product(self,user_id,city_id,grid_id):# 对外接口，生产business produce warMap:query businessWrite:query->update operationalData:update
        try:
           p=DBSession.query(businessWrite).filter_by(city_id=int(city_id)).filter_by(grid_id=int(grid_id)).one()
           #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
           u=checkopdata(user_id)#cache
           war=DBSession.query(warMap).filter_by(city_id=int(city_id)).one()
           mark=minusstateeli(u,war,grid_id,p.producttime)
           mark=0
           ti=int(time.mktime(time.localtime())-time.mktime(beginTime))
           factor=1
           if ti-p.producttime>=production[p.ground_id-300][3]:#time
               if u.wealth_god==1 and ti-u.wealthgodtime<3600:
                   if u.wealth_god_lev==1:
                       factor=1.2
                   elif u.wealth_god_lev==2:
                       factor=1.4
                   elif u.wealth_god_lev==3:
                       factor=1.6
                   elif u.wealth_god_lev==4:
                       factor=1.8
                   elif u.wealth_god_lev==5:
                       factor=2
               if u.wealth_god==2 and ti-u.wealthgodtime<21600:
                   if u.wealth_god_lev==1:
                       factor=1.2
                   elif u.wealth_god_lev==2:
                       factor=1.4
                   elif u.wealth_god_lev==3:
                       factor=1.6
                   elif u.wealth_god_lev==4:
                       factor=1.8
                   elif u.wealth_god_lev==5:
                       factor=2
               if u.wealth_god==3 and ti-u.wealthgodtime<86400:
                   if u.wealth_god_lev==1:
                       factor=1.2
                   elif u.wealth_god_lev==2:
                       factor=1.4
                   elif u.wealth_god_lev==3:
                       factor=1.6
                   elif u.wealth_god_lev==4:
                       factor=1.8
                   elif u.wealth_god_lev==5:
                       factor=2 
               else:
                   u.wealth_god=0
                   u.wealthgodtime=-1                                    
               if mark==0:
                   u.corn=u.corn+int(production[p.ground_id-300][0]*factor)
               u.exp=u.exp+production[p.ground_id-300][1]
               p.producttime=ti
               read(city_id)
               replacecache(u.userid,u)#cache
               return dict(id=1)
           else:
               return dict(id=0)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def expand(self,user_id,city_id,type):#对外接口，扩地operationalData:query->update
        try:
            #u=DBSession.query(operationalData).filter_by(userid=int(user_id)).one()
            u=checkopdata(user_id)#cache
            type=int(type)
            if u.landkind==EXPANDLEV :
                return dict(id=-2)
            if type==0:
                u.landkind=u.landkind+1
            elif type==2:
                corn=expanding[u.landkind][0]
                if u.corn-corn>=0:
                    u.corn=u.corn-corn
                    u.landkind=u.landkind+1
                else:
                    return dict(id=0)
            else:
                cae=expanding[u.landkind][1]
                if u.cae-cae>=0:
                    u.cae=u.cae-cae
                    u.landkind=u.landkind+1
                else:
                    return dict(id=0)
            u.exp=u.exp+expanding[u.landkind-1][2]
            replacecache(u.userid,u)#cache
            return dict(id=1)
        except InvalidRequestError:
            return dict(id=0)
    @expose('json')
    def retlev(self,uid,rrstring):#对外接口，返回好友等级operationalData:query
        f=None
        try:
            dict0={}
            #writelog(0,1,'begin')
            list1=rrstring.split(';')
            for string2 in list1 :
                list2=string2.split(',')
                oid=list2[0]#otherid 为varchar类型
                ukind=int(list2[1])
                try:
                    uu=DBSession.query(operationalData).filter_by(otherid=oid).filter_by(user_kind=ukind).one()
                    v=0
                    try:
                        f=DBSession.query(visitFriend).filter_by(userid=int(uid)).filter_by(friendid=int(uu.userid)).one()
                        v=f.visited
                    except:
                        v=0
                    u=checkopdata(uu.userid)#cache
                    dict0[list2[0]]=dict(level=u.lev,visited=v)
                except InvalidRequestError:
                    dict0[list2[0]]=dict(level=-1)
            #writelog(1,1,'normalend')
            return dict0
        except InvalidRequestError:
            #writelog(1,1,'except')
            return dict(id=0)         
    @expose('stchong.templates.help')      
    def help(self):
        return dict(page='help')
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
