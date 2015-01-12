#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
import MySQLdb
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

class HostTYHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        thead = ["编码","影院名称","影院编码","影院code","IP地址","密码","院线","鼎新版本","系统版本"]
        self.render("host.html",web_title="运维管理平台",user=self.current_user,thead=thead,tbody=self.application.data.GetHost("cinema_ty"),page="通用主机",host="host_ty")

class HostTYACHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,input):
        if input == 'add':
            self.render("host_action.html",web_title="运维管理平台",user=self.current_user,page="添加通用主机",group=self.application.data.GetAll('cinema_group'),action='host_ty')
        elif input == 'edit':
            id = self.get_argument('id')
            data,group = self.application.data.GetOne('cinema_ty',id)
            self.render("host_edit.html",web_title="运维管理平台",user=self.current_user,page="修改通用主机",data=data,group=group)
        else:
            self.render("404.html")

    def post(self,input):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor()
        if input == 'add':
            cinema_name = self.get_argument('cinema_name')
            cinema_num = self.get_argument('cinema_num')
            cinema_code = self.get_argument('cinema_code')
            cinema_ip = self.get_argument('cinema_ip')
            cinema_passwd = self.get_argument('cinema_passwd')
            cinema_group = self.get_argument('cinema_group')
            version_dx = self.get_argument('version_dx')
            version_sys = self.get_argument('version_sys')
            cursor.execute("insert into cinema_ty values(null,'%s','%s','%s','%s','%s','%s','%s','%s');"%(cinema_ip,cinema_name,cinema_code,cinema_num,cinema_passwd,cinema_group,version_dx,version_sys))
            cursor.close()
            conn.close()
            self.redirect("/host_ty")
        elif input == 'edit':
            id = self.get_argument('rid')
            cinema_name = self.get_argument('cinema_name')
            cinema_num = self.get_argument('cinema_num')
            cinema_code = self.get_argument('cinema_code')
            cinema_ip = self.get_argument('cinema_ip')
            cinema_passwd = self.get_argument('cinema_passwd')
            cinema_group = self.get_argument('cinema_group')
            version_dx = self.get_argument('version_dx')
            version_sys = self.get_argument('version_sys')
            cursor.execute("update cinema_ty set cinema_name='%s',cinema_num='%s',cinema_code='%s',cinema_ip='%s',cinema_passwd='%s',cinema_group='%s',version_dx='%s',version_sys='%s' where id = %s;"%(cinema_name,cinema_num,cinema_code,cinema_ip,cinema_passwd,cinema_group,version_dx,version_sys,id))
            cursor.close()
            conn.close()
            self.redirect("/host_ty")
        else:
            self.render("404.html")

class HostWDHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        thead = ["编码","影院名称","影院编码","影院code","IP地址","密码","鼎新版本","系统版本"]
        self.render("host.html",web_title="运维管理平台",user=self.current_user,thead=thead,tbody=self.application.data.GetHost("cinema_wd"),page="万达主机",host="host_wd")

class HostWDACHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,input):
        if input == 'add':
            self.render("host_action.html",web_title="运维管理平台",user=self.current_user,page="添加万达主机")
        elif input == 'edit':
            id = self.get_argument('id')
            self.render("host_edit.html",web_title="运维管理平台",user=self.current_user,page="修改万达主机",data=self.application.data.GetOne('cinema_wd',id),group='')
        else:
            self.render("404.html")

    def post(self,input):
        conn = MySQLdb.connect(host=options.dbhost,port=options.dbport,user=options.dbuser,passwd=options.dbpasswd,db=options.db,charset=options.charset)
        cursor = conn.cursor()
        if input == 'add':
            cinema_name = self.get_argument('cinema_name')
            cinema_num = self.get_argument('cinema_num')
            cinema_code = self.get_argument('cinema_code')
            cinema_ip = self.get_argument('cinema_ip')
            cinema_passwd = self.get_argument('cinema_passwd')
            version_dx = self.get_argument('version_dx')
            version_sys = self.get_argument('version_sys')
            cursor.execute("insert into cinema_ty values(null,'%s','%s','%s','%s','%s','%s','%s');"%(cinema_ip,cinema_name,cinema_code,cinema_num,cinema_passwd,version_dx,version_sys))
            cursor.close()
            conn.close()
            self.redirect("/host_ty")
        elif input == 'edit':
            id = self.get_argument('rid')
            cinema_name = self.get_argument('cinema_name')
            cinema_num = self.get_argument('cinema_num')
            cinema_code = self.get_argument('cinema_code')
            cinema_ip = self.get_argument('cinema_ip')
            cinema_passwd = self.get_argument('cinema_passwd')
            version_dx = self.get_argument('version_dx')
            version_sys = self.get_argument('version_sys')
            cursor.execute("update cinema_ty set cinema_name='%s',cinema_num='%s',cinema_code='%s',cinema_ip='%s',cinema_passwd='%s',version_dx='%s',version_sys='%s' where id = %s;"%(cinema_name,cinema_num,cinema_code,cinema_ip,cinema_passwd,version_dx,version_sys,id))
            cursor.close()
            conn.close()
            self.redirect("/host_ty")
        else:
            self.render("404.html")