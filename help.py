
#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import tornado.gen

import MySQLdb
import paramiko
import os
from tornado.options import define,options

define('port',default=8000,help="tornado web port",type=int)

def SSHClient(ip,passwd,command,port=22,user='root'):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip,port,user,passwd,timeout=3306)
    except Exception as e:
        return "Can\'t connect this IP: %s Error: %s"%(ip,e)
    stdin,stdout,stderr = ssh.exec_command(command)
    return stdout.read()

class Application(tornado.web.Application):
    def __init__(self):

        handlers = [
            (r'/',IndexHandler),
            (r'/admin',AdminHandler)
        ]
        settings = dict(
            template_path = os.path.join(os.path.dirname(__file__),"templates"),
            static_path = os.path.join(os.path.dirname(__file__),"static"),
            debug=True
        )
        conn = MySQLdb.Connect(host="127.0.0.1",port=3306,user="root",passwd="123qwe",db="yunwei",charset="utf8")
        self.cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        tornado.web.Application.__init__(self, handlers,**settings)

class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("test.html")

class AdminHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        ip = self.get_argument("ip")
        comm = self.get_argument("command")
        if self.application.cursor.execute("select cinema_passwd from cinema_ty;"):
            passwd = self.application.cursor.fetchall()[0]['cinema_passwd']
            out = SSHClient(ip,passwd,comm)
            self.write(out)
            self.finish()
        else:
            self.write("not find this IP:%s in DB"%ip)
            self.finish()


if __name__ == '__main__':
    tornado.options.parse_command_line()
    server = tornado.httpserver.HTTPServer(Application())
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()