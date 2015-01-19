#!/usr/bin/env python
# -*- coding:utf8 -*-

from tornado.options import options
import MySQLdb
import sys

class DbModel(object):
    def __init__(self):
        self.count = 0
        reload(sys)
        sys.setdefaultencoding("utf8")

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

    def GetDAll(self,sql):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    def GetAll(self,sql):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    def GetOne(self,sql):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        data =  cursor.fetchall()[0]
        cursor.close()
        conn.close()
        return data

    def Getnoself(self,sql):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(sql)
        noself = cursor.fetchall()
        cursor.close()
        conn.close()
        return noself

    def Commit(self,sql):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor()
        num = cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return num


