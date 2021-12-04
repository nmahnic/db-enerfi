#!/usr/bin/env python
import sqlobject as so
import os
import defs
import functions

# uri = "mysql://{}:{}@{}/{}".format(defs.USER,defs.PASSWORD,defs.HOST,defs.DBASE)
# print(uri)
# connection = so.connectionForURI(uri)
connection = so.connectionForURI("mysql://guest:guest@localhost/Enerfi")
so.sqlhub.processConnection = connection


class User(so.SQLObject):
    class sqlmeta:
        table = "user"
    name = so.StringCol(length=50, varchar=True)
    lastname = so.StringCol(length=50, varchar=True)
    email = so.StringCol(length=50, varchar=True)
    # password = so.StringCol(length=50, varchar=True)
    password = so.BLOBCol()
    # salt = so.StringCol(length=50, varchar=True)
    #salt = so.BLOBCol()

class Dum(so.SQLObject):
    class sqlmeta:
        table = "dum"
    user = so.ForeignKey('User')
    name = so.StringCol(length=50, varchar=True)
    enable = so.BoolCol()
    measures = so.MultipleJoin('Measure')

class Meter(so.SQLObject):
    class sqlmeta:
        table = "meter"
    macAddress = so.StringCol(length=50, varchar=True)
    user = so.ForeignKey('User')
    dum = so.ForeignKey('Dum')
    # duma = so.SingleJoin('Dum')


class Measure(so.SQLObject):
    class sqlmeta:
        table = "measure"
    timestamp = so.TimestampCol()
    vrms = so.FloatCol()
    irms = so.FloatCol()
    active_power = so.FloatCol()
    pf = so.FloatCol()
    thd = so.FloatCol()
    cos_phi = so.FloatCol()
    dum = so.ForeignKey('Dum')


def getMeasureByDum():
    measures = Dum.selectBy(id=1).getOne().measures
    d = [to_dict(measure) for measure in measures]
    return d

def to_dict(obj):
    d = dict((c, getattr(obj, c)) for c in obj.sqlmeta.columns)
    d['id'] = obj.id
    return d


def findLastDumIdGenerated():
    return Dum.select().count()


def finderUserByID(id):
    query = User.selectBy(id=id)
    if query.count() != 0:
        return query[0]
    else:
        return None

def findDumByMac(mac):
    queryMeter = Meter.selectBy(macAddress=mac)
    if queryMeter.count() != 0:
        queryDum = Dum.selectBy(id=queryMeter[0].dumID)
        if queryDum.count() != 0:
            return queryDum[0]
        else:
            return None
    else:
        return None

def findMeterByMac(mac):
    queryMeter = Meter.selectBy(macAddress=mac)
    if queryMeter.count() != 0:
        return queryMeter[0]
    else:
        return None

def findUser(name,lastname,email):
    query = User.selectBy(
        name=name,
        lastname=lastname,
        email=email
    )
    if query.count() != 0:
        print(query.getOne())
        return True
    else:
        return False

def validUser(email, passwd):
    query = User.selectBy(email=email)
    passwd = passwd.encode('utf-8')
    if query.count() != 0:
        user = query.getOne()
        if functions.check_password(passwd, user.password):
            return user
        else:
            return None

    else:
        return None

def getUser(name,lastname,email):
    query = User.selectBy(
        name=name,
        lastname=lastname,
        email=email
    )
    if query.count() != 0:
        return query.getOne()
    else:
        return None

def listAlluser():
    users = User.select()
    d = [to_dict(user) for user in users]
    # print(d)
    return d

def listAlldum():
    dums = Dum.select()
    d = [to_dict(dum) for dum in dums]
    return d

def listAllmeter():
    meters = Meter.select()
    d = [to_dict(meter) for meter in meters]
    return d

def listAllmeasure():
    measures = Measure.select().limit(100)
    d = [to_dict(measure) for measure in measures]
    return d

def listMeterByUser(userValid):
    meters = Meter.selectBy(userID=userValid.id)
    if meters.count() != 0:
        d = [to_dict(meter) for meter in meters]
        return d
    else:
        return None

def listDumByUser(userValid):
    dums = Dum.selectBy(userID=userValid.id)
    if dums.count() != 0:
        d = [to_dict(dum) for dum in dums]
        return d
    else:
        return None


def listMeasureByUser(dum):
    measures = Measure.selectBy(dumID=dum.id)
    if measures.count() != 0:
        d = [to_dict(measure) for measure in measures]
        return d
    else:
        return None
