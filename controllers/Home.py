#coding:utf-8
import sys
import os.path
import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop
#from MySQL import MysqlQuery

reload(sys)
sys.setdefaultencoding("utf8")

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
#                return self.get_secure_cookie("user")
        pass

class IndexHandler(BaseHandler):
        #@tornado.web.authenticated
    def get(self):
                #name = tornado.escape.xhtml_escape(self.current_user)
                #self.render('index.html',username=name)
        self.render('index.html')

class TopHandler(BaseHandler):
    pass

class NewHandler(BaseHandler):
    pass

if __name__ == "__main__":
    pass
#   a = MysqlQuery().query_select('SELECT * FROM Articles.topArticle')
#   print MysqlQuery().query_select('SELECT imgUrl FROM Articles.topArticle order by id desc limit 1')[0][0]
#   print a[0][2].decode('utf8')
