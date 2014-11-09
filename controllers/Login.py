#coding:utf-8
import sys
import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop

import MongoConn

reload(sys)
sys.setdefaultencoding("utf8")

class Auth():
        def __init__(self):
                pass;

        def authPassword(self,username):
                try:
			dbconn = MongoConn.DBConn()
			conn = None

			dbconn.connect()
			conn = dbconn.getConn()
			userInfo = conn.DJ_MySQL_Admin.userInfo
			password=userInfo.find({"name":username})[0]['password']
			conn.close()
                        #password = MySQL.MysqlQuery().query_select('select password from DB_DAS.user where username="%s"' %(username))[0][0]
                        if password:
                                return password
                        else:
                                print "no user"
                except Exception,e:
                        print e



class BaseHandler(tornado.web.RequestHandler):
        def get_current_user(self):
                return self.get_secure_cookie("user")


class LoginHandler(BaseHandler):
        def get(self):
		name = 'None'
		self.render("login.html",username=name)
        def post(self):
                username = self.get_argument('username')
                password = self.get_argument('password')
                t = Auth()
                password_e  = t.authPassword(username)
               	if ( password_e == password ):
                    	self.set_secure_cookie("user", self.get_argument("username"))
                       	self.redirect('/', permanent=True)
              	else:
                  	self.redirect('/login', permanent=True)

if __name__ == "__main__":
	t = Auth()
	username = 'admin'
	password = 'admin'
	password_p =  MySQL.MysqlQuery().query_select('select password("%s")' %(password))[0][0]
	password_e  = t.authPassword(username)
	print password_e,password_p 
	try:
             	if ( password_e == password_p ):
			print "user"
		else:
			print "w"
                      #	self.redirect('/', permanent=True)
             # 	else:
              #      	self.redirect('/login', permanent=True)
  	except Exception,e:
            	print e
