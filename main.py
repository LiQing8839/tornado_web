#!/usr/bin/env python
# -*- coding:utf8 -*-

import os.path
import base64
from uuid import uuid4

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpclient
import tornado.httpserver
import tornado.gen
import tornado.websocket
from tornado.options import define,options

from models.dbmodel import DbModel
from models.model import *

from views.index import *
from views.host import *
from views.command import *
from views.blog import *
from views.file import *


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
            (r'/command',CommandHandler),
            (r'/command/(\w+)',CommandACHandler),
            (r'/blog',BlogHandler),
            (r'/blog/(\w+)',BlogACHandler),
            (r'/upload',UploadHandler),
            (r'/sync',SyncHandler),
            (r'/file/(\w+)',FileHandler),
            (r'/login',LoginHandler),
            (r'/logout',LogoutHandler),
        ]
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__),"templates"),
            static_path = os.path.join(os.path.dirname(__file__),"static"),
            cookie_secret = base64.b64encode(uuid4().bytes+uuid4().bytes),
            xsrf_cookies = True,
            login_url = "/login",
            gzip = True,
            compress_response = True,
            autoreload = True,
        )
        self.data = DbModel()
        tornado.web.Application.__init__(self,handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
