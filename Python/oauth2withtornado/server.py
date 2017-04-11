# !/usr/bin/env python
# -*- coding: utf-8 -*-
import tornado.web
import tornado.ioloop


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('test')


if __name__ == "__main__":
    application = tornado.web.Application([(r"/", MainHandler)])
    application.listen(8686)
    tornado.ioloop.IOLoop.current().start()
