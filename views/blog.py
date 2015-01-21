#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
import sys
from index import BaseHandler

reload(sys)
sys.setdefaultencoding("utf8")
class BlogHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        thead = ["标题","内容","分类","创建时间","修改时间","作者"]
        sql = "select * from blog"
        self.render("blog.html",web_title="运维管理平台",user=self.current_user,thead=thead,tbody=self.application.data.GetDAll(sql),page="文章列表")

class BlogACHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self,input):
        if input == 'add':
            sql = "select * from blog_group"
            self.render("blog_action.html",web_title="运维管理平台",user=self.current_user,page="添加文章",group=self.application.data.GetAll(sql))
        elif input == 'edit':
            id = self.get_argument('blog_id')
            data = self.application.data.GetOne("select * from blog where id = %s"%id)
            group = self.application.data.Getnoself("select * from blog_group where blog_class != (select blog_class from blog where id = %s);"%id)
            self.render("blog_edit.html",web_title="运维管理平台",user=self.current_user,page="修改文章",data=data,group=group)
        elif input == 'list':
            id = self.get_argument('id')
            data = self.application.data.GetOne("select * from blog where id = %s"%id)
            tmp = data['content']
            data['content'] = tmp.split("\n")
            self.render("blog_list.html",web_title="运维管理平台",user=self.current_user,page="文章",data=data)
        elif input == 'del':
            id = self.get_argument('blog_id')
            if self.application.data.Commit("delete from blog where id = %s"%id):
                self.redirect("/blog")
            else:
                self.render("404.html",error="文章删除失败，可能文章已经在其他客户端被删")
        else:
            self.render("404.html",error="没有找到页面")

    @tornado.web.authenticated
    def post(self,input):
        if input == 'add':
            values = (self.get_argument('title'), self.get_argument('content'), self.get_argument('class'), self.current_user)
            self.application.data.Commit("insert into blog(id,blog_title,blog_content,blog_class,blog_mtime,blog_ctime,user_email) values(null,'%s','%s','%s',now(),now(),'%s');"%(values))
            self.redirect("/blog")
        if input == 'edit':
            values = (self.get_argument('title'), self.get_argument('content'), self.get_argument('class'), self.get_argument('rid'))
            self.application.data.Commit("update blog set blog_title='%s',blog_content='%s',blog_class='%s',blog_ctime=now() where id = %s"%(values))
            self.redirect("/blog/list?id=%s"%self.get_argument('rid'))
        else:
            self.render("404.html",error="没有找到页面")
