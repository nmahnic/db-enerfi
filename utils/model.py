#!/usr/bin/env python
import sqlobject as so
import os
import defs

# uri = "mysql://{}:{}@{}/{}".format(defs.USER,defs.PASSWORD,defs.HOST,defs.DBASE)
# print(uri)
# connection = so.connectionForURI(uri)
connection = so.connectionForURI("mysql://guest:guest@localhost/Enerfi")
so.sqlhub.processConnection = connection


class User(so.SQLObject):
    class sqlmeta:
        table = "user"
    name = so.StringCol(length=50, varchar=True)
    surname = so.StringCol(length=50, varchar=True)
    surname = so.StringCol(length=50, varchar=True)
    usernick = so.StringCol(length=50, varchar=True)
    password = so.StringCol(length=50, varchar=True)
    mail = so.StringCol(length=50, varchar=True)

class Dum(so.SQLObject):
    class sqlmeta:
        table = "dum"
    user_id = so.ForeignKey('User')
    name = so.StringCol(length=50, varchar=True)

class Meter(so.SQLObject):
    class sqlmeta:
        table = "meter"
    macAddress = so.StringCol(length=50, varchar=True)
    ip = so.StringCol(length=50, varchar=True)
    user_id = so.ForeignKey('User')
    dum_id = so.ForeignKey('Dum')

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
    freq_1st = so.FloatCol()
    freq_2nd = so.FloatCol()
    freq_1st = so.FloatCol()
    freq_3rd = so.FloatCol()
    freq_4th = so.FloatCol()
    freq_5th = so.FloatCol()
    freq_6th = so.FloatCol()
    freq_7th = so.FloatCol()
    freq_8th = so.FloatCol()
    freq_9th = so.FloatCol()
    freq_10th = so.FloatCol()
    dum_id = so.ForeignKey('Dum')


def to_dict(obj):
    d = dict((c, getattr(obj, c)) for c in obj.sqlmeta.columns)
    d['id'] = obj.id
    return d


def finder(name):
    query = User.selectBy(name=name).getOne()
    d = to_dict(query)
    return d

def findUser(name,surname,usernick,password,mail):
    query = User.selectBy(
        name=name,
        surname=surname,
        usernick=usernick,
        password=password,
        mail=mail
    )
    if query.count() != 0:
        print(query.getOne())
        return True
    else:
        return False


def listAlluser():
    users = User.select()
    d = [to_dict(user) for user in users]
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
    measures = Measure.select()
    d = [to_dict(measure) for measure in measures]
    return d