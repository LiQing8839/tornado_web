#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
import tornado.gen
import json
import os
from views.index import BaseHandler

class DBHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self,input):
        data = yield self.GetData(input)
        self.write(data)

    @tornado.gen.coroutine
    def GetData(self,input):
        if input == 'ips':
            ips = self.get_argument('ip')
            command = self.get_argument('command')
            data = os.popen('python models/command.py "%s" "%s"'%(ips,command)).read()

        elif input == 'group':
            group = self.get_argument('group')
            command = self.get_argument('command')
            if group == 'wanda':
                sql = "select cinema_ip from cinema_wd"
                ips = ','.join([i['cinema_ip'] for i in self.application.data.GetDAll(sql)])
            else:
                sql = "select cinema_ip from cinema_ty where cinema_group = '%s'"%group
                ips = ','.join([i['cinema_ip'] for i in self.application.data.GetDAll(sql)])
            data = os.popen('python models/command.py "%s" "%s"'%(ips,command)).read()

        elif input not in ['report', 'error', 'log']:
            d = {'r':'reports', 'e':'errors' ,'l':'logs'}
            if input in d:
                data = '%d'%self.application.data.GetCount(d[input])
            else:
                data = '%d'%self.application.data.GetCount(input)

        else:
            d = {'report':'reports', 'error':'errors' ,'log':'logs'}
            sql = "select * from %s order by id desc limit 5"%d[input]
            data = json.dumps(self.application.data.GetDAll(sql))
        raise tornado.gen.Return(data)