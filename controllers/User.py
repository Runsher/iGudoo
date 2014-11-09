#encoding=utf-8
import  tornado.web
class BaseHandler(tornado.web.RequestHandler):
        def get_current_user(self):
                return self.get_secure_cookie("user")

class IndexHandler(BaseHandler):
        @tornado.web.authenticated
        def get(self):
		pass
		self.render('user.html')

        def post(self):
                pass
