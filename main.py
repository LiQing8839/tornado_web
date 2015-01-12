#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.httpserver
import tornado.gen
import tornado.websocket

import os.path
import base64
import MySQLdb
from uuid import uuid4

from tornado.options import define,options
from views.index import *
from views.model import DBHandler

define("port",default=8000,help="port of tornado web",type=int)
define("dbhost",default="127.0.0.1",help="mysql host",type=str)
define("dbport",default=3306,help="mysql port",type=int)
define("dbuser",default="root",help="mysql user",type=str)
define("dbpasswd",default="",help="mysql passwd",type=str)
define("db",default="",help="mysql database",type=str)
define("charset",default="utf8",help="mysql charset",type=str)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/',IndexHandler),
            (r'/admin/(\w+)',DBHandler),
            (r'/dashboard',DashboardHandler),
            (r'/host_ty',HostTYHandler),
            (r'/host_ty/(\w+)',HostTYACHandler),
            (r'/host_wd',HostWDHandler),
            (r'/host_wd/(\w+)',HostWDACHandler),
            (r'/login',LoginHandler),
            (r'/logout',LogoutHandler),
        ]
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__),"templates"),
            static_path = os.path.join(os.path.dirname(__file__),"static"),
            cookie_secret = base64.b64encode(uuid4().bytes+uuid4().bytes),
            xsrf_cookies = True,
            login_url = "/login",
            debug = True,
        )
        self.data = DbModel()
        tornado.web.Application.__init__(self,handlers, **settings)

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

if __name__ == '__main__':
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()