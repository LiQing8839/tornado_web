#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
from index import BaseHandler

class CommandHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("command.html",web_title="运维管理平台",user=self.current_user,page="命令提示符",action="",ty=self.application.data.GetIP('cinema_ty'),wd=self.application.data.GetIP('cinema_wd'))
class CommandACHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,input):
        if input == 'ips':
            self.render("command.html",web_title="运维管理平台",user=self.current_user,page="命令提示符",action="ips",ty=self.application.data.GetIP('cinema_ty'),wd=self.application.data.GetIP('cinema_wd'))
        elif input == 'group':
            self.render("command.html",web_title="运维管理平台",user=self.current_user,page="命令提示符",action="group",group=self.application.data.GetAll('cinema_group'))
        else:
            self.render("404.html")
