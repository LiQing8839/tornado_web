#!/usr/bin/env python
# -*- coding:utf8 -*-

from tornado.options import  options
import MySQLdb

class DbModel(object):
    def __init__(self):
        self.count = 0

    def GetPasswd(self,user):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        if cursor.execute("select password from user where email = '%s';"%user):
            passwd = cursor.fetchall()[0]['password']
            cursor.close()
            conn.close()
            return passwd
        else:
            cursor.close()
            conn.close()
            return False

    def GetCount(self,table):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select count(id) from %s"%table)
        self.count = cursor.fetchall()[0]['count(id)']
        cursor.close()
        conn.close()
        return self.count

    def GetTable(self,table):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from %s order by id desc limit 5;"%table)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    def GetHost(self,table):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from %s"%table)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    def GetAll(self,table):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor()
        cursor.execute("select * from %s"%table)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    def GetOne(self,table,id):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from %s where id = '%s'"%(table,id))
        data =  cursor.fetchall()[0]
        if table == 'cinema_ty':
            cursor.execute("select * from cinema_group where cinema_group != (select cinema_group from cinema_ty where id = %s);"%id)
            noself = cursor.fetchall()
            cursor.close()
            conn.close()
            return data,noself
        else:
            cursor.close()
            conn.close()
            return data
