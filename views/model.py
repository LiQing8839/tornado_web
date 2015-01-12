#!/usr/bin/env python
# -*- coding:utf8 -*-

import tornado.web
import tornado.gen
import json
from index import BaseHandler

class DBHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self,input):
        data = yield self.GetData(input)
        self.write(data)

    @tornado.gen.coroutine
    def GetData(self,input):
        if input not in ['report', 'error', 'log']:
            d = {'r':'reports', 'e':'errors' ,'l':'logs'}
            if input in d:
                data = '%d'%self.application.data.GetCount(d[input])
            else:
                data = '%d'%self.application.data.GetCount(input)
        else:
            d = {'report':'reports', 'error':'errors' ,'log':'logs'}
            data = json.dumps(self.application.data.GetTable(d[input]))
        raise tornado.gen.Return(data)