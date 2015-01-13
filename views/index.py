#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
import md5

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("username")

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login.html',web_title="运维平台登陆",error='')

    def post(self):
        username = self.get_argument("username")
        password = md5.md5(self.get_argument("password"))
        passwd = self.application.data.GetPasswd(username)
        if passwd:
            if passwd == password.hexdigest():
                self.set_secure_cookie("username", username)
                self.redirect("/")
            else:
                self.render("login.html",web_title="运维平台登陆",error="密码错误")
        else:
            self.render("login.html",web_title="运维平台登陆",error="没有此账户")

class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("username")
        self.redirect("/")

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("index.html",web_title="运维管理平台",user=self.current_user)

class DashboardHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.render("dashboard.html",web_title="运维管理平台",user=self.current_user,page="")

