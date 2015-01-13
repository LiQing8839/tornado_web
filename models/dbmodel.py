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

    def GetIP(self,table):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select cinema_ip from %s;"%table)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    """
    def History_command(self,email,ips,command,data):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor()
        num = cursor.execute("insert into command_log values(null,'%s','%s','%s','%s');"%(email,ips,command,data))
        cursor.close()
        conn.close()
        return int(num)
    """

    def GetGroupIP(self,group):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select cinema_ip from cinema_ty where cinema_group = '%s'"%group)
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data