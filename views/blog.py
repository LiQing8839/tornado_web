#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
import MySQLdb
from index import BaseHandler

class BlogHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):


class BlogACHandler(BaseHandler):
