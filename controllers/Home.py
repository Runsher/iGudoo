#coding:utf-8
import sys
import os.path
import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop
import MongoConn

dbconn = MongoConn.DBConn()
conn = None

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
     	return self.get_secure_cookie("user")

class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
       	name = tornado.escape.xhtml_escape(self.current_user)
      	dbconn.connect()
     	conn = dbconn.getConn()
      	userInfo = conn.iGudoo_Admin.userInfo
      	userLevel = userInfo.find({"name":name})[0]['level']
     	conn.close()
      	currentInfo = []
      	self.render('index.html',userLevel=userLevel,userName=name)
        #self.render('index.html')

class TopHandler(BaseHandler):
    pass

class NewHandler(BaseHandler):
    pass

if __name__ == "__main__":
    pass
#   a = MysqlQuery().query_select('SELECT * FROM Articles.topArticle')
#   print MysqlQuery().query_select('SELECT imgUrl FROM Articles.topArticle order by id desc limit 1')[0][0]
#   print a[0][2].decode('utf8')
